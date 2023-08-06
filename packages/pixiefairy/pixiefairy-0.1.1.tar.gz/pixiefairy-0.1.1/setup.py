# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pixiefairy']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.1.2,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'fastapi>=0.75.1,<0.76.0',
 'gevent>=21.12.0,<22.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pydantic-yaml>=0.6.3,<0.7.0',
 'shellingham>=1.4.0,<2.0.0',
 'typer>=0.4.1,<0.5.0',
 'urllib3>=1.26.9,<2.0.0',
 'uvicorn>=0.17.6,<0.18.0']

entry_points = \
{'console_scripts': ['pixiefairy = pixiefairy.cli:main']}

setup_kwargs = {
    'name': 'pixiefairy',
    'version': '0.1.1',
    'description': 'Pixiefairy a Pixiecore API companion',
    'long_description': '# Pixie Fairy - a Pixiecore API companion\n\n[![](https://img.shields.io/pypi/v/pixiecore.svg)](https://pypi.org/pypi/pixiefairy)\n[![Tag and build](https://github.com/mbovo/pixiefairy/actions/workflows/build-image.yml/badge.svg)](https://github.com/mbovo/pixiefairy/actions/workflows/build-image.yml)\n\nPixiefairy is a companion for [pixiecore](https://github.com/danderson/netboot/tree/master/pixiecore) tool to manage network booting of machines.\nPixiecore in [API mode](https://github.com/danderson/netboot/tree/master/pixiecore#pixiecore-in-api-mode) send a request to an external service for each pxe booting event; *pixiefairy* is that service, answering to api call and serving the required info, like the kernel, the initrd and the command line to boot.\n\nPixiefairy is higly configurable, it decide which mac-address to boot and wich set of parameters serve.\n\n## Installation\n\nPixiefairy requires `python >= 3.9`\nIt\'s as easy as\n\n```bash\npip3 install pixiefairy\n```\n\nThen you will have available the `pixiefairy` binary\n\n## Usage\n\nPixiefairy can be started using the `start` command. It requires a config.yaml file with a bunch of defaults in order to know how to serve the requests.\n\n```bash\npixiefairy start -c config.yaml\n```\n\n## Configuration\n\nAn example configuration can be found into [examples/config.yaml](./examples/config.yaml) like\n\n```yaml\ndefaults:\n  boot:\n                # the kernel to boot into\n    kernel: "file:///root/vmlinuz-amd64"\n    initrd:     # the list of initrd files to load at boot\n      - "file:///root/initramfs-amd64.xz"\n    message: "" # optional, a boot message\n    cmdline: "" # optional, the command line to boot\n  net:\n    dhcp: true                 # use dhcp or send n ip=.... kernel parameters to configure the network\n    gateway: "192.168.1.0"     # the default gateway to send to the requestor\n    netmask: "255.255.255.0"   # the netmask to send to requestor\n    dns: "8.8.8.8"         # default dns server\n    ntp: "192.168.1.0"         # default ntp server\n  deny_unknown_clients: false  # either boot unknown clients or boot only the mac address listed in mapping below\nmapping:  # optional\n  aa:bb:cc:dd:ee:ff:  # the matching mac address\n    net: null             # net block, optional, identical to the net block in defaults, override\n    boot: null            # boot block, optional, identical to the boot block in defaults, override\n```\n\n## Dev Requirements\n\nIn order to partecipate to the development you need the following requirements\n\n- [Taskfile](https://taskfile.dev)\n- Python >=3.9\n\nAnd bootstrap the local dev environment with:\n\n```bash\ntask setup\n```\n\nThis will setup locally a python virtualenv with all the dependencies, ready to start coding\n',
    'author': 'Manuel Bovo',
    'author_email': 'manuel.bovo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mbovo/pixiefairy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
