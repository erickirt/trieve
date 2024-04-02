use crate::{
    data::models::{
        Organization, OrganizationWithSubAndPlan, Pool, RedisPool, StripePlan, StripeSubscription,
    },
    errors::ServiceError,
    get_env,
};
use actix_web::web;
use diesel::prelude::*;
use diesel_async::RunQueryDsl;
use serde_json::json;

#[tracing::instrument]
pub fn get_stripe_client() -> stripe::Client {
    let stripe_secret = get_env!("STRIPE_SECRET", "STRIPE_SECRET must be set");

    stripe::Client::new(stripe_secret)
}

#[tracing::instrument(skip(redis_pool, pool))]
pub async fn refresh_redis_org_plan_sub(
    organization_id: uuid::Uuid,
    redis_pool: actix_web::web::Data<RedisPool>,
    pool: web::Data<Pool>,
) -> Result<(), ServiceError> {
    use crate::data::schema::organizations::dsl as organizations_columns;
    use crate::data::schema::stripe_plans::dsl as stripe_plans_columns;
    use crate::data::schema::stripe_subscriptions::dsl as stripe_subscriptions_columns;

    let mut conn = pool
        .get()
        .await
        .expect("Failed to get connection from pool");
    let org_plan_sub: (Organization, Option<StripePlan>, Option<StripeSubscription>) =
        organizations_columns::organizations
            .left_outer_join(stripe_subscriptions_columns::stripe_subscriptions)
            .left_outer_join(
                stripe_plans_columns::stripe_plans
                    .on(stripe_plans_columns::id.eq(stripe_subscriptions_columns::plan_id)),
            )
            .select((
                organizations_columns::organizations::all_columns(),
                stripe_plans_columns::stripe_plans::all_columns().nullable(),
                stripe_subscriptions_columns::stripe_subscriptions::all_columns().nullable(),
            ))
            .filter(organizations_columns::id.eq(organization_id))
            .first::<(Organization, Option<StripePlan>, Option<StripeSubscription>)>(&mut conn)
            .await
            .map_err(|_| ServiceError::BadRequest("Could not find organizations".to_string()))?;
    let org_plan_sub =
        OrganizationWithSubAndPlan::from_components(org_plan_sub.0, org_plan_sub.1, org_plan_sub.2);

    let mut redis_conn = redis_pool
        .get()
        .await
        .map_err(|_| ServiceError::BadRequest("Could not create redis client".to_string()))?;

    redis::cmd("SET")
        .arg(format!("organization:{}", org_plan_sub.id))
        .arg(serde_json::to_string(&org_plan_sub).map_err(|_| {
            ServiceError::BadRequest("Could not stringify organization".to_string())
        })?)
        .query_async(&mut *redis_conn)
        .await
        .map_err(|_| ServiceError::BadRequest("Could not set organization in redis".to_string()))?;

    redis::cmd("SET")
        .arg(format!("organization:{}", org_plan_sub.name))
        .arg(serde_json::to_string(&org_plan_sub).map_err(|_| {
            ServiceError::BadRequest("Could not stringify organization".to_string())
        })?)
        .query_async(&mut *redis_conn)
        .await
        .map_err(|_| ServiceError::BadRequest("Could not set organization in redis".to_string()))?;

    Ok(())
}

#[tracing::instrument(skip(redis_pool, pool))]
pub async fn create_stripe_subscription_query(
    stripe_id: String,
    plan_id: uuid::Uuid,
    organization_id: uuid::Uuid,
    redis_pool: web::Data<RedisPool>,
    pool: web::Data<Pool>,
) -> Result<(), ServiceError> {
    use crate::data::schema::stripe_subscriptions::dsl as stripe_subscriptions_columns;

    let stripe_subscription =
        StripeSubscription::from_details(stripe_id, plan_id, organization_id, None);

    let mut conn = pool
        .get()
        .await
        .expect("Failed to get connection from pool");
    diesel::insert_into(stripe_subscriptions_columns::stripe_subscriptions)
        .values(&stripe_subscription)
        .execute(&mut conn)
        .await
        .map_err(|e| {
            log::error!("Failed to insert stripe subscription: {}", e);
            ServiceError::BadRequest("Failed to insert stripe subscription".to_string())
        })?;

    refresh_redis_org_plan_sub(stripe_subscription.organization_id, redis_pool, pool).await?;

    Ok(())
}

