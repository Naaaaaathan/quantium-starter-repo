from src.visualisation import app


def test_visualisation_components_are_rendered(dash_duo):
    dash_duo.start_server(app)

    dash_duo.start_server(app)

    dash_duo.wait_for_text_to_equal("#header","Were sales higher before or after the Pink Morsel price increase on the 15th of January, 2021?",timeout=10,)
    dash_duo.wait_for_element("#example-graph", timeout=10)
    dash_duo.wait_for_element("#region-selector", timeout=10)
