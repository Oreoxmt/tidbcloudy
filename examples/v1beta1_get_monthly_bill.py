import os

import tidbcloudy

public_key = os.environ.get("PUBLIC_KEY")
private_key = os.environ.get("PRIVATE_KEY")
debug_mode = os.environ.get("TIDBCLOUDY_LOG")

api = tidbcloudy.TiDBCloud(public_key=public_key, private_key=private_key)
billing = api.get_monthly_bill(month="2023-10")
# billing = api.get_current_month_bill()
print(billing)
print(billing.overview)
print(billing.summaryByProject)
print(billing.summaryByService)