#[tracing::instrument(skip(pool))]
pub async fn create_stripe_plan_query(
    stripe_id: String,
    amount: i64,
    pool: web::Data<Pool>,
) -> Result<StripePlan, ServiceError> {
    use crate::data::schema::stripe_plans::dsl as stripe_plans_columns;

    // TODO: Make this configurable
    let stripe_plan = StripePlan::from_details(
        stripe_id,
        10000,
        1000000000,
        100,
        1,
        10000,
        amount,
        "Project".to_string(),
    );

    let mut conn = pool
        .get()
        .await
        .expect("Failed to get connection from pool");
    let created_stripe_plan: StripePlan = diesel::insert_into(stripe_plans_columns::stripe_plans)
        .values(&stripe_plan)
        .get_result(&mut conn)
        .await
        .map_err(|e| {
            log::error!("Failed to insert stripe plan: {}", e);
            ServiceError::BadRequest("Failed to insert stripe plan".to_string())
        })?;

    Ok(created_stripe_plan)
}

#[tracing::instrument(skip(pool))]
pub async fn get_plan_by_id_query(
    plan_id: uuid::Uuid,
    pool: web::Data<Pool>,
) -> Result<StripePlan, ServiceError> {
    use crate::data::schema::stripe_plans::dsl as stripe_plans_columns;

    let mut conn = pool
        .get()
        .await
        .expect("Failed to get connection from pool");
    let stripe_plan: StripePlan = stripe_plans_columns::stripe_plans
        .filter(stripe_plans_columns::id.eq(plan_id))
        .first(&mut conn)
        .await
        .map_err(|e| {
            log::error!("Failed to get stripe plan: {}", e);
            ServiceError::BadRequest("Failed to get stripe plan".to_string())
        })?;

    Ok(stripe_plan)
}

#[tracing::instrument(skip(pool))]
pub async fn get_all_plans_query(pool: web::Data<Pool>) -> Result<Vec<StripePlan>, ServiceError> {
    use crate::data::schema::stripe_plans::dsl as stripe_plans_columns;

    let mut conn = pool
        .get()
        .await
        .expect("Failed to get connection from pool");
    let stripe_plans: Vec<StripePlan> = stripe_plans_columns::stripe_plans
        .load(&mut conn)
        .await
        .map_err(|e| {
            log::error!("Failed to get stripe plans: {}", e);
            ServiceError::BadRequest("Failed to get stripe plans".to_string())
        })?;

    Ok(stripe_plans)
}

#[tracing::instrument]
pub async fn create_stripe_payment_link(
    plan: StripePlan,
    organization_id: uuid::Uuid,
) -> Result<String, ServiceError> {
    let admin_dashboard_url = get_env!("ADMIN_DASHBOARD_URL", "ADMIN_DASHBOARD_URL must be set");

    let stripe_secret = get_env!("STRIPE_SECRET", "STRIPE_SECRET must be set");
    let payment_link_create_request = reqwest::Client::new()
        .post("https://api.stripe.com/v1/payment_links")
        .header("Authorization", format!("Bearer {}", stripe_secret));

    let payment_link_form_url_encoded = json!({
        "line_items[0][price]": plan.stripe_id,
        "line_items[0][quantity]": 1,
        "allow_promotion_codes": true,
        "after_completion[redirect][url]": format!("{}/dashboard/billing", admin_dashboard_url),
        "after_completion[type]": "redirect",
        "metadata[organization_id]": organization_id.to_string(),
        "metadata[plan_id]": plan.id.to_string()
    });

    let payment_link_response = payment_link_create_request
        .header("Content-Type", "application/x-www-form-urlencoded")
        .form(&payment_link_form_url_encoded)
        .send()
        .await
        .map_err(|e| {
            log::error!("Failed to create stripe payment link: {}", e);
            ServiceError::BadRequest("Failed to create stripe payment link".to_string())
        })?;

    let payment_link_response_json: serde_json::Value =
        payment_link_response.json().await.map_err(|e| {
            log::error!("Failed to get stripe payment link json: {}", e);
            ServiceError::BadRequest("Failed to get stripe payment link json".to_string())
        })?;

    log::info!("Payment link response: {:?}", payment_link_response_json);

    let payment_link =
        payment_link_response_json["url"]
            .as_str()
            .ok_or(ServiceError::BadRequest(
                "Failed to get stripe payment link url".to_string(),
            ))?;

    Ok(payment_link.to_string())
}

