# tap-workato

`tap-workato` is a Singer tap for Workato.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation
This tap is installable via pypi

```bash
pipx install tap-workato
```

Or, if using via Meltano you can add configuration like so in the `meltano.yml` file:

```yaml
plugins:
  extractors:
  - name: tap-workato
    namespace: tap_workato
    pip_url: -e .
    capabilities:
    - state
    - catalog
    - discover
    settings:
    - name: user_token
      kind: password
    - name: user_email
      kind: password
```

and then run the following from the CLI:

```shell
meltano install extractor tap-workato
```

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-workato --about
```

Available streams include:
-  `api_clients`
-  `api_collection`
-  `connections`
-  `customer_accounts` *
-  `customer_api_access_profiles` *
-  `customer_api_clients` *
-  `customer_api_collections` *
-  `customer_api_endpoints` *
-  `customer_connections` *
-  `customer_connections` *
-  `customer_members` *
-  `customer_recipes` *
-  `customer_roles` *
-  `folders`
-  `jobs`
-  `on_prem_agents`
-  `on_prem_groups`
-  `recipes`
-  `roles`

Notes:
- _* The endpoints utilized by these streams are 
  Embedded Vendor APIs and require the `oem_vendor` privilege in Workato._
- The workato Embedded API does not allow for extracting customer jobs 
  data at this time.

### Source Authentication and Authorization

You will need authentication tokens set up in your Workato account. Namely a user 
email and a user token. See the 
instructions [here](https://docs.workato.com/oem/oem-api.html#authentication).

## Usage

You can easily run `tap-workato` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-workato --version
tap-workato --help
tap-workato --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_workato/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-workato` CLI interface directly using `poetry run`:

```bash
poetry run tap-workato --help
```

Other useful workflows are included in the `tox.ini`:

```bash
poetry run tox -e format
poetry run tox -e lint
poetry run tox -e pytest
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-workato
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-workato --version
# OR run a test `elt` pipeline:
meltano elt tap-workato target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.
