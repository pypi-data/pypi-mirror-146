# pytbx
> A collection of useful tools for my engineering projects


Docs: https://t11c.gitlab.io/pytbx

Made this with [nbdev](https://nbdev.fast.ai) from [fast.ai](https://www.fast.ai). As <code>nbdev</code> is designed for github, I used the template from [Thomas Capelle](https://gitlab.com/tcapelle/nbdev_template) to make it work on  gitlab.


## Install
Simply install it with pip:

`pip install pytbx`

## How to use
... muss noch

## Setup Dev environment

### Requirements
  * pipenv
  * jupyter lab installed
  * jekyll installed (to view the docs)


### set up

clone repo

    git clone https://gitlab.com/t11c/pytbx

install python environment with pipenv

    pipenv install --dev

register ipykernel

    pipenv run python -m ipykernel install --user --name=pytbx

install git-hooks

    pipenv run nbdev_install_git_hooks
