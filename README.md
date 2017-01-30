#SESaR
##Semantic-, Emotional-, Structure Processor & Response Generator
######A demo of a linguistic processor, built for the VPRO Robot project

## Table of Contents
- [Installation](#installation)
- [Running the script](#Running the script)

## Installation
After cloning the repository, you first need to initialize the submodules:
```
git submodule init
git submodule update
```

You may then setup a virtualenv to install the required packages in. This step is optional.
```
virtualenv .
source bin/activate
```

Finally, install the packages with:
```
pip install -r requirements.txt
```

## Running the script
You can run the server with `python start.py`. There's also an accompanying web client located in `/web_client`. Use `grunt serve` or `grunt build` to run the web client.

Alternatively, you may choose to run the `SESaR_03.ipynb` Jupyter Notebook.
