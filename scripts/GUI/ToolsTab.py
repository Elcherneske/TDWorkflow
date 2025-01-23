from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout,
                            QHBoxLayout, QGroupBox, QLineEdit)
from .Setting import Setting

class ToolsTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.setting = Setting()
        self.msconvert_path = None
        self.toppic_path = None
        self.informed_proteomics_path = None
        self.spectator_path = None
        self._init_ui()
    
    def check(self) -> bool:
        if not self.args.get_tool_path('msconvert'):
            print("MSConvert路径为空，请选择有效的路径。")
            return False
        if not self.args.get_tool_path('toppic'):
            print("TopPIC路径为空，请选择有效的路径。")
            return False
        if not self.args.get_tool_path('informed_proteomics'):
            print("InformedProteomics路径为空，请选择有效的路径。")
            return False
        if not self.args.get_tool_path('spectator'):
            print("Spectator路径为空，请选择有效的路径。")
            return False
        if not self.args.get_tool_path('topfd'):
            print("TopFD路径为空，请选择有效的路径。")
            return False
        return True
    
    def _init_ui(self):
        layout = QVBoxLayout()
        # MSConvert路径设置
        layout.addWidget(self._create_msconvert_group())
        # TopPIC路径设置
        layout.addWidget(self._create_toppic_group())
        # TopFD路径设置
        layout.addWidget(self._create_topfd_group())
        # InformedProteomics路径设置
        layout.addWidget(self._create_informed_proteomics_group())
        # Spectator路径设置
        layout.addWidget(self._create_spectator_group())
        
        layout.addStretch()
        self.setLayout(layout)
    
    def _create_msconvert_group(self):
        group = QGroupBox("MSConvert setting")
        layout = QHBoxLayout()
        self.msconvert_path = QLineEdit()
        if self.setting.get_config('Tools', 'msconvert'):
            self.msconvert_path.setText(self.setting.get_config('Tools', 'msconvert'))
            self.args.set_tool_path('msconvert', self.setting.get_config('Tools', 'msconvert'))
        else:
            self.msconvert_path.setPlaceholderText("Please select the path of MSConvert")
        self.msconvert_path.textChanged.connect(lambda text: (self.args.set_tool_path('msconvert', text), self.setting.set_config('Tools', 'msconvert', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(self.msconvert_path))
        
        layout.addWidget(QLabel("MSConvert path:"))
        layout.addWidget(self.msconvert_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group
    
    def _create_toppic_group(self):
        group = QGroupBox("TopPIC setting")
        layout = QHBoxLayout()
        self.toppic_path = QLineEdit()
        if self.setting.get_config('Tools', 'toppic'):
            self.toppic_path.setText(self.setting.get_config('Tools', 'toppic'))
            self.args.set_tool_path('toppic', self.setting.get_config('Tools', 'toppic'))
        else:
            self.toppic_path.setPlaceholderText("Please select the path of TopPIC")
        self.toppic_path.textChanged.connect(lambda text: (self.args.set_tool_path('toppic', text), self.setting.set_config('Tools', 'toppic', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(self.toppic_path))
        
        layout.addWidget(QLabel("TopPIC path:"))
        layout.addWidget(self.toppic_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group
    
    def _create_topfd_group(self):
        group = QGroupBox("TopFD setting")
        layout = QHBoxLayout()
        self.topfd_path = QLineEdit()
        if self.setting.get_config('Tools', 'topfd'):
            self.topfd_path.setText(self.setting.get_config('Tools', 'topfd'))
            self.args.set_tool_path('topfd', self.setting.get_config('Tools', 'topfd'))
        else:
            self.topfd_path.setPlaceholderText("Please select the path of TopFD")
        self.topfd_path.textChanged.connect(lambda text: (self.args.set_tool_path('topfd', text), self.setting.set_config('Tools', 'topfd', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(self.topfd_path))

        layout.addWidget(QLabel("TopFD path:"))
        layout.addWidget(self.topfd_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group

    def _create_informed_proteomics_group(self):
        group = QGroupBox("InformedProteomics setting")
        layout = QHBoxLayout()
        self.informed_proteomics_path = QLineEdit()
        if self.setting.get_config('Tools', 'informed_proteomics'):
            self.informed_proteomics_path.setText(self.setting.get_config('Tools', 'informed_proteomics'))
            self.args.set_tool_path('informed_proteomics', self.setting.get_config('Tools', 'informed_proteomics'))
        else:
            self.informed_proteomics_path.setPlaceholderText("Please select the path of InformedProteomics")
        self.informed_proteomics_path.textChanged.connect(lambda text: (self.args.set_tool_path('informed_proteomics', text), self.setting.set_config('Tools', 'informed_proteomics', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(self.informed_proteomics_path))
        
        layout.addWidget(QLabel("InformedProteomics path:"))
        layout.addWidget(self.informed_proteomics_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group

    def _create_spectator_group(self):
        group = QGroupBox("Spectator setting")
        layout = QHBoxLayout()
        self.spectator_path = QLineEdit()
        if self.setting.get_config('Tools', 'spectator'):
            self.spectator_path.setText(self.setting.get_config('Tools', 'spectator'))
            self.args.set_tool_path('spectator', self.setting.get_config('Tools', 'spectator'))
        else:
            self.spectator_path.setPlaceholderText("Please select the path of Spectator")
        self.spectator_path.textChanged.connect(lambda text: (self.args.set_tool_path('spectator', text), self.setting.set_config('Tools', 'spectator', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(self.spectator_path))
        
        layout.addWidget(QLabel("Spectator path:"))
        layout.addWidget(self.spectator_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group
    
    def _browse_file(self, line_edit):
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getOpenFileName(self, "select file")
        if filename:
            line_edit.setText(filename)