#[tracing::instrument(skip(pool))]
pub async fn get_subscription_by_id_query(
    subscription_id: uuid::Uuid,
    pool: web::Data<Pool>,
) -> Result<StripeSubscription, ServiceError> {
    use crate::data::schema::stripe_subscriptions::dsl as stripe_subscriptions_columns;

    let mut conn = pool
        .get()
        .await
        .expect("Failed to get connection from pool");
    let stripe_subscription: StripeSubscription =
        stripe_subscriptions_columns::stripe_subscriptions
            .filter(stripe_subscriptions_columns::id.eq(subscription_id))
            .first(&mut conn)
            .await
            .map_err(|e| {
                log::error!("Failed to get stripe subscription: {}", e);
                ServiceError::BadRequest("Failed to get stripe subscription".to_string())
            })?;

    Ok(stripe_subscription)
}

#[tracing::instrument(skip(redis_pool, pool))]
pub async fn delete_subscription_by_id_query(
    subscription_id: uuid::Uuid,
    redis_pool: web::Data<RedisPool>,
    pool: web::Data<Pool>,
) -> Result<(), ServiceError> {
    use crate::data::schema::stripe_subscriptions::dsl as stripe_subscriptions_columns;

    let mut conn = pool
        .get()
        .await
        .expect("Failed to get connection from pool");
    let deleted_subscription: StripeSubscription = diesel::delete(
        stripe_subscriptions_columns::stripe_subscriptions
            .filter(stripe_subscriptions_columns::id.eq(subscription_id)),
    )
    .get_result::<StripeSubscription>(&mut conn)
    .await
    .map_err(|e| {
        log::error!("Failed to delete stripe subscription: {}", e);
        ServiceError::BadRequest("Failed to delete stripe subscription".to_string())
    })?;

    refresh_redis_org_plan_sub(deleted_subscription.organization_id, redis_pool, pool).await?;

    Ok(())
}

#[tracing::instrument(skip(pool))]
pub async fn get_option_subscription_by_organization_id_query(
    organization_id: uuid::Uuid,
    pool: web::Data<Pool>,
) -> Result<Option<StripeSubscription>, ServiceError> {
    use crate::data::schema::stripe_subscriptions::dsl as stripe_subscriptions_columns;

    let mut conn = pool
        .get()
        .await
        .expect("Failed to get connection from pool");
    let stripe_subscriptions: Vec<StripeSubscription> =
        stripe_subscriptions_columns::stripe_subscriptions
            .filter(stripe_subscriptions_columns::organization_id.eq(organization_id))
            .load(&mut conn)
            .await
            .map_err(|e| {
                log::error!("Failed to get stripe subscription: {}", e);
                ServiceError::BadRequest("Failed to get stripe subscription".to_string())
            })?;

    Ok(stripe_subscriptions.into_iter().next())
}

#[tracing::instrument(skip(pool, redis_pool))]
pub async fn set_stripe_subscription_current_period_end(
    stripe_subscription_id: String,
    current_period_end: chrono::NaiveDateTime,
    redis_pool: web::Data<RedisPool>,
    pool: web::Data<Pool>,
) -> Result<(), ServiceError> {
    use crate::data::schema::stripe_subscriptions::dsl as stripe_subscriptions_columns;

    let mut conn = pool
        .get()
        .await
        .expect("Failed to get connection from pool");
    let updated_subscription: StripeSubscription = diesel::update(
        stripe_subscriptions_columns::stripe_subscriptions
            .filter(stripe_subscriptions_columns::stripe_id.eq(stripe_subscription_id)),
    )
    .set(stripe_subscriptions_columns::current_period_end.eq(current_period_end))
    .get_result(&mut conn)
    .await
    .map_err(|e| {
        log::error!("Failed to update stripe subscription: {}", e);
        ServiceError::BadRequest("Failed to update stripe subscription".to_string())
    })?;

    refresh_redis_org_plan_sub(updated_subscription.organization_id, redis_pool, pool).await?;

    Ok(())
}

