USE osu_heatmap;

CREATE TABLE IF NOT EXISTS api_tokens (
    user_id INT DEFAULT NULL,
    access_id VARCHAR(255),
    refresh_id VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS users (
    user_id INT DEFAULT NULL,
    user_rank int
);