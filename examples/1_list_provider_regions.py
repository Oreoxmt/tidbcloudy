import os

import tidbcloudy

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)

for spec in api.list_provider_regions():
    print(spec)

for spec in api.list_provider_regions():
    print(spec.to_object())
