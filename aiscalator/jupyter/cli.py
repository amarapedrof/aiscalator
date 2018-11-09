# -*- coding: utf-8 -*-
# Apache Software License 2.0
#
# Copyright (c) 2018, Christophe Duong
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
CLI module for Jupyter related commands.
"""
import logging
import os
import sys

import click

from aiscalator import __version__
from aiscalator.core.config import AiscalatorConfig
from aiscalator.jupyter import command


@click.group()
@click.version_option(version=__version__)
def jupyter():
    """Notebook environment to explore and handle data."""
    pass


@jupyter.command()
def setup():
    """Setup the docker image to run notebooks."""
    # TODO to implement
    logging.error("Not implemented yet")


@jupyter.command()
@click.option('--name', prompt='What is the name of your step?',
              help="Name of the new step to create",
              metavar='<STEP>')
# TODO: import an existing notebook and create a new aiscalate step from it
@click.argument('path', type=click.Path())
def new(name, path):
    """Create a new notebook associated with a new aiscalate step config."""
    file_conf = os.path.join(path, name, name) + '.conf'
    file_json = os.path.join(path, name, name) + '.json'
    if os.path.exists(file_conf):
        prompt_edit(file_conf)
    elif os.path.exists(file_json):
        prompt_edit(file_json)
    else:
        click.echo(command.jupyter_new(name, path))


def prompt_edit(file):
    """
    When creating a new step, if it is already defined,
    ask to edit instead

    Parameters
    ----------
    file : str
        existing configuration file

    """
    msg = file + ' already exists. Did you mean to run:\n'
    for i in sys.argv:
        if i != "new":
            msg += i + ' '
        else:
            break
    msg += "edit " + file + " instead?"
    if click.confirm(msg, abort=True):
        conf = AiscalatorConfig(step_config=file,
                                steps_selection=[])
        click.echo(command.jupyter_edit(conf))


@jupyter.command()
@click.argument('conf', type=click.Path(exists=True))
@click.argument('notebook', nargs=-1)
# TODO add parameters override from CLI
def edit(conf, notebook):
    """Edit the notebook from an aiscalate config with JupyterLab."""
    app_config = AiscalatorConfig(step_config=conf,
                                  steps_selection=notebook)
    click.echo(command.jupyter_edit(app_config))


@jupyter.command()
@click.argument('conf', type=click.Path(exists=True))
@click.argument('notebook', nargs=-1)
# TODO add parameters override from CLI
def run(conf, notebook):
    """Run the notebook from an aiscalate config without GUI."""
    # TODO run multiple notebooks
    # we have to stage notebooks with same dockerfile together,
    # merge their requirements so that groups of notebooks can be
    # run together in the same container sequentially
    app_config = AiscalatorConfig(step_config=conf,
                                  steps_selection=notebook)
    click.echo(command.jupyter_run(app_config))


# TODO check a step configuration file (validate against template step.conf)
