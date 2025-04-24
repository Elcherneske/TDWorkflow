import streamlit as st
from Args import Args
from FunctionPages.ReportPage import ReportPage

class MainPage():
    def __init__(self):
        self.args = Args().args

    def run(self):
        self.init_session_state()
        self.show_main_page()     
        
    def init_session_state(self):
        # 仅在状态不存在时初始化，防止被刷新覆盖
        if 'user_select_file' not in st.session_state:
            st.session_state['user_select_file'] = self.args.file_path
        st.session_state['sample'] = None

    def show_main_page(self):
        if st.session_state['user_select_file']:
            ReportPage().run()

if __name__ == "__main__":
    main_page = MainPage()
    main_page.run()