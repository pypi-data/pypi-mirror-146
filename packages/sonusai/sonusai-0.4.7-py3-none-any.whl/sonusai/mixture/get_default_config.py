import sonusai
from sonusai.mixture import load_config


def get_default_config() -> dict:
    try:
        return load_config(sonusai.mixture.default_config)
    except Exception as e:
        raise sonusai.SonusAIError(f'Error loading default config: {e}')
