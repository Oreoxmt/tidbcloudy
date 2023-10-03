import os

import tidbcloudy
from tidbcloudy.specification import ProjectAWSCMEKSpecs

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
# Create a project with AWS CMEK enabled
project = api.create_project(name="0", aws_cmek_enabled=True, update_from_server=True)
print(project)

# Configure AWS CMEK for the project
cmek_config = ProjectAWSCMEKSpecs()
cmek_config \
    .set_cmek("your_aws_region_1", "your_aws_kms_arn_1") \
    .set_cmek("your_aws_region_2", "your_aws_kms_arn_2")
project.config_aws_cmek(cmek_config)

# List all AWS CMEKs of the project
for cmek in project.iter_aws_cmek():
    print(cmek)
