from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel, QVBoxLayout,
                            QHBoxLayout, QGroupBox, QLineEdit)
from .Setting import Setting

class ToolsTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.setting = Setting()
        self._init_ui()
    
    def check(self) -> bool:
        if not self.args.get_tool_path('msconvert'):
            print("MSConvert路径为空，请选择有效的路径。")
            return False
        if not self.args.get_tool_path('toppic'):
            print("TopPIC路径为空，请选择有效的路径。")
            return False
        if not self.args.get_tool_path('pbfgen'):
            print("PBFGen路径为空，请选择有效的路径。")
            return False
        if not self.args.get_tool_path('promex'):
            print("Promex路径为空，请选择有效的路径。")
            return False
        if not self.args.get_tool_path('mspathfinder'):
            print("MSPathFinder路径为空，请选择有效的路径。")
            return False
        if not self.args.get_tool_path('spectator'):
            print("Spectator路径为空，请选择有效的路径。")
            return False
        return True
    
    def _init_ui(self):
        layout = QVBoxLayout()
        # MSConvert路径设置
        layout.addWidget(self._create_msconvert_group())
        # TopPIC路径设置
        layout.addWidget(self._create_toppic_group())
        # PBFGen路径设置
        layout.addWidget(self._create_pbfgen_group())
        # Promex路径设置
        layout.addWidget(self._create_promex_group())
        # MSPathFinder路径设置
        layout.addWidget(self._create_mspathfinder_group())
        # Spectator路径设置
        layout.addWidget(self._create_spectator_group())
        
        layout.addStretch()
        self.setLayout(layout)
    
    def _create_msconvert_group(self):
        group = QGroupBox("MSConvert setting")
        layout = QHBoxLayout()
        msconvert_path = QLineEdit()
        if self.setting.get_config('Tools', 'msconvert'):
            msconvert_path.setText(self.setting.get_config('Tools', 'msconvert'))
            self.args.set_tool_path('msconvert', self.setting.get_config('Tools', 'msconvert'))
        else:
            msconvert_path.setPlaceholderText("Please select the path of MSConvert")
        msconvert_path.textChanged.connect(lambda text: (self.args.set_tool_path('msconvert', text), self.setting.set_config('Tools', 'msconvert', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(msconvert_path))
        
        layout.addWidget(QLabel("MSConvert path:"))
        layout.addWidget(msconvert_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group
    
    def _create_toppic_group(self):
        group = QGroupBox("TopPIC setting")
        layout = QHBoxLayout()
        toppic_path = QLineEdit()
        if self.setting.get_config('Tools', 'toppic'):
            toppic_path.setText(self.setting.get_config('Tools', 'toppic'))
            self.args.set_tool_path('toppic', self.setting.get_config('Tools', 'toppic'))
        else:
            toppic_path.setPlaceholderText("Please select the path of TopPIC")
        toppic_path.textChanged.connect(lambda text: (self.args.set_tool_path('toppic', text), self.setting.set_config('Tools', 'toppic', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(toppic_path))
        
        layout.addWidget(QLabel("TopPIC path:"))
        layout.addWidget(toppic_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group
    
    def _create_topfd_group(self):
        group = QGroupBox("TopFD setting")
        layout = QHBoxLayout()
        topfd_path = QLineEdit()
        if self.setting.get_config('Tools', 'topfd'):
            topfd_path.setText(self.setting.get_config('Tools', 'topfd'))
            self.args.set_tool_path('topfd', self.setting.get_config('Tools', 'topfd'))
        else:
            topfd_path.setPlaceholderText("Please select the path of TopFD")
        topfd_path.textChanged.connect(lambda text: (self.args.set_tool_path('topfd', text), self.setting.set_config('Tools', 'topfd', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(topfd_path))

        layout.addWidget(QLabel("TopFD path:"))
        layout.addWidget(topfd_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group

    def _create_pbfgen_group(self):
        group = QGroupBox("Pbfgen setting")
        layout = QHBoxLayout()
        pbfgen_path = QLineEdit()
        if self.setting.get_config('Tools', 'pbfgen'):
            pbfgen_path.setText(self.setting.get_config('Tools', 'pbfgen'))
            self.args.set_tool_path('pbfgen', self.setting.get_config('Tools', 'pbfgen'))
        else:
            pbfgen_path.setPlaceholderText("Please select the path of PBFGen")
        pbfgen_path.textChanged.connect(lambda text: (self.args.set_tool_path('pbfgen', text), self.setting.set_config('Tools', 'pbfgen', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(pbfgen_path))
        
        layout.addWidget(QLabel("PBFGen path:"))
        layout.addWidget(pbfgen_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group
    
    def _create_promex_group(self):
        group = QGroupBox("Promex setting")
        layout = QHBoxLayout()
        promex_path = QLineEdit()
        if self.setting.get_config('Tools', 'promex'):
            promex_path.setText(self.setting.get_config('Tools', 'promex'))
            self.args.set_tool_path('promex', self.setting.get_config('Tools', 'promex'))
        else:
            promex_path.setPlaceholderText("Please select the path of Promex")
        promex_path.textChanged.connect(lambda text: (self.args.set_tool_path('promex', text), self.setting.set_config('Tools', 'promex', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(promex_path))
        
        layout.addWidget(QLabel("Promex path:"))
        layout.addWidget(promex_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group

    def _create_mspathfinder_group(self):
        group = QGroupBox("MSPathfinder setting")
        layout = QHBoxLayout()
        mspathfinder_path = QLineEdit()
        if self.setting.get_config('Tools', 'mspathfinder'):
            mspathfinder_path.setText(self.setting.get_config('Tools', 'mspathfinder'))
            self.args.set_tool_path('mspathfinder', self.setting.get_config('Tools', 'mspathfinder'))
        else:
            mspathfinder_path.setPlaceholderText("Please select the path of MSPathfinder")
        mspathfinder_path.textChanged.connect(lambda text: (self.args.set_tool_path('mspathfinder', text), self.setting.set_config('Tools', 'mspathfinder', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(mspathfinder_path))
        
        layout.addWidget(QLabel("MSPathfinder path:"))
        layout.addWidget(mspathfinder_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group

    def _create_spectator_group(self):
        group = QGroupBox("Spectator setting")
        layout = QHBoxLayout()
        spectator_path = QLineEdit()
        if self.setting.get_config('Tools', 'spectator'):
            spectator_path.setText(self.setting.get_config('Tools', 'spectator'))
            self.args.set_tool_path('spectator', self.setting.get_config('Tools', 'spectator'))
        else:
            spectator_path.setPlaceholderText("Please select the path of Spectator")
        spectator_path.textChanged.connect(lambda text: (self.args.set_tool_path('spectator', text), self.setting.set_config('Tools', 'spectator', text)))
        browse_btn = QPushButton("browse")
        update_btn = QPushButton("update")
        browse_btn.clicked.connect(lambda: self._browse_file(spectator_path))
        
        layout.addWidget(QLabel("Spectator path:"))
        layout.addWidget(spectator_path)
        layout.addWidget(browse_btn)
        layout.addWidget(update_btn)
        group.setLayout(layout)
        return group
    
    def _browse_file(self, line_edit):
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getOpenFileName(self, "select file")
        if filename:
            line_edit.setText(filename)