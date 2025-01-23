from .BaseWorkflow import BaseWorkflow

class OnlyToppicWorkflow(BaseWorkflow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.input_files = args.get_ms_file_path()
        self.fasta_file = args.get_fasta_path()

    def prepare_workflow(self):
        self.commands = [
            self._toppic_command()
        ]
    
    def _toppic_command(self):
        toppic_command = [self.args.tool_paths['toppic']]
        
        if self.args.get_toppic_config_option('activation'):
            toppic_command.append('--activation')
            toppic_command.append(self.args.get_toppic_config_option('activation'))
        
        if self.args.get_toppic_config_option('fixed_mod'):
            toppic_command.append('--fixed-mod')
            toppic_command.append(self.args.get_toppic_config_option('fixed_mod'))

        if self.args.get_toppic_config_option('n_terminal_form'):
            toppic_command.append('--n-terminal-form')
            toppic_command.append(self.args.get_toppic_config_option('n_terminal_form'))

        if self.args.get_toppic_config_option('num_shift'):
            toppic_command.append('--num-shift')
            toppic_command.append(str(self.args.get_toppic_config_option('num_shift')))

        if self.args.get_toppic_config_option('min_shift'):
            toppic_command.append('--min-shift')
            toppic_command.append(str(self.args.get_toppic_config_option('min_shift')))

        if self.args.get_toppic_config_option('max_shift'):
            toppic_command.append('--max-shift')
            toppic_command.append(str(self.args.get_toppic_config_option('max_shift')))

        if self.args.get_toppic_config_option('variable_ptm_num'):
            toppic_command.append('--variable-ptm-num')
            toppic_command.append(str(self.args.get_toppic_config_option('variable_ptm_num')))

        if self.args.get_toppic_config_option('variable_ptm_file_name'):
            toppic_command.append('--variable-ptm-file-name')
            toppic_command.append(self.args.get_toppic_config_option('variable_ptm_file_name'))

        if self.args.get_toppic_config_option('decoy'):
            toppic_command.append('--decoy')

        if self.args.get_toppic_config_option('mass_error_tolerance'):
            toppic_command.append('--mass-error-tolerance')
            toppic_command.append(str(self.args.get_toppic_config_option('mass_error_tolerance')))

        if self.args.get_toppic_config_option('proteoform_error_tolerance'):
            toppic_command.append('--proteoform-error-tolerance')
            toppic_command.append(str(self.args.get_toppic_config_option('proteoform_error_tolerance')))

        if self.args.get_toppic_config_option('spectrum_cutoff_type'):
            toppic_command.append('--spectrum-cutoff-type')
            toppic_command.append(self.args.get_toppic_config_option('spectrum_cutoff_type'))
        
        if self.args.get_toppic_config_option('spectrum_cutoff_value'):
            toppic_command.append('--spectrum-cutoff-value')
            toppic_command.append(str(self.args.get_toppic_config_option('spectrum_cutoff_value')))

        if self.args.get_toppic_config_option('proteoform_cutoff_type'):
            toppic_command.append('--proteoform-cutoff-type')
            toppic_command.append(self.args.get_toppic_config_option('proteoform_cutoff_type'))

        if self.args.get_toppic_config_option('proteoform_cutoff_value'):
            toppic_command.append('--proteoform-cutoff-value')
            toppic_command.append(str(self.args.get_toppic_config_option('proteoform_cutoff_value')))

        if self.args.get_toppic_config_option('approximate_spectra'):
            toppic_command.append('--approximate-spectra')

        if self.args.get_toppic_config_option('lookup_table'):
            toppic_command.append('--lookup-table')

        if self.args.get_toppic_config_option('local_ptm_file_name'):
            toppic_command.append('--local-ptm-file-name')
            toppic_command.append(self.args.get_toppic_config_option('local_ptm_file_name'))

        if self.args.get_toppic_config_option('miscore_threshold'):
            toppic_command.append('--miscore-threshold')
            toppic_command.append(str(self.args.get_toppic_config_option('miscore_threshold')))

        if self.args.get_toppic_config_option('thread_number'):
            toppic_command.append('--thread-number')
            toppic_command.append(str(self.args.get_toppic_config_option('thread_number')))

        if self.args.get_toppic_config_option('num_combined_spectra'):
            toppic_command.append('--num-combined-spectra')
            toppic_command.append(str(self.args.get_toppic_config_option('num_combined_spectra')))

        if self.args.get_toppic_config_option('combined_file_name'):
            toppic_command.append('--combined-file-name')
            toppic_command.append(self.args.get_toppic_config_option('combined_file_name'))

        if self.args.get_toppic_config_option('no_topfd_feature'):
            toppic_command.append('--no-topfd-feature')

        if self.args.get_toppic_config_option('keep_temp_files'):
            toppic_command.append('--keep-temp-files')

        if self.args.get_toppic_config_option('keep_decoy_ids'):
            toppic_command.append('--keep-decoy-ids')

        if self.args.get_toppic_config_option('skip_html_folder'):
            toppic_command.append('--skip-html-folder')
        
        toppic_command.append(self.fasta_file)

        for file in self.input_files:
            toppic_command.append(file)

        return toppic_command

