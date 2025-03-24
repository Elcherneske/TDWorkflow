from .BaseWorkflow import BaseWorkflow

class MSConvertWorkflow(BaseWorkflow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.input_files = args.get_ms_file_path()

    def prepare_workflow(self):
        self.commands = [
            self._msconvert_command()
        ] 

    def _msconvert_command(self):
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
