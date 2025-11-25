use axum::{Router, routing::get};
use sqlx::Error;

crate::models::activity::{Activity};

fn get_activity_data(activity_id: u64) -> Result<Activity, Error> {}

pub fn router() -> Router {
    Router::new().route(
        "/data/{activity_id}",
        get(get_activity_data).delete(delete_activity_data),
    )
}
