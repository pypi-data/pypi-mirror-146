# `fw2ai`

This is a tool for analysing binaries from extracted firmware images. It has the capabilities to convert relevant artefacts from binary files that can used with AI to simplify firmware analysis.

## Getting started

### Configuration

Configuration file defines following parameters that can be customized.

> default config file name (resides in current directory): `./config.ini`

| Section | Parameter     | Default        | Description                              |
| ------- | ------------- | -------------- | ---------------------------------------- |
| general | config_path   | `./config.ini` | Path to configuration file               |
| general | firmwares_dir | `./firmwares`  | Directory containing firmwares           |
| general | output_dir    | `./output`     | Directory where output will be generated |
| log     | log_path      | `./log.txt`    | Path to log file                         |
| log     | log_level     | `INFO`         | Log level                                |

### Default configuration

```ini
[general]
config_path=./config.ini
firmwares_dir=./firmwares
output_dir=./output

[log]
log_level=INFO
log_path=./log.txt
```

### Logging

Logging levels supported are:

1. CRITICAL
2. ERROR
3. WARNING
4. INFO
5. DEBUG

### Usage

```bash
fw2ai --help

fw2ai [-f | --fw-dir] /path/to/dir/with/all/firmware

fw2ai [-o | --output-dir ] /path/to/output/dir

fw2ai [-c | --config ] /path/to/config/file
```

## Developer Notes

### CLI architecture

There are three parameter types:

1. Arguments: Mandatory

   ```bash
    pip install requests
   ```

2. Options: Optional eg.

   ```bash
    pip install requests --proxy http://10.11.22.33
   ```

3. Flags: Optional (for enabling or disabling features)
   ```bash
   ls -al
   ls --help
   ```

### PyPi Lifecycle

#### Authenticaion

File name: `~/.pypirc`

```ini
[pypi]
  username = __token__
  password = <PUT THE TOKEN HERE>
```

#### Generate source and binary distribution

```bash
python setup.py sdist bdist_wheel
```

#### Test locally

Install locally

```bash
pip install -e .
```

#### Uploading to PyPi

Upload to PyPi:

```bash
python -m twine upload dist/* --verbose
```

### Git push

```bash
git push -u origin main
```

### Git Configuration

There are 3 levels of git config; project, global and system. [Ref](https://stackoverflow.com/questions/8801729/is-it-possible-to-have-different-git-configuration-for-different-projects)

1. project: Project configs are only available for the current project and stored in .git/config in the project's directory.
2. global: Global configs are available for all projects for the current user and stored in ~/.gitconfig.
3. system: System configs are available for all the users/projects and stored in /etc/gitconfig.
   Create a project specific config, you have to execute this under the project's directory:

```bash
$ git config user.name "Mahesh Patil"
$ git config user.email "cpuinfo10@gmail.com"
```

Create a global config:

```bash
$ git config --global user.name "Mahesh Patil"
$ git config --global user.email "cpuinfo10@gmail.com"
```

Create a system config:

```bash
$ git config --system user.name "Mahesh Patil"
$ git config --system user.email "cpuinfo10@gmail.com
```

### Design Notes

#### Handling CLI arguments, options and flags

Three popular options [Ref](https://github.com/atkinsonm/click-demo) for handling CLI arguments, options and flags are:

1. sys.argv
2. argparse
3. click

Check [Video](https://www.youtube.com/watch?v=uXS9hmp4lp4):
