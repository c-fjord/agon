use std::sync::Arc;

use crate::models::activity::Activity;
use sqlx::Error;

pub struct ActivityRepository {
    conn: sqlx::PgPool,
}

pub trait ActivityRepositoryTrait {
    fn new(conn: &Arc<sqlx::PgPool>) -> Self;
    async fn find(&self, id: i64) -> Result<Activity, Error>;
    async fn delete(&self, id: u64) -> Result<(), Error>;
}

impl ActivityRepositoryTrait for ActivityRepository {
    fn new(conn: &Arc<sqlx::PgPool>) -> Self {
        Self {
            conn: Arc::clone(conn),
        }
    }
    async fn find(&self, id: i64) -> Result<Activity, Error> {
        let query = sqlx::query_as::<_, Activity>("SELECT * FROM activity WHERE id = ?").bind(id);

        let activity = query.fetch_one(&self.conn).await?;

        Ok(activity)
    }
    async fn delete(&self, id: u64) -> Result<(), Error> {
        let query = sqlx::query_as::<_, Activity>("DELETE FROM activity WHERE id=$1").bind(id);
        query.bond;

        Ok()
    }
}
