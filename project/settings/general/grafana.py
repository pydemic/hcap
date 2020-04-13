from ..env import env

_url = env("HCAP__GRAFANA_URL", default="http://localhost:3000")
_token = env("HCAP__GRAFANA_DASHBOARD_TOKEN", default="OMynCUCWz")

GRAFANA_DASHBOARD_URL = f"{_url}/d/{_token}/capacidade-hospitalar?orgId=1"
