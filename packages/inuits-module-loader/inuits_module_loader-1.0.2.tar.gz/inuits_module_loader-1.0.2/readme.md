# Readme
This library is the same as the Django utils module loader, but without needing Django as dependency.
It is used to load modules/classes based on their dotted string path.

## Install
pip install inuits-module-loader

## Usage
```python
from inuits_module_loader import import_string
import_string("dotted.path.to.your.module.or.class")
```

## Example
This example will dynamically load classes in the extensions/resources folder that extend the default classes in the application.
Default class: resources.your_file_name.YourClassName

Class in extensions folder: extensions.resources.your_file_name.YourClassName

It is recommended to name the extension file and class the same as the default class, and import the default class with an alias in your extension class.

### Extended class
```python
from resources.your_file_name.YourClassName import YourClassName as DefaultYourClassName

class YourClassName(DefaultYourClassName):

    def do_something(self):
        return True
```

### App
```python
from inuits_module_loader import import_string
import logging

logger = logging.getLogger(__name__)

# This function will try to load your class from the extension folder and fall back to the default class if there is no extension available for that class.
def load_resource(resource: str):
    try:
        logger.info(f"Loading {resource} extension.")
        return import_string(f"extensions.resources.{resource}")
    except ModuleNotFoundError:
        logger.info(f"No {resource} extension found, loading core {resource}")
        return import_string(f"resources.{resource}")
    except ImportError as error:
        logger.info(f"{error}, loading core {resource}")
        return import_string(f"resources.{resource}")

# If you name your extended file and class the same as the default file and class you can easily add or remove classes from the extensions folder without adding additional code in the app.
your_class = load_resource("your_file_name.YourClassName")()

```




