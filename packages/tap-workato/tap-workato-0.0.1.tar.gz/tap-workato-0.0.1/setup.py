# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_workato', 'tap_workato.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.4.5,<0.5.0']

entry_points = \
{'console_scripts': ['tap-workato = tap_workato.tap:TapWorkato.cli']}

setup_kwargs = {
    'name': 'tap-workato',
    'version': '0.0.1',
    'description': '`tap-workato` is a Singer tap for Workato, built with the Meltano SDK for Singer Taps.',
    'long_description': '# tap-workato\n\n`tap-workato` is a Singer tap for Workato.\n\nBuilt with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.\n\n## Installation\nThis tap is installable via pypi\n\n```bash\npipx install tap-workato\n```\n\nOr, if using via Meltano you can add configuration like so in the `meltano.yml` file:\n\n```yaml\nplugins:\n  extractors:\n  - name: tap-workato\n    namespace: tap_workato\n    pip_url: -e .\n    capabilities:\n    - state\n    - catalog\n    - discover\n    settings:\n    - name: user_token\n      kind: password\n    - name: user_email\n      kind: password\n```\n\nand then run the following from the CLI:\n\n```shell\nmeltano install extractor tap-workato\n```\n\n## Configuration\n\n### Accepted Config Options\n\nA full list of supported settings and capabilities for this\ntap is available by running:\n\n```bash\ntap-workato --about\n```\n\nAvailable streams include:\n-  `api_clients`\n-  `api_collection`\n-  `connections`\n-  `customer_accounts` *\n-  `customer_api_access_profiles` *\n-  `customer_api_clients` *\n-  `customer_api_collections` *\n-  `customer_api_endpoints` *\n-  `customer_connections` *\n-  `customer_connections` *\n-  `customer_members` *\n-  `customer_recipes` *\n-  `customer_roles` *\n-  `folders`\n-  `jobs`\n-  `on_prem_agents`\n-  `on_prem_groups`\n-  `recipes`\n-  `roles`\n\nNotes:\n- _* The endpoints utilized by these streams are \n  Embedded Vendor APIs and require the `oem_vendor` privilege in Workato._\n- The workato Embedded API does not allow for extracting customer jobs \n  data at this time.\n\n### Source Authentication and Authorization\n\nYou will need authentication tokens set up in your Workato account. Namely a user \nemail and a user token. See the \ninstructions [here](https://docs.workato.com/oem/oem-api.html#authentication).\n\n## Usage\n\nYou can easily run `tap-workato` by itself or in a pipeline using [Meltano](https://meltano.com/).\n\n### Executing the Tap Directly\n\n```bash\ntap-workato --version\ntap-workato --help\ntap-workato --config CONFIG --discover > ./catalog.json\n```\n\n## Developer Resources\n\n### Initialize your Development Environment\n\n```bash\npipx install poetry\npoetry install\n```\n\n### Create and Run Tests\n\nCreate tests within the `tap_workato/tests` subfolder and\n  then run:\n\n```bash\npoetry run pytest\n```\n\nYou can also test the `tap-workato` CLI interface directly using `poetry run`:\n\n```bash\npoetry run tap-workato --help\n```\n\nOther useful workflows are included in the `tox.ini`:\n\n```bash\npoetry run tox -e format\npoetry run tox -e lint\npoetry run tox -e pytest\n```\n\n### Testing with [Meltano](https://www.meltano.com)\n\n_**Note:** This tap will work in any Singer environment and does not require Meltano.\nExamples here are for convenience and to streamline end-to-end orchestration scenarios._\n\nYour project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in\nthe file.\n\nNext, install Meltano (if you haven\'t already) and any needed plugins:\n\n```bash\n# Install meltano\npipx install meltano\n# Initialize meltano within this directory\ncd tap-workato\nmeltano install\n```\n\nNow you can test and orchestrate using Meltano:\n\n```bash\n# Test invocation:\nmeltano invoke tap-workato --version\n# OR run a test `elt` pipeline:\nmeltano elt tap-workato target-jsonl\n```\n\n### SDK Dev Guide\n\nSee the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to \ndevelop your own taps and targets.\n',
    'author': 'Josh Lloyd',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Widen/tap-workato',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
