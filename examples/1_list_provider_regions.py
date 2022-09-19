import os

import tidbcloudy

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)

for spec in api.list_provider_regions():
    print(f"- type: {spec.cluster_type.value}")
    print(f"  provider: {spec.cloud_provider.value}")
    print(f"  region: {spec.region}")
    print(f"  components:")
    for tidb in spec.tidb:
        print(f"  - tidb: {tidb.node_size}; "
              f"min={tidb.node_quantity_range.min} step={tidb.node_quantity_range.step}")
    for tikv in spec.tikv:
        print(f"  - tikv: {tikv.node_size}; "
              f"min={tikv.node_quantity_range.min} "
              f"step={tikv.node_quantity_range.step}; "
              f"{tikv.storage_size_gib_range.min}..{tikv.storage_size_gib_range.max} GiB")
    for tiflash in spec.tiflash:
        print(
            f"  - tiflash: {tiflash.node_size}; "
            f"min={tiflash.node_quantity_range.min} step={tiflash.node_quantity_range.step}; "
            f"{tiflash.storage_size_gib_range.min}..{tiflash.storage_size_gib_range.max} GiB")
