# Streamlit Community Cloud setup

## Why the app showed localhost errors

A Streamlit Community Cloud app runs in a remote container. `localhost` refers to that container, not a PostgreSQL or MongoDB server on your laptop. EduVault therefore needs externally hosted database endpoints for live mode.

## Run the deployed app immediately

After the code update deploys, an app without database credentials starts in **DEMO MODE** with clearly labelled generated records. This keeps the dashboard usable, but does not provide live query statistics or live database information.

## Enable live PostgreSQL and MongoDB

1. Create or choose a hosted PostgreSQL database and a hosted MongoDB database (for example, a MongoDB Atlas cluster).
2. Initialize the EduVault PostgreSQL schema and populate the required academic tables.
3. Create/populate the MongoDB `activity_logs` collection with the fields used by EduVault.
4. In Streamlit Community Cloud, open the deployed app, select **Manage app → Settings → Secrets**, and paste the TOML below after replacing every placeholder.
5. Save the secrets and restart/reboot the app if it does not restart automatically.

```toml
DATABASE_URL = "postgresql://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require"
MONGO_URI = "mongodb+srv://USER:PASSWORD@CLUSTER.mongodb.net/?retryWrites=true&w=majority"
MONGO_DB = "eduvault_mongo"
EDUVAULT_DEMO_MODE = "false"
```

The `DATABASE_URL` and `MONGO_URI` values must be the external connection strings supplied by the database providers. Do not use `localhost`, and do not put real credentials in GitHub or in a committed `.env` file.

The database providers must accept connections from the Streamlit app's runtime network. Check provider TLS requirements and network/IP access rules if authentication succeeds but the connection still times out.

## Demo/live mode control

- Omit the database connection keys and `EDUVAULT_DEMO_MODE`: the app automatically opens in clearly labelled demo mode.
- Set `EDUVAULT_DEMO_MODE = "true"`: explicitly use sample records when a database is unavailable.
- Set `EDUVAULT_DEMO_MODE = "false"`: require both real database connections. The app stops with a visible error if either connection fails.

When both PostgreSQL and MongoDB connect, the dashboard reports **LIVE DATA MODE** and uses the configured databases. Server-wide PostgreSQL workload history still requires the DBA to enable `pg_stat_statements`; live query timing, EXPLAIN plans, replication state, and index metadata depend on the actual database server and user permissions.

## Local development

You can continue to use a local `.env` file. It is ignored by Git. Alternatively, create `.streamlit/secrets.toml` for local Streamlit development; that file is also ignored by Git. Use the same root-level TOML keys shown above.
