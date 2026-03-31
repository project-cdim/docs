# 4. Plugin Configuration

This chapter describes the files and classes that make up a plugin.

## 4.1. File Structure

A plugin is a Python module.
Place one directory per Design Engine plugin under `layout-design-compose/layout-design/plugins/` in the Layout Design.

```text
plugins/
├── Plugin1/
│   ├── plugin_file.py
│   └── other_dir/module.py
├── Plugin2/
│   ├── plugin_file.py
│   └── other_dir/module.py
└── sample_design_engine/
```

Name the plugin file using the format `plugin_XXX.py` starting with `plugin_`.
Define the classes explained in [4.2. Class Structure](04_Configuration.md#42-class-structure) in the plugin file.
Add any other needed modules or configuration files as required.  
At startup, the Layout Design searches for plugin files under `layout-design-compose/layout-design/plugins/` and loads them as plugins using the `importlib` module.
When loading, if the properties/functions described in [4.2. Class Structure](04_Configuration.md#42-class-structure) and [5. Implementing the Plugin](05_Implementing_plugin.md) are not implemented, the Layout Design will fail to start.

## 4.2. Class Structure

Implement your plugin by inheriting from the base class shown below.

![Plugin Class Diagram](images/04_plugin.png)

`BaseDesignEnginePlugin` is the base class for plugins and is defined in `layout-design-compose/layout-design/layout-design/src/common/base.py`.
Plugins inherit this class and implement the methods described in [2.2. Plugin Overview](02_LayoutDesignFunctions.md#22-plugin-overview).
See [5. Implementing the Plugin](05_Implementing_plugin.md) for implementation details.

Import as follows:
```python
from common.base import BaseDesignEnginePlugin
```
