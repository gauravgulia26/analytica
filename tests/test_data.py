from analytica.core.config.paths import DATA_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR


def test_data_paths_configured():
    assert DATA_DIR.name == "data"
    assert RAW_DATA_DIR.name == "raw"
    assert PROCESSED_DATA_DIR.name == "processed"
