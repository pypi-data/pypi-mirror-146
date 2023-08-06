import importlib
import re
from sys import exc_info
from traceback import format_exception
from typing import List

import toml


class PluginManager:
    @classmethod
    def get_plugins(cls, chain: str, setting_toml_path: str) -> List:
        obj = toml.load(setting_toml_path)
        plugins = []
        for module_name in obj["senka"]["plugin"]["senka_plugin"]:
            try:
                module = importlib.import_module(
                    f"{module_name}.{module_name}", "module_name"
                )
                dir = re.sub("_(.)", lambda x: x.group(1).upper(), module_name)
                dir = dir[0].upper() + dir[1:]
                plugin_class = getattr(module, dir)
                if plugin_class.chain.lower() == chain.lower():
                    plugins.append(plugin_class)
            except Exception as e:
                etype, value, tb = exc_info()
                info = format_exception(etype, value, tb)[-2]
                raise RuntimeError(
                    f"Failed to get plugin. plugin name: {module_name}. Exception in {info}. {e}"
                )
        return plugins
