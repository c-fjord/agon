use serde::Serialize;
use sqlx::FromRow;

#[derive(Serialize, FromRow)]
pub struct Metadata {
    id: i32,
    name: String,
    moving_time: i32,
    elapsed_time: i32,
    activity_type: String,
    distance: f32,
    start_date: String,
}
