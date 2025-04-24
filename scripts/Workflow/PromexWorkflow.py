from .BaseWorkflow import BaseWorkflow

class PromexWorkflow(BaseWorkflow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.input_files = args.get_ms_file_path()

    def prepare_workflow(self):
        self.commands = []
        for input_file in self.input_files:
            command = self._promex_command(input_file)
            if command:
                self.commands.append(command)
    
    def _promex_command(self, input_file):
        if not self.args.tool_paths['promex']:
            self.log("Promex路径为空，请检查配置。")
            return None
        
        promex_command = [self.args.tool_paths['promex']]
        
        # Required input file
        promex_command.append('-i')
        promex_command.append(input_file)
        
        if self.args.get_output_dir():
            promex_command.append('-o')
            promex_command.append(self.args.get_output_dir())

        # Optional charge range
        if self.args.get_promex_config_option('MinCharge'):
            promex_command.append('-MinCharge')
            promex_command.append(str(self.args.get_promex_config_option('MinCharge')))
        
        if self.args.get_promex_config_option('MaxCharge'):
            promex_command.append('-MaxCharge')
            promex_command.append(str(self.args.get_promex_config_option('MaxCharge')))

        # Optional mass range
        if self.args.get_promex_config_option('MinMass'):
            promex_command.append('-MinMass')
            promex_command.append(str(self.args.get_promex_config_option('MinMass')))
        
        if self.args.get_promex_config_option('MaxMass'):
            promex_command.append('-MaxMass')
            promex_command.append(str(self.args.get_promex_config_option('MaxMass')))

        # Optional feature map
        if self.args.get_promex_config_option('FeatureMap') is not None:
            promex_command.append('-FeatureMap')
            if not self.args.get_promex_config_option('FeatureMap'):
                promex_command.append('false')

        # Optional score output
        if self.args.get_promex_config_option('Score'):
            promex_command.append('-Score')

        # Optional thread count
        if self.args.get_promex_config_option('MaxThreads'):
            promex_command.append('-MaxThreads')
            promex_command.append(str(self.args.get_promex_config_option('MaxThreads')))

        # Optional CSV output
        if self.args.get_promex_config_option('Csv'):
            promex_command.append('-Csv')

        # Optional bin resolution
        if self.args.get_promex_config_option('BinResPPM'):
            promex_command.append('-BinResPPM')
            promex_command.append(str(self.args.get_promex_config_option('BinResPPM')))

        # Optional score threshold
        if self.args.get_promex_config_option('ScoreThreshold'):
            promex_command.append('-ScoreThreshold')
            promex_command.append(str(self.args.get_promex_config_option('ScoreThreshold')))

        # Optional ms1ft file
        if self.args.get_promex_config_option('ms1ft'):
            promex_command.append('-ms1ft')
            promex_command.append(self.args.get_promex_config_option('ms1ft'))

        # Optional parameter file
        if self.args.get_promex_config_option('ParamFile'):
            promex_command.append('-ParamFile')
            promex_command.append(self.args.get_promex_config_option('ParamFile'))

        return promex_command