#[tracing::instrument]
pub async fn cancel_stripe_subscription(
    subscription_stripe_id: String,
) -> Result<(), ServiceError> {
    let stripe_client = get_stripe_client();
    let stripe_subscription_id: stripe::SubscriptionId =
        subscription_stripe_id.parse().map_err(|_| {
            ServiceError::BadRequest("Failed to parse stripe subscription id".to_string())
        })?;
    stripe::Subscription::cancel(
        &stripe_client,
        &stripe_subscription_id,
        stripe::CancelSubscription::default(),
    )
    .await
    .map_err(|e| {
        log::error!("Failed to cancel stripe subscription: {}", e);
        ServiceError::BadRequest("Request to stripe failed".to_string())
    })?;

    Ok(())
}

#[tracing::instrument(skip(redis_pool, pool))]
pub async fn update_stripe_subscription_plan_query(
    subscription_id: uuid::Uuid,
    plan_id: uuid::Uuid,
    redis_pool: web::Data<RedisPool>,
    pool: web::Data<Pool>,
) -> Result<(), ServiceError> {
    use crate::data::schema::stripe_subscriptions::dsl as stripe_subscriptions_columns;

    let mut conn = pool
        .get()
        .await
        .expect("Failed to get connection from pool");
    let updated_subscription: StripeSubscription = diesel::update(
        stripe_subscriptions_columns::stripe_subscriptions
            .filter(stripe_subscriptions_columns::id.eq(subscription_id)),
    )
    .set(stripe_subscriptions_columns::plan_id.eq(plan_id))
    .get_result::<StripeSubscription>(&mut conn)
    .await
    .map_err(|e| {
        log::error!("Failed to update stripe subscription: {}", e);
        ServiceError::BadRequest("Failed to update stripe subscription".to_string())
    })?;

    refresh_redis_org_plan_sub(updated_subscription.organization_id, redis_pool, pool).await?;

    Ok(())
}

#[tracing::instrument]
pub async fn update_stripe_subscription(
    subscription_stripe_id: String,
    plan_stripe_id: String,
) -> Result<(), ServiceError> {
    let stripe_client = get_stripe_client();

    let stripe_subscription_id: stripe::SubscriptionId =
        subscription_stripe_id.parse().map_err(|_| {
            ServiceError::BadRequest("Failed to parse stripe subscription id".to_string())
        })?;
    let list_sub_items = stripe::generated::billing::subscription_item::ListSubscriptionItems::new(
        stripe_subscription_id.clone(),
    );
    let subscription_items = stripe::SubscriptionItem::list(&stripe_client, &list_sub_items)
        .await
        .map_err(|e| {
            log::error!("Failed to list stripe subscription items: {}", e);
            ServiceError::BadRequest("Failed to list stripe subscription items".to_string())
        })?;

    let mut update_subscription_items: Vec<stripe::UpdateSubscriptionItems> = vec![];
    let mut deleted_item = stripe::UpdateSubscriptionItems::default();
    for stripe_item in subscription_items.data.iter() {
        deleted_item.id = Some(stripe_item.id.to_string());
        deleted_item.deleted = Some(true);
        update_subscription_items.push(deleted_item.clone());
    }

    let new_stripe_item = stripe::UpdateSubscriptionItems {
        plan: Some(plan_stripe_id),
        quantity: Some(1),
        ..Default::default()
    };
    update_subscription_items.push(new_stripe_item);

    let update_subscription = stripe::UpdateSubscription::<'_> {
        items: Some(update_subscription_items),
        ..Default::default()
    };

    stripe::Subscription::update(
        &stripe_client,
        &stripe_subscription_id.clone(),
        update_subscription,
    )
    .await
    .map_err(|e| {
        log::error!("Failed to update stripe subscription: {}", e);
        ServiceError::BadRequest("Failed to update stripe subscription".to_string())
    })?;

    Ok(())
}
