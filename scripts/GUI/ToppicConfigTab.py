from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                            QLabel, QLineEdit, QComboBox, QCheckBox, 
                            QScrollArea, QPushButton, QSpinBox, QDoubleSpinBox,
                            QFileDialog, QMessageBox)
from .Setting import Setting

class ToppicConfigTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        # 用于保存所有UI控件
        self.ui = {
            'topfd': {},
            'toppic': {},
            'topmg': {}
        }
        self._init_ui()
    
    def _init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout()
        
        # 添加保存/加载按钮
        buttons_layout = QHBoxLayout()
        save_button = QPushButton("保存设置")
        load_button = QPushButton("加载设置")
        save_button.clicked.connect(self._save_settings)
        load_button.clicked.connect(self._load_settings)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(load_button)
        main_layout.addLayout(buttons_layout)
        
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
    
    def _save_settings(self):
        """保存当前设置到文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存Toppic设置", "", "设置文件 (*.ini);;所有文件 (*)"
        )
        
        if not file_path:
            QMessageBox.information(self, "错误", "未选择保存路径！")
            return
            
        try:
            # 从self.ui收集当前设置
            settings = {
                'topfd': self._collect_topfd_settings(),
                'toppic': self._collect_toppic_settings(),
                'topmg': self._collect_topmg_settings()
            }
            
            # 使用Setting类保存设置
            Setting.save(file_path, settings)
            QMessageBox.information(self, "成功", "设置已成功保存！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置失败: {str(e)}")
    
    def _collect_topfd_settings(self):
        """收集TopFD设置"""
        settings = {}
        for key, widget in self.ui['topfd'].items():
            if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                settings[key] = str(widget.value())
            elif isinstance(widget, QLineEdit):
                settings[key] = widget.text()
            elif isinstance(widget, QComboBox):
                settings[key] = widget.currentText()
            elif isinstance(widget, QCheckBox):
                settings[key] = str(widget.isChecked())
        return settings
    
    def _collect_toppic_settings(self):
        """收集TopPIC设置"""
        settings = {}
        for key, widget in self.ui['toppic'].items():
            if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                settings[key] = str(widget.value())
            elif isinstance(widget, QLineEdit):
                settings[key] = widget.text()
            elif isinstance(widget, QComboBox):
                settings[key] = widget.currentText()
            elif isinstance(widget, QCheckBox):
                settings[key] = str(widget.isChecked())
        return settings
    
    def _collect_topmg_settings(self):
        """收集TopMG设置"""
        settings = {}
        for key, widget in self.ui['topmg'].items():
            if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                settings[key] = str(widget.value())
            elif isinstance(widget, QLineEdit):
                settings[key] = widget.text()
            elif isinstance(widget, QComboBox):
                settings[key] = widget.currentText()
            elif isinstance(widget, QCheckBox):
                settings[key] = str(widget.isChecked())
        return settings
    
    def _load_settings(self):
        """从文件加载设置"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "加载Toppic设置", "", "设置文件 (*.ini);;所有文件 (*)"
        )
        
        if not file_path:
            QMessageBox.information(self, "错误", "未选择加载路径！")
            return
            
        try:
            # 创建Setting实例加载配置
            setting_instance = Setting(file_path)
            
            # 更新TopFD设置
            self._update_topfd_settings(setting_instance)
            
            # 更新TopPIC设置
            self._update_toppic_settings(setting_instance)
            
            # 更新TopMG设置
            self._update_topmg_settings(setting_instance)
            
            QMessageBox.information(self, "成功", "设置已成功加载！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载设置失败: {str(e)}")
    
    def _update_topfd_settings(self, setting_instance):
        """从配置更新TopFD设置"""
        for key, widget in self.ui['topfd'].items():
            value = setting_instance.get('topfd', key)
            if value:
                if isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                    self.args.set_topfd_config_option(key, int(value))
                elif isinstance(widget, QDoubleSpinBox):
                    widget.setValue(float(value))
                    self.args.set_topfd_config_option(key, float(value))
                elif isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_topfd_config_option(key, value)
                elif isinstance(widget, QComboBox):
                    widget.setCurrentText(value)
                    self.args.set_topfd_config_option(key, value)
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(value.lower() == 'true')
                    self.args.set_topfd_config_option(key, value.lower() == 'true')
            else:
                if isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_topfd_config_option(key, value)
    
    def _update_toppic_settings(self, setting_instance):
        """从配置更新TopPIC设置"""
        for key, widget in self.ui['toppic'].items():
            value = setting_instance.get('toppic', key)
            if value:
                if isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                    self.args.set_toppic_config_option(key, int(value))
                elif isinstance(widget, QDoubleSpinBox):
                    widget.setValue(float(value))
                    self.args.set_toppic_config_option(key, float(value))
                elif isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_toppic_config_option(key, value)
                elif isinstance(widget, QComboBox):
                    widget.setCurrentText(value)
                    self.args.set_toppic_config_option(key, value)
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(value.lower() == 'true')
                    self.args.set_toppic_config_option(key, value.lower() == 'true')
            else:
                if isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_toppic_config_option(key, value)
    
    def _update_topmg_settings(self, setting_instance):
        """从配置更新TopMG设置"""
        for key, widget in self.ui['topmg'].items():
            value = setting_instance.get('topmg', key)
            if value:
                if isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                    self.args.set_topmg_config_option(key, int(value))
                elif isinstance(widget, QDoubleSpinBox):
                    widget.setValue(float(value))
                    self.args.set_topmg_config_option(key, float(value))
                elif isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_topmg_config_option(key, value)
                elif isinstance(widget, QComboBox):
                    widget.setCurrentText(value)
                    self.args.set_topmg_config_option(key, value)
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(value.lower() == 'true')
                    self.args.set_topmg_config_option(key, value.lower() == 'true')
            else:
                if isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_topmg_config_option(key, value)

    def _create_topfd_group(self):
        group = QGroupBox("TopFD Configuration")
        layout = QVBoxLayout()
        
        # 添加 TopFD 相关参数
        ms1_sn_layout = self._create_number_input("MS1 S/N ratio:", "ms1_sn", 1, 1000, 3, 'topfd', double=True)
        ms2_sn_layout = self._create_number_input("MS2 S/N ratio:", "ms2_sn", 1, 1000, 1, 'topfd', double=True)
        max_charge_layout = self._create_number_input("Max charge state:", "max_charge", 2, 99, 30, 'topfd')   
        max_mass_layout = self._create_number_input("Max monoisotopic mass:", "max_mass", 1000, 1000000, 70000, 'topfd', double=True)
        mz_error_layout = self._create_number_input("m/z error tolerance:", "mz_error", 0.01, 10.0, 0.02, 'topfd', double=True)
        precursor_window_layout = self._create_number_input("Precursor window size:", "precursor_window", 0.1, 10.0, 3.0, 'topfd', double=True)
        ecscore_cutoff_layout = self._create_number_input("ECScore cutoff value:", "ecscore_cutoff", 0, 1, 0.5, 'topfd', double=True)
        min_scan_number_layout = self._create_number_input("Min scan number:", "min_scan_number", 1, 3, 3, 'topfd')
        thread_number_layout = self._create_number_input("Number of threads:", "thread_number", 1, 16, 1, 'topfd')

        layout.addLayout(ms1_sn_layout)
        layout.addLayout(ms2_sn_layout)
        layout.addLayout(max_charge_layout)
        layout.addLayout(max_mass_layout)
        layout.addLayout(mz_error_layout)
        layout.addLayout(precursor_window_layout)
        layout.addLayout(ecscore_cutoff_layout)
        layout.addLayout(min_scan_number_layout)
        layout.addLayout(thread_number_layout)
        
        group.setLayout(layout)
        return group

    def _create_topmg_configuration_group(self):
        group = QGroupBox("TopMG Configuration")
        layout = QVBoxLayout()
        
        # Fragmentation Method
        activation_layout = QHBoxLayout()
        activation_layout.addWidget(QLabel("Activation method:"))
        activation_combo = QComboBox()
        activation_combo.addItems(["CID", "ETD", "HCD", "UVPD", "FILE"])
        self.args.set_topmg_config_option('activation', 'FILE')
        activation_combo.currentTextChanged.connect(
            lambda text: self.args.set_topmg_config_option('activation', text)
        )
        activation_layout.addWidget(activation_combo)
        self.ui['topmg']['activation'] = activation_combo

        # Fixed Modifications
        fixed_mod_layout = QHBoxLayout()
        fixed_mod_layout.addWidget(QLabel("Fixed modification:"))
        fixed_mod_combo = QComboBox()
        fixed_mod_combo.addItems(["Custom", "C57", "C58"])
        self.args.set_topmg_config_option('fixed-mod', 'Custom')
        fixed_mod_combo.currentTextChanged.connect(
            lambda text: self.args.set_topmg_config_option('fixed-mod', text)
        )
        fixed_mod_layout.addWidget(fixed_mod_combo)
        self.ui['topmg']['fixed-mod'] = fixed_mod_combo

        fixed_mod_file_layout = QHBoxLayout()
        fixed_mod_file = QLineEdit()
        fixed_mod_file.textChanged.connect(
            lambda text: self.args.set_topmg_config_option('fixed-mod-file', text)
        )
        browse_fixed_mod = QPushButton("Browse")
        browse_fixed_mod.clicked.connect(
            lambda: self._browse_file(fixed_mod_file)
        )
        fixed_mod_file_layout.addWidget(fixed_mod_file)
        fixed_mod_file_layout.addWidget(browse_fixed_mod)
        self.ui['topmg']['fixed-mod-file'] = fixed_mod_file

        # N-terminal Forms
        n_terminal_layout = QHBoxLayout()
        n_terminal_layout.addWidget(QLabel("N-terminal forms:"))
        n_terminal_form_input = QLineEdit()
        n_terminal_form_input.setText("NONE,NME,NME_ACETYLATION,M_ACETYLATION")
        n_terminal_form_input.textChanged.connect(
            lambda text: self.args.set_topmg_config_option('n-terminal-form', text)
        )
        n_terminal_layout.addWidget(n_terminal_form_input)
        self.ui['topmg']['n-terminal-form'] = n_terminal_form_input

        # Decoy Option
        decoy_layout = QHBoxLayout()
        decoy_checkbox = QCheckBox("Use decoy database")
        decoy_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('decoy', bool(state))
        )
        decoy_layout.addWidget(decoy_checkbox)
        self.ui['topmg']['decoy'] = decoy_checkbox

        # Mass Error Tolerance
        mass_error_tolerance_layout = self._create_number_input("Mass error tolerance (PPM):", "mass-error-tolerance", 1, 100, 10, 'topmg')

        # Proteoform Error Tolerance
        proteoform_error_tolerance_layout = self._create_number_input("Proteoform error tolerance (Dalton):", "proteoform-error-tolerance", 0.1, 10.0, 1.2, 'topmg', double=True)

        # Maximum Shift
        max_shift_layout = self._create_number_input("Maximum shift (Dalton):", "max-shift", 0, 2000, 500, 'topmg', double=True)

        # Spectrum Cutoff Type
        spectrum_cutoff_type_layout = QHBoxLayout()
        spectrum_cutoff_type_layout.addWidget(QLabel("Spectrum cutoff type:"))
        spectrum_cutoff_type_combo = QComboBox()
        spectrum_cutoff_type_combo.addItems(["EVALUE", "FDR"])
        self.args.set_topmg_config_option('spectrum-cutoff-type', 'EVALUE')
        spectrum_cutoff_type_combo.currentTextChanged.connect(
            lambda text: self.args.set_topmg_config_option('spectrum-cutoff-type', text)
        )
        spectrum_cutoff_type_layout.addWidget(spectrum_cutoff_type_combo)
        self.ui['topmg']['spectrum-cutoff-type'] = spectrum_cutoff_type_combo

        # Spectrum Cutoff Value
        spectrum_cutoff_value_layout = self._create_number_input("Spectrum cutoff value:", "spectrum-cutoff-value", 0.001, 1.0, 0.01, 'topmg', double=True)

        # Proteoform Cutoff Type
        proteoform_cutoff_type_layout = QHBoxLayout()
        proteoform_cutoff_type_layout.addWidget(QLabel("Proteoform cutoff type:"))
        proteoform_cutoff_type_combo = QComboBox()
        proteoform_cutoff_type_combo.addItems(["EVALUE", "FDR"])
        self.args.set_topmg_config_option('proteoform-cutoff-type', 'EVALUE')
        proteoform_cutoff_type_combo.currentTextChanged.connect(
            lambda text: self.args.set_topmg_config_option('proteoform-cutoff-type', text)
        )
        proteoform_cutoff_type_layout.addWidget(proteoform_cutoff_type_combo)
        self.ui['topmg']['proteoform-cutoff-type'] = proteoform_cutoff_type_combo

        # Proteoform Cutoff Value
        proteoform_cutoff_value_layout = self._create_number_input("Proteoform cutoff value:", "proteoform-cutoff-value", 0.001, 1.0, 0.01, 'topmg', double=True)

        # Modification File Name
        mod_file_layout = QHBoxLayout()
        mod_file_layout.addWidget(QLabel("Modification file name:"))
        mod_file_name_input = QLineEdit()
        mod_file_name_input.textChanged.connect(
            lambda text: self.args.set_topmg_config_option('mod-file-name', text)
        )
        mod_file_layout.addWidget(mod_file_name_input)
        self.ui['topmg']['mod-file-name'] = mod_file_name_input

        # Thread Number
        thread_number_layout = self._create_number_input("Thread number:", "thread-number", 1, 16, 1, 'topmg')

        # Proteoform Graph Gap
        proteo_graph_gap_layout = self._create_number_input("Proteoform graph gap:", "proteo-graph-gap", 0, 100, 40, 'topmg', double=True)

        # Variable PTM in Gap
        var_ptm_in_gap_layout = self._create_number_input("Variable PTMs in gap:", "var-ptm-in-gap", 0, 10, 5, 'topmg')

        # Maximum Number of Variable PTMs
        max_var_ptm_layout = self._create_number_input("Maximum number of variable PTMs:", "var-ptm", 0, 10, 5, 'topmg')

        # Maximum Number of Unexpected Modifications
        num_shift_layout = QHBoxLayout()
        num_shift_layout.addWidget(QLabel("Maximum number of unexpected modifications:"))
        num_shift_combo = QComboBox()
        num_shift_combo.addItems(["0", "1", "2"])
        self.args.set_topmg_config_option('num-shift', '0')
        num_shift_combo.currentTextChanged.connect(
            lambda text: self.args.set_topmg_config_option('num-shift', int(text))
        )
        num_shift_layout.addWidget(num_shift_combo)
        self.ui['topmg']['num-shift'] = num_shift_combo

        # Use ASF-DIAGONAL
        use_asf_diagonal_layout = QHBoxLayout()
        use_asf_diagonal_checkbox = QCheckBox("Use ASF-DIAGONAL method")
        use_asf_diagonal_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('use-asf-diagonal', bool(state))
        )
        use_asf_diagonal_layout.addWidget(use_asf_diagonal_checkbox)
        self.ui['topmg']['use-asf-diagonal'] = use_asf_diagonal_checkbox

        # Whole Protein Only
        whole_protein_only_layout = QHBoxLayout()
        whole_protein_only_checkbox = QCheckBox("Report only proteoforms from whole proteins")
        whole_protein_only_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('whole-protein-only', bool(state))
        )
        whole_protein_only_layout.addWidget(whole_protein_only_checkbox)
        self.ui['topmg']['whole-protein-only'] = whole_protein_only_checkbox

        # Skip HTML Folder
        skip_html_folder_layout = QHBoxLayout()
        skip_html_folder_checkbox = QCheckBox("Skip generation of HTML files")
        skip_html_folder_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('skip-html-folder', bool(state))
        )
        skip_html_folder_layout.addWidget(skip_html_folder_checkbox)
        self.ui['topmg']['skip-html-folder'] = skip_html_folder_checkbox

        # Combined File Name
        combined_file_layout = QHBoxLayout()
        combined_file_layout.addWidget(QLabel("Combined file name:"))
        combined_file_name_input = QLineEdit()
        combined_file_name_input.textChanged.connect(
            lambda text: self.args.set_topmg_config_option('combined-file-name', text)
        )
        combined_file_layout.addWidget(combined_file_name_input)
        self.ui['topmg']['combined-file-name'] = combined_file_name_input

        # Keep Temp Files
        keep_temp_files_layout = QHBoxLayout()
        keep_temp_files_checkbox = QCheckBox("Keep temporary files")
        keep_temp_files_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('keep-temp-files', bool(state))
        )
        keep_temp_files_layout.addWidget(keep_temp_files_checkbox)
        self.ui['topmg']['keep-temp-files'] = keep_temp_files_checkbox

        # Keep Decoy Identifications
        keep_decoy_ids_layout = QHBoxLayout()
        keep_decoy_ids_checkbox = QCheckBox("Keep decoy identifications")
        keep_decoy_ids_checkbox.stateChanged.connect(
            lambda state: self.args.set_topmg_config_option('keep-decoy-ids', bool(state))
        )
        keep_decoy_ids_layout.addWidget(keep_decoy_ids_checkbox)
        self.ui['topmg']['keep-decoy-ids'] = keep_decoy_ids_checkbox

        layout.addLayout(activation_layout)
        layout.addLayout(fixed_mod_layout)
        layout.addLayout(fixed_mod_file_layout)
        layout.addLayout(n_terminal_layout)
        layout.addLayout(decoy_layout)
        layout.addLayout(mass_error_tolerance_layout)
        layout.addLayout(proteoform_error_tolerance_layout)
        layout.addLayout(max_shift_layout)
        layout.addLayout(spectrum_cutoff_type_layout)
        layout.addLayout(spectrum_cutoff_value_layout)
        layout.addLayout(proteoform_cutoff_type_layout)
        layout.addLayout(proteoform_cutoff_value_layout)
        layout.addLayout(mod_file_layout)
        layout.addLayout(thread_number_layout)
        layout.addLayout(proteo_graph_gap_layout)
        layout.addLayout(var_ptm_in_gap_layout)
        layout.addLayout(max_var_ptm_layout)
        layout.addLayout(num_shift_layout)
        layout.addLayout(use_asf_diagonal_layout)
        layout.addLayout(whole_protein_only_layout)
        layout.addLayout(skip_html_folder_layout)
        layout.addLayout(combined_file_layout)
        layout.addLayout(keep_temp_files_layout)
        layout.addLayout(keep_decoy_ids_layout)

        group.setLayout(layout)
        return group

    def _create_toppic_configuration_group(self):
        group = QGroupBox("TopPIC Configuration")
        layout = QVBoxLayout()
        
        # Fragmentation Method
        activation_layout = QHBoxLayout()
        activation_layout.addWidget(QLabel("Activation method:"))
        activation_combo = QComboBox()
        activation_combo.addItems(["CID", "ETD", "HCD", "UVPD"])
        self.args.set_toppic_config_option('activation', 'CID')
        activation_combo.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('activation', text)
        )
        activation_layout.addWidget(activation_combo)
        self.ui['toppic']['activation'] = activation_combo

        # Modification Settings
        fixed_mod_layout = QHBoxLayout()
        fixed_mod_layout.addWidget(QLabel("Fixed modification:"))
        fixed_mod_combo = QComboBox()
        fixed_mod_combo.addItems(["Custom", "C57", "C58"])
        self.args.set_toppic_config_option('fixed_mod', 'Custom')
        fixed_mod_combo.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('fixed_mod', text)
        )
        fixed_mod_layout.addWidget(fixed_mod_combo)
        self.ui['toppic']['fixed_mod'] = fixed_mod_combo

        fixed_mod_file_layout = QHBoxLayout()
        fixed_mod_file = QLineEdit()
        fixed_mod_file.textChanged.connect(
            lambda text: self.args.set_toppic_config_option('fixed_mod_file', text)
        )
        browse_fixed_mod = QPushButton("Browse")
        browse_fixed_mod.clicked.connect(
            lambda: self._browse_file(fixed_mod_file)
        )
        fixed_mod_file_layout.addWidget(fixed_mod_file)
        fixed_mod_file_layout.addWidget(browse_fixed_mod)
        self.ui['toppic']['fixed_mod_file'] = fixed_mod_file
        
        variable_ptm_layout = QHBoxLayout()
        variable_ptm_layout.addWidget(QLabel("Variable modification file:"))
        variable_ptm_file = QLineEdit()
        variable_ptm_file.textChanged.connect(
            lambda text: self.args.set_toppic_config_option('variable_ptm_file_name', text)
        )
        browse_variable_ptm = QPushButton("Browse")
        browse_variable_ptm.clicked.connect(
            lambda: self._browse_file(variable_ptm_file)
        )
        variable_ptm_layout.addWidget(variable_ptm_file)
        variable_ptm_layout.addWidget(browse_variable_ptm)
        self.ui['toppic']['variable_ptm_file_name'] = variable_ptm_file

        num_shift_layout = self._create_number_input("Max unexpected modifications:", "num_shift", 0, 2, 1, 'toppic')
        min_shift_layout = self._create_number_input("Min mass shift:", "min_shift", -2000, 0, -500, 'toppic', double=True)
        max_shift_layout = self._create_number_input("Max mass shift:", "max_shift", 0, 2000, 500, 'toppic', double=True)
        var_ptm_num_layout = self._create_number_input("Max variable modifications:", "variable_ptm_num", 0, 10, 3, 'toppic')
        
        layout.addLayout(activation_layout)
        layout.addLayout(fixed_mod_layout)
        layout.addLayout(fixed_mod_file_layout)
        layout.addLayout(variable_ptm_layout)
        layout.addLayout(num_shift_layout)
        layout.addLayout(min_shift_layout)
        layout.addLayout(max_shift_layout)
        layout.addLayout(var_ptm_num_layout)
        
        # Error Tolerance
        mass_error_layout = self._create_number_input("Mass error tolerance (PPM):","mass_error_tolerance", 1, 100, 10, 'toppic', double=True)
        proteoform_error_layout = self._create_number_input("Proteoform error tolerance (Da):","proteoform_error_tolerance", 0.1, 10.0, 1.2, 'toppic', double=True)

        layout.addLayout(activation_layout)
        layout.addLayout(fixed_mod_layout)
        layout.addLayout(fixed_mod_file_layout)
        layout.addLayout(variable_ptm_layout)
        layout.addLayout(num_shift_layout)
        layout.addLayout(min_shift_layout)
        layout.addLayout(max_shift_layout)
        layout.addLayout(var_ptm_num_layout)
        layout.addLayout(mass_error_layout)
        layout.addLayout(proteoform_error_layout)

        # Cutoff Settings
        spectrum_cutoff_layout = QHBoxLayout()
        spectrum_cutoff_layout.addWidget(QLabel("Spectrum-level cutoff:"))
        spectrum_type = QComboBox()
        spectrum_type.addItems(["EVALUE", "FDR"])   
        self.args.set_toppic_config_option('spectrum_cutoff_type', 'EVALUE')
        spectrum_type.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('spectrum_cutoff_type', text)
        )
        spectrum_cutoff_layout.addWidget(spectrum_type)
        self.ui['toppic']['spectrum_cutoff_type'] = spectrum_type
        
        spectrum_value_layout = self._create_number_input("Spectrum-level cutoff value:", "spectrum_cutoff_value", 0.0001, 1.0, 0.01, 'toppic', double=True)

        proteoform_cutoff_layout = QHBoxLayout()
        proteoform_cutoff_layout.addWidget(QLabel("Proteoform-level cutoff:"))
        proteoform_type = QComboBox()
        proteoform_type.addItems(["EVALUE", "FDR"])
        self.args.set_toppic_config_option('proteoform_cutoff_type', 'EVALUE')
        proteoform_type.currentTextChanged.connect(
            lambda text: self.args.set_toppic_config_option('proteoform_cutoff_type', text)
        )
        proteoform_cutoff_layout.addWidget(proteoform_type)
        self.ui['toppic']['proteoform_cutoff_type'] = proteoform_type
        
        proteoform_value_layout = self._create_number_input("Proteoform-level cutoff value:", "proteoform_cutoff_value", 0.0001, 1.0, 0.01, 'toppic', double=True)

        layout.addLayout(spectrum_cutoff_layout)
        layout.addLayout(spectrum_value_layout)
        layout.addLayout(proteoform_cutoff_layout)
        layout.addLayout(proteoform_value_layout)

        # Performance Settings
        thread_num_layout = self._create_number_input("Thread number:", "thread_number", 1, 32, 1, 'toppic')
        combined_spectra_layout = self._create_number_input("Number of combined spectra:", "num_combined_spectra", 1, 10, 1, 'toppic')

        approximate_layout = QHBoxLayout()
        approximate = QCheckBox("Use approximate spectra")
        self.args.set_toppic_config_option('approximate_spectra', False)
        approximate.stateChanged.connect(
            lambda state: self.args.set_toppic_config_option('approximate_spectra', bool(state))
        )
        approximate_layout.addWidget(approximate)
        self.ui['toppic']['approximate_spectra'] = approximate
        
        lookup_table_layout = QHBoxLayout()
        lookup_table = QCheckBox("Use lookup table")
        self.args.set_toppic_config_option('lookup_table', False)
        lookup_table.stateChanged.connect(
            lambda state: self.args.set_toppic_config_option('lookup_table', bool(state))
        )
        lookup_table_layout.addWidget(lookup_table)
        self.ui['toppic']['lookup_table'] = lookup_table

        layout.addLayout(thread_num_layout)
        layout.addLayout(combined_spectra_layout)
        layout.addLayout(approximate_layout)
        layout.addLayout(lookup_table_layout)

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
                
        # 将控件添加到UI字典中
        self.ui[group][arg] = spinbox
        
        layout.addWidget(spinbox)
        return layout

    def _browse_file(self, line_edit, file_type="All Files (*.*)"):
        filename, _ = QFileDialog.getOpenFileName(self, "选择文件", "", file_type)
        if filename:
            line_edit.setText(filename) 