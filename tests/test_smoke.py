from pathlib import Path

import spacex_dash_app


def test_dataset_is_present() -> None:
    assert Path(spacex_dash_app.DATA_PATH).exists()


def test_dataset_loads_with_expected_columns() -> None:
    dataframe = spacex_dash_app.load_spacex_data()
    assert not dataframe.empty
    assert {"Launch Site", "class", "Outcome", "Payload Mass (kg)"} <= set(dataframe.columns)


def test_dash_app_exposes_server() -> None:
    assert spacex_dash_app.app is not None
    assert spacex_dash_app.server is not None
