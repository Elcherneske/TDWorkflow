from .BaseWorkflow import BaseWorkflow

class TopfdWorkflow(BaseWorkflow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.input_files = args.get_ms_file_path()

    def prepare_workflow(self):
        # 示例：设置OnlyTopfd的命令序列
        self.commands = [
            self._topfd_command()
        ] 

    def _topfd_command(self):
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
        
        for input_file in self.input_files:
            topfd_command.append(input_file)

        return topfd_command

if __name__ == '__main__':
    pass
