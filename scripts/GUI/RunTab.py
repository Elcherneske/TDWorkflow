from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                            QGroupBox, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog)
from .Setting import Setting

class RunTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.setting = Setting()
        self.output_text = None
        self.run_button = None
        self._init_ui()
    
    def update_output(self, text):
        self.output_text.append(text)
        # 检查行数并保持最多1000行
        if self.output_text.document().blockCount() > 1000:
            cursor = self.output_text.textCursor()
            cursor.movePosition(cursor.Start)
            cursor.movePosition(cursor.Down, cursor.MoveAnchor, 1)  # 移动到第二行
            cursor.movePosition(cursor.End, cursor.KeepAnchor)  # 选中所有内容
            cursor.removeSelectedText()  # 删除选中的内容
            cursor.deleteChar()  # 删除选中的换行符
            self.output_text.setTextCursor(cursor)
    
    def check(self) -> bool:
        if not self.args.get_output_dir():
            print("输出路径为空，请选择有效的路径。")
            return False
        return True
    
    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_output_group())
        layout.addWidget(self._create_run_button())
        layout.addWidget(self._create_output_text())
        self.setLayout(layout)
    
    def _create_output_group(self):
        group = QGroupBox("Output setting")
        layout = QHBoxLayout()
        output_path = QLineEdit()
        if self.setting.get_config('Output', 'output_dir'):
            output_path.setText(self.setting.get_config('Output', 'output_dir'))
            self.args.set_output_dir(self.setting.get_config('Output', 'output_dir'))
        else:
            output_path.setPlaceholderText("Please select the path of output directory")
        output_path.textChanged.connect(lambda text: (self.setting.set_config('Output', 'output_dir', text), self.args.set_output_dir(text)))
        browse_btn = QPushButton("browse")
        browse_btn.clicked.connect(lambda: self._browse_directory(output_path))
        
        layout.addWidget(QLabel("output path:"))
        layout.addWidget(output_path)
        layout.addWidget(browse_btn)
        group.setLayout(layout)
        return group

    def _create_run_button(self):
        group = QGroupBox("Run")
        layout = QHBoxLayout()
        self.run_btn = QPushButton("Run")
        
        layout.addWidget(QLabel("Run Button:"))
        layout.addWidget(self.run_btn)
        group.setLayout(layout)
        return group
    
    def _create_output_text(self):
        group = QGroupBox("Output Log")
        layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        
        layout.addWidget(self.output_text)
        group.setLayout(layout)
        return group
    
    def _browse_directory(self, output_path):
        directory = QFileDialog.getExistingDirectory(self, "select output directory")
        if directory:
            output_path.setText(directory)
            self.setting.set_config('Output', 'output_dir', directory)
            self.args.set_output_dir(directory)