from .BaseWorkflow import BaseWorkflow

class OnlyMSpathfinderWorkflow(BaseWorkflow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.input_files = args.get_ms_file_path()
        self.fasta_file = args.get_fasta_path()

    def prepare_workflow(self):
        self.commands = [
            self._mspathfinder_command()
        ]
    
    def _mspathfinder_command(self):
        mspathfinder_command = [self.args.tool_paths['mspathfinder']]
        
        # Required input file
        mspathfinder_command.append('-i')
        for file in self.input_files:
            mspathfinder_command.append(file)

        # Required database file
        mspathfinder_command.append('-d')
        mspathfinder_command.append(self.fasta_file)

        if self.args.get_output_dir():
            mspathfinder_command.append('-o')
            mspathfinder_command.append(self.args.get_output_dir())

        # Optional internal cleavage mode
        if self.args.get_mspathfinder_config_option('ic'):
            mspathfinder_command.append('-ic')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('ic')))

        # Optional tag search
        if self.args.get_mspathfinder_config_option('TagSearch') is not None:
            mspathfinder_command.append('-TagSearch')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('TagSearch')).lower())

        # Optional memory matches
        if self.args.get_mspathfinder_config_option('MemMatches'):
            mspathfinder_command.append('-MemMatches')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('MemMatches')))

        # Optional number of matches per spectrum
        if self.args.get_mspathfinder_config_option('NumMatchesPerSpec'):
            mspathfinder_command.append('-n')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('NumMatchesPerSpec')))

        # Optional include decoys
        if self.args.get_mspathfinder_config_option('IncludeDecoys'):
            mspathfinder_command.append('-IncludeDecoys')

        # Optional modification file
        if self.args.get_mspathfinder_config_option('ModificationFile'):
            mspathfinder_command.append('-mod')
            mspathfinder_command.append(self.args.get_mspathfinder_config_option('ModificationFile'))

        # Optional TDA mode
        if self.args.get_mspathfinder_config_option('tda') is not None:
            mspathfinder_command.append('-tda')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('tda')))

        # Optional overwrite
        if self.args.get_mspathfinder_config_option('overwrite'):
            mspathfinder_command.append('-overwrite')

        # Optional tolerances
        if self.args.get_mspathfinder_config_option('PMTolerance'):
            mspathfinder_command.append('-t')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('PMTolerance')))

        if self.args.get_mspathfinder_config_option('FragTolerance'):
            mspathfinder_command.append('-f')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('FragTolerance')))

        # Optional sequence length range
        if self.args.get_mspathfinder_config_option('MinLength'):
            mspathfinder_command.append('-MinLength')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('MinLength')))

        if self.args.get_mspathfinder_config_option('MaxLength'):
            mspathfinder_command.append('-MaxLength')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('MaxLength')))

        # Optional charge ranges
        if self.args.get_mspathfinder_config_option('MinCharge'):
            mspathfinder_command.append('-MinCharge')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('MinCharge')))

        if self.args.get_mspathfinder_config_option('MaxCharge'):
            mspathfinder_command.append('-MaxCharge')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('MaxCharge')))

        if self.args.get_mspathfinder_config_option('MinFragCharge'):
            mspathfinder_command.append('-MinFragCharge')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('MinFragCharge')))

        if self.args.get_mspathfinder_config_option('MaxFragCharge'):
            mspathfinder_command.append('-MaxFragCharge')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('MaxFragCharge')))

        # Optional mass range
        if self.args.get_mspathfinder_config_option('MinMass'):
            mspathfinder_command.append('-MinMass')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('MinMass')))

        if self.args.get_mspathfinder_config_option('MaxMass'):
            mspathfinder_command.append('-MaxMass')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('MaxMass')))

        # Optional feature file
        if self.args.get_mspathfinder_config_option('FeatureFile'):
            mspathfinder_command.append('-feature')
            mspathfinder_command.append(self.args.get_mspathfinder_config_option('FeatureFile'))

        # Optional thread count
        if self.args.get_mspathfinder_config_option('ThreadCount'):
            mspathfinder_command.append('-threads')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('ThreadCount')))

        # Optional activation method
        if self.args.get_mspathfinder_config_option('ActivationMethod'):
            mspathfinder_command.append('-act')
            mspathfinder_command.append(str(self.args.get_mspathfinder_config_option('ActivationMethod')))

        # Optional scans file
        if self.args.get_mspathfinder_config_option('ScansFile'):
            mspathfinder_command.append('-scansFile')
            mspathfinder_command.append(self.args.get_mspathfinder_config_option('ScansFile'))

        # Optional flip scoring
        if self.args.get_mspathfinder_config_option('UseFlipScoring'):
            mspathfinder_command.append('-flip')

        # Optional parameter file
        if self.args.get_mspathfinder_config_option('ParamFile'):
            mspathfinder_command.append('-ParamFile')
            mspathfinder_command.append(self.args.get_mspathfinder_config_option('ParamFile'))

        return mspathfinder_command

