import pytest
import main


def test_load_config_success(tmp_path):
    cfg = main.load_config('config.yaml')
    assert 'paths' in cfg
    assert 'models' in cfg


def test_load_config_missing():
    with pytest.raises(FileNotFoundError):
        main.load_config('no-such-file.yaml')
