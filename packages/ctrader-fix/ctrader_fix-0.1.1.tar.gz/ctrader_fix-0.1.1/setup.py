# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ctrader_fix']

package_data = \
{'': ['*']}

install_requires = \
['Twisted==21.7.0']

setup_kwargs = {
    'name': 'ctrader-fix',
    'version': '0.1.1',
    'description': 'A Python package for interacting with cTrader FIX API',
    'long_description': '# cTraderFixPy\n\n\n[![PyPI version](https://badge.fury.io/py/ctrader-fix.svg)](https://badge.fury.io/py/ctrader-fix)\n![versions](https://img.shields.io/pypi/pyversions/ctrader-fix.svg)\n[![GitHub license](https://img.shields.io/github/license/spotware/cTraderFixPy.svg)](https://github.com/spotware/cTraderFixPy/blob/main/LICENSE)\n\nA Python package for interacting with cTrader FIX API.\n\nThis package uses Twisted and it works asynchronously.\n\n- Free software: MIT\n- Documentation: https://spotware.github.io/cTraderFixPy/.\n\n\n## Features\n\n* Works asynchronously by using Twisted\n\n* Allows you to easily interact with cTrader FIX API and it manages everything in background\n\n* Generate FIX message by using Python objects\n\n## Insallation\n\n```\npip install ctrader-fix\n```\n\n# Config\n\nConfig file sample:\n\n```json\n{\n  "Host": "",\n  "Port": 0,\n  "SSL": false,\n  "Username": "",\n  "Password": "",\n  "BeginString": "FIX.4.4",\n  "SenderCompID": "",\n  "SenderSubID": "QUOTE",\n  "TargetCompID": "cServer",\n  "TargetSubID": "QUOTE",\n  "HeartBeat": "30"\n}\n```\n\n# Usage\n\n```python\nfrom twisted.internet import reactor\nimport json\nfrom ctrader_fix import *\n\n# Callback for receiving all messages\ndef onMessageReceived(client, responseMessage):\n    print("Received: ", responseMessage.getMessage().replace("\x01", "|"))\n    messageType = responseMessage.getFieldValue(35)\n    if messageType == "A":\n        print("We are logged in")\n\n# Callback for client disconnection\ndef disconnected(client, reason): \n    print("Disconnected, reason: ", reason)\n\n# Callback for client connection\ndef connected(client):\n    print("Connected")\n    logonRequest = LogonRequest(config)\n    send(logonRequest)\n\n# you can use two separate config files for QUOTE and TRADE\nwith open("config-trade.json") as configFile:\n    config = json.load(configFile)\n\nclient = Client(config["Host"], config["Port"], ssl = config["SSL"])\n\n# Setting client callbacks\nclient.setConnectedCallback(connected)\nclient.setDisconnectedCallback(disconnected)\nclient.setMessageReceivedCallback(onMessageReceived)\n# Starting the client service\nclient.startService()\nreactor.run()\n```\n\nPlease check documentation or samples for a complete example.\n\n## Dependencies\n\n* <a href="https://pypi.org/project/twisted/">Twisted</a>\n',
    'author': 'Spotware',
    'author_email': 'connect@spotware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spotware/cTraderFixPy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
