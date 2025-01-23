from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
from abc import abstractmethod

class BaseWorkflow(QThread):
    # 定义信号用于向GUI发送输出
    output_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.commands = []

    @abstractmethod
    def prepare_workflow(self):
        """准备工作流程，子类必须实现此方法来设置commands"""
        pass
        
    def run(self):
        self.prepare_workflow()
        for command in self.commands:
            self.output_received.emit("command: " + ' '.join(command))
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output_received.emit(output.strip())
        self.output_received.emit("============Process finished============")

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("输出窗口")
            self.setGeometry(100, 100, 600, 400)

            self.text_edit = QTextEdit(self)
            self.text_edit.setReadOnly(True)

            layout = QVBoxLayout()
            layout.addWidget(self.text_edit)

            container = QWidget()
            container.setLayout(layout)
            self.setCentralWidget(container)

        def print_output(self, output):
            self.text_edit.append(f"收到的输出: {output}")

    app = QApplication(sys.argv)
    window = MainWindow()

    command = ["python", "test.py"]
    worker = BaseWorkflow()
    worker.commands = [command]
    worker.output_received.connect(window.print_output)
    worker.start()

    window.show()
    sys.exit(app.exec_())
