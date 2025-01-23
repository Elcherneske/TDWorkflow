class Args:
    def __init__(self):
        self.tool_paths = {   # 存储各种工具的路径
            'msconvert': None,
            'toppic': None,
            'topfd': None,
            'informed_proteomics': None,
        }
        self.general_config_options = {}
        self.msconvert_config_options = {
            'output_format': None,
            'mz_precision': None,
            'intensity_precision': None,
            'peak_picking': None,
        }
        self.topfd_config_options = {
            'activation': None,
            'ms1_sn': None,
            'ms2_sn': None,
            'max_charge': None,
            'max_mass': None,
            'mz_error': None,
            'precursor_window': None,
            'ecscore_cutoff': None,
            'min_scan_number': None,
            'thread_number': None,
            'skip_html_folder': None,
            'disable_additional_feature_search': None,
            'disable_final_filtering': None
        }
        self.toppic_config_options = {
            'activation': None,
            'fixed_mod': None,
            'fixed_mod_file': None,
            'variable_ptm_file': None,
            'n_terminal_forms': None,
            'num_shift': None,
            'min_shift': None,
            'max_shift': None,
            'variable_ptm_num': None,
            'variable_ptm_file_name': None,
            'decoy': None,
            'mass_error_tolerance': None,
            'proteoform_error_tolerance': None,
            'spectrum_cutoff_type': None,
            'spectrum_cutoff_value': None,
            'proteoform_cutoff_type': None,
            'proteoform_cutoff_value': None,
            'thread_number': None,
            'num_combined_spectra': None,
            'approximate_spectra': None,
            'lookup_table': None,
            'local_ptm_file_name': None,
            'miscore_threshold': None,
            'keep_temp_files': None,
            'keep_decoy_ids': None,
            'skip_html_folder': None,
            'no_topfd_feature': None,
            'combined_file_name': None
        }
        self.informed_proteomics_config_options = {}
        self.mode = None
        self.ms_file_path = []
        self.fasta_path = None
        self.output_dir = None
    
    def set_tool_path(self, tool_name, path):
        self.tool_paths[tool_name] = path
    
    def get_tool_path(self, tool_name):
        return self.tool_paths.get(tool_name, None)
    
    def set_mode(self, mode):
        self.mode = mode
    
    def get_mode(self):
        return self.mode
    
    def add_ms_file_path(self, path):
        self.ms_file_path.append(path)
    
    def get_ms_file_path(self):
        return self.ms_file_path
    
    def clear_ms_file_path(self):
        self.ms_file_path = []
    
    def set_ms_file_path(self, text):
        filenames = text.split(';')
        self.clear_ms_file_path()
        for filename in filenames:
            self.add_ms_file_path(filename)
    
    def set_fasta_path(self, path):
        self.fasta_path = path
    
    def get_fasta_path(self):
        return self.fasta_path
    
    def set_output_dir(self, path):
        self.output_dir = path
    
    def get_output_dir(self):
        return self.output_dir  
    
    def set_general_config_option(self, key, value):
        self.general_config_options[key] = value
    
    def get_general_config_option(self, key):
        return self.general_config_options.get(key, None)

    def set_msconvert_config_option(self, key, value):
        self.msconvert_config_options[key] = value
    
    def get_msconvert_config_option(self, key):
        return self.msconvert_config_options.get(key, None) 
    
    def set_toppic_config_option(self, key, value):
        self.toppic_config_options[key] = value
    
    def get_toppic_config_option(self, key):
        return self.toppic_config_options.get(key, None)   

    def set_topfd_config_option(self, key, value):
        self.topfd_config_options[key] = value
    
    def get_topfd_config_option(self, key):
        return self.topfd_config_options.get(key, None)
    
    def set_informed_proteomics_config_option(self, key, value):
        self.informed_proteomics_config_options[key] = value
    
    def get_informed_proteomics_config_option(self, key):
        return self.informed_proteomics_config_options.get(key, None)   
