from .BaseWorkflow import BaseWorkflow

class ToppicSuitWorkflow(BaseWorkflow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.input_files = args.get_ms_file_path()
        self.fasta_file = args.get_fasta_path()
        self.output_dir = args.get_output_dir()

    def prepare_workflow(self):
        self.commands = []
        command = self._msconvert_command(self.input_files)
        if command:
            self.commands.append(command)

        mzml_files = []
        for input_file in self.input_files:
            mzml_files.append(f"{self.output_dir}/{input_file.split('/')[-1].rsplit('.', 1)[0]}.mzML")
            
        command = self._topfd_command(mzml_files)
        if command:
            self.commands.append(command)

        msalign_files = []
        for mzml_file in mzml_files:
            msalign_files.append(f"{self.output_dir}/{mzml_file.split('/')[-1].rsplit('.', 1)[0]}_ms2.msalign")

        command = self._toppic_command(msalign_files)
        if command:
            self.commands.append(command)
    
    def _msconvert_command(self, input_files):
        if not self.args.tool_paths['msconvert']:
            self.log("MSConvert路径为空，请检查配置。")
            return None
        
        msconvert_command = [self.args.tool_paths['msconvert']]

        msconvert_command.append('--zlib')
        
        if self.args.get_msconvert_config_option('output_format') == "mzML":
            msconvert_command.append('--mzML')
        elif self.args.get_msconvert_config_option('output_format') == "mzXML":
            msconvert_command.append('--mzXML')
        elif self.args.get_msconvert_config_option('output_format') == "mgf":
            msconvert_command.append('--mgf')
        elif self.args.get_msconvert_config_option('output_format') == "ms1":
            msconvert_command.append('--ms1')
        elif self.args.get_msconvert_config_option('output_format') == "ms2":
            msconvert_command.append('--ms2')
        elif self.args.get_msconvert_config_option('output_format') == "cms1":
            msconvert_command.append('--cms1')
        elif self.args.get_msconvert_config_option('output_format') == "cms2":
            msconvert_command.append('--cms2')
        else:
            msconvert_command.append('--mzML')
        
        if self.args.get_msconvert_config_option('mz_precision') == "64":
            msconvert_command.append('--mz64')
        elif self.args.get_msconvert_config_option('mz_precision') == "32":
            msconvert_command.append('--mz32')
        
        if self.args.get_msconvert_config_option('intensity_precision') == "64":
            msconvert_command.append('--inten64')
        elif self.args.get_msconvert_config_option('intensity_precision') == "32":
            msconvert_command.append('--inten32')

        if self.args.output_dir:
            msconvert_command.append('-o')
            msconvert_command.append(self.args.output_dir)

        if self.args.get_msconvert_config_option('peak_picking'):
            msconvert_command.append('--filter')
            msconvert_command.append('"peakPicking vendor msLevel=1-"')

        msconvert_command.append('--filter')
        msconvert_command.append('"titleMaker <RunId>.<ScanNumber>.<ScanNumber>.<ChargeState> File:"""^<SourcePath^>""", NativeID:"""^<Id^>""""')

        for input_file in input_files:
            msconvert_command.append(input_file)

        return msconvert_command
    
    def _topfd_command(self, input_files):
        if not self.args.tool_paths['topfd']:
            self.log("TopFD路径为空，请检查配置。")
            return None
        
        topfd_command = [self.args.tool_paths['topfd']]
        if self.args.get_topfd_config_option('activation'):
            topfd_command.append('--activation')
            topfd_command.append(self.args.get_topfd_config_option('activation'))
        
        if self.args.get_topfd_config_option('max_charge'):
            topfd_command.append('--max-charge')
            topfd_command.append(str(self.args.get_topfd_config_option('max_charge')))
        
        if self.args.get_topfd_config_option('max_mass'):
            topfd_command.append('--max-mass')
            topfd_command.append(str(self.args.get_topfd_config_option('max_mass')))
        
        if self.args.get_topfd_config_option('mz_error'):
            topfd_command.append('--mz-error')
            topfd_command.append(str(self.args.get_topfd_config_option('mz_error')))
        
        if self.args.get_topfd_config_option('ms1_sn'):
            topfd_command.append('--ms-one-sn-ratio')
            topfd_command.append(str(self.args.get_topfd_config_option('ms1_sn')))
        
        if self.args.get_topfd_config_option('ms2_sn'):
            topfd_command.append('--ms-two-sn-ratio')
            topfd_command.append(str(self.args.get_topfd_config_option('ms2_sn')))
        
        if self.args.get_topfd_config_option('precursor_window'):
            topfd_command.append('--precursor-window')
            topfd_command.append(str(self.args.get_topfd_config_option('precursor_window')))
        
        if self.args.get_topfd_config_option('ecscore_cutoff'):
            topfd_command.append('--ecscore-cutoff')
            topfd_command.append(str(self.args.get_topfd_config_option('ecscore_cutoff')))
        
        if self.args.get_topfd_config_option('min_scan_number'):
            topfd_command.append('--min-scan-number')
            topfd_command.append(str(self.args.get_topfd_config_option('min_scan_number')))
        
        if self.args.get_topfd_config_option('thread_number'):
            topfd_command.append('--thread-number')
            topfd_command.append(str(self.args.get_topfd_config_option('thread_number')))
        
        if self.args.get_topfd_config_option('skip_html_folder'):
            topfd_command.append('--skip-html-folder')
        
        if self.args.get_topfd_config_option('disable_additional_feature_search'):
            topfd_command.append('--disable-additional-feature-search')
        
        if self.args.get_topfd_config_option('disable_final_filtering'):
            topfd_command.append('--disable-final-filtering')

        for input_file in input_files:
            topfd_command.append(input_file)

        return topfd_command

    def _toppic_command(self, input_files):
        if not self.args.tool_paths['toppic']:
            self.log("TopPIC路径为空，请检查配置。")
            return None
        
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

        for file in input_files:
            toppic_command.append(file)
        return toppic_command


if __name__ == '__main__':
    pass

