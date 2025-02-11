from .BaseWorkflow import BaseWorkflow

class OnlyTopmgWorkflow(BaseWorkflow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.input_files = args.get_ms_file_path()
        self.fasta_file = args.get_fasta_path()

    def prepare_workflow(self):
        self.commands = [
            self._topmg_command()
        ]
    
    def _topmg_command(self):
        topmg_command = [self.args.tool_paths['topmg']]
        
        if self.args.get_topmg_config_option('activation'):
            topmg_command.append('--activation')
            topmg_command.append(self.args.get_topmg_config_option('activation'))
        
        if self.args.get_topmg_config_option('fixed-mod'):
            topmg_command.append('--fixed-mod')
            topmg_command.append(self.args.get_topmg_config_option('fixed-mod'))

        if self.args.get_topmg_config_option('n-terminal-form'):
            topmg_command.append('--n-terminal-form')
            topmg_command.append(self.args.get_topmg_config_option('n-terminal-form'))

        if self.args.get_topmg_config_option('decoy'):
            topmg_command.append('--decoy')

        if self.args.get_topmg_config_option('mass-error-tolerance'):
            topmg_command.append('--mass-error-tolerance')
            topmg_command.append(str(self.args.get_topmg_config_option('mass-error-tolerance')))

        if self.args.get_topmg_config_option('proteoform-error-tolerance'):
            topmg_command.append('--proteoform-error-tolerance')
            topmg_command.append(str(self.args.get_topmg_config_option('proteoform-error-tolerance')))

        if self.args.get_topmg_config_option('max-shift'):
            topmg_command.append('--max-shift')
            topmg_command.append(str(self.args.get_topmg_config_option('max-shift')))

        if self.args.get_topmg_config_option('spectrum-cutoff-type'):
            topmg_command.append('--spectrum-cutoff-type')
            topmg_command.append(self.args.get_topmg_config_option('spectrum-cutoff-type'))
        
        if self.args.get_topmg_config_option('spectrum-cutoff-value'):
            topmg_command.append('--spectrum-cutoff-value')
            topmg_command.append(str(self.args.get_topmg_config_option('spectrum-cutoff-value')))

        if self.args.get_topmg_config_option('proteoform-cutoff-type'):
            topmg_command.append('--proteoform-cutoff-type')
            topmg_command.append(self.args.get_topmg_config_option('proteoform-cutoff-type'))

        if self.args.get_topmg_config_option('proteoform-cutoff-value'):
            topmg_command.append('--proteoform-cutoff-value')
            topmg_command.append(str(self.args.get_topmg_config_option('proteoform-cutoff-value')))

        if self.args.get_topmg_config_option('mod-file-name'):
            topmg_command.append('--mod-file-name')
            topmg_command.append(self.args.get_topmg_config_option('mod-file-name'))

        if self.args.get_topmg_config_option('thread-number'):
            topmg_command.append('--thread-number')
            topmg_command.append(str(self.args.get_topmg_config_option('thread-number')))

        if self.args.get_topmg_config_option('no-topfd-feature'):
            topmg_command.append('--no-topfd-feature')

        if self.args.get_topmg_config_option('proteo-graph-gap'):
            topmg_command.append('--proteo-graph-gap')
            topmg_command.append(str(self.args.get_topmg_config_option('proteo-graph-gap')))

        if self.args.get_topmg_config_option('var-ptm-in-gap'):
            topmg_command.append('--var-ptm-in-gap')
            topmg_command.append(str(self.args.get_topmg_config_option('var-ptm-in-gap')))

        if self.args.get_topmg_config_option('use-asf-diagonal'):
            topmg_command.append('--use-asf-diagonal')

        if self.args.get_topmg_config_option('var-ptm'):
            topmg_command.append('--var-ptm')
            topmg_command.append(str(self.args.get_topmg_config_option('var-ptm')))

        if self.args.get_topmg_config_option('num-shift'):
            topmg_command.append('--num-shift')
            topmg_command.append(str(self.args.get_topmg_config_option('num-shift')))

        if self.args.get_topmg_config_option('whole-protein-only'):
            topmg_command.append('--whole-protein-only')

        if self.args.get_topmg_config_option('combined-file-name'):
            topmg_command.append('--combined-file-name')
            topmg_command.append(self.args.get_topmg_config_option('combined-file-name'))

        if self.args.get_topmg_config_option('keep-temp-files'):
            topmg_command.append('--keep-temp-files')

        if self.args.get_topmg_config_option('keep-decoy-ids'):
            topmg_command.append('--keep-decoy-ids')

        if self.args.get_topmg_config_option('skip-html-folder'):
            topmg_command.append('--skip-html-folder')

        topmg_command.append(self.fasta_file)

        for file in self.input_files:
            topmg_command.append(file)

        return topmg_command
