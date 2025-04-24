from .BaseWorkflow import BaseWorkflow

class MSConvertWorkflow(BaseWorkflow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.input_files = args.get_ms_file_path()

    def prepare_workflow(self):
        self.commands = []
        command = self._msconvert_command()
        if command:
            self.commands.append(command)

    def _msconvert_command(self):
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
        else:
            msconvert_command.append('--mz32')
        
        if self.args.get_msconvert_config_option('intensity_precision') == "64":
            msconvert_command.append('--inten64')
        elif self.args.get_msconvert_config_option('intensity_precision') == "32":
            msconvert_command.append('--inten32')
        else:
            msconvert_command.append('--inten32')

        if self.args.output_dir:
            msconvert_command.append('-o')
            msconvert_command.append(self.args.output_dir)

        # 处理peakPicking
        if self.args.get_msconvert_config_option('peak_picking_enabled'):
            msconvert_command.append('--filter')
            
            # 构建peakPicking过滤器
            if self.args.get_msconvert_config_option('peak_picking_algorithm'):
                algorithm = self.args.get_msconvert_config_option('peak_picking_algorithm')
            else:
                algorithm = 'vendor'

            if self.args.get_msconvert_config_option('peak_picking_ms_level_min'):
                ms_level_min = self.args.get_msconvert_config_option('peak_picking_ms_level_min')
            else:
                ms_level_min = '1'

            if self.args.get_msconvert_config_option('peak_picking_ms_level_max'):
                ms_level_max = self.args.get_msconvert_config_option('peak_picking_ms_level_max')
            else:
                ms_level_max = '1000000'
            
            peak_picking_filter = f'"peakPicking {algorithm} msLevel={ms_level_min}-{ms_level_max}'
            
            # 如果是cwt算法，添加特有参数
            if algorithm == 'cwt':
                min_snr = self.args.get_msconvert_config_option('peak_picking_min_snr')
                if min_snr is not None:
                    peak_picking_filter += f" snr={min_snr}"
                
                peak_spacing = self.args.get_msconvert_config_option('peak_picking_peak_spacing')
                if peak_spacing is not None:
                    peak_picking_filter += f" peakSpace={peak_spacing}"
            
            peak_picking_filter += '"'
            msconvert_command.append(peak_picking_filter)

        # 添加scan summing过滤器
        if self.args.get_msconvert_config_option('scan_summing_enabled'):
            msconvert_command.append('--filter')
            
            scan_summing_filter = '"scanSumming '
            
            # 添加precursor tolerance参数
            if self.args.get_msconvert_config_option('scan_summing_precursor_tol'):
                scan_summing_filter += f"precursorTol={self.args.get_msconvert_config_option('scan_summing_precursor_tol')} "
            
            # 添加scan time tolerance参数
            if self.args.get_msconvert_config_option('scan_summing_scan_time_tol'):
                scan_summing_filter += f"scanTimeTol={self.args.get_msconvert_config_option('scan_summing_scan_time_tol')} "
            
            # 添加ion mobility tolerance参数
            if self.args.get_msconvert_config_option('scan_summing_ion_mobility_tol'):
                scan_summing_filter += f"ionMobilityTol={self.args.get_msconvert_config_option('scan_summing_ion_mobility_tol')} "
            
            # 添加sum MS1 scans参数
            if self.args.get_msconvert_config_option('scan_summing_sum_ms1'):
                scan_summing_filter += "sumMs1=1 "
            else:
                scan_summing_filter += "sumMs1=0 "
            
            scan_summing_filter = scan_summing_filter.strip() + '"'
            msconvert_command.append(scan_summing_filter)

        # 添加subset过滤器
        if self.args.get_msconvert_config_option('subset_enabled'):

            # 添加MS Level参数
            if self.args.get_msconvert_config_option('subset_ms_level_min') or self.args.get_msconvert_config_option('subset_ms_level_max'):
                msconvert_command.append('--filter')
                filter_name = 'msLevel '
                if self.args.get_msconvert_config_option('subset_ms_level_min'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_ms_level_min')}"
                filter_name += '-'
                if self.args.get_msconvert_config_option('subset_ms_level_max'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_ms_level_max')}"
                filter_name = f'"{filter_name}"'
                msconvert_command.append(filter_name)

            # 添加Scan Number参数
            if self.args.get_msconvert_config_option('subset_scan_number_min') or self.args.get_msconvert_config_option('subset_scan_number_max'):
                msconvert_command.append('--filter')
                filter_name = 'scanNumber '
                if self.args.get_msconvert_config_option('subset_scan_number_min'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_scan_number_min')}"
                filter_name += '-'
                if self.args.get_msconvert_config_option('subset_scan_number_max'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_scan_number_max')}"
                filter_name = f'"{filter_name}"'
                msconvert_command.append(filter_name)

            # 添加Scan Time参数
            if self.args.get_msconvert_config_option('subset_scan_time_min') or self.args.get_msconvert_config_option('subset_scan_time_max'):
                msconvert_command.append('--filter')
                filter_name = 'scanTime '
                if self.args.get_msconvert_config_option('subset_scan_time_min'):
                    filter_name += f"[{self.args.get_msconvert_config_option('subset_scan_time_min')}"
                else:
                    filter_name += '[0'
                filter_name += ','
                if self.args.get_msconvert_config_option('subset_scan_time_max'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_scan_time_max')}]"
                else:
                    filter_name += '1e8]'
                filter_name = f'"{filter_name}"'
                msconvert_command.append(filter_name)

            # 添加Scan Events参数
            if self.args.get_msconvert_config_option('subset_scan_events_min') or self.args.get_msconvert_config_option('subset_scan_events_max'):
                msconvert_command.append('--filter')
                filter_name = 'scanEvent '
                if self.args.get_msconvert_config_option('subset_scan_events_min'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_scan_events_min')}"
                filter_name += '-'
                if self.args.get_msconvert_config_option('subset_scan_events_max'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_scan_events_max')}"
                filter_name = f'"{filter_name}"'
                msconvert_command.append(filter_name)

            # 添加Charge States参数
            if self.args.get_msconvert_config_option('subset_charge_states_min') or self.args.get_msconvert_config_option('subset_charge_states_max'):
                msconvert_command.append('--filter')
                filter_name = 'chargeState '
                if self.args.get_msconvert_config_option('subset_charge_states_min'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_charge_states_min')}"
                filter_name += '-'
                if self.args.get_msconvert_config_option('subset_charge_states_max'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_charge_states_max')}"
                filter_name = f'"{filter_name}"'
                msconvert_command.append(filter_name)

            # 添加Number of Data Points参数
            if self.args.get_msconvert_config_option('subset_data_points_min') or self.args.get_msconvert_config_option('subset_data_points_max'):
                msconvert_command.append('--filter')
                filter_name = 'defaultArrayLength '
                if self.args.get_msconvert_config_option('subset_data_points_min'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_data_points_min')}"
                filter_name += '-'
                if self.args.get_msconvert_config_option('subset_data_points_max'):
                    filter_name += f"{self.args.get_msconvert_config_option('subset_data_points_max')}"
                filter_name = f'"{filter_name}"'
                msconvert_command.append(filter_name)

            # 添加Collision Energy参数
            if self.args.get_msconvert_config_option('subset_collision_energy_min') and self.args.get_msconvert_config_option('subset_collision_energy_max'):
                msconvert_command.append('--filter')
                filter_name = 'collisionEnergy '
                filter_name += f"low={self.args.get_msconvert_config_option('subset_collision_energy_min')}"
                filter_name += f" high={self.args.get_msconvert_config_option('subset_collision_energy_max')}"
                filter_name += f" acceptNonCID=True acceptMissingCE=False"
                filter_name = f'"{filter_name}"'
                msconvert_command.append(filter_name)
            
            # 添加Scan Polarity参数
            if self.args.get_msconvert_config_option('subset_scan_polarity') and self.args.get_msconvert_config_option('subset_scan_polarity') != "Any":
                msconvert_command.append('--filter')
                filter_name = f"polarity {self.args.get_msconvert_config_option('subset_scan_polarity')} "
                msconvert_command.append(filter_name)

            # 添加Activation Type参数
            if self.args.get_msconvert_config_option('subset_activation_type') and self.args.get_msconvert_config_option('subset_activation_type') != "Any":
                msconvert_command.append('--filter')
                filter_name = f"activationType {self.args.get_msconvert_config_option('subset_activation_type')} "
                msconvert_command.append(filter_name)
            
            # 添加Analysis Type参数
            if self.args.get_msconvert_config_option('subset_analysis_type') and self.args.get_msconvert_config_option('subset_analysis_type') != "Any":
                analysis_type = self.args.get_msconvert_config_option('subset_analysis_type')
                msconvert_command.append('--filter')
                filter_name = f"analyzerType {analysis_type} "
                msconvert_command.append(filter_name)

        msconvert_command.append('--filter')
        msconvert_command.append('"titleMaker <RunId>.<ScanNumber>.<ScanNumber>.<ChargeState> File:"""^<SourcePath^>""", NativeID:"""^<Id^>""""')

        for input_file in self.input_files:
            msconvert_command.append(input_file)

        return msconvert_command
    
if __name__ == '__main__':
    import subprocess
    command = ['C:\\Users\\Elcher\\AppData\\Local\\Apps\\ProteoWizard\\msconvert.exe', '--zlib', '--mzML', '--mz32', '--inten32', '-o', 'D:/', '--filter', '"peakPicking vendor msLevel=1-"', '--filter', '"titleMaker <RunId>.<ScanNumber>.<ScanNumber>.<ChargeState> File:"""^<SourcePath^>""", NativeID:"""^<Id^>""""', 'D:/BaiduNetdiskDownload/20250113-2-400ng-HistoneQC-2.raw']
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
