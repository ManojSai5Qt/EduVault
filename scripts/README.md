# Project scripts

These are maintenance helpers; the Streamlit application starts from the repository root with `python -m streamlit run app.py`.

## Run the dashboard on Windows

From PowerShell, run:

```powershell
.\scripts\run_app.ps1
```

The launcher uses the Python installation available on your PATH. It does not depend on a personal pgAdmin installation path.

## Optional demo-data seeder

`data/seed_demo_data.py` inserts sample academic records into PostgreSQL and sample content/activity documents into MongoDB. Run it only when you intentionally want those additional demo records:

```powershell
python .\scripts\data\seed_demo_data.py
```

It expects the local database settings in the repository-root `.env` file and the required tables/collections to exist. It is not needed to start the dashboard.

## Diagnostics

- `diagnostics/check_postgres_schema.py`: lists PostgreSQL table columns and data types.
- `diagnostics/check_postgres_constraints.py`: inspects null rules, defaults and constraints.
- `diagnostics/check_relationships.py`: displays selected PostgreSQL and MongoDB relationship values.
- `diagnostics/inspect_mongodb.py`: shows document counts and sample fields from two MongoDB collections.

Run a diagnostic from the repository root, for example:

```powershell
python .\scripts\diagnostics\check_postgres_schema.py
```

All diagnostic scripts read the project-root `.env` through the existing database helpers. Never commit your real `.env` credentials.
