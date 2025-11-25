use std::{error::Error, sync::Arc};

use axum::{Router, routing::get};
use sqlx::PgPool;

mod routes;

mod utils;

#[derive(Clone, Default)]
pub struct AppState {
    db: sqlx::PgPool,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let url = "";
    let pool = sqlx::postgres::PgPool::connect(url).await?;

    let app_state = Arc::new(AppState { db: pool.clone() });

    // build our application with a route
    let app = Router::new()
        .route("/", get(|| async { "Hello, World!" }))
        .merge(activity::router())
        .merge(metadata::router())
        .with_state(app_state);

    // run our app with hyper, listening globally on port 3000
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();

    Ok(())
}
