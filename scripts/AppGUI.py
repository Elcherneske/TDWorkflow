import sys
import time
import os
import subprocess
import webbrowser
from PyQt5.QtWidgets import (QWidget, QTabWidget, QHBoxLayout,
                             QApplication)
from Args import Args
from GUI.ToolsTab import ToolsTab
from GUI import MSConvertConfigTab
from GUI import WorkflowConfigTab
from GUI import RunTab
from GUI import ToppicConfigTab
from GUI import InformedProteomicsConfigTab
from GUI import SpectrumProcessingTab
from Workflow.WorkflowManager import WorkflowManager

class AppGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.args = Args()  # 创建Args实例
        self.tabs = None
        self.output_tab = None

        self.streamlit_process = None  # 初始化streamlit进程变量
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
        self.spectrum_processing_tab = SpectrumProcessingTab(self.args)

        # 添加标签页
        self.tabs.addTab(self.tools_tab, "Tools")
        self.tabs.addTab(self.workflow_config_tab, "Workflow")
        self.tabs.addTab(self.msconvert_config_tab, "MSConvert")
        self.tabs.addTab(self.toppic_config_tab, "Toppic")
        self.tabs.addTab(self.informed_proteomics_config_tab, "Informed Proteomics")
        self.tabs.addTab(self.spectrum_processing_tab, "Spectrum Processing")
        self.tabs.addTab(self.run_tab, "Run")
        
        # 添加运行接口
        self.run_btn = self.run_tab.run_btn
        self.stop_btn = self.run_tab.stop_btn
        self.run_btn.clicked.connect(self._run_process)
        self.stop_btn.clicked.connect(self._stop_process)
        
        # 添加可视化按钮的点击事件
        self.vis_btn = self.run_tab.vis_btn
        self.vis_btn.clicked.connect(self._streamlit_process)

        # 主布局
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def update_output(self, text):
        self.run_tab.update_output(text)
    
    def _run_process(self):
        mode = self.args.get_mode()
        self.workflow = WorkflowManager.create_workflow(mode, self.args)
        self.workflow.output_received.connect(self.update_output)
        self.workflow.start()
    
    def _stop_process(self):
        if hasattr(self, 'workflow') and self.workflow and self.workflow.isRunning():
            # 首先终止当前正在运行的子进程
            if hasattr(self.workflow, 'process') and self.workflow.process:
                try:
                    # 在Windows上，terminate()相当于SIGTERM
                    # 在某些情况下可能不够强硬，所以我们先尝试温和的方式
                    self.workflow.process.terminate()
                    
                    # 给进程一点时间来正常关闭
                    time.sleep(0.5)
                    
                    # 检查进程是否仍在运行
                    if self.workflow.process.poll() is None:
                        # 如果进程仍在运行，使用kill()方法强制终止它
                        # 这相当于向进程发送SIGKILL信号
                        self.workflow.process.kill()
                        
                    self.update_output("子进程已终止。")
                except Exception as e:
                    self.update_output(f"终止子进程时出错: {str(e)}")
            
            # 然后终止工作流线程
            try:
                self.workflow.terminate()
                self.update_output("工作流已停止。")
            except Exception as e:
                self.update_output(f"停止工作流时出错: {str(e)}")
                
            self.update_output("处理过程已被中断。")
        
    def _streamlit_process(self):
        # 如果进程尚未创建或已经终止，则创建并启动进程
        if self.streamlit_process is None or self.streamlit_process.poll() is not None:
            dirname = os.path.dirname(os.path.dirname(__file__))
            filename = os.path.join(dirname, 'Tools', 'STWeb', 'MainPage.py')
            if self.args.output_dir:
                # 使用subprocess启动一个独立的进程运行streamlit
                self.streamlit_process = subprocess.Popen(
                    [sys.executable, "-m", "streamlit", "run", filename, '--', '--file_path', self.args.output_dir],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                # 使用subprocess启动一个独立的进程运行streamlit
                self.streamlit_process = subprocess.Popen(
                    [sys.executable, "-m", "streamlit", "run", filename],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            # 等待一小段时间让Streamlit启动
            time.sleep(0.5)
        else:
            # 打开默认浏览器访问streamlit页面
            webbrowser.open('http://localhost:8501')
    
    def closeEvent(self, event):
        # 窗口关闭时终止streamlit进程
        if self.streamlit_process and self.streamlit_process.poll() is None:
            self.streamlit_process.terminate()
            # 给进程一点时间来正常关闭
            time.sleep(0.25)
            # 如果进程仍在运行，强制终止
            if self.streamlit_process.poll() is None:
                self.streamlit_process.kill()
        event.accept()
        
