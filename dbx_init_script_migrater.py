# This is a quick and dirty script to migrate GIS v1 init scripts in a workspace to GIS v2
# GIS - Global Init Scripts

import sys
import re
import base64

from dbx_api_client import DatabricksAPIClient

# Provide your workspace URL, user and personal authentication token (PAT)
api_client = DatabricksAPIClient(user="abhinav.garg@databricks.com", 
    token="dapiac7e8b172b5086179ec7303da59978e5", workspaceUrl="https://eastus2.azuredatabricks.net/")

# Just copying a test file from ./dbx_test_src to GIS v1 init script path
api_client._copy_test_file()

file_list = api_client._list_init_script_dir()
for f in file_list:
    # Check if it's a GIS v1 init script or just another file/folder
    if(re.search("dbfs:\/databricks\/init\/.*\.sh", f) is not None):
        print("Found global init script {}".format(f))
        try:
            # Copy the GIS v1 init script to local at ./dbx_gis_v1
            api_client._cp_legacy_gis_to_local(srcPath=f)

            # Generate the base64-encoded form of the init script
            local_f = f.replace("dbfs:/databricks/init/","./dbx_gis_v1/")
            with open(local_f) as file_obj:
                file_str = file_obj.read()
            encoded_file = file_str.encode()
            base64_encoded_file = base64.standard_b64encode(encoded_file).decode()

            ## Upload the init script as GIS v2 (it'll be disabled by default)
            script_name = f.replace("dbfs:/databricks/init/","")
            api_client._upload_init_script_as_gis_v2(script_name=script_name,
                base64_encoded_content=base64_encoded_file)
        except:
            print("Something went wrong while processing the file {}, {}".format(f, sys.exc_info()[0]))
            continue

# Removing the test file from GIS v1 init script path
# This test file is also available on local at ./dbx_gis_v1
api_client._remove_test_file()