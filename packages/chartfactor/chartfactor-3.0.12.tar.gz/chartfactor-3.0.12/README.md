# ChartFactor for Python

# How to install and test

After download the project go to the root directory

### Uninstall any previous installation

```commandline
python -m pip uninstall chartfactor --yes
```

### Build the chartfactor package like this

```commandline
python setup.py sdist
```
The previous command will create a `dist` folder with tha package in the `chartfactor-1.0.tar.gz` file.

### Install the package locally

```commandline
python -m pip install ./dist/chartfactor-1.0.tar.gz
```

# Usage

Go to the Jupyter Notebook and in a new python notebook do the following

#### Cell 1

```python
from chartfactor import cf
import pandas as pd
```

#### Cell 2

```python
ts = pd.read_csv('./csvs/ticket_sales.csv')
```

#### Cell 3

```python
jsonConfig = {
    "showRowNumber": False,
    "autoSizeColumns": False,
    "config": {
        "filters": [
            # {
            #     "path": "company",
            #     "operation": "TS",
            #     "value": [
            #         "pedia"
            #     ]
            # }
        ],
        "groups": [
            {
                "name": "catname",
                "label": "catname",
                "sort": {
                    "name": "commission",
                    "func": "sum",
                    "dir": "desc"
                },
                "limit": 10
            },
            {
                "name": "eventname",
                "label": "eventname",
                "sort": {
                    "name": "eventname",
                    "func": "unique",
                    "dir": "asc"
                },
                "limit": 5
            }
        ],
        "metrics": [
            {
                "name": "pricepaid",
                "func": "sum"
            }
        ],
        "fields": [

        ],
        "exclude": []
    },
    "rows": [],
    "limit": 8,
    "offset": 0,
    "visualization" : "Bars"
}
```

#### Cell 4

```python
prov = cf.provider(ts, jsonConfig)
# prov.get_config()
# prov.run_count_query()
# prov.run_raw_query()
prov.visualize()
```

# How to run test

Inside the `test` folder execute the following command: 

```commandline
python -m unittest
```

# Increase jupyter notebook data rate limit

This may only be required on Windows environments. Run the following command in a terminal to generate the `jupyter_notebook_config.py` file if not exists:

```commandline
jupyter notebook --generate-config
```

After that, locate the file in the `.jupyter` folder and add the following line at the end:

```python
c.NotebookApp.iopub_data_rate_limit = 1.0e10
```

# Configuring deployment credentials

Create and configure `~/.pypirc` which is the `pypi.org` configuration file, in order to set the user and the token to upload the package.
1) Create the file:
```commandline
touch ~/.pypirc
```

2) Assign permissions:
```commandline
chmod 600 ~/.pypirc
```

3) Open the file:
```commandline
open ~/.pypirc
```

4) Add this configuration:

```markdown
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
repository = https://upload.pypi.org/legacy/

[testpypi]
username = __token__
repository = https://test.pypi.org/legacy/
```

Notice that instead of using the `password` field, we are going to save the  API tokens and passwords securely using `keyring` (which is installed by Twine):

5) Configuring the test server:
```markdown
keyring set https://test.pypi.org/legacy/ __token__
```

6) Enter the generated token for the test environment:
```markdown
Password for '__token__' in 'https://test.pypi.org/legacy/': TOKEN
```

7) Configuring the production server:
```markdown
keyring set https://upload.pypi.org/legacy/ __token__
```

8) Enter the generated token for the production environment:
```markdown
Password for '__token__' in 'https://upload.pypi.org/legacy/': TOKEN
```
# Install Python Package Dependencies

## To build the project successfully
```
pip install -r requirements.txt
```

## To load packages for developers
```
pip install -r requirements-dev.txt
```

The execution of the command above will install if not exists the following packages:

* twine>=3.7.1
* build>=0.7.0
* wheel>=0.37.1

If is necessary to upgrade the packages to a newer version just run the following command:
```commandline
python3 -m pip install --upgrade {twine|build|wheel}
```

# Code Obfuscation

The code obfuscation allows to modify a program code so that it is no longer useful to a hacker but remains fully functional.

Two processes to achieve code obfuscation and its corresponding deployment are detailed below.

## Using `pyarmor` package to build a pyarmored wheel (Recommended)

### Installing Anaconda

In order to create easily the virtual environments with the different python versions, and also obfuscate the code 
and be able to run the chartfactor-py package in every python version, it's necessary to install the Anaconda software.

First download it from the [official website](https://docs.anaconda.com/anaconda/install/).

Next, open the software, go to the `Environments` tab, and create two virtual environment for python 3.6 and 3.7 with the following names:
* env3.6
* env3.7

### Executing the `build-pyarmored-wheel.sh` file

The `build-pyarmored-wheel.sh` file was created to automatically build, obfuscate and deploy the package to the `pypi.org` server. 
After installing `Anaconda` successfully and created the virtual environments, execute the following command inside the `chartfactor-py` folder: 

```shell
sh build-pyarmored-wheel.sh -v 1.x <-t|-p>
```

Flags:
* `-v` package version
* `-t` upload package to the test environment
* `-p` upload package to the production environment

## Using `pyc-wheel` package

This package allows you to compile all `py` files in a wheel to `pyc` files. For more information go to the [pyc-wheel page](https://pypi.org/project/pyc-wheel/)

In the chartfactor-py folder execute the following build command:

```commandline
python3 -m build
```

After execution, 2 files should have been generated in the dist folder:
* chartfactor-1.x.tar.gz
* chartfactor-1.x-py3-none-any.whl

Next, the following command must be executed to convert the `.py` files to `.pyc` (compiled and with the code obfuscated) inside the .whl file.

```commandline
python -m pyc_wheel dist/chartfactor-1.x-py3-none-any.whl
```

> You can add this option `--with_backup` to create a backup during the process.

Once the .whl file has been processed, it must be uploaded to the pypi.org or test.pypi.org repository, whichever the case may be.

To achieve that do the following:

#### Test server
```commandline
python3 -m twine upload --repository testpypi ./*
```

#### Production server
```commandline
python3 -m twine upload dist/*
```

For each case you must enter the user name `__token__` and the provided token after.

To install the package run the following command:

```commandline
pip uninstall chartfactor
```

# Installing the Chartfactor.py package as an end-user
## From test server

```commandline
pip install -i https://test.pypi.org/simple/ chartfactor==1.x
```

## From production server

```commandline
python3 -m pip install chartfactor
```

