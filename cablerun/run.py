# Author: Lachlan Whyborn
# Last Modified: Thu 25 Jul 2024 14:48:13

import os
from .config import apply_defaults, build_cable_stages
import .templates as templates

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

        # Prepare the job dispatcher and use to dispatch each stage
        self.dispatcher = hpcpy.ClientFactory.get_client()
        self.submit_stages()

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

        # Write the configuration log to disk, to be read by the dispatch
        # for each stage
        with open("configuration_log.yaml", 'w') as conf_log_f:
            yaml.dump(configuration_log, conf_log_f)

    def _submit_stages():
        """Use the client to submit the set of jobs for the configuration."""

        # Write the basic script to file, for clarity
        with open("submission_template.sh", 'w') as script_f:
            script_f.write(templates.BASE_SCRIPT)

        # Build the set of directives not included as keywords
        directives = []
        directives.append(f"-l mem={config['mem']:s}")
        directives.append(f"-l ncpus={config['ncpus']:d}")

        # Initialise the previous job ID for job dependency
        prev_id = None
        for stage in self.configuration_log["queued_stages"]:
            prev_id = self.dispatcher.submit("submission_template.sh",
                    render = True,
                    depends_on = prev_id,
                    queue = config["queue"],
                    walltime = config["walltime"],
                    storage = config["storage"],
                    directives = directives)

