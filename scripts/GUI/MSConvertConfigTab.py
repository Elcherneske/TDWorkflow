from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QGroupBox, QLabel, QComboBox, QCheckBox,
                            QPushButton, QFileDialog, QMessageBox)
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
        
        # Add save/load buttons at the top
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Settings")
        self.load_button = QPushButton("Load Settings")
        self.save_button.clicked.connect(self._save_settings)
        self.load_button.clicked.connect(self._load_settings)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.load_button)
        layout.addLayout(buttons_layout)
        
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
    
    def _save_settings(self):
        """Save current MSConvert settings to a file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save MSConvert Settings", "", "Settings Files (*.ini);;All Files (*)"
        )
        
        if not file_path:
            return
            
        try:
            # Collect current settings
            settings = {
                'output_format': self.args.get_msconvert_config_option('output_format'),
                'peak_picking': str(self.args.get_msconvert_config_option('peak_picking')),
                'mz_precision': self.args.get_msconvert_config_option('mz_precision'),
                'intensity_precision': self.args.get_msconvert_config_option('intensity_precision')
            }
            
            # Use Setting class to save settings
            self.setting.save_msconvert_settings(file_path, settings)
            QMessageBox.information(self, "Success", "Settings saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
    
    def _load_settings(self):
        """Load MSConvert settings from a file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load MSConvert Settings", "", "Settings Files (*.ini);;All Files (*)"
        )
        
        if not file_path:
            return
            
        try:
            # Use Setting class to load settings
            settings = self.setting.load_msconvert_settings(file_path)
            if settings:
                self._update_ui_from_settings(settings)
                QMessageBox.information(self, "Success", "Settings loaded successfully!")
            else:
                QMessageBox.warning(self, "Warning", "No valid settings found in the file.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load settings: {str(e)}")
    
    def _update_ui_from_settings(self, settings):
        """Update UI components based on loaded settings"""
        # Update output format
        if 'output_format' in settings:
            output_format = settings['output_format']
            self.args.set_msconvert_config_option('output_format', output_format)
            self.output_combo.setCurrentText(output_format)
        
        # Update peak picking
        if 'peak_picking' in settings:
            peak_picking = settings['peak_picking'].lower() == 'true'
            self.args.set_msconvert_config_option('peak_picking', peak_picking)
            self.peak_picking_checkbox.setChecked(peak_picking)
        
        # Update precision settings
        if 'mz_precision' in settings:
            mz_precision = settings['mz_precision']
            self.args.set_msconvert_config_option('mz_precision', mz_precision)
            self.mz_combo.setCurrentText(mz_precision)
            
        if 'intensity_precision' in settings:
            intensity_precision = settings['intensity_precision']
            self.args.set_msconvert_config_option('intensity_precision', intensity_precision)
            self.intensity_combo.setCurrentText(intensity_precision)
    
    def _create_output_format_layout(self):
        layout = QHBoxLayout()
        self.output_combo = QComboBox()
        self.output_combo.addItems(["mzML", "mzXML", "mgf", "ms1", "ms2"])
        self.args.set_msconvert_config_option('output_format', 'mzML')
        self.output_combo.currentTextChanged.connect(
            lambda text: self.args.set_msconvert_config_option('output_format', text)
        )
        layout.addWidget(QLabel("Output Format:"))
        layout.addWidget(self.output_combo)
        return layout
    
    def _create_peak_picking_layout(self):
        layout = QHBoxLayout()
        self.peak_picking_checkbox = QCheckBox("Enable Peak Picking")
        self.args.set_msconvert_config_option('peak_picking', False)
        self.peak_picking_checkbox.stateChanged.connect(
            lambda state: self.args.set_msconvert_config_option('peak_picking', bool(state))
        )
        layout.addWidget(self.peak_picking_checkbox)
        return layout

    def _create_precision_layout(self):
        layout = QHBoxLayout()
        
        # mz精度设置
        self.mz_combo = QComboBox()
        self.mz_combo.addItems(["32", "64"])
        self.args.set_msconvert_config_option('mz_precision', '32')
        self.mz_combo.currentTextChanged.connect(
            lambda text: self.args.set_msconvert_config_option('mz_precision', text)
        )
        layout.addWidget(QLabel("m/z Precision:"))
        layout.addWidget(self.mz_combo)
        
        # intensity精度设置 
        self.intensity_combo = QComboBox()
        self.intensity_combo.addItems(["32", "64"])
        self.args.set_msconvert_config_option('intensity_precision', '32')
        self.intensity_combo.currentTextChanged.connect(
            lambda text: self.args.set_msconvert_config_option('intensity_precision', text)
        )
        layout.addWidget(QLabel("Intensity Precision:"))
        layout.addWidget(self.intensity_combo)
        
        return layout