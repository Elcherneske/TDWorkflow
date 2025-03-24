from .BaseWorkflow import BaseWorkflow
import os

class SpectrumSumWorkflow(BaseWorkflow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.input_files = args.get_ms_file_path()
        self.output_dir = args.get_output_dir()
    
    def prepare_workflow(self):
        self.commands = []
        for input_file in self.input_files:
            self.commands.append(self._sum_spectrum_command(input_file))
    
    def _sum_spectrum_command(self, input_file):
        python_path = self.args.get_tool_path('python')
        if not python_path:
            raise ValueError("Python path is not set. Please configure it in the Tools tab.")
        script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Tools", "spectrum_sum.py")

        sum_spectrum_command = [python_path, script_path]
        if self.args.get_spectrum_sum_config_option('tool'):
            sum_spectrum_command.extend(["--tool", self.args.get_spectrum_sum_config_option('tool')])

        if self.args.get_spectrum_sum_config_option('method'):
            sum_spectrum_command.extend(["--method", self.args.get_spectrum_sum_config_option('method')])
        
        if self.args.get_spectrum_sum_config_option('block_size'):
            sum_spectrum_command.extend(["--block-size", self.args.get_spectrum_sum_config_option('block_size')])
        
        if self.args.get_spectrum_sum_config_option('start_scan'):
            sum_spectrum_command.extend(["--start-scan", self.args.get_spectrum_sum_config_option('start_scan')])
        
        if self.args.get_spectrum_sum_config_option('end_scan'):
            sum_spectrum_command.extend(["--end-scan", self.args.get_spectrum_sum_config_option('end_scan')])
        
        if self.args.get_spectrum_sum_config_option('ms_level'):
            sum_spectrum_command.extend(["--ms-level", self.args.get_spectrum_sum_config_option('ms_level')])
        
        if self.args.get_spectrum_sum_config_option('rt_tolerance'):
            sum_spectrum_command.extend(["--rt-tolerance", self.args.get_spectrum_sum_config_option('rt_tolerance')])
        
        if self.args.get_spectrum_sum_config_option('mz_tolerance'):
            sum_spectrum_command.extend(["--mz-tolerance", self.args.get_spectrum_sum_config_option('mz_tolerance')])
        
        sum_spectrum_command.extend(["--input", input_file])

        if self.output_dir:
            sum_spectrum_command.extend(["--output-dir", self.output_dir])
        
        return sum_spectrum_command
        
        
        
        
        
