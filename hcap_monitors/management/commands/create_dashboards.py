from hcap_utils.contrib.management import BaseCommand

from hcap_monitors.state_dashboard_generator import generate_json_dashboards
from hcap_geo.models import Region


class Command(BaseCommand):
    help = "Creates Grafana dashboard's json for each state based on the template.json"

    def safe_handle(
        self,
        **options,
    ):
        states = Region.objects.filter(kind=Region.KIND_STATE).values_list("name", "code")
        generate_json_dashboards(states)
