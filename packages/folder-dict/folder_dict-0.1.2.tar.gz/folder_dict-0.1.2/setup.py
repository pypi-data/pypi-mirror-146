# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['folder_dict']

package_data = \
{'': ['*']}

install_requires = \
['path-dict>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'folder-dict',
    'version': '0.1.2',
    'description': 'TThe versatile dict for Python!',
    'long_description': '# Folder Dict\nThe versatile dict for Python!\n\n# Installation\n```\npip install folder-dict\n```\nor clone this repository and run the following command.\n```\npip install -e ./\n```\n\nImport\n```py\nfrom folder_dict import FolderDict\n```\n\n# Usage\n- Import and Construct  \n    ```py\n    # Empty Folder Dict\n    fd = FolderDict(sep="/")\n    > fd\n    --> FolderDict({})\n    ```\n\n- Subscription  \n    ```py \n    user =  {\n\t    "name": "Joe",\n    \t"age": 22,\n    \t"hobbies": ["Playing football", "Podcasts"],\n\t    "friends": {\n    \t\t"Sue": {"age": 30},\n\t    \t"Ben": {"age": 35},\n    \t    }\n    }\n\n    fd = FolderDict(user, sep="/")\n    > fd["name"]\n    --> Joe\n    \n    > fd["friend/Sue/age"]\n    --> 30\n\n    > fd["/friend/Ben"]\n    --> FolderDict({\n        "age": 30,\n    })\n    ```\n\n    - Multiple inputs \n        ```py\n        > fd["name", "age","friends/Ben/age"]\n        --> ("Joe", 22, 35)\n        ```\n\n\n- Assignment  \n    Assigns the object at the given path into the FolderDict.\n    ```py\n    fd = FolderDict(sep="/")\n    fd["path/to/obj_name"] = 10\n    \n    > fd["path/to/obj_name"]\n    10\n    ```\n    - Multiple inputs  \n    ```py\n    fd["a/b", "c/d"] = (0,1)\n    > fd\n    --> FolderDict({\n        "a/b": 0,\n        "c/d": 1\n    })\n    ```\n\n- list\n    Lists all paths contained in the FolderDict.\n    ```py\n    fd["a/b", "c/d"] = (0,1)\n    > fd.list()\n    --> ["/a/b", "/c/d"]\n    ```\n\n- Direct card `~`  \n    Get paths ending with "c".\n    ```py\n    fd["a/b/c", "d/e/f/abc", "g/h/c", "i/j"] = (1,2,3,4)\n    > fd.list("~c")\n    --> ["/a/b/c", "/d/e/f/abc", "/g/h/c"]\n    ```\n    *cf.*\n    ```py\n    > fd.list("~/c")\n    --> ["a/b/c", "g/h/c"]\n    ```\n\n- Properties\n    ```py\n    fd["a/b","a/c"] = (1,2)\n\n    # dict\n    > fd.dict\n    --> {\'a\': {\'b\': 1, \'c\': 2}}\n    \n    # PathDict\n    > fd.PathDict\n    -->PathDict({\n      "a": {\n        "b": 1,\n        "c": 2  \n      }\n    })\n\n    # sep\n    > fd.sep\n    --> \'/\'\n    ```\n\n',
    'author': 'Yasuhiro Shimomura',
    'author_email': '22shimoyasu22@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Geson-anko/folder_dict',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
