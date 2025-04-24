from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                            QLabel, QLineEdit, QComboBox, QCheckBox, 
                            QScrollArea, QPushButton, QSpinBox, QDoubleSpinBox,
                            QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from .Setting import Setting

class InformedProteomicsConfigTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        # 用于保存所有UI控件
        self.ui = {
            'pbfgen': {},
            'promex': {},
            'mspathfinder': {}
        }
        self._init_ui()
    
    def check(self) -> bool:
        return True
    
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
        
        # 添加三个主要配置组
        scroll_layout.addWidget(self._create_pbfgen_group())
        scroll_layout.addWidget(self._create_promex_group())
        scroll_layout.addWidget(self._create_mspathfinder_group())
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def _create_pbfgen_group(self):
        group = QGroupBox("PbfGen Configuration")
        layout = QVBoxLayout()
        
        # 扫描范围设置
        start_scan_layout = self._create_number_input("Start scan number:", "start_scan", -1, 999999, -1, "pbfgen")
        end_scan_layout = self._create_number_input("End scan number:", "end_scan", -1, 999999, -1, "pbfgen")
        
        # 参数文件设置
        param_file_layout = QHBoxLayout()
        param_file_layout.addWidget(QLabel("Parameter file:"))
        param_file_edit = QLineEdit()
        param_file_edit.setPlaceholderText("Please select the path of parameter file")
        param_file_edit.textChanged.connect(lambda text: self.args.set_pbfgen_config_option('ParamFile', text))
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self._browse_file(param_file_edit))
        param_file_layout.addWidget(param_file_edit)
        param_file_layout.addWidget(browse_btn)
        
        # 保存到UI字典
        self.ui['pbfgen']['ParamFile'] = param_file_edit
        
        layout.addLayout(start_scan_layout)
        layout.addLayout(end_scan_layout)
        layout.addLayout(param_file_layout)
        group.setLayout(layout)
        return group

    def _create_promex_group(self):
        group = QGroupBox("ProMex Configuration")
        layout = QVBoxLayout()
        
        # 电荷态范围
        min_charge_layout = self._create_number_input("Minimum charge:", "MinCharge", 1, 60, 1, "promex")
        max_charge_layout = self._create_number_input("Maximum charge:", "MaxCharge", 1, 99, 60, "promex")
        # 质量范围
        min_mass_layout = self._create_number_input("Minimum mass (Da):", "MinMass", 600, 100000, 2000, "promex")
        max_mass_layout = self._create_number_input("Maximum mass (Da):", "MaxMass", 600, 100000, 50000, "promex")
        # 其他参数
        score_threshold_layout = self._create_number_input("Score threshold:", "ScoreThreshold", -100, 100, -10, "promex", double=True)
        max_threads_layout = self._create_number_input("Max threads:", "MaxThreads", 0, 32, 0, "promex")
        
        # BinResPPM下拉框
        bin_res_layout = QHBoxLayout()
        bin_res_layout.addWidget(QLabel("Binning resolution (PPM):"))
        bin_res = QComboBox()
        bin_res.addItems(["1", "2", "4", "8", "16", "32", "64", "128"])
        bin_res.setCurrentText("16")  # 默认值
        bin_res.currentTextChanged.connect(lambda text: self.args.set_promex_config_option('BinResPPM', int(text)))
        bin_res_layout.addWidget(bin_res)
        
        # 保存到UI字典
        self.ui['promex']['BinResPPM'] = bin_res

        # 复选框选项
        feature_map = QCheckBox("Output feature heatmap")
        feature_map.setChecked(True)  # 默认选中
        self.args.set_promex_config_option('FeatureMap', True)
        feature_map.stateChanged.connect(lambda state: self.args.set_promex_config_option('FeatureMap', bool(state)))
        self.ui['promex']['FeatureMap'] = feature_map
        
        score = QCheckBox("Output extended scoring")
        score.setChecked(True)  # 默认选中
        self.args.set_promex_config_option('Score', True)
        score.stateChanged.connect(lambda state: self.args.set_promex_config_option('Score', bool(state)))        
        self.ui['promex']['Score'] = score

        csv = QCheckBox("Write feature data to CSV")
        csv.setChecked(True)  # 默认选中
        self.args.set_promex_config_option('csv', True)
        csv.stateChanged.connect(lambda state: self.args.set_promex_config_option('csv', bool(state)))
        self.ui['promex']['csv'] = csv

        # MS1FT文件
        ms1ft_layout = QHBoxLayout()
        ms1ft_layout.addWidget(QLabel("MS1FT file:"))
        ms1ft_edit = QLineEdit()
        ms1ft_edit.setPlaceholderText("Path to MS1FT file")
        ms1ft_edit.textChanged.connect(lambda text: self.args.set_promex_config_option('ms1ft', text))
        browse_ms1ft = QPushButton("Browse")
        browse_ms1ft.clicked.connect(lambda: self._browse_file(ms1ft_edit))
        ms1ft_layout.addWidget(ms1ft_edit)
        ms1ft_layout.addWidget(browse_ms1ft)
        self.ui['promex']['ms1ft'] = ms1ft_edit
        
        # ParamFile文件
        param_file_layout = QHBoxLayout()
        param_file_layout.addWidget(QLabel("Parameter file:"))
        param_file_edit = QLineEdit()
        param_file_edit.setPlaceholderText("Path to parameter file")
        param_file_edit.textChanged.connect(lambda text: self.args.set_promex_config_option('ParamFile', text))
        browse_param = QPushButton("Browse")
        browse_param.clicked.connect(lambda: self._browse_file(param_file_edit))
        param_file_layout.addWidget(param_file_edit)
        param_file_layout.addWidget(browse_param)
        self.ui['promex']['ParamFile'] = param_file_edit

        layout.addLayout(min_charge_layout)
        layout.addLayout(max_charge_layout)
        layout.addLayout(min_mass_layout)
        layout.addLayout(max_mass_layout)
        layout.addLayout(score_threshold_layout)
        layout.addLayout(max_threads_layout)
        layout.addLayout(bin_res_layout)
        layout.addWidget(feature_map)
        layout.addWidget(score)
        layout.addWidget(csv)
        layout.addLayout(ms1ft_layout)
        layout.addLayout(param_file_layout)
        
        group.setLayout(layout)
        return group

    def _create_mspathfinder_group(self):
        group = QGroupBox("MSPathFinder Configuration")
        layout = QVBoxLayout()
        
        # 搜索模式
        search_mode_layout = QHBoxLayout()
        search_mode_layout.addWidget(QLabel("Search Mode:"))
        search_mode = QComboBox()
        search_mode.addItems(["NoInternalCleavage", "SingleInternalCleavage", "MultipleInternalCleavages"])
        search_mode.setCurrentText("SingleInternalCleavage")
        search_mode.currentTextChanged.connect(lambda text: self.args.set_mspathfinder_config_option('ic', text))
        search_mode_layout.addWidget(search_mode)
        self.ui['mspathfinder']['ic'] = search_mode
        
        # 激活方法
        activation_layout = QHBoxLayout()
        activation_layout.addWidget(QLabel("Activation Method:"))
        activation = QComboBox()
        activation.addItems(["CID", "ETD", "HCD", "ECD", "PQD", "UVPD", "Unknown"])
        activation.setCurrentText("Unknown")
        activation.currentTextChanged.connect(lambda text: self.args.set_mspathfinder_config_option('ActivationMethod', text))
        activation_layout.addWidget(activation)
        self.ui['mspathfinder']['ActivationMethod'] = activation
        
        # 数值参数
        mem_matches_layout = self._create_number_input("Memory matches:", "MemMatches", 1, 100, 3, "mspathfinder")
        num_matches_layout = self._create_number_input("Matches per spectrum:", "NumMatchesPerSpec", 1, 100, 1, "mspathfinder")
        pmt_tolerance_layout = self._create_number_input("Precursor tolerance (PPM):", "PMTolerance", 0, 100, 10, "mspathfinder")
        frag_tolerance_layout = self._create_number_input("Fragment tolerance (PPM):", "FragTolerance", 0, 100, 10, "mspathfinder")
        # 序列长度范围
        min_length_layout = self._create_number_input("Minimum sequence length:", "MinLength", 0, 1000, 21, "mspathfinder")
        max_length_layout = self._create_number_input("Maximum sequence length:", "MaxLength", 0, 1000, 500, "mspathfinder")
        # 电荷态范围
        min_charge_layout = self._create_number_input("Minimum charge:", "MinCharge", 1, 99, 2, "mspathfinder")
        max_charge_layout = self._create_number_input("Maximum charge:", "MaxCharge", 1, 99, 50, "mspathfinder")
        min_frag_charge_layout = self._create_number_input("Minimum fragment charge:", "MinFragCharge", 1, 99, 1, "mspathfinder")
        max_frag_charge_layout = self._create_number_input("Maximum fragment charge:", "MaxFragCharge", 1, 99, 20, "mspathfinder")
        # 质量范围
        min_mass_layout = self._create_number_input("Minimum mass (Da):", "MinMass", 0, 100000, 3000, "mspathfinder")
        max_mass_layout = self._create_number_input("Maximum mass (Da):", "MaxMass", 0, 100000, 50000, "mspathfinder")
        # 线程数
        thread_count_layout = self._create_number_input("Maximum number of threads (0 for automatic):", "ThreadCount", 0, 100, 0, "mspathfinder")

        # 复选框选项
        tag_search = QCheckBox("Include Tag-based Search")
        tag_search.setChecked(True)  # 默认选中
        self.args.set_mspathfinder_config_option('TagSearch', True)
        tag_search.stateChanged.connect(lambda state: self.args.set_mspathfinder_config_option('TagSearch', bool(state)))
        self.ui['mspathfinder']['TagSearch'] = tag_search
        
        include_decoys = QCheckBox("Include decoy results")
        include_decoys.setChecked(False)  # 默认不包含
        self.args.set_mspathfinder_config_option('IncludeDecoys', False)
        include_decoys.stateChanged.connect(lambda state: self.args.set_mspathfinder_config_option('IncludeDecoys', bool(state)))
        self.ui['mspathfinder']['IncludeDecoys'] = include_decoys

        use_flip_scoring = QCheckBox("Use FLIP scoring")
        use_flip_scoring.setChecked(False)  # 默认不使用
        self.args.set_mspathfinder_config_option('UseFlipScoring', False)
        use_flip_scoring.stateChanged.connect(lambda state: self.args.set_mspathfinder_config_option('UseFlipScoring', bool(state)))
        self.ui['mspathfinder']['UseFlipScoring'] = use_flip_scoring

        tda_checkbox = QCheckBox("Search decoy database")
        tda_checkbox.setChecked(False)  # 默认不搜索
        self.args.set_mspathfinder_config_option('tda', 0)
        tda_checkbox.stateChanged.connect(lambda state: self.args.set_mspathfinder_config_option('tda', 1 if state else 0))
        self.ui['mspathfinder']['tda'] = tda_checkbox

        overwrite_checkbox = QCheckBox("Overwrite existing results")
        overwrite_checkbox.setChecked(False)  # 默认不覆盖
        self.args.set_mspathfinder_config_option('overwrite', False)
        overwrite_checkbox.stateChanged.connect(lambda state: self.args.set_mspathfinder_config_option('overwrite', bool(state)))
        self.ui['mspathfinder']['overwrite'] = overwrite_checkbox

        # 文件选择
        mod_file_layout = QHBoxLayout()
        mod_file_layout.addWidget(QLabel("Modification file:"))
        mod_file_edit = QLineEdit()
        mod_file_edit.setPlaceholderText("Please select the path of modification file")
        mod_file_edit.textChanged.connect(lambda text: self.args.set_mspathfinder_config_option('ModificationFile', text))
        browse_mod = QPushButton("Browse")
        browse_mod.clicked.connect(lambda: self._browse_file(mod_file_edit))
        mod_file_layout.addWidget(mod_file_edit)
        mod_file_layout.addWidget(browse_mod)
        self.ui['mspathfinder']['ModificationFile'] = mod_file_edit
        
        feature_file_layout = QHBoxLayout()
        feature_file_layout.addWidget(QLabel("Feature file:"))
        feature_file_edit = QLineEdit()
        feature_file_edit.setPlaceholderText("Please select the path of feature file")
        feature_file_edit.textChanged.connect(lambda text: self.args.set_mspathfinder_config_option('FeatureFile', text))
        browse_feature = QPushButton("Browse")
        browse_feature.clicked.connect(lambda: self._browse_file(feature_file_edit))
        feature_file_layout.addWidget(feature_file_edit)
        feature_file_layout.addWidget(browse_feature)
        self.ui['mspathfinder']['FeatureFile'] = feature_file_edit

        scans_file_layout = QHBoxLayout()
        scans_file_layout.addWidget(QLabel("Scans file:"))
        scans_file_edit = QLineEdit()
        scans_file_edit.setPlaceholderText("Please select the path of scans file")
        scans_file_edit.textChanged.connect(lambda text: self.args.set_mspathfinder_config_option('ScansFilePath', text))
        browse_scans = QPushButton("Browse")
        browse_scans.clicked.connect(lambda: self._browse_file(scans_file_edit))
        scans_file_layout.addWidget(scans_file_edit)
        scans_file_layout.addWidget(browse_scans)
        self.ui['mspathfinder']['ScansFile'] = scans_file_edit

        param_file_layout = QHBoxLayout()
        param_file_layout.addWidget(QLabel("Parameter file:"))
        param_file_edit = QLineEdit()
        param_file_edit.setPlaceholderText("Please select the path of parameter file")
        param_file_edit.textChanged.connect(lambda text: self.args.set_mspathfinder_config_option('ParamFile', text))
        browse_param = QPushButton("Browse")
        browse_param.clicked.connect(lambda: self._browse_file(param_file_edit))
        param_file_layout.addWidget(param_file_edit)
        param_file_layout.addWidget(browse_param)
        self.ui['mspathfinder']['ParamFile'] = param_file_edit
        
        # 添加所有组件到布局
        layout.addLayout(search_mode_layout)
        layout.addLayout(activation_layout)
        layout.addLayout(mem_matches_layout)
        layout.addLayout(num_matches_layout)
        layout.addLayout(pmt_tolerance_layout)
        layout.addLayout(frag_tolerance_layout)
        layout.addLayout(min_length_layout)
        layout.addLayout(max_length_layout)
        layout.addLayout(min_charge_layout)
        layout.addLayout(max_charge_layout)
        layout.addLayout(min_frag_charge_layout)
        layout.addLayout(max_frag_charge_layout)
        layout.addLayout(min_mass_layout)
        layout.addLayout(max_mass_layout)
        layout.addLayout(thread_count_layout)
        layout.addWidget(tag_search)
        layout.addWidget(include_decoys)
        layout.addWidget(use_flip_scoring)
        layout.addWidget(tda_checkbox)
        layout.addWidget(overwrite_checkbox)
        layout.addLayout(mod_file_layout)
        layout.addLayout(feature_file_layout)
        layout.addLayout(scans_file_layout)
        layout.addLayout(param_file_layout)
        
        group.setLayout(layout)
        return group

    def _create_number_input(self, label, arg, min_val, max_val, default, group, double=False):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        
        if double:
            spinbox = QDoubleSpinBox()
            spinbox.setDecimals(4)
            spinbox.setRange(float(min_val), float(max_val))
            spinbox.setValue(float(default))
            if group == "promex":
                self.args.set_promex_config_option(arg, float(default))
                spinbox.valueChanged.connect(
                    lambda value: self.args.set_promex_config_option(arg, float(value))
                )
            elif group == "pbfgen":
                self.args.set_pbfgen_config_option(arg, float(default))
                spinbox.valueChanged.connect(
                    lambda value: self.args.set_pbfgen_config_option(arg, float(value))
                )
            elif group == "mspathfinder":
                self.args.set_mspathfinder_config_option(arg, float(default))
                spinbox.valueChanged.connect(
                    lambda value: self.args.set_mspathfinder_config_option(arg, float(value))
                )
        else:
            spinbox = QSpinBox()
            spinbox.setRange(int(min_val), int(max_val))
            spinbox.setValue(int(default))
            if group == "promex":
                self.args.set_promex_config_option(arg, int(default))
                spinbox.valueChanged.connect(
                    lambda value: self.args.set_promex_config_option(arg, int(value))
                )
            elif group == "pbfgen":
                self.args.set_pbfgen_config_option(arg, int(default))
                spinbox.valueChanged.connect(
                    lambda value: self.args.set_pbfgen_config_option(arg, int(value))
                )
            elif group == "mspathfinder":
                self.args.set_mspathfinder_config_option(arg, int(default))
                spinbox.valueChanged.connect(
                    lambda value: self.args.set_mspathfinder_config_option(arg, int(value))
                )
        layout.addWidget(spinbox)
        # 将控件添加到UI字典中
        self.ui[group][arg] = spinbox

        return layout

    def _browse_file(self, line_edit, file_type="All Files (*.*)"):
        filename, _ = QFileDialog.getOpenFileName(self, "Select file", "", file_type)
        if filename:
            line_edit.setText(filename)

    def _save_settings(self):
        """保存当前设置到文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存InformedProteomics设置", "", "设置文件 (*.ini);;所有文件 (*)"
        )
        
        if not file_path:
            QMessageBox.information(self, "错误", "未选择保存路径！")
            return
            
        try:
            # 从self.ui收集当前设置
            settings = {
                'pbfgen': self._collect_pbfgen_settings(),
                'promex': self._collect_promex_settings(),
                'mspathfinder': self._collect_mspathfinder_settings()
            }
            
            # 使用Setting类保存设置
            Setting.save(file_path, settings)
            QMessageBox.information(self, "成功", "设置已成功保存！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置失败: {str(e)}")
    
    def _collect_pbfgen_settings(self):
        """收集PbfGen设置"""
        settings = {}
        for key, widget in self.ui['pbfgen'].items():
            if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                settings[key] = str(widget.value())
            elif isinstance(widget, QLineEdit):
                settings[key] = widget.text()
            elif isinstance(widget, QComboBox):
                settings[key] = widget.currentText()
            elif isinstance(widget, QCheckBox):
                settings[key] = str(widget.isChecked())
        return settings
    
    def _collect_promex_settings(self):
        """收集ProMex设置"""
        settings = {}
        for key, widget in self.ui['promex'].items():
            if isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
                settings[key] = str(widget.value())
            elif isinstance(widget, QLineEdit):
                settings[key] = widget.text()
            elif isinstance(widget, QComboBox):
                settings[key] = widget.currentText()
            elif isinstance(widget, QCheckBox):
                settings[key] = str(widget.isChecked())
        return settings
    
    def _collect_mspathfinder_settings(self):
        """收集MSPathFinder设置"""
        settings = {}
        for key, widget in self.ui['mspathfinder'].items():
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
            self, "加载InformedProteomics设置", "", "设置文件 (*.ini);;所有文件 (*)"
        )
        
        if not file_path:
            QMessageBox.information(self, "错误", "未选择加载路径！")
            return
            
        try:
            # 创建Setting实例加载配置
            setting_instance = Setting(file_path)
            
            # 更新PbfGen设置
            self._update_pbfgen_settings(setting_instance)
            
            # 更新ProMex设置
            self._update_promex_settings(setting_instance)
            
            # 更新MSPathFinder设置
            self._update_mspathfinder_settings(setting_instance)
            
            QMessageBox.information(self, "成功", "设置已成功加载！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载设置失败: {str(e)}")
    
    def _update_pbfgen_settings(self, setting_instance):
        """从配置更新PbfGen设置"""
        for key, widget in self.ui['pbfgen'].items():
            value = setting_instance.get('pbfgen', key)
            if value:
                if isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                    self.args.set_pbfgen_config_option(key, int(value))
                elif isinstance(widget, QDoubleSpinBox):
                    widget.setValue(float(value))
                    self.args.set_pbfgen_config_option(key, float(value))
                elif isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_pbfgen_config_option(key, value)
                elif isinstance(widget, QComboBox):
                    widget.setCurrentText(value)
                    self.args.set_pbfgen_config_option(key, value)
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(value.lower() == 'true')
                    self.args.set_pbfgen_config_option(key, value.lower() == 'true')
            else:
                if isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_pbfgen_config_option(key, value)
    
    def _update_promex_settings(self, setting_instance):
        """从配置更新ProMex设置"""
        for key, widget in self.ui['promex'].items():
            value = setting_instance.get('promex', key)
            if value:
                if isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                    self.args.set_promex_config_option(key, int(value))
                elif isinstance(widget, QDoubleSpinBox):
                    widget.setValue(float(value))
                    self.args.set_promex_config_option(key, float(value))
                elif isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_promex_config_option(key, value)
                elif isinstance(widget, QComboBox):
                    widget.setCurrentText(value)
                    self.args.set_promex_config_option(key, value)
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(value.lower() == 'true')
                    self.args.set_promex_config_option(key, value.lower() == 'true')
            else:
                if isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_promex_config_option(key, value)
    
    def _update_mspathfinder_settings(self, setting_instance):
        """从配置更新MSPathFinder设置"""
        for key, widget in self.ui['mspathfinder'].items():
            value = setting_instance.get('mspathfinder', key)
            if value:
                if isinstance(widget, QSpinBox):
                    widget.setValue(int(value))
                    self.args.set_mspathfinder_config_option(key, int(value))
                elif isinstance(widget, QDoubleSpinBox):
                    widget.setValue(float(value))
                    self.args.set_mspathfinder_config_option(key, float(value))
                elif isinstance(widget, QLineEdit):
                    widget.setText(value)
                    self.args.set_mspathfinder_config_option(key, value)
                elif isinstance(widget, QComboBox):
                    widget.setCurrentText(value)
                    self.args.set_mspathfinder_config_option(key, value)
                elif isinstance(widget, QCheckBox):
                    widget.setChecked(value.lower() == 'true')
                    self.args.set_mspathfinder_config_option(key, value.lower() == 'true')
                else:
                    if isinstance(widget, QLineEdit):
                        widget.setText(value)
                        self.args.set_mspathfinder_config_option(key, value)

