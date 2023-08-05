# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['virustotal_python']

package_data = \
{'': ['*']}

install_requires = \
['requests[socks]>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'virustotal-python',
    'version': '1.0.0',
    'description': 'A Python library to interact with the public VirusTotal v3 and v2 APIs.',
    'long_description': '# virustotal-python 🐍\n![PyPI](https://img.shields.io/pypi/v/virustotal-python.svg?style=flat-square)\n[![CI](https://github.com/dbrennand/virustotal-python/actions/workflows/ci.yml/badge.svg)](https://github.com/dbrennand/virustotal-python/actions/workflows/ci.yml)\n[![Publish](https://github.com/dbrennand/virustotal-python/actions/workflows/publish.yml/badge.svg)](https://github.com/dbrennand/virustotal-python/actions/workflows/publish.yml)\n\nA Python library to interact with the public VirusTotal v3 and v2 APIs.\n\n> This library is intended to be used with the public VirusTotal APIs. However, it *could* be used to interact with premium API endpoints as well.\n>\n> It is highly recommended that you use the VirusTotal v3 API as it is the "default and encouraged way to programmatically interact with VirusTotal".\n\n## Installation 🛠\n\n```bash\n# PyPi\npip install virustotal-python\n# Manually\npip install .\n# Poetry\npoetry install --no-dev\n```\n\n## Get a VirusTotal API Key 🔑\n\n[Sign up](https://www.virustotal.com/gui/join-us) for a VirusTotal account. Then, view your VirusTotal API key.\n\n![VirusTotal view API key](images/APIKey.png)\n\n## Getting Started\n\n```python\nimport virustotal_python\n\nwith virustotal_python.Virustotal("<VirusTotal API Key>") as vtotal:\n    # Your code here...\n\n# Use the (old) VirusTotal version 2 API\nwith virustotal_python.Virustotal(\n    API_KEY="<VirusTotal API Key>", API_VERSION=2\n) as vtotal:\n    # Your code here...\n\n# You can also set proxies and timeouts for requests made by the library\n# NOTE: To use proxies, you must have the PySocks extra installed\nwith virustotal_python.Virustotal(\n    API_KEY="<VirusTotal API Key>",\n    PROXIES={"http": "http://10.10.1.10:3128", "https": "https://10.10.1.10:1080"},\n    TIMEOUT=5.0,\n) as vtotal:\n    # Your code here...\n\n# You can also omit the API_KEY parameter and provide your\n# API key via the environment variable VIRUSTOTAL_API_KEY\n# Bash: export VIRUSTOTAL_API_KEY="<VirusTotal API Key>"\n# PowerShell: $Env:VIRUSTOTAL_API_KEY = "<VirusTotal API Key>"\n# Then...\nwith virustotal_python.Virustotal() as vtotal:\n    # Your code here...\n```\n\n## Code Snippets\n\n> Further usage examples can be found in [examples](examples).\n\n### Send a file for analysis 🔎\n\n```python\nimport virustotal_python\nimport os.path\nfrom pprint import pprint\n\nFILE_PATH = "/path/to/file/to/scan.txt"\n\n# Create dictionary containing the file to send for multipart encoding upload\nfiles = {"file": (os.path.basename(FILE_PATH), open(os.path.abspath(FILE_PATH), "rb"))}\n\nwith virustotal_python.Virustotal("<VirusTotal API Key>") as vtotal:\n    resp = vtotal.request("files", files=files, method="POST")\n    pprint(resp.json())\n```\n\n### Get information about a file 📁\n\n```python\nimport virustotal_python\nfrom pprint import pprint\n\n# The ID (either SHA-256, SHA-1 or MD5 hash) identifying the file\nFILE_ID = "9f101483662fc071b7c10f81c64bb34491ca4a877191d464ff46fd94c7247115"\n\nwith virustotal_python.Virustotal("<VirusTotal API Key>") as vtotal:\n    resp = vtotal.request(f"files/{FILE_ID}")\n    pprint(resp.data)\n```\n\n### Send a URL 🔗 for analysis and get the report 📄\n\n```python\nimport virustotal_python\nfrom pprint import pprint\nfrom base64 import urlsafe_b64encode\n\nurl = "ihaveaproblem.info"\n\nwith virustotal_python.Virustotal("<VirusTotal API Key>") as vtotal:\n    try:\n        resp = vtotal.request("urls", data={"url": url}, method="POST")\n        # Safe encode URL in base64 format\n        # https://developers.virustotal.com/reference/url\n        url_id = urlsafe_b64encode(url.encode()).decode().strip("=")\n        report = vtotal.request(f"urls/{url_id}")\n        pprint(report.object_type)\n        pprint(report.data)\n    except virustotal_python.VirustotalError as err:\n        print(f"Failed to send URL: {url} for analysis and get the report: {err}")\n```\n\n### Get information about a domain:\n\n```python\nimport virustotal_python\nfrom pprint import pprint\n\ndomain = "virustotal.com"\n\nwith virustotal_python.Virustotal("<VirusTotal API Key>") as vtotal:\n    resp = vtotal.request(f"domains/{domain}")\n    pprint(resp.data)\n```\n\n## Development\n\n[Black](https://github.com/psf/black) is used for code formatting.\n\n### Unit Tests\n\nInstall the development dependencies using Poetry:\n\n```bash\npoetry install && poetry shell\n```\n\nTo run the unit tests, run `pytest` from the root of the project:\n\n```bash\npytest --cov=virustotal_python\n```\n\n### Publishing a new release\n\n```bash\n# Run from the master branch\nexport VERSION=x.x.x\ngit commit --allow-empty -m "Publish $VERSION"\ngit tag -a $VERSION -m "Version $VERSION"\ngit push --tags\n```\n\n## Authors & Contributors\n\n* [**dbrennand**](https://github.com/dbrennand) - *Author*\n\n* [**smk762**](https://github.com/smk762) - *Contributor*\n\n## Changelog\n\nSee the [CHANGELOG](CHANGELOG.md) for details.\n\n## License\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) for details.\n',
    'author': 'dbrennand',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbrennand/virustotal-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
