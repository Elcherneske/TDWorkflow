import sys
import time
from PyQt5.QtWidgets import (QWidget, QTabWidget, QHBoxLayout,
                             QApplication)
from Args import Args
from GUI.ToolsTab import ToolsTab
from GUI.MSConvertConfigTab import MSConvertConfigTab
from GUI.WorkflowConfigTab import WorkflowConfigTab
from GUI.RunTab import RunTab
from GUI.ToppicConfigTab import ToppicConfigTab
from GUI.InformedProteomicsConfigTab import InformedProteomicsConfigTab
from Workflow.WorkflowManager import WorkflowManager

class AppGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.args = Args()  # 创建Args实例
        self.tabs = None
        self.output_tab = None
        self._init_ui()
    
    def _init_ui(self):
        self.setWindowTitle('Top-Down Mass Spectrometry Analysis Pipeline')
        self.setGeometry(100, 100, 1200, 1200)

        # 创建标签页
        self.tabs = QTabWidget()
        
        # 创建各个标签页实例
        self.tools_tab = ToolsTab(self.args)
        self.workflow_config_tab = WorkflowConfigTab(self.args)
        self.msconvert_config_tab = MSConvertConfigTab(self.args)
        self.toppic_config_tab = ToppicConfigTab(self.args)
        self.informed_proteomics_config_tab = InformedProteomicsConfigTab(self.args)
        self.run_tab = RunTab(self.args)

        # 添加标签页
        self.tabs.addTab(self.tools_tab, "Tools config")
        self.tabs.addTab(self.workflow_config_tab, "Workflow config")
        self.tabs.addTab(self.msconvert_config_tab, "MSConvert config")
        self.tabs.addTab(self.toppic_config_tab, "Toppic config")
        self.tabs.addTab(self.informed_proteomics_config_tab, "Informed Proteomics config")
        self.tabs.addTab(self.run_tab, "Run")
        
        # 添加运行接口
        self.run_btn = self.run_tab.run_btn
        self.stop_btn = self.run_tab.stop_btn
        self.run_btn.clicked.connect(self._run_process)
        self.stop_btn.clicked.connect(self._stop_process)

        # 主布局
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def update_output(self, text):
        self.run_tab.update_output(text)
    
    def _run_process(self):
        mode = self.args.get_mode()
        self.workflow = WorkflowManager.create_workflow(mode, self.args) #need self., otherwise it will be deleted before finishing
        self.workflow.output_received.connect(self.update_output)
        self.workflow.start()
    
    def _stop_process(self):
        if self.workflow and self.workflow.isRunning():
            self.workflow.terminate()
            self.update_output("Process has been interrupted.")
        

