import os

import tidbcloudy

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
project = api.create_project(name="your_project_name", aws_cmek_enabled=False, update_from_server=True)
print(project)
