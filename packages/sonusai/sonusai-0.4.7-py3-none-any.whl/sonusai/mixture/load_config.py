import yaml

import sonusai


def load_config(name: str) -> dict:
    with open(file=name, mode='r') as f:
        config = yaml.safe_load(f)

    config_variable_substitution(config)
    return config


def config_variable_substitution(config: dict) -> None:
    """Find custom SonusAI variables in given dictionary and substitute their values in place"""
    for key, value in config.items():
        print(f'config[{key}] = {value}')
        if isinstance(value, dict):
            config_variable_substitution(value)
        else:
            if isinstance(value, str):
                if value == '${default_noise}':
                    config[key] = sonusai.mixture.default_noise
                    return
                if value == '${frame_size}':
                    config[key] = sonusai.mixture.frame_size
                    return
