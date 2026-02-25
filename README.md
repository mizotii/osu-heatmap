# osu-heatmap

A lightweight web app that fetches osu! user statistics and renders per-player heatmaps and score summaries across all modes. This repository contains a Python/Flask backend (API + data sync) and a Svelte frontend client. Project now deprecated.

## Features

- OAuth2 login via osu! (v2)
- Per-user heatmaps for `osu`, `taiko`, `fruits` (catch), and `mania`
- Scheduled background updates of player statistics
- Simple search and profile pages
- Serves the compiled Svelte frontend from the Flask backend in production
