from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                            QLabel, QLineEdit, QComboBox, QCheckBox, 
                            QScrollArea, QPushButton, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt
from .Setting import Setting

class InformedProteomicsConfigTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.setting = Setting()
        self._init_ui()
    
    def check(self) -> bool:
        return True
    
    def _init_ui(self):
        # 创建主布局
        main_layout = QVBoxLayout()
        
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
        start_scan = self._create_number_input("Start scan number:", "start_scan", -1, 999999, -1, "pbfgen")
        end_scan = self._create_number_input("End scan number:", "end_scan", -1, 999999, -1, "pbfgen")
        
        # 参数文件设置
        param_file_layout = QHBoxLayout()
        param_file_layout.addWidget(QLabel("Parameter file:"))
        param_file_edit = QLineEdit()
        param_file_edit.setPlaceholderText("Please select the path of parameter file")
        param_file_edit.textChanged.connect(lambda text: self.args.set_mspathfinder_config_option('ParamFile', text))
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self._browse_file(param_file_edit))
        param_file_layout.addWidget(param_file_edit)
        param_file_layout.addWidget(browse_btn)
        
        layout.addLayout(start_scan)
        layout.addLayout(end_scan)
        layout.addLayout(param_file_layout)
        group.setLayout(layout)
        return group

    def _create_promex_group(self):
        group = QGroupBox("ProMex Configuration")
        layout = QVBoxLayout()
        
        # 电荷态范围
        min_charge = self._create_number_input("Minimum charge:", "MinCharge", 1, 60, 1, "promex")
        max_charge = self._create_number_input("Maximum charge:", "MaxCharge", 1, 99, 60, "promex")
        
        # 质量范围
        min_mass = self._create_number_input("Minimum mass (Da):", "MinMass", 600, 100000, 2000, "promex")
        max_mass = self._create_number_input("Maximum mass (Da):", "MaxMass", 600, 100000, 50000, "promex")
        
        # 其他参数
        score_threshold = self._create_number_input("Score threshold:", "ScoreThreshold", -100, 100, -10, "promex", double=True)
        max_threads = self._create_number_input("Max threads:", "MaxThreads", 0, 32, 0, "promex")
        
        bin_res = QComboBox()
        bin_res.addItems(["1", "2", "4", "8", "16", "32", "64", "128"])
        bin_res.setCurrentText("16")  # 默认值
        bin_res.currentTextChanged.connect(lambda text: self.args.set_promex_config_option('BinResPPM', int(text)))

        # 复选框选项
        feature_map = QCheckBox("Output feature heatmap")
        self.args.set_promex_config_option('FeatureMap', False)
        feature_map.stateChanged.connect(lambda state: self.args.set_promex_config_option('FeatureMap', bool(state)))
        
        score = QCheckBox("Output extended scoring")
        self.args.set_promex_config_option('Score', False)
        score.stateChanged.connect(lambda state: self.args.set_promex_config_option('Score', bool(state)))        

        csv = QCheckBox("Write feature data to CSV")
        self.args.set_promex_config_option('csv', False)
        csv.stateChanged.connect(lambda state: self.args.set_promex_config_option('csv', bool(state)))

        layout.addLayout(min_charge)
        layout.addLayout(max_charge)
        layout.addLayout(min_mass)
        layout.addLayout(max_mass)
        layout.addLayout(score_threshold)
        layout.addLayout(max_threads)
        layout.addWidget(bin_res)
        layout.addWidget(feature_map)
        layout.addWidget(score)
        layout.addWidget(csv)
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
        
        # 激活方法
        activation_layout = QHBoxLayout()
        activation_layout.addWidget(QLabel("Activation Method:"))
        activation = QComboBox()
        activation.addItems(["CID", "ETD", "HCD", "ECD", "PQD", "UVPD", "Unknown"])
        activation.setCurrentText("Unknown")
        activation.currentTextChanged.connect(lambda text: self.args.set_mspathfinder_config_option('ActivationMethod', text))
        activation_layout.addWidget(activation)
        
        # 数值参数
        mem_matches = self._create_number_input("Memory matches:", "MemMatches", 1, 100, 3, "mspathfinder")
        num_matches = self._create_number_input("Matches per spectrum:", "NumMatchesPerSpec", 1, 100, 1, "mspathfinder")
        pmt_tolerance = self._create_number_input("Precursor tolerance (PPM):", "PMTolerance", 0, 100, 10, "mspathfinder")
        frag_tolerance = self._create_number_input("Fragment tolerance (PPM):", "FragTolerance", 0, 100, 10, "mspathfinder")
        
        # 序列长度范围
        min_length = self._create_number_input("Minimum sequence length:", "MinLength", 0, 1000, 21, "mspathfinder")
        max_length = self._create_number_input("Maximum sequence length:", "MaxLength", 0, 1000, 500, "mspathfinder")
        
        # 电荷态范围
        min_charge = self._create_number_input("Minimum charge:", "MinCharge", 1, 99, 2, "mspathfinder")
        max_charge = self._create_number_input("Maximum charge:", "MaxCharge", 1, 99, 50, "mspathfinder")
        min_frag_charge = self._create_number_input("Minimum fragment charge:", "MinFragCharge", 1, 99, 1, "mspathfinder")
        max_frag_charge = self._create_number_input("Maximum fragment charge:", "MaxFragCharge", 1, 99, 20, "mspathfinder")
        
        # 质量范围
        min_mass = self._create_number_input("Minimum mass (Da):", "MinMass", 0, 100000, 3000, "mspathfinder")
        max_mass = self._create_number_input("Maximum mass (Da):", "MaxMass", 0, 100000, 50000, "mspathfinder")

        thread_count = self._create_number_input("Maximum number of threads (0 for automatic):", "ThreadCount", 0, 100, 0, "mspathfinder")

        # 复选框选项
        tag_search = QCheckBox("Include Tag-based Search")
        tag_search.setChecked(False)
        self.args.set_mspathfinder_config_option('TagSearch', False)  # Default value
        tag_search.stateChanged.connect(lambda state: self.args.set_mspathfinder_config_option('TagSearch', bool(state)))
        
        include_decoys = QCheckBox("Include decoy results")
        include_decoys.setChecked(False)  # 默认不包含
        self.args.set_mspathfinder_config_option('IncludeDecoys', False)
        include_decoys.stateChanged.connect(lambda state: self.args.set_mspathfinder_config_option('IncludeDecoys', bool(state)))        

        use_flip_scoring = QCheckBox("Use FLIP scoring")
        use_flip_scoring.setChecked(False)  # 默认不使用
        self.args.set_mspathfinder_config_option('UseFlipScoring', False)
        use_flip_scoring.stateChanged.connect(lambda state: self.args.set_mspathfinder_config_option('UseFlipScoring', bool(state)))        

        tda_checkbox = QCheckBox("Search decoy database:")
        tda_checkbox.setChecked(False)  # 默认不搜索
        self.args.set_mspathfinder_config_option('tda', False)
        tda_checkbox.stateChanged.connect(lambda state: self.args.set_mspathfinder_config_option('tda', bool(state)))        

        overwrite_checkbox = QCheckBox("Overwrite existing results:")
        overwrite_checkbox.setChecked(False)  # 默认不覆盖
        self.args.set_mspathfinder_config_option('overwrite', False)
        overwrite_checkbox.stateChanged.connect(lambda state: self.args.set_mspathfinder_config_option('overwrite', bool(state)))

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
        
        feature_file_layout = QHBoxLayout()
        feature_file_layout.addWidget(QLabel("Feature file:"))
        feature_file_edit = QLineEdit()
        feature_file_edit.setPlaceholderText("Please select the path of feature file")
        feature_file_edit.textChanged.connect(lambda text: self.args.set_mspathfinder_config_option('FeatureFile', text))
        browse_feature = QPushButton("Browse")
        browse_feature.clicked.connect(lambda: self._browse_file(feature_file_edit))
        feature_file_layout.addWidget(feature_file_edit)
        feature_file_layout.addWidget(browse_feature)

        scans_file_layout = QHBoxLayout()
        scans_file_layout.addWidget(QLabel("Scans file:"))
        scans_file_edit = QLineEdit()
        scans_file_edit.setPlaceholderText("Please select the path of scans file")
        scans_file_edit.textChanged.connect(lambda text: self.args.set_mspathfinder_config_option('ScansFilePath', text))
        browse_scans = QPushButton("Browse")
        browse_scans.clicked.connect(lambda: self._browse_file(scans_file_edit))
        scans_file_layout.addWidget(scans_file_edit)
        scans_file_layout.addWidget(browse_scans)

        param_file_layout = QHBoxLayout()
        param_file_layout.addWidget(QLabel("Parameter file:"))
        param_file_edit = QLineEdit()
        param_file_edit.setPlaceholderText("Please select the path of parameter file")
        param_file_edit.textChanged.connect(lambda text: self.args.set_mspathfinder_config_option('ParamFile', text))
        browse_param = QPushButton("Browse")
        browse_param.clicked.connect(lambda: self._browse_file(param_file_edit))
        param_file_layout.addWidget(param_file_edit)
        param_file_layout.addWidget(browse_param)
        
        # 添加所有组件到布局
        layout.addLayout(search_mode_layout)
        layout.addLayout(activation_layout)
        layout.addLayout(mem_matches)
        layout.addLayout(num_matches)
        layout.addLayout(pmt_tolerance)
        layout.addLayout(frag_tolerance)
        layout.addLayout(min_length)
        layout.addLayout(max_length)
        layout.addLayout(min_charge)
        layout.addLayout(max_charge)
        layout.addLayout(min_frag_charge)
        layout.addLayout(max_frag_charge)
        layout.addLayout(min_mass)
        layout.addLayout(max_mass)
        layout.addLayout(thread_count)
        layout.addWidget(tag_search)
        layout.addWidget(include_decoys)
        layout.addWidget(use_flip_scoring)
        layout.addWidget(tda_checkbox)
        layout.addWidget(overwrite_checkbox)
        layout.addLayout(mod_file_layout)
        layout.addLayout(feature_file_layout)        

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
        return layout

    def _browse_file(self, line_edit, file_type="All Files (*.*)"):
        from PyQt5.QtWidgets import QFileDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Select file", "", file_type)
        if filename:
            line_edit.setText(filename)
