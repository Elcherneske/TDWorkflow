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
        scroll_layout.addWidget(self._create_toppic_configuration_group())

        # TopMG 配置组
        scroll_layout.addWidget(self._create_topmg_configuration_group())
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def _create_topfd_group(self):
        group = QGroupBox("TopFD Configuration")
        layout = QVBoxLayout()
        
        # 添加 TopFD 相关参数
        ms1_sn = self._create_number_input("MS1 S/N ratio:", "ms1_sn", 1, 1000, 3, 'topfd', double=True)
        ms2_sn = self._create_number_input("MS2 S/N ratio:", "ms2_sn", 1, 1000, 1, 'topfd', double=True)
        max_charge = self._create_number_input("Max charge state:", "max_charge", 2, 99, 30, 'topfd')   
        max_mass = self._create_number_input("Max monoisotopic mass:", "max_mass", 1000, 1000000, 70000, 'topfd', double=True)
        mz_error = self._create_number_input("m/z error tolerance:", "mz_error", 0.01, 10.0, 0.02, 'topfd', double=True)
        precursor_window = self._create_number_input("Precursor window size:", "precursor_window", 0.1, 10.0, 3.0, 'topfd', double=True)
        ecscore_cutoff = self._create_number_input("ECScore cutoff value:", "ecscore_cutoff", 0, 1, 0.5, 'topfd', double=True)
        min_scan_number = self._create_number_input("Min scan number:", "min_scan_number", 1, 3, 3, 'topfd')
        thread_number = self._create_number_input("Number of threads:", "thread_number", 1, 16, 1, 'topfd')


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

    def _create_topmg_configuration_group(self):
        group = QGroupBox("TopMG Configuration")
        layout = QVBoxLayout()
        
        # Fragmentation Method
        activation_combo = QComboBox()
        activation_combo.addItems(["CID", "ETD", "HCD", "UVPD", "FILE"])
        self.args.set_topmg_config_option('activation', 'FILE')
        activation_combo.currentTextChanged.connect(
            lambda text: self.args.set_topmg_config_option('activation', text)
        )

        layout.addWidget(QLabel("Activation method:"))
        layout.addWidget(activation_combo)

        # Fixed Modifications
        fixed_mod_combo = QComboBox()
        fixed_mod_combo.addItems(["C57", "C58", "Custom"])
        self.args.set_topmg_config_option('fixed-mod', 'C57')
        fixed_mod_combo.currentTextChanged.connect(
            lambda text: self.args.set_topmg_config_option('fixed-mod', text)
        )

        fixed_mod_file = QLineEdit()
        fixed_mod_file.textChanged.connect(
            lambda text: self.args.set_topmg_config_option('fixed-mod-file', text)
        )
        browse_fixed_mod = QPushButton("Browse")
        browse_fixed_mod.clicked.connect(
            lambda: self._browse_file(fixed_mod_file)
        )

        layout.addWidget(QLabel("Fixed modification:"))
        layout.addWidget(fixed_mod_combo)
        layout.addWidget(fixed_mod_file)
        layout.addWidget(browse_fixed_mod)

        # N-terminal Forms
        n_terminal_form_input = QLineEdit()
        n_terminal_form_input.setText("NONE,NME,NME_ACETYLATION,M_ACETYLATION")
        n_terminal_form_input.textChanged.connect(
            lambda text: self.args.set_topmg_config_option('n-terminal-form', text)
        )
        layout.addWidget(QLabel("N-terminal forms:"))
        layout.addWidget(n_terminal_form_input)

        # Decoy Option
        decoy_checkbox = QCheckBox("Use decoy database")
        decoy_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('decoy', bool(state))
        )
        layout.addWidget(decoy_checkbox)

        # Mass Error Tolerance
        mass_error_tolerance = self._create_number_input("Mass error tolerance (PPM):", "mass-error-tolerance", 1, 100, 10, 'topmg')
        layout.addLayout(mass_error_tolerance)

        # Proteoform Error Tolerance
        proteoform_error_tolerance = self._create_number_input("Proteoform error tolerance (Dalton):", "proteoform-error-tolerance", 0.1, 10.0, 1.2, 'topmg', double=True)
        layout.addLayout(proteoform_error_tolerance)

        # Maximum Shift
        max_shift = self._create_number_input("Maximum shift (Dalton):", "max-shift", 0, 2000, 500, 'topmg', double=True)
        layout.addLayout(max_shift)

        # Spectrum Cutoff Type
        spectrum_cutoff_type_combo = QComboBox()
        spectrum_cutoff_type_combo.addItems(["EVALUE", "FDR"])
        self.args.set_topmg_config_option('spectrum-cutoff-type', 'EVALUE')
        spectrum_cutoff_type_combo.currentTextChanged.connect(
            lambda text: self.args.set_topmg_config_option('spectrum-cutoff-type', text)
        )

        layout.addWidget(QLabel("Spectrum cutoff type:"))
        layout.addWidget(spectrum_cutoff_type_combo)

        # Spectrum Cutoff Value
        spectrum_cutoff_value = self._create_number_input("Spectrum cutoff value:", "spectrum-cutoff-value", 0.001, 1.0, 0.01, 'topmg', double=True)
        layout.addLayout(spectrum_cutoff_value)

        # Proteoform Cutoff Type
        proteoform_cutoff_type_combo = QComboBox()
        proteoform_cutoff_type_combo.addItems(["EVALUE", "FDR"])
        self.args.set_topmg_config_option('proteoform-cutoff-type', 'EVALUE')
        proteoform_cutoff_type_combo.currentTextChanged.connect(
            lambda text: self.args.set_topmg_config_option('proteoform-cutoff-type', text)
        )

        layout.addWidget(QLabel("Proteoform cutoff type:"))
        layout.addWidget(proteoform_cutoff_type_combo)

        # Proteoform Cutoff Value
        proteoform_cutoff_value = self._create_number_input("Proteoform cutoff value:", "proteoform-cutoff-value", 0.001, 1.0, 0.01, 'topmg', double=True)
        layout.addLayout(proteoform_cutoff_value)

        # Modification File Name
        mod_file_name_input = QLineEdit()
        mod_file_name_input.textChanged.connect(
            lambda text: self.args.set_topmg_config_option('mod-file-name', text)
        )
        layout.addWidget(QLabel("Modification file name:"))
        layout.addWidget(mod_file_name_input)

        # Thread Number
        thread_number = self._create_number_input("Thread number:", "thread-number", 1, 16, 1, 'topmg')
        layout.addLayout(thread_number)

        # Proteoform Graph Gap
        proteo_graph_gap = self._create_number_input("Proteoform graph gap:", "proteo-graph-gap", 0, 100, 40, 'topmg', double=True)
        layout.addLayout(proteo_graph_gap)

        # Variable PTM in Gap
        var_ptm_in_gap = self._create_number_input("Variable PTMs in gap:", "var-ptm-in-gap", 0, 10, 5, 'topmg')
        layout.addLayout(var_ptm_in_gap)

        # Maximum Number of Variable PTMs
        max_var_ptm = self._create_number_input("Maximum number of variable PTMs:", "var-ptm", 0, 10, 5, 'topmg')
        layout.addLayout(max_var_ptm)

        # Maximum Number of Unexpected Modifications
        num_shift_combo = QComboBox()
        num_shift_combo.addItems(["0", "1", "2"])
        self.args.set_topmg_config_option('num-shift', '0')
        num_shift_combo.currentTextChanged.connect(
            lambda text: self.args.set_topmg_config_option('num-shift', int(text))
        )

        layout.addWidget(QLabel("Maximum number of unexpected modifications:"))
        layout.addWidget(num_shift_combo)

        # Use ASF-DIAGONAL
        use_asf_diagonal_checkbox = QCheckBox("Use ASF-DIAGONAL method")
        use_asf_diagonal_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('use-asf-diagonal', bool(state))
        )
        layout.addWidget(use_asf_diagonal_checkbox)

        # Whole Protein Only
        whole_protein_only_checkbox = QCheckBox("Report only proteoforms from whole proteins")
        whole_protein_only_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('whole-protein-only', bool(state))
        )
        layout.addWidget(whole_protein_only_checkbox)

        # Skip HTML Folder
        skip_html_folder_checkbox = QCheckBox("Skip generation of HTML files")
        skip_html_folder_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('skip-html-folder', bool(state))
        )
        layout.addWidget(skip_html_folder_checkbox)

        # Combined File Name
        combined_file_name_input = QLineEdit()
        combined_file_name_input.textChanged.connect(
            lambda text: self.args.set_topmg_config_option('combined-file-name', text)
        )
        layout.addWidget(QLabel("Combined file name:"))
        layout.addWidget(combined_file_name_input)

        # Keep Temp Files
        keep_temp_files_checkbox = QCheckBox("Keep temporary files")
        keep_temp_files_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('keep-temp-files', bool(state))
        )
        layout.addWidget(keep_temp_files_checkbox)

        # Keep Decoy Identifications
        keep_decoy_ids_checkbox = QCheckBox("Keep decoy identifications")
        keep_decoy_ids_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('keep-decoy-ids', bool(state))
        )
        layout.addWidget(keep_decoy_ids_checkbox)

        group.setLayout(layout)
        return group



    def _create_toppic_configuration_group(self):
        group = QGroupBox("TopPIC Configuration")
        layout = QVBoxLayout()
        
        # Fragmentation Method
        activation_combo = QComboBox()
        activation_combo.addItems(["CID", "ETD", "HCD", "UVPD"])
        self.args.set_toppic_config_option('activation', 'CID')
        activation_combo.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('activation', text)
        )
        layout.addWidget(QLabel("Activation method:"))
        layout.addWidget(activation_combo)

        # Modification Settings
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
        
        variable_ptm_file = QLineEdit()
        variable_ptm_file.textChanged.connect(
            lambda text: self.args.set_toppic_config_option('variable_ptm_file_name', text)
        )
        browse_variable_ptm = QPushButton("Browse")
        browse_variable_ptm.clicked.connect(
            lambda: self._browse_file(variable_ptm_file)
        )

        num_shift = self._create_number_input("Max unexpected modifications:", "num_shift", 0, 2, 1, 'toppic')
        min_shift = self._create_number_input("Min mass shift:", "min_shift", -2000, 0, -500, 'toppic', double=True)
        max_shift = self._create_number_input("Max mass shift:", "max_shift", 0, 2000, 500, 'toppic', double=True)
        var_ptm_num = self._create_number_input("Max variable modifications:", "variable_ptm_num", 0, 10, 3, 'toppic')
        
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
        
        # Error Tolerance
        mass_error = self._create_number_input("Mass error tolerance (PPM):","mass_error_tolerance", 1, 100, 10, 'toppic', double=True)
        proteoform_error = self._create_number_input("Proteoform error tolerance (Da):","proteoform_error_tolerance", 0.1, 10.0, 1.2, 'toppic', double=True)

        layout.addLayout(mass_error)
        layout.addLayout(proteoform_error)

        # Cutoff Settings
        spectrum_type = QComboBox()
        spectrum_type.addItems(["EVALUE", "FDR"])   
        self.args.set_toppic_config_option('spectrum_cutoff_type', 'EVALUE')
        spectrum_type.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('spectrum_cutoff_type', text)
        )
        spectrum_value = self._create_number_input("Spectrum-level cutoff:", "spectrum_cutoff_value", 0.0001, 1.0, 0.01, 'toppic', double=True)

        proteoform_type = QComboBox()
        proteoform_type.addItems(["EVALUE", "FDR"])
        self.args.set_toppic_config_option('proteoform_cutoff_type', 'EVALUE')
        proteoform_type.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('proteoform_cutoff_type', text)
        )
        proteoform_value = self._create_number_input("Proteoform-level cutoff:", "proteoform_cutoff_value", 0.0001, 1.0, 0.01, 'toppic', double=True)

        layout.addWidget(QLabel("Spectrum-level cutoff:"))
        layout.addWidget(spectrum_type)
        layout.addLayout(spectrum_value)
        layout.addWidget(QLabel("Proteoform-level cutoff:"))
        layout.addWidget(proteoform_type)
        layout.addLayout(proteoform_value)

        # Performance Settings
        thread_num = self._create_number_input("Thread number:", "thread_num", 1, 32, 1, 'toppic')
        combined_spectra = self._create_number_input("Number of combined spectra:", "num_combined_spectra", 1, 10, 1, 'toppic')

        approximate = QCheckBox("Use approximate spectra")
        self.args.set_toppic_config_option('approximate_spectra', False)
        approximate.stateChanged.connect(
            lambda state: self.args.set_toppic_config_option('approximate_spectra', bool(state))
        )
        layout.addLayout(thread_num)
        layout.addLayout(combined_spectra)
        layout.addWidget(approximate)

        lookup_table = QCheckBox("Use lookup table")
        self.args.set_toppic_config_option('lookup_table', False)
        lookup_table.stateChanged.connect(
            lambda state: self.args.set_toppic_config_option('lookup_table', bool(state))
        )
        layout.addWidget(lookup_table)

        group.setLayout(layout)
        return group

    def _create_number_input(self, label, arg, min_val, max_val, default, group, double=False):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))        

        if double:
            spinbox = QDoubleSpinBox()
            spinbox.setDecimals(4)  # 修改为4位小数
            spinbox.setRange(float(min_val), float(max_val))  # 确保范围为浮点数
            spinbox.setValue(float(default))  # 确保默认值为浮点数
            if group == "topfd":
                self.args.set_topfd_config_option(arg, float(default))
                spinbox.valueChanged.connect(
                    lambda text: self.args.set_topfd_config_option(arg, float(text))
                )
            elif group == "topmg":
                self.args.set_topmg_config_option(arg, float(default))
                spinbox.valueChanged.connect(
                    lambda text: self.args.set_topmg_config_option(arg, float(text))
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
            if group == "topfd":
                self.args.set_topfd_config_option(arg, int(default))
                spinbox.valueChanged.connect(
                    lambda text: self.args.set_topfd_config_option(arg, int(text))
                )
            elif group == "topmg":
                self.args.set_topmg_config_option(arg, int(default))
                spinbox.valueChanged.connect(
                    lambda text: self.args.set_topmg_config_option(arg, int(text))
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