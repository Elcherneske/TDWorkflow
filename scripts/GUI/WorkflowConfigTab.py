from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QGroupBox, QLabel, QComboBox, QLineEdit, QPushButton)
from .Setting import Setting

class WorkflowConfigTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.setting = Setting()
        self.mode_combo = None
        self.ms_file_path_edit = None
        self.fasta_path_edit = None
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
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["only convert", "only topfd", "only toppic", "toppic"])
        self.args.set_mode('only convert')
        self.mode_combo.currentTextChanged.connect(
            lambda text: self.args.set_mode(text)
        )
        layout.addWidget(QLabel("Mode:"))
        layout.addWidget(self.mode_combo)
        group.setLayout(layout)
        return group
    
    def _create_file_group(self):
        group = QGroupBox("Input Files")
        layout = QHBoxLayout()
        self.ms_file_path_edit = QLineEdit()
        self.ms_file_path_edit.setPlaceholderText("Please select the path of MS files")
        self.ms_file_path_edit.textChanged.connect(lambda text: self.args.set_ms_file_path(text))
        browse_btn = QPushButton("browse")
        browse_btn.clicked.connect(self._browse_ms_files)
        
        layout.addWidget(QLabel("MS file path:"))
        layout.addWidget(self.ms_file_path_edit)
        layout.addWidget(browse_btn)
        group.setLayout(layout)
        return group

    def _create_fasta_group(self):
        group = QGroupBox("FASTA Database")
        layout = QHBoxLayout()
        self.fasta_path_edit = QLineEdit()
        if self.setting.get_config('Fasta', 'fasta_path'):
            self.fasta_path_edit.setText(self.setting.get_config('Fasta', 'fasta_path'))
            self.args.set_fasta_path(self.setting.get_config('Fasta', 'fasta_path'))
        else:
            self.fasta_path_edit.setPlaceholderText("Please select the path of FASTA file")
        self.fasta_path_edit.textChanged.connect(lambda text: (self.args.set_fasta_path(text), self.setting.set_config('Fasta', 'fasta_path', text)))
        browse_btn = QPushButton("browse")
        browse_btn.clicked.connect(self._browse_fasta_file)
        
        layout.addWidget(QLabel("FASTA file path:"))
        layout.addWidget(self.fasta_path_edit)
        layout.addWidget(browse_btn)
        group.setLayout(layout)
        return group
        
    def _browse_ms_files(self):
        from PyQt5.QtWidgets import QFileDialog
        filenames, _ = QFileDialog.getOpenFileNames(self, "Select MS files")
        if filenames:
            self.ms_file_path_edit.setText(";".join(filenames))
            self.args.clear_ms_file_path()
            for filename in filenames:
                self.args.add_ms_file_path(filename)
                
    def _browse_fasta_file(self):
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select FASTA file")
        if filename:
            self.fasta_path_edit.setText(filename)
            self.args.set_fasta_path(filename)
            self.setting.set_config('Fasta', 'fasta_path', filename)