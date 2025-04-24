import os
import streamlit as st
import pandas as pd
from Args import Args 

class FileUtils:
    """_summary_
    文件查询工具,用于统一维护文件查询路径
    可以查询用户名下对应的文件地址

    """
    
    @staticmethod
    def list_samples():
        selected_path = st.session_state['user_select_file']
        samples = []
        if not os.path.exists(selected_path):
            raise FileNotFoundError(f"路径不存在: {selected_path}")
        for filename in os.listdir(selected_path):
            if filename.endswith("ms1.feature"):
                sample_name = filename.rsplit("_ms1.feature", 1)[0]
                samples.append(sample_name)
        return samples

    @staticmethod
    def get_html_report_path():
        selected_path = st.session_state['user_select_file']
        sample_name = st.session_state['sample']

        target_suffix = f"{sample_name}_html"
        for filename in os.listdir(selected_path):
            if filename.endswith(target_suffix):
                return os.path.join(selected_path, filename)
        raise FileNotFoundError(f"未找到HTML报告文件: {target_suffix}")
    
    @staticmethod
    def get_file_path(suffix):
        selected_path = st.session_state['user_select_file']
        sample_name = st.session_state['sample']

        target_suffix = f"{sample_name}{suffix}"
        for filename in os.listdir(selected_path):
            if filename.endswith(target_suffix):
                return os.path.join(selected_path, filename)
        raise FileNotFoundError(f"未找到指定后缀文件: {target_suffix}")






