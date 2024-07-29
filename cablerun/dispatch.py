# Author: Lachlan Whyborn
# Last Modified: Wed 24 Jul 2024 06:18:22 PM AEST

def prep_stage():
    preprocessor = Preprocessor()
    preprocessor.prepare_stage()

class Preprocessor(object):
    
    def __init__(self):
        """Initialise the stage dispatcher."""

        # The only things the runner needs to know from the config
        # are the location of the executable and the input directories
        self.config = {}
        self._prepare_config()
        
        # Read the configuration log
        with open("configuration_log.yaml", 'r') as conf_log_f:
            self.configuration_log = yaml.safe_load(conf_log_f)

    def _prepare_config(self):
        """Read the config and ensure the inputs and executable are specified."""
        
        # Start by addressing the config options
        with open("config.yaml", 'r') as config_f:
            user_config = yaml.safe_load(config_f)

        config["exe"] = user_config.get("exe", None)
        config["input"] = user_config.get("input", None)

        # Check that all entries in config are not None
        for key in config.keys():
            if key is None:
                raise ValueError(f"Need to provide a value for {key} in config.yaml.")

    def prepare_stage(self):
        """Prepare a new cable stage."""

        # Use the stage_id to build the working directory and inform restart symlinks
        stage_id = len(self.configuration_log["completed_stages"])
        stage_dir = f"stage{stage_id:03d}"

        # Where the stage will run
        os.makedirs(f"stage{stage_id:03d}", exist_ok = True)

        # Add prior restarts to the inputs, with most recent first
        for prev_id in reversed(range(stage_id)):
            config["input"].append(f"stage{prev_id:03d}/restart")

        # Now symlink the inputs
        for input_dir in config["inputs"]:
            utils.symlink_directory(input_dir, stage_dir)

        # Determine the name of the stage, and use it to apply namelists
        current_stage = self.configuration_log["queued_stages"].pop(0)
        self.configuration_log["current_stage"] = current_stage
        
        # Capture all the namelists in the directory
        for nml in glob.glob("*.nml"):
            # Check if there's an equivalent namelist to patch for the stage
            if os.path.isfile(os.path.join(current_stage, nml)):
                new_nml = utils.apply_namelist(nml, os.path.join(current_stage, nml))
                new_nml.write(os.path.join(stage_dir, nml))
            else:
                shutil.copy(nml, os.path.join(stage_dir, nml))

        # Copy the executable to the stage directory
        shutil.copy(config["exe"], os.path.join(stage_dir), os.path.basename(config["exe"))

        # Write the configuration log to disk, and send a copy to the working dir
        with open("configuration_log.yaml", 'w') as conf_log_f:
            yaml.dump(self.configuration_log, conf_log_f)

        shutil.copy("configuration_log.yaml", os.path.join(stage_dir, "configuration_log.yaml"))
