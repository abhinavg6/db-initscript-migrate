# Interface for Databricks API, using Databricks CLI

from databricks_cli.sdk import ApiClient
from databricks_cli.dbfs.api import DbfsApi
from databricks_cli.dbfs.dbfs_path import DbfsPath

class DatabricksAPIClient(object):

    def __init__(self, user, token, workspaceUrl):
        self.dbcli_apiclient = ApiClient(user, password=token, host=workspaceUrl, 
                                verify=True, command_name='Python Client')
        self.dbfs_api_client = DbfsApi(self.dbcli_apiclient)

    # List init script directory
    def _list_init_script_dir(self, srcPath="dbfs:/databricks/init"):
        print("Starting to list the legacy global init scripts folder")
        files = self.dbfs_api_client.list_files(dbfs_path=DbfsPath(srcPath))
        file_list = [f.dbfs_path.absolute_path for f in files]
        return file_list

    # Copy global init script to local
    def _cp_legacy_gis_to_local(self, srcPath="dbfs:/databricks/init", destPath="./dbx_gis_v1"):
        print("Starting to copy the legacy global init scripts to path {}".format(destPath))
        self.dbfs_api_client.cp(recursive=True, overwrite=True, src=srcPath, dst=destPath)
        print("Copied the legacy global init scripts to path {}".format(destPath))

    def _copy_test_file(self):
        self.dbfs_api_client.cp(recursive=False, overwrite=True, src="./dbx_test_src/random.sh", 
            dst="dbfs:/databricks/init")
        print("copied test file")

    def _remove_test_file(self):
        self.dbfs_api_client.delete(dbfs_path=DbfsPath("dbfs:/databricks/init/random.sh"), recursive=False)
        print("removed test file")

    # Upload the init script as a global init script v2
    # By default disabled & placed at the last location in the order of execution
    def _upload_init_script_as_gis_v2(self, script_name, base64_encoded_content):
        request_data  = {
            "name": script_name,
            "script": base64_encoded_content
        }
        self.dbcli_apiclient.perform_query(method='POST', path='/global-init-scripts', data=request_data)
        print("Script uploaded as GIS v2 - {}".format(script_name))
