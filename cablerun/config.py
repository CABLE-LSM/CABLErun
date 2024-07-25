# Author: Lachlan Whyborn
# Last Modified: Thu 25 Jul 2024 01:00:37 PM AEST

config_defaults = {
        "queue": "normal",
        "project": os.environ.get("PROJECT", None),
        "jobname": os.path.split(os.getcwd()),
        "ncpus": None,
        "mem": "192GB",
        "walltime": "10:00:00",
        "storage": [],
        "input": [],
        "exe": None
        }

def apply_defaults(config, user_config):
    """Read the user's config, compare against the defaults."""
    
    for key, value in config_defaults.items():
        config[key] = user_config.get(key, value)

def build_cable_stages(stage_config):
    """Build the queue of CABLE stages which form the configuration."""

    # Since Python3.7, dictionary order is guaranteed so we can read
    # the entries in order without needing to supply an index
    # We just want to populate cable_stages with the list of stages
    # to run
    cable_stages = []
    for stage_name, stage_opts in stage_config.items():
        # Check if stage is a multi-step or single step
        if stage_name.startswith("multistep"):
            # The multi-step stage can run each internal stage
            # a different number of times. For example, a two
            # step stage may ask for the first step (S1) 5 times,
            # but the second step (S2) only 3 times. The stage
            # looks like [S1, S2, S1, S2, S1, S2, S1, S1].
            # So what we need to do is first record the number
            # of times each step is run
            step_names = []; step_counts = []
            for step_name, step_opts in stage_opts.items():
                step_names.append(step_name)
                step_counts.append(step_opts["count"])

            # Now iterate to the maximum number of steps
            for step in range(max(step_counts)):
                for step_id in range(len(step_names)):
                    if step_counts[step_id] > step:
                        cable_stages.append(step_names[step_id])
        # Finish handling of multistep stage

        else:
            # A single step stage, in general we only want to run this
            # once, but check for the count anyway
            for stage_count in range(stage_opts["count"]):
                cable_stages.append(stage_name)

    return cable_stages
