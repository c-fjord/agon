pub fn router() -> Router {
    Router::new().route(
        "/metadata/{activity_id}",
        get(get_activity_data)
            .put(update_activity_metadata)
            .delete(delete_activity_metadata),
    )
}
