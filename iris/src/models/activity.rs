use serde::Serialize;
use sqlx::FromRow;

#[derive(Serialize, FromRow)]
pub struct Activity {
    time: Vec<f32>,
    latitude: Vec<f32>,
    longitude: Vec<f32>,
    altitude: Vec<f32>,
    heartrate: Vec<f32>,
    distance: Vec<f32>,
}
