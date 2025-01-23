from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QGroupBox, QLabel, QComboBox, QCheckBox)
from .Setting import Setting


class MSConvertConfigTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.setting = Setting()
        self._init_ui()
    
    def check(self) -> bool:
        return True
    
    def _init_ui(self):
        layout = QVBoxLayout()
        options_group = QGroupBox("MSConvert Options")
        options_layout = QVBoxLayout()
        
        # 添加各种配置选项
        options_layout.addLayout(self._create_output_format_layout())
        options_layout.addLayout(self._create_peak_picking_layout())
        options_layout.addLayout(self._create_precision_layout())
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        layout.addStretch()
        self.setLayout(layout)
    
    def _create_output_format_layout(self):
        layout = QHBoxLayout()
        output_combo = QComboBox()
        output_combo.addItems(["mzML", "mzXML", "mgf", "ms1", "ms2"])
        self.args.set_msconvert_config_option('output_format', 'mzML')
        output_combo.currentTextChanged.connect(
            lambda text: self.args.set_msconvert_config_option('output_format', text)
        )
        layout.addWidget(QLabel("Output Format:"))
        layout.addWidget(output_combo)
        return layout
    
    def _create_peak_picking_layout(self):
        layout = QHBoxLayout()
        peak_picking_checkbox = QCheckBox("Enable Peak Picking")
        self.args.set_msconvert_config_option('peak_picking', False)
        peak_picking_checkbox.stateChanged.connect(
            lambda state: self.args.set_msconvert_config_option('peak_picking', bool(state))
        )
        layout.addWidget(peak_picking_checkbox)
        return layout

    def _create_precision_layout(self):
        layout = QHBoxLayout()
        
        # mz精度设置
        mz_combo = QComboBox()
        mz_combo.addItems(["32", "64"])
        self.args.set_msconvert_config_option('mz_precision', '32')
        mz_combo.currentTextChanged.connect(
            lambda text: self.args.set_msconvert_config_option('mz_precision', text)
        )
        layout.addWidget(QLabel("m/z Precision:"))
        layout.addWidget(mz_combo)
        
        # intensity精度设置 
        intensity_combo = QComboBox()
        intensity_combo.addItems(["32", "64"])
        self.args.set_msconvert_config_option('intensity_precision', '32')
        intensity_combo.currentTextChanged.connect(
            lambda text: self.args.set_msconvert_config_option('intensity_precision', text)
        )
        layout.addWidget(QLabel("Intensity Precision:"))
        layout.addWidget(intensity_combo)
        
        return layout