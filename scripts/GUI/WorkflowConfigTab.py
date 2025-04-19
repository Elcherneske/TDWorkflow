from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLabel, QComboBox, QLineEdit, QPushButton)
from .Setting import Setting

class WorkflowConfigTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.setting = Setting()
        self._init_ui()
    
    def check(self) -> bool:
        if not self.args.get_ms_file_path():
            print("MS文件路径为空，请选择有效的路径。")
            return False
        
        if not self.args.get_fasta_path():
            print("FASTA文件路径为空，请选择有效的路径。")
            return False
        
        if not self.args.get_mode():
            print("工作模式未设置，请选择有效的模式。")
            return False
            
        return True
    
    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_mode_group())
        layout.addWidget(self._create_file_group())
        layout.addWidget(self._create_fasta_group())
        layout.addStretch()
        self.setLayout(layout)
    
    def _create_mode_group(self):
        group = QGroupBox("Pipeline Mode")
        layout = QHBoxLayout()
        mode_combo = QComboBox()
        mode_combo.addItems([
            "msconvert",
            "topfd",
            "toppic",
            "topmg",
            "pbfgen",
            "promex",
            "mspathfinder",
            "pbfgen and promex",
            "sum spectrum",
            "toppic suit"
        ])
        self.args.set_mode('msconvert')
        mode_combo.currentTextChanged.connect(
            lambda text: self.args.set_mode(text)
        )
        layout.addWidget(QLabel("Mode:"))
        layout.addWidget(mode_combo)
        group.setLayout(layout)
        return group
    
    def _create_file_group(self):
        group = QGroupBox("Input Files")
        layout = QHBoxLayout()
        ms_file_path_edit = QLineEdit()
        ms_file_path_edit.setPlaceholderText("Please select the path of MS files")
        ms_file_path_edit.textChanged.connect(lambda text: self.args.set_ms_file_path(text))
        browse_btn = QPushButton("browse")
        browse_btn.clicked.connect(lambda: self._browse_ms_files(ms_file_path_edit))
        
        layout.addWidget(QLabel("MS file path:"))
        layout.addWidget(ms_file_path_edit)
        layout.addWidget(browse_btn)
        group.setLayout(layout)
        return group

    def _create_fasta_group(self):
        group = QGroupBox("FASTA Database")
        layout = QHBoxLayout()
        fasta_path_edit = QLineEdit()
        if self.setting.get_config('Fasta', 'fasta_path'):
            fasta_path_edit.setText(self.setting.get_config('Fasta', 'fasta_path'))
            self.args.set_fasta_path(self.setting.get_config('Fasta', 'fasta_path'))
        else:
            fasta_path_edit.setPlaceholderText("Please select the path of FASTA file")
        fasta_path_edit.textChanged.connect(lambda text: (self.args.set_fasta_path(text), self.setting.set_config('Fasta', 'fasta_path', text)))
        browse_btn = QPushButton("browse")
        browse_btn.clicked.connect(lambda: self._browse_fasta_file(fasta_path_edit))
        
        layout.addWidget(QLabel("FASTA file path:"))
        layout.addWidget(fasta_path_edit)
        layout.addWidget(browse_btn)
        group.setLayout(layout)
        return group
        
    def _browse_ms_files(self, ms_file_path_edit):
        from PyQt5.QtWidgets import QFileDialog
        filenames, _ = QFileDialog.getOpenFileNames(self, "Select MS files")
        if filenames:
            ms_file_path_edit.setText(";".join(filenames))
            self.args.clear_ms_file_path()
            for filename in filenames:
                self.args.add_ms_file_path(filename)
                
    def _browse_fasta_file(self, fasta_path_edit):
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select FASTA file")
        if filename:
            fasta_path_edit.setText(filename)
            self.args.set_fasta_path(filename)
            self.setting.set_config('Fasta', 'fasta_path', filename)