

class ConfigFileValidationFailed(Exception):
    def __init__(self, configfile: str, msg: str) -> None:
        super().__init__(
            f"The configuration file {configfile} doesn't conform to the acceptable specified format.",
            msg
        )

class FeatureSelectorModeUnaccetableException(Exception):
    def __init__(self, mode: str) -> None:
        super().__init__(
            f"the specified feature selector mode {mode} does not exist, please choose one of these ('lsf', 'rsf', 'igf')."
        )
