from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                            QGroupBox, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog)
from .Setting import ToolsSetting
import os
import io
import re
import datetime
class RunTab(QWidget):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.setting = ToolsSetting()
        self.output_text = None
        self.run_button = None
        self.stop_button = None
        self.vis_button = None
        
        self.log_file = None
        self.log_buffer = io.StringIO()
        self.buffer_size = 0
        self.last_progress_line = ""
        self._init_ui()
    
    def check(self) -> bool:
        if not self.args.get_output_dir():
            print("输出路径为空，请选择有效的路径。")
            return False
        return True

    def _is_progress_line(self, text):
        # progress_pattern = re.compile(r'Processing MS\d+ spectrum scan \d+ \.\.\.\s+\d+% finished\.\s*[\r\n]*')
        # return progress_pattern.match(text.strip()) is not None
        if "Processing MS" in text and "finished" in text and "spectrum scan" in text:
            return True
        return False

    def update_output(self, text):
        # Check if current text is a progress update
        if self._is_progress_line(text):
            cursor = self.output_text.textCursor()
            cursor.movePosition(cursor.End)
            cursor.movePosition(cursor.PreviousCharacter)  # Move cursor one line up
            cursor.movePosition(cursor.StartOfLine)
            cursor.movePosition(cursor.PreviousCharacter)  # Move cursor one line up
            cursor.movePosition(cursor.End, cursor.KeepAnchor)
            last_line = cursor.selectedText()
            # If the last line is also a progress update, replace it
            if self._is_progress_line(last_line):
                cursor.removeSelectedText()
                # No need to move the cursor as it's already at the right position
            else:
                # Move cursor back to end for appending
                cursor.movePosition(cursor.End)
                self.output_text.setTextCursor(cursor)
        
        # Now append the text
        self.output_text.append(text)
        
        # Handle log file writing
        if self.args.get_output_dir():
            if self.log_file is None:
                # 使用当前时间创建日志文件名
                current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                log_filename = f"{current_time}_log.txt"
                log_path = os.path.join(self.args.get_output_dir(), log_filename)
                try:
                    self.log_file = open(log_path, 'a', encoding='utf-8')
                except (IOError, OSError) as e:
                    print(f"Error opening log file: {e}")
                    return
            
            self.log_buffer.write(text + "\n")
            self.buffer_size += len(text) + 1 
            if self.buffer_size >= 4096:
                self._flush_log_buffer()
        else:
            raise ValueError("Output directory is not set")
        
        if text == "============Process finished============" or text == "Process has been interrupted.":
            self._flush_log_buffer()
            if self.log_file:
                self.log_file.close()
                self.log_file = None
        
    def _flush_log_buffer(self):
        """Flush the log buffer to the log file"""
        if self.log_file and self.buffer_size > 0:
            try:
                self.log_file.write(self.log_buffer.getvalue())
                self.log_file.flush()
                self.log_buffer = io.StringIO()  # Reset buffer
                self.buffer_size = 0
            except (IOError, OSError) as e:
                print(f"Error writing to log file: {e}")
    
    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_output_group())
        layout.addWidget(self._create_run_button())
        layout.addWidget(self._create_stop_button())
        layout.addWidget(self._create_vis_button())
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

    def _create_stop_button(self):
        group = QGroupBox("Stop")
        layout = QHBoxLayout()
        self.stop_btn = QPushButton("Stop")
        layout.addWidget(QLabel("Stop Button:"))
        layout.addWidget(self.stop_btn)
        group.setLayout(layout)
        return group

    def _create_vis_button(self):
        group = QGroupBox("Visualization")
        layout = QHBoxLayout()
        self.vis_btn = QPushButton("Visualization")
        layout.addWidget(QLabel("Visualization Button:"))
        layout.addWidget(self.vis_btn)
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