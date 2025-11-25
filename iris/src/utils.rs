use axum::{
    Json,
    http::StatusCode,
    response::{IntoResponse, Response},
};
use serde_json::json;

pub struct APIError {
    pub message: String,
    pub status_code: StatusCode,
}

impl IntoResponse for APIError {
    fn into_response(self) -> Response {
        (
            self.status_code,
            Json(json!({ "StatusCode": self.status_code.as_u16(), "Message": self.message })),
        )
            .into_response()
    }
}
