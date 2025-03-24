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
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout()
        # Spectrum summing options
        layout.addWidget(self._create_summing_options_group())
        layout.addStretch()
        self.setLayout(layout)
    
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
        
        # Summing method selection
        method_layout = QHBoxLayout()
        method_group = QButtonGroup(self)
        
        self.block_radio = QRadioButton("Block Summing")
        self.block_radio.setChecked(True)
        self.block_radio.toggled.connect(self._toggle_summing_options)
        method_group.addButton(self.block_radio)
        self.args.set_spectrum_sum_config_option('method', 'block')
        
        self.range_radio = QRadioButton("Range Summing")
        self.range_radio.toggled.connect(self._toggle_summing_options)
        method_group.addButton(self.range_radio)

        self.precursor_radio = QRadioButton("Precursor Summing")
        self.precursor_radio.toggled.connect(self._toggle_summing_options)
        method_group.addButton(self.precursor_radio)
        
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
            lambda ms_level: self.args.set_spectrum_sum_config_option('ms_level', ms_level)
        )
        ms_level_layout.addRow("MS Level:", ms_level_combo)
        layout.addLayout(ms_level_layout)
        
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
        return layout
    
    def _create_range_summing_options(self):
        layout = QFormLayout()
        start_scan = QSpinBox()
        start_scan.setRange(1, 100000)
        start_scan.setValue(1)
        start_scan.valueChanged.connect(
            lambda value: self.args.set_spectrum_sum_config_option('start_scan', value)
        )
        
        end_scan = QSpinBox()
        end_scan.setRange(1, 100000)
        end_scan.setValue(100)
        end_scan.valueChanged.connect(
            lambda value: self.args.set_spectrum_sum_config_option('end_scan', value)
        )
        
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

        precursor_rt = QDoubleSpinBox()
        precursor_rt.setRange(0, 100000)
        precursor_rt.setValue(10)
        precursor_rt.valueChanged.connect(
            lambda value: self.args.set_spectrum_sum_config_option('precursor_rt', value)
        )

        layout.addRow("Precursor M/Z:", precursor_mz)
        layout.addRow("Precursor RT:", precursor_rt)
        return layout
    
        
