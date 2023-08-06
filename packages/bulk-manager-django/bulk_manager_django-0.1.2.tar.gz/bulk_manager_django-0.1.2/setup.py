# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bulk_manager_django']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3', 'default-mutable>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'bulk-manager-django',
    'version': '0.1.2',
    'description': 'Easier management of the bulk create/update/delete for Django',
    'long_description': "Bulk Manager Django\n==========\n\n### *Easier management of the bulk create/update/delete for Django*\n\nBulk Manager is a plugin for Django to facilitate the bulk features of database operations.\n\n## Features\n\n- Easy to use\n- Performance optimization\n\n## Advantages\n\n- Highly flexible\n- Lightweight\n- Open-source\n- Real use cases\n- Support & documentation\n\n## Authors\n\n- Rudy Fernandez\n\n## Install\nThe easiest way to install default_mutable using pip:\n`pip install bulk-manager-django`\n\n### Methods\n\n| Attribute | Description |\n|:-:|:-|\n| `prepareCreate`  | *Add the object to the list*  |\n| `create`  | *Bulk create all the objects in the create list* |\n| `set`  | *Change an object value* |\n| `getValueFromMemory`  | *Access a specific value from an object if previously set* |\n| `update`  | *Bulk update* |\n| `prepareDelete`  | *Add the object to the list* |\n| `delete`  | *Bulk delete* |\n| `execute`  | *Perform all actions (create, update and delete) at once* |\n\n#### prepareCreate\n\n| Argument | Type | Default | Description |\n|:-:|:-:|:-:|:-|\n| `obj` | Model or list of Models |  | *Model or list of Models to update* |\n\n#### create\n\n| Argument | Type | Default | Description |\n|:-:|:-:|:-:|:-|\n| `listObj` | list | [] | *List of strings of all Models to create. If empty, create all pending records* |\n\n#### set\n\n| Argument | Type | Default | Description |\n|:-:|:-:|:-:|:-|\n| `obj` | Model |  | *Object to update* |\n| `attr` | list or str |  | *'grandfather.father.attr' or ['grandfather', 'father', 'attr']* |\n| `value` | Any |  | *Value to set* |\n\n#### getValueFromMemory\n\n| `obj` | Model |  | *Object to get the value from* |\n| `attr` | str |  | *Attribute of the object* |\n| `default_value` | Any |  | *Default value to return if not in memory* |\nFor every value updated with the method 'set' is stored in memory. 'getValueFromMemory' checks if the value has previously been updated.\n\n#### update\n\n| Argument | Type | Default | Description |\n|:-:|:-:|:-:|:-|\n| `listObj` | list | [] | *List of strings of all Models to update. If empty, create all pending records* |\n\n#### prepareDelete\n\n| Argument | Type | Default | Description |\n|:-:|:-:|:-:|:-|\n| `obj` | Model |  | *Record to delete* |\n\n#### delete\n\n| Argument | Type | Default | Description |\n|:-:|:-:|:-:|:-|\n| `listObj` | list | [] | *List of strings of all Models to delete. If empty, delete all pending records. Deletion occurs in the same order of the list* |\n\n#### execute\n\n| Argument | Type | Default | Description |\n|:-:|:-:|:-:|:-|\n| `create_order` | list | [] | *List of strings of all Models to delete. If empty, create all pending records. Creation occurs in the same order of the list* |\n| `delete_order` | list | [] | *List of strings of all Models to delete. If empty, delete all pending records. Delation occurs in the same order of the list* |\n\n### [Examples](https://github.com/roodrepo/bulk_manager_django/tree/v0-dev/examples)\n\n```python\nfrom bulk_manager_django.BulkManager import BulkManager\nBM = BulkManager()\n\nBM.prepareCreate([\n   DemoTable(\n      name        = 'built-in create1',\n      is_enabled  = True,\n      insert_type = 'built-in',\n   ),\n   DemoTable(\n      name        = 'built-in create2',\n      is_enabled  = True,\n      insert_type = 'built-in',\n   ),\n   DemoTable(\n      name        = 'built-in create3',\n      is_enabled  = True,\n      insert_type = 'built-in',\n   )\n])\n\nBM.create() # or BM.execute()\n\nfor record in DemoTable.objects.filter(insert_type = 'bulk-manager'):\n      BM.set(record, 'description', 'updated description')\n      \n      BM.set(record, 'platform_name', 'updated platform_name')\n      \n      BM.set(record, 'is_enabled', randomBool())\n      \nBM.update() # or BM.execute()\n\nfor record in DemoTable.objects.filter(insert_type = 'bulk-manager'):\n      BM.prepareDelete(record)\n      \n   \n\nBM.delete(['DemoTable']) # or BM.delete() or BM.execute() or BM.execute(delete_order= ['DemoTable'])\n\n```",
    'author': 'Rood Repo',
    'author_email': 'roodrepo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roodrepo/bulk_manager_django',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
