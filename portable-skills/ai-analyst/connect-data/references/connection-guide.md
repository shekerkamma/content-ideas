# Connection Guide — SQL Dialects & Setup

## CSV Files

**Connection string:** File path to directory containing `.csv` files

**Template:**
```yaml
type: csv
path: data/my_dataset/
delimiter: ","
encoding: utf-8
```

**Notes:**
- Relative paths resolve from the repo root
- All `.csv` files in the directory are loaded as tables
- Table names are derived from filenames (lowercase, underscores)

---

## DuckDB

**Connection string:** Path to `.duckdb` file

**Template:**
```yaml
type: duckdb
path: data/my_dataset.duckdb
```

**SQL Dialect:** DuckDB's SQL is largely compatible with PostgreSQL, with extensions for analytics (PIVOT, window functions, etc.)

**Notes:**
- DuckDB provides in-process SQL execution — very fast for local datasets
- Can read CSV, Parquet, JSON natively
- Supports complex queries and window functions

---

## MotherDuck

**Connection string:** Cloud database via MCP token

**Template:**
```yaml
type: motherduck
database: my_database
schema: my_schema
token_env: MOTHERDUCK_TOKEN
```

**SQL Dialect:** MotherDuck is based on DuckDB, so SQL is the same

**Setup:**
1. Sign up at motherduck.com
2. Get your authentication token
3. Store in environment: `export MOTHERDUCK_TOKEN="your_token"`
4. Verify: `duckdb -c "SELECT 1"`

**Notes:**
- MotherDuck is cloud-hosted DuckDB — fast analytics on cloud data
- Can query external data (S3, GCS, BigQuery, etc.) directly
- Requires stable internet connection

---

## PostgreSQL

**Connection string:** Host, database, user, password

**Template:**
```yaml
type: postgres
host: localhost
port: 5432
database: my_db
schema: public
user: my_user
password_env: PG_PASSWORD
```

**SQL Dialect:** PostgreSQL (ANSI SQL with extensions)

**Setup:**
1. Install PostgreSQL locally or use cloud (RDS, Heroku, etc.)
2. Store password in environment: `export PG_PASSWORD="your_password"`
3. Test: `psql -h localhost -U my_user -d my_db -c "SELECT 1"`

**Notes:**
- PostgreSQL is a mature relational database
- Excellent support for complex queries, CTEs, window functions
- Can handle very large datasets with indexing

---

## Google BigQuery

**Connection string:** Project ID, dataset, credentials file

**Template:**
```yaml
type: bigquery
project_id: my-gcp-project
dataset: my_dataset
credentials_file: ~/.gcp/service-account-key.json
```

**SQL Dialect:** BigQuery SQL (ANSI SQL with analytics extensions)

**Setup:**
1. Create a GCP project and enable BigQuery
2. Create a service account and download JSON key
3. Store key at `~/.gcp/service-account-key.json`
4. Test: `bq query --use_legacy_sql=false "SELECT 1"`

**Notes:**
- BigQuery is Google's data warehouse — handles petabyte-scale data
- Excellent for very large datasets
- Pay per query (not per storage)
- Fast columnar analysis

---

## Snowflake

**Connection string:** Account, warehouse, database, user, password

**Template:**
```yaml
type: snowflake
account: xy12345.us-east-1
warehouse: compute_wh
database: my_db
schema: public
user: my_user
password_env: SNOWFLAKE_PASSWORD
```

**SQL Dialect:** Snowflake SQL (ANSI SQL with extensions)

**Setup:**
1. Create a Snowflake account
2. Create a warehouse and database
3. Create a user and assign role
4. Store password in environment: `export SNOWFLAKE_PASSWORD="your_password"`
5. Test: `snowsql -a xy12345 -u my_user -d my_db -c "SELECT 1"`

**Notes:**
- Snowflake is a cloud data warehouse — scales elastically
- Great for shared analytics (separation of compute and storage)
- Supports semi-structured data (JSON, Parquet)

---

## Connection Testing

For each type, use the ConnectionManager helper:

```python
from helpers.connection_manager import ConnectionManager

config = {
    "type": "postgres",
    "host": "localhost",
    "database": "my_db",
    "user": "my_user",
    "password_env": "PG_PASSWORD"
}

cm = ConnectionManager(config)

# Test connection
if cm.test_connection():
    print("✓ Connected!")
    tables = cm.list_tables()
    print(f"Found {len(tables)} tables")
else:
    print("✗ Connection failed")
```

---

## Credential Security

**Best practices:**
1. **Never store passwords in manifest files** — always use environment variables
2. **Use service accounts for cloud services** — not personal credentials
3. **Rotate credentials regularly** — especially for production databases
4. **Use VPN or SSH tunnels for remote databases** — when connecting from outside the network
5. **Restrict database user permissions** — read-only for analysis, never admin

**Environment variable naming convention:**
- `PG_PASSWORD` for PostgreSQL
- `MOTHERDUCK_TOKEN` for MotherDuck
- `BIGQUERY_CREDENTIALS` for BigQuery
- `SNOWFLAKE_PASSWORD` for Snowflake
- `DATABASE_URL` for connection strings (PostgreSQL-style)
