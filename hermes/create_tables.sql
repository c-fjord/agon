CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    moving_time INTEGER,
    elapsed_time INTEGER,
    type TEXT,
    distance FLOAT8,
    start_date TIMESTAMPTZ NOT NULL
);

CREATE TABLE activity_data (
    time TIMESTAMPTZ NOT NULL,
    latitude FLOAT8,
    longitude FLOAT8,
    altitude FLOAT8,
    heartrate INTEGER,
    distance FLOAT8,
    activity_id INTEGER REFERENCES activities ON DELETE CASCADE ON UPDATE CASCADE
);

SELECT create_hypertable('activity_data', 'time');