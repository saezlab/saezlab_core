import os
import sys
import pathlib as pl
import platformdirs


from omegaconf import OmegaConf, DictConfig

__all__ = [
    'ConfigLoader',
]


class ConfigLoader:
    """Loader for YAML configuration files with merging and priority logic.

    This class provides a static method to load and merge configuration files from
    package defaults, user directory, working directory, and an explicit path, returning
    a single merged DictConfig object.
    """

    @staticmethod
    def load(
        config_path: str,
        search_paths: list[str] | None = None,
        default_config: str | None = None,
    ) -> DictConfig:
        """Loads and merges YAML configs in priority order.

        1. Package default (if provided)
        2. User config in home dir (if exists)
        3. Config in working dir (if exists)
        4. Explicit config_path (highest priority)

        Returns:
            DictConfig: The merged configuration object.
        """
        configs = []
        # 1. Package default
        if default_config and os.path.exists(default_config):
            configs.append(OmegaConf.load(default_config))
        # 2. User config
        user_config = os.path.expanduser('~/.saezlab_core.yaml')
        if os.path.exists(user_config):
            configs.append(OmegaConf.load(user_config))
        # 3. Working dir config
        cwd_config = os.path.join(os.getcwd(), 'saezlab_core.yaml')
        if os.path.exists(cwd_config):
            configs.append(OmegaConf.load(cwd_config))
        # 4. Explicit config_path
        if config_path and os.path.exists(config_path):
            configs.append(OmegaConf.load(config_path))
        # Merge all configs (later overrides earlier)
        if configs:
            merged = OmegaConf.merge(*configs)
        else:
            merged = OmegaConf.create({})
        return merged


def read_config(path: str | pl.Path) -> DictConfig:

    path = pl.Path(path)

    return OmegaConf.load(path) if path.exists() else DictConfig({})


def merge_config(default: DictConfig, override: DictConfig) -> DictConfig:

    merged = OmegaConf.merge(default, override)

    return merged


def path_discovery(module: str) -> list[pl.Path]:

    paths = []

    # Default config
    paths.append(pl.Path(sys.modules[module].__path__[0], "_config", "default.yaml"))

    # Home user config
    paths.append(pl.Path(platformdirs.user_config_dir(module), "config.yaml"))

    # Current working directory config
    paths.append(pl.Path(os.getcwd(), f"{module}.yaml"))

    return paths


def load_config(*paths) -> DictConfig:

    config = DictConfig({})

    for path in paths:
        this_config = read_config(path)
        config = merge_config(config, this_config)

    return config


def get_config(module: str) -> DictConfig:

    paths = path_discovery(module)

    config = load_config(*paths)

    return config