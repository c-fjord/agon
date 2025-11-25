use sqlx::Error;
pub struct MetadataRepository {}

use crate::models::Metadata;

impl MetadataRepositoryTrait for MetadataRepository {
    async fn find(&self, id: u64) -> Result<Metadata, Error> {
        let query = sqlx::query_as::<_, ActivityMetadata>("SELECT * FROM metadata WHERE id=$1")
            .bind(activity_id);

        let metadata = query.fetch_one(conn).await?;

        Ok(metadata)
    }
    async fn update(&self, metadata: Metadata) -> Result<(), Error> {}
    async fn delete(&self, id: u64) -> Result<(), Error> {}
}
