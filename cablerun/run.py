# Author: Lachlan Whyborn
# Last Modified: Thu 25 Jul 2024 01:00:37 PM AEST

import os
from config import apply_defaults

class Runner(object):

    def __init__(self):
        """Initialise a new runner of CABLE configurations."""

        # Start by reading in the main config file, which is the same as
        # a payu config file
        self.config = {}
        self._prepare_config()

        # Now prepare the stages of the spin-up
        self.configuration_log = {}
        self._prepare_stages()

    def _prepare_config(self):
        """Prepare the configuration of the runner. This follows
        the form of Payu configuration, for the relevant options."""

        # Start by addressing the config options
        with open("config.yaml", 'r') as config_f:
            user_config = yaml.safe_load(config_f)

        apply_defaults(self.config, user_config)

    def _prepare_stages():
        """Prepare the stages in the CABLE configuration."""

        # And add the stage config file, which we use for configuring CABLE
        # runs
        with open("stage_config.yaml", 'r') as stage_config_f:
            stage_config = yaml.safe_load(stage_config_f)

        # Build the configuration log, which we use to track the status of
        # the configuration
        self.configuration_log = {
                "queued_stages" = [],
                "current_stage" = "",
                "completed_stages" = []
                }

        self.configuration_log["queued_stages"] = build_cable_stages(stage_config)

def build_client(config):
    """Build the client."""

    # We hook into hpcpy to assist in building the submitter
    client = hpcpy.ClientFactory.get_client()


def build_new_configuration_log(stage_config):
    """Build a new configuration log."""

    cable_stages = prepare_configuration(stage_config)

    configuration_log["queued_stages"] = cable_stages
    configuration_log["current_stage"] = ""
    configuration_log["completed_stages"] = []

    return configuration_log

def prepare_configuration(stage_config):
    """Read the stage config to prepare the configuration."""


    # Finish handling of single step stage
    return cable_stages
