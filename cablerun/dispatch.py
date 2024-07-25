# Author: Lachlan Whyborn
# Last Modified: Wed 24 Jul 2024 06:18:22 PM AEST

def dispatch():
    """Dispatch a CABLE stage."""

    with open("configuration_log.yaml", 'r') as conf_log_f:
        configuration_log = yaml.safe_load(conf_log_f)

    current_stage = configuration_log["queued_stages"].pop(0)
    configuration_log["current_stage"] = current_stage

    with open("configuration_log.yaml", 'w') as conf_log_f:
        yaml.dump(configuration_log, conf_log_f)

    # Prepare the inputs to the stage
    with open("config.yaml") as config_f:
        config = yaml.safe_load(config_f)

    # Add the restarts from the previous stage
    num_completed_stages = len(configuration_log["completed_stages"])
    for stage_count in reversed(range(num_completed_stages)):
        config["input"].append(f"stage{stage_count:03d}/restart/")
    
    symlink_inputs(config["input"], f"stage{num_completed_stages+1:03d}")

def symlink_inputs(inputs, targetdir):
    """Symlink inputs to the target directory."""

    for path in inputs:
        for file in os.listdir(path):
            os.symlink(os.path.abspath(file), os.path.join(targetdir, os.path.split(file)[1]))
