from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                            QLabel, QLineEdit, QPushButton, QTextEdit, 
                            QFileDialog, QRadioButton, QSpinBox, QComboBox,
                            QFormLayout, QButtonGroup, QMessageBox, QDoubleSpinBox)
from .Setting import Setting
import os

class SpectrumProcessingTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        # 用于保存所有UI控件
        self.ui = {
            'spectrum_sum': {}
        }
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout()
        
        # 添加保存/加载按钮
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("保存设置")
        load_button = QPushButton("加载设置")
        save_button.clicked.connect(self._save_settings)
        load_button.clicked.connect(self._load_settings)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(load_button)
        layout.addLayout(buttons_layout)
        
        # Spectrum summing options
        layout.addWidget(self._create_summing_options_group())
        layout.addStretch()
        self.setLayout(layout)
    
    def _save_settings(self):
        """保存当前设置到文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存光谱处理设置", "", "设置文件 (*.ini);;所有文件 (*)"
        )
        
        if not file_path:
            QMessageBox.information(self, "错误", "未选择保存路径！")
            return
            
        try:
            # 从self.ui收集当前设置
            settings = {
                'spectrum_sum': self._collect_spectrum_sum_settings()
            }
            
            # 使用Setting类保存设置
            Setting.save(file_path, settings)
            QMessageBox.information(self, "成功", "设置已成功保存！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置失败: {str(e)}")
    
    def _collect_spectrum_sum_settings(self):
        """收集光谱合并设置"""
        settings = {}
        for key, widget in self.ui['spectrum_sum'].items():
            if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                settings[key] = str(widget.value())
            elif isinstance(widget, QLineEdit):
                settings[key] = widget.text()
            elif isinstance(widget, QComboBox):
                settings[key] = widget.currentText()
            elif isinstance(widget, QRadioButton):
                if widget.isChecked():
                    settings['method'] = key
        return settings
    
    def _load_settings(self):
        """从文件加载设置"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "加载光谱处理设置", "", "设置文件 (*.ini);;所有文件 (*)"
        )
        
        if not file_path:
            QMessageBox.information(self, "错误", "未选择加载路径！")
            return
            
        try:
            # 创建Setting实例加载配置
            setting_instance = Setting(file_path)
            
            # 更新光谱合并设置
            self._update_spectrum_sum_settings(setting_instance)
            
            QMessageBox.information(self, "成功", "设置已成功加载！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载设置失败: {str(e)}")
    
    def _update_spectrum_sum_settings(self, setting_instance):
        """从配置更新光谱合并设置"""
        # 更新方法选择
        method = setting_instance.get('spectrum_sum', 'method')
        if method:
            if method == 'block':
                self.block_radio.setChecked(True)
            elif method == 'range':
                self.range_radio.setChecked(True)
            elif method == 'precursor':
                self.precursor_radio.setChecked(True)
            self.args.set_spectrum_sum_config_option('method', method)
        
        # 更新其他控件
        for key, widget in self.ui['spectrum_sum'].items():
            if key != 'block' and key != 'range' and key != 'precursor':
                value = setting_instance.get('spectrum_sum', key)
                if value:
                    if isinstance(widget, QSpinBox):
                        widget.setValue(int(value))
                        self.args.set_spectrum_sum_config_option(key, int(value))
                    elif isinstance(widget, QDoubleSpinBox):
                        widget.setValue(float(value))
                        self.args.set_spectrum_sum_config_option(key, float(value))
                    elif isinstance(widget, QLineEdit):
                        widget.setText(value)
                        self.args.set_spectrum_sum_config_option(key, value)
                    elif isinstance(widget, QComboBox):
                        widget.setCurrentText(value)
                        self.args.set_spectrum_sum_config_option(key, value)
                else:
                    if isinstance(widget, QLineEdit):
                        widget.setText(value)
                        self.args.set_spectrum_sum_config_option(key, value)
    
    def _create_summing_options_group(self):
        group = QGroupBox("Spectrum Summing Options")
        layout = QVBoxLayout()

        tool_layout = QHBoxLayout()
        tool_combo = QComboBox()
        tool_combo.addItems([
            "openms",
            "openmsutils"
        ])
        self.args.set_spectrum_sum_config_option('tool', 'openms')
        tool_combo.currentTextChanged.connect(
            lambda text: self.args.set_spectrum_sum_config_option('tool', text)
        )
        tool_layout.addWidget(QLabel("Tools:"))
        tool_layout.addWidget(tool_combo)
        layout.addLayout(tool_layout)
        self.ui['spectrum_sum']['tool'] = tool_combo
        
        # Summing method selection
        method_layout = QHBoxLayout()
        method_group = QButtonGroup(self)
        
        self.block_radio = QRadioButton("Block Summing")
        self.block_radio.setChecked(True)
        self.block_radio.toggled.connect(self._toggle_summing_options)
        method_group.addButton(self.block_radio)
        self.args.set_spectrum_sum_config_option('method', 'block')
        self.ui['spectrum_sum']['block'] = self.block_radio
        
        self.range_radio = QRadioButton("Range Summing")
        self.range_radio.toggled.connect(self._toggle_summing_options)
        method_group.addButton(self.range_radio)
        self.ui['spectrum_sum']['range'] = self.range_radio

        self.precursor_radio = QRadioButton("Precursor Summing")
        self.precursor_radio.toggled.connect(self._toggle_summing_options)
        method_group.addButton(self.precursor_radio)
        self.ui['spectrum_sum']['precursor'] = self.precursor_radio
        
        method_layout.addWidget(self.block_radio)
        method_layout.addWidget(self.range_radio)
        method_layout.addWidget(self.precursor_radio)
        layout.addLayout(method_layout)
        
        # Block summing options
        self.block_options_widget = QWidget()
        self.block_options = self._create_block_summing_options()
        self.block_options_widget.setLayout(self.block_options)
        layout.addWidget(self.block_options_widget)
        
        # Range summing options
        self.range_options_widget = QWidget()
        self.range_options = self._create_range_summing_options()
        self.range_options_widget.setLayout(self.range_options)
        self.range_options_widget.setVisible(False)
        layout.addWidget(self.range_options_widget)

        # Precursor summing options
        self.precursor_options_widget = QWidget()
        self.precursor_options = self._create_precursor_summing_options()
        self.precursor_options_widget.setLayout(self.precursor_options)
        self.precursor_options_widget.setVisible(False)
        layout.addWidget(self.precursor_options_widget)
        
        # MS Level selection
        ms_level_layout = QFormLayout()
        ms_level_combo = QComboBox()
        ms_level_combo.addItems(["MS1", "MS2"])
        ms_level_combo.currentIndexChanged.connect(
            lambda index: self.args.set_spectrum_sum_config_option('ms_level', index)
        )
        ms_level_layout.addRow("MS Level:", ms_level_combo)
        layout.addLayout(ms_level_layout)
        self.ui['spectrum_sum']['ms_level'] = ms_level_combo
        
        group.setLayout(layout)
        return group
    
    def _toggle_summing_options(self):
        self.block_options_widget.setVisible(self.block_radio.isChecked())
        self.range_options_widget.setVisible(self.range_radio.isChecked())
        self.precursor_options_widget.setVisible(self.precursor_radio.isChecked())
        if self.precursor_radio.isChecked():
            self.args.set_spectrum_sum_config_option('method', 'precursor')
        elif self.range_radio.isChecked():
            self.args.set_spectrum_sum_config_option('method', 'range')
        else:
            self.args.set_spectrum_sum_config_option('method', 'block')
    
    def _create_block_summing_options(self):
        layout = QFormLayout()
        block_size = QSpinBox()
        block_size.setRange(2, 100)
        block_size.setValue(5)
        block_size.valueChanged.connect(
            lambda value: self.args.set_spectrum_sum_config_option('block_size', value)
        )
        layout.addRow("Block Size:", block_size)
        self.ui['spectrum_sum']['block_size'] = block_size
        return layout
    
    def _create_range_summing_options(self):
        layout = QFormLayout()
        start_scan = QSpinBox()
        start_scan.setRange(1, 100000)
        start_scan.setValue(1)
        start_scan.valueChanged.connect(
            lambda value: self.args.set_spectrum_sum_config_option('start_scan', value)
        )
        self.ui['spectrum_sum']['start_scan'] = start_scan
        
        end_scan = QSpinBox()
        end_scan.setRange(1, 100000)
        end_scan.setValue(100)
        end_scan.valueChanged.connect(
            lambda value: self.args.set_spectrum_sum_config_option('end_scan', value)
        )
        self.ui['spectrum_sum']['end_scan'] = end_scan
        
        layout.addRow("Start Scan:", start_scan)
        layout.addRow("End Scan:", end_scan)
        return layout
    
    def _create_precursor_summing_options(self):
        layout = QFormLayout()
        precursor_mz = QDoubleSpinBox()
        precursor_mz.setRange(0, 100000)
        precursor_mz.setValue(100)
        precursor_mz.valueChanged.connect(
            lambda value: self.args.set_spectrum_sum_config_option('precursor_mz', value)
        )
        self.ui['spectrum_sum']['precursor_mz'] = precursor_mz

        precursor_rt = QDoubleSpinBox()
        precursor_rt.setRange(0, 100000)
        precursor_rt.setValue(10)
        precursor_rt.valueChanged.connect(
            lambda value: self.args.set_spectrum_sum_config_option('precursor_rt', value)
        )
        self.ui['spectrum_sum']['precursor_rt'] = precursor_rt

        layout.addRow("Precursor M/Z:", precursor_mz)
        layout.addRow("Precursor RT:", precursor_rt)
        return layout
        
