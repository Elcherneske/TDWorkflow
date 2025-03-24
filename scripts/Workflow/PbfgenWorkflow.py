from .BaseWorkflow import BaseWorkflow

class PbfgenWorkflow(BaseWorkflow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.input_files = args.get_ms_file_path()

    def prepare_workflow(self):
        self.commands = []
        for input_file in self.input_files:
            self.commands.append(self._pbfgen_command(input_file))

    
    def _pbfgen_command(self, input_file):
        pbfgen_command = [self.args.tool_paths['pbfgen']]
        
        # Required input file
        pbfgen_command.append('-i')
        pbfgen_command.append(input_file)
        
        if self.args.get_output_dir():
            pbfgen_command.append('-o')
            pbfgen_command.append(self.args.get_output_dir()) 

        # Optional start scan
        if self.args.get_pbfgen_config_option('start'):
            pbfgen_command.append('-start')
            pbfgen_command.append(str(self.args.get_pbfgen_config_option('start')))

        # Optional end scan
        if self.args.get_pbfgen_config_option('end'):
            pbfgen_command.append('-end')
            pbfgen_command.append(str(self.args.get_pbfgen_config_option('end')))

        # Optional parameter file
        if self.args.get_pbfgen_config_option('ParamFile'):
            pbfgen_command.append('-ParamFile')
            pbfgen_command.append(self.args.get_pbfgen_config_option('ParamFile'))

        return pbfgen_command
