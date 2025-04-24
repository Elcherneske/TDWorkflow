import argparse

class Args:
    def __init__(self):
        parser = self.init_arg_parser()
        self.args = parser.parse_args()  # 修正参数解析逻辑
        self.file_path = self.args.file_path

    def init_arg_parser(self):
        parser = argparse.ArgumentParser()
        # 添加类型提示和帮助说明
        parser.add_argument('--file_path', 
                          type=str,
                          default=r"D:\desktop\ZJU_CHEM\TDVis\files\user_test\100ngQC-ETDHCD",
                          help="质谱数据文件路径")
        return parser
