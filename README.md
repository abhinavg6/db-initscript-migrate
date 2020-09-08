# db-initscript-migrate

## Repo for migrating the Databricks global init scripts v1 to v2

[Migrate your v1 global init scripts to v2](https://docs.databricks.com/clusters/init-scripts.html#migrate-from-legacy-to-new-global-init-scripts) in a Databricks workspace. This repo is to assist with `Step 1` in the migration docs. The bits are:
* dbx_init_script_migrater.py - The main script that should be run to migrate the v1 global init scripts to v2.
* dbx_api_client.py - An API client to interact with the Databricks DBFS and Global Init Scripts APIs.
* dbx_gis_v1 - A folder where all v1 global init scripts will be copied to during the migration process.
* dbx_test_src - A folder containing a test shell script that would be copied as a v1 global init script before the migration process.

## Migration Process
* Make sure you've installed `databricks-cli` via `pip` in your environment.
* Replace the workspace URL and credentials (user and PAT) in `dbx_init_script_migrater.py`. This should be done per workspace.
* Per workspace, run the script as `python dbx_init_script_migrater.py`