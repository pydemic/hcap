from pathlib import Path


def generate_json_dashboards(states):
    monitor_path = Path(__file__).parent
    dashboards_path = monitor_path / "grafana" / "dashboards"
    template_content = open(monitor_path / "template.json", "r").read()

    for (state, state_code) in states:
        state_content = template_content.replace("Bahia", state)
        state_content = state_content.replace("ninechars", state_code)
        open(dashboards_path / f"{state}.json", "w").write(state_content)
