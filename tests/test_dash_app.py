"""Browser-level smoke tests for the required dashboard elements."""

from app import REGIONS, app


def test_health_endpoint_is_ready():
    response = app.server.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_header_is_present(dash_duo):
    dash_duo.start_server(app)
    header = dash_duo.wait_for_element("#dashboard-header")
    assert header.is_displayed()
    assert "Pink Morsel" in header.text


def test_visualization_is_present(dash_duo):
    dash_duo.start_server(app)
    graph = dash_duo.wait_for_element("#sales-line-chart .js-plotly-plot")
    assert graph.is_displayed()


def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app)
    picker = dash_duo.wait_for_element("#region-picker")
    assert picker.is_displayed()
    labels = [label.text.lower() for label in picker.find_elements("css selector", "label")]
    assert labels == REGIONS
