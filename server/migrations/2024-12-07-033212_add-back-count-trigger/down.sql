-- This file should undo anything in `up.sql`
DROP TRIGGER increase_chunk_metadata_counts_trigger ON chunk_metadata;
DROP TRIGGER delete_chunk_metadata_counts_trigger ON chunk_metadata;
DROP FUNCTION update_chunk_metadata_counts;
