# from tests import _PATH_CONFIG
import random
import os
import yaml

def test_seed():
    """Test that the seed is set to 42"""
    _PATH_CONFIG = "imperfect_trainings/config/experiment/"
    config_files = os.listdir(_PATH_CONFIG)
    
    # open every yaml file in the config/experiment folder
    for config_name in config_files:
        file_path = _PATH_CONFIG + config_name

        # read the yaml file
        with open(file_path, "r") as f:
            config = yaml.safe_load(f)
            if "seed_value" not in config:
                assert False, f"No seed_value found in {config_name}"
            assert config["seed_value"] == 42, f"Seed_value in {config_name} is not set to 42"
