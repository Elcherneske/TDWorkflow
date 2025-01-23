from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                            QLabel, QLineEdit, QComboBox, QCheckBox, 
                            QScrollArea, QPushButton, QSpinBox, QDoubleSpinBox)

class ToppicConfigTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self._init_ui()
    
    def _init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout()
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # TopFD 配置组
        scroll_layout.addWidget(self._create_topfd_group())
        
        # TopPIC 配置组
        scroll_layout.addWidget(self._create_fragmentation_group())
        scroll_layout.addWidget(self._create_modification_group())
        scroll_layout.addWidget(self._create_error_tolerance_group())
        scroll_layout.addWidget(self._create_cutoff_group())
        scroll_layout.addWidget(self._create_performance_group())
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def _create_topfd_group(self):
        group = QGroupBox("TopFD Configuration")
        layout = QVBoxLayout()
        
        # 添加 TopFD 相关参数
        ms1_sn = self._create_number_input("MS1 S/N ratio:", "ms1_sn", 1, 1000, 3, topfd=True, double=True)
        ms2_sn = self._create_number_input("MS2 S/N ratio:", "ms2_sn", 1, 1000, 1, topfd=True, double=True)
        max_charge = self._create_number_input("Max charge state:", "max_charge", 1, 30, 30, topfd=True)    
        max_mass = self._create_number_input("Max monoisotopic mass:", "max_mass", 1, 70000, 70000, topfd=True, double=True)
        mz_error = self._create_number_input("m/z error tolerance:", "mz_error", 0.01, 10.0, 0.02, topfd=True, double=True)
        precursor_window = self._create_number_input("Precursor window size:", "precursor_window", 0.1, 10.0, 3.0, topfd=True, double=True)
        ecscore_cutoff = self._create_number_input("ECScore cutoff value:", "ecscore_cutoff", 0, 1, 0.5, topfd=True, double=True)
        min_scan_number = self._create_number_input("Min scan number:", "min_scan_number", 1, 3, 3, topfd=True)
        thread_number = self._create_number_input("Number of threads:", "thread_number", 1, 16, 1, topfd=True)

        layout.addLayout(ms1_sn)
        layout.addLayout(ms2_sn)
        layout.addLayout(max_charge)
        layout.addLayout(max_mass)
        layout.addLayout(mz_error)
        layout.addLayout(precursor_window)
        layout.addLayout(ecscore_cutoff)
        layout.addLayout(min_scan_number)
        layout.addLayout(thread_number)
        
        group.setLayout(layout)
        return group

    def _create_fragmentation_group(self):
        group = QGroupBox("Fragmentation Method")
        layout = QVBoxLayout()
        
        # 创建激活方式选择
        activation_combo = QComboBox()
        activation_combo.addItems(["CID", "ETD", "HCD", "UVPD"])
        self.args.set_toppic_config_option('activation', 'CID')
        activation_combo.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('activation', text)
        )
        
        layout.addWidget(QLabel("Activation method:"))
        layout.addWidget(activation_combo)
        
        group.setLayout(layout)
        return group

    def _create_modification_group(self):
        group = QGroupBox("Modification Settings")
        layout = QVBoxLayout()
        
        # 固定修饰
        fixed_mod_combo = QComboBox()
        fixed_mod_combo.addItems(["C57", "C58", "Custom"])
        self.args.set_toppic_config_option('fixed_mod', 'C57')
        fixed_mod_combo.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('fixed_mod', text)
        )

        fixed_mod_file = QLineEdit()
        fixed_mod_file.textChanged.connect(
            lambda text: self.args.set_toppic_config_option('fixed_mod_file', text)
        )
        browse_fixed_mod = QPushButton("Browse")
        browse_fixed_mod.clicked.connect(
            lambda: self._browse_file(fixed_mod_file)
        )
        
        # 可变修饰
        variable_ptm_file = QLineEdit()
        variable_ptm_file.textChanged.connect(
            lambda text: self.args.set_toppic_config_option('variable_ptm_file_name', text)
        )
        browse_variable_ptm = QPushButton("Browse")
        browse_variable_ptm.clicked.connect(
            lambda: self._browse_file(variable_ptm_file)
        )

        # 修饰数量限制
        num_shift = self._create_number_input("Max unexpected modifications:", "num_shift", 0, 2, 1)
        min_shift = self._create_number_input("Min mass shift:", "min_shift", -1000, 0, -500, double=True)
        max_shift = self._create_number_input("Max mass shift:", "max_shift", 0, 1000, 500, double=True)
        var_ptm_num = self._create_number_input("Max variable modifications:", "variable_ptm_num", 0, 10, 3)
        
        layout.addWidget(QLabel("Fixed modification:"))
        layout.addWidget(fixed_mod_combo)
        layout.addWidget(fixed_mod_file)
        layout.addWidget(browse_fixed_mod)
        layout.addWidget(QLabel("Variable modification file:"))
        layout.addWidget(variable_ptm_file)
        layout.addWidget(browse_variable_ptm)
        layout.addLayout(num_shift)
        layout.addLayout(min_shift)
        layout.addLayout(max_shift)
        layout.addLayout(var_ptm_num)
        
        group.setLayout(layout)
        return group

    def _create_error_tolerance_group(self):
        group = QGroupBox("Error Tolerance")
        layout = QVBoxLayout()
        
        mass_error = self._create_number_input("Mass error tolerance (PPM):","mass_error_tolerance", 1, 100, 10, double=True)
        proteoform_error = self._create_number_input("Proteoform error tolerance (Da):","proteoform_error_tolerance", 0.1, 10.0, 1.2, double=True)
        
        layout.addLayout(mass_error)
        layout.addLayout(proteoform_error)
        
        group.setLayout(layout)
        return group

    def _create_cutoff_group(self):
        group = QGroupBox("Cutoff Settings")
        layout = QVBoxLayout()
        
        # Spectrum level
        spectrum_type = QComboBox()
        spectrum_type.addItems(["EVALUE", "FDR"])   
        self.args.set_toppic_config_option('spectrum_cutoff_type', 'EVALUE')
        spectrum_type.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('spectrum_cutoff_type', text)
        )
        spectrum_value = self._create_number_input("Spectrum-level cutoff:", "spectrum_cutoff_value", 0.0001, 1.0, 0.01, double=True)

        # Proteoform level
        proteoform_type = QComboBox()
        proteoform_type.addItems(["EVALUE", "FDR"])
        self.args.set_toppic_config_option('proteoform_cutoff_type', 'EVALUE')
        proteoform_type.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('proteoform_cutoff_type', text)
        )
        proteoform_value = self._create_number_input("Proteoform-level cutoff:", "proteoform_cutoff_value", 0.0001, 1.0, 0.01, double=True)

        layout.addWidget(QLabel("Spectrum-level cutoff:"))
        layout.addWidget(spectrum_type)
        layout.addLayout(spectrum_value)
        layout.addWidget(QLabel("Proteoform-level cutoff:"))
        layout.addWidget(proteoform_type)
        layout.addLayout(proteoform_value)
        
        group.setLayout(layout)
        return group

    def _create_performance_group(self):
        group = QGroupBox("Performance Settings")
        layout = QVBoxLayout()
        
        thread_num = self._create_number_input("Thread number:", "thread_num", 1, 32, 1)
        combined_spectra = self._create_number_input("Number of combined spectra:", "num_combined_spectra", 1, 10, 1)
        
        # Checkboxes for various options
        approximate = QCheckBox("Use approximate spectra")
        self.args.set_toppic_config_option('approximate_spectra', False)
        approximate.stateChanged.connect(
            lambda state: self.args.set_toppic_config_option('approximate_spectra', state == Qt.Checked)
        )
        lookup_table = QCheckBox("Use lookup table")
        self.args.set_toppic_config_option('lookup_table', False)
        lookup_table.stateChanged.connect(
            lambda state: self.args.set_toppic_config_option('lookup_table', state == Qt.Checked)
        )
        
        layout.addLayout(thread_num)
        layout.addLayout(combined_spectra)
        layout.addWidget(approximate)
        layout.addWidget(lookup_table)
        
        group.setLayout(layout)
        return group

    def _create_number_input(self, label, arg, min_val, max_val, default, topfd=False, double=False):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        
        if double:
            spinbox = QDoubleSpinBox()
            spinbox.setDecimals(4)  # 修改为4位小数
            spinbox.setRange(float(min_val), float(max_val))  # 确保范围为浮点数
            spinbox.setValue(float(default))  # 确保默认值为浮点数
            if topfd:
                self.args.set_topfd_config_option(arg, float(default))
                spinbox.valueChanged.connect(
                    lambda text: self.args.set_topfd_config_option(arg, float(text))
                )
            else:
                self.args.set_toppic_config_option(arg, float(default))
                spinbox.valueChanged.connect(
                    lambda text: self.args.set_toppic_config_option(arg, float(text))
                )
        else:
            spinbox = QSpinBox()
            spinbox.setRange(int(min_val), int(max_val))  # 确保范围为整数
            spinbox.setValue(int(default))  # 确保默认值为整数
            if topfd:
                self.args.set_topfd_config_option(arg, int(default))
                spinbox.valueChanged.connect(
                    lambda text: self.args.set_topfd_config_option(arg, int(text))
                )
            else:
                self.args.set_toppic_config_option(arg, int(default))
                spinbox.valueChanged.connect(
                    lambda text: self.args.set_toppic_config_option(arg, int(text))
                )


        layout.addWidget(spinbox)
        
        return layout

    def _browse_file(self, line_edit):
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select file", "", file_type)
        if filename:
            line_edit.setText(filename) 