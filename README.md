# gerrit-check-mocks Fetch Endpoint

A fetch endpoint to be integrated with [gerrit-checks-mock](https://github.com/alonbl/gerrit-checks-mock) plugin.
The endpoint supports sandbox for testing and GitHub workflow status.

## Usage

```
usage: gerrit-checks-mock-fetch-endpoint [-h] [--version] [--log-level LEVEL] [--log-file FILE] [--bind-address ADDR] [--bind-port PORT] --config FILE

Gerrit checks-mock plugin fetch endpoint

options:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  --log-level LEVEL    Log level CRITICAL, ERROR, WARNING, INFO, DEBUG
  --log-file FILE      Log file to use, default is stdout
  --bind-address ADDR  Bind address
  --bind-port PORT     Bind port
  --config FILE        Configuration file, may be specified multiple times
```

## Gerrit Hooks

### Credentials

#### ~/.gitconfig

```ini
[credential "@GIT_URL@"]
    helper = "!f() { test \"$1\" = get && cat @PATH@/secret; }; f"
```

#### @PATH@/secret

GitHub fine grained with:

* Contents: Read and Write
* Workflows: Read and Write

Format:

```ini
username=@USER@
password=@PASSWORD@
```

### `etc/checks-mock.conf`

```ini
GERRIT_CHECKS_MOCK_URL_PREFIX=@GIT_URL@
GERRIT_CHECKS_REF_PREFIX=gerrit

project_transform() {
    local project="$1"
    echo "{project}-ci"
}
```

### Hook

```sh
ln -s \
    /usr/libexec/gerrit-checks-mock-fetch-endpoint/fetch-mock-hook \
    @GERRIT_SITE@/hooks/patchset-created
ln -s \
    /usr/libexec/gerrit-checks-mock-fetch-endpoint/fetch-mock-hook \
    @GERRIT_SITE@/hooks/comment-added
```

## Configuration File

```ini
[main]
drivers = sandbox, github, bitbucket
log_file =
log_level = INFO
bind_address =
bind_port = 8080
```

### Sandbox Driver

A sandbox is a standalone demo which can be used for debug. No additional
configuration is required.

#### Fetch Endpoint Configuration

```ini
[sandbox]
```

### GitHub Driver


#### Fetch Endpoint Configuration

```ini
[github]
base_url = https://api.github.com/repos/@SPACE@
branch_prefix = @GERRIT_ID@
repo_pattern = ^(?P<repo>.*)$
repo_replacement = \g<repo>-ci
remote_name_style = asis|underscore
timeout = 2
token = @APP_TOKEN@
```

Do not use anonymous access, GitHub blocks requests after a threshold.

GitHub token is fine grained token:
* Actions: Read

### BitBucket Driver

#### Fetch Endpoint Configuration

```ini
[bitbucket]
base_url = https://api.bitbucket.org/2.0/repositories/@WORKSPACE@
branch_prefix = @GERRIT_ID@/changes/
repo_pattern = ^(?P<repo>.*)$
repo_replacement = \g<repo>-ci
remote_name_style = asis|underscore
timeout = 2
user = @USER@
password = @APP PASSWORD@
```

The BitBucket password must be app password.
* Select your user.
* Select personal settings.
* Select app passwords.
  * Select create app password
  * For replication select repository write
  * For query select pipelines read

## Systemd Configuration

### /etc/default/gerrit-checks-mock-fetch-endpoint

```sh
ARGS=--config=/etc/gerrit-checks-mock-fetch-endpoint/main.conf --config=/etc/gerrit-checks-mock-fetch-endpoint/secrets.conf
```

```sh
# systemctl enable gerrit-checks-mock-fetch-endpoint
# systemctl start gerrit-checks-mock-fetch-endpoint
```

## Development

### Build

```sh
$ tox
```

### Generate checks.py

The `checks.py` is generated out of `./polygerrit-ui/app/api/checks.ts` in
Gerrit tree.

The generation is done using `ts2python` but it requires some manual changes.

* Generate the file using:

```sh
sed -e 's/declare //' -e '/^import/d' ../checks.ts > checks-in.ts
./ts2pythonParser.py checks-in.ts
sed -e 's/(Enum)/(str, Enum)/' checks-in.py > checks.py
```

* Add the following the header:

```
# flake8: noqa
# mypy: ignore-errors
# pylint: disable=unused-import, invalid-name, unused-argument, too-few-public-methods
```

* Rework the imports to make it sane, remove requirements of external
  dependencies and duplication due to older python versions.
* Remove unneeded code.
* Replace NotRequired with Optional until python-3.11.

### Debug

```
$ curl -X POST -H "Accept: application/json" -H "Content-Type: application/json" http://localhost:8080/fetch -d '{"project": "test1", "changeId": "test1~master~I324324324", "revision": 9}'
```
