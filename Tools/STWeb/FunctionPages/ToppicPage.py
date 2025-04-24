import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder
from .FileUtils import FileUtils  
from .ServerUtils import ServerControl


class ToppicShowPage():
    def __init__(self):
        # 定义文件后缀映射
        self.file_suffixes = {
            "Proteoform (Single)": "_ms2_toppic_proteoform_single.tsv",
            "Proteoform": "_ms2_toppic_proteoform.tsv",
            "PrSM": "_ms2_toppic_prsm.tsv",
            "PrSM (Single)": "_ms2_toppic_prsm_single.tsv"
        }
        
        # 配置各文件类型默认显示的列
        self.default_columns = {
            "_ms2_toppic_proteoform_single.tsv": ['Prsm ID', 'Precursor mass', 'Retention time','Fixed PTMs'],
            "_ms2_toppic_proteoform.tsv": ['Proteoform ID', 'Protein name', 'Mass'],
            "_ms2_toppic_prsm.tsv": ['PrSM ID', 'E-value', 'Score'],
            "_ms2_toppic_prsm_single.tsv": ['Feature ID', 'Sequence', 'Modifications']
        }
    def run(self):
        self.show_toppic()

    def _get_toppic_files(self):
        """扫描用户目录获取所有TOPPIC文件"""
        base_path = st.session_state['user_select_file']
        if not base_path or not os.path.exists(base_path):
            return None
        
        # 获取目录下所有文件
        all_files = os.listdir(base_path)

        file_map = {}
        for filename in all_files:
            for suffix in self.file_suffixes.values():
                file_map[suffix] = FileUtils.get_file_path(suffix)
        return file_map

    def show_toppic(self):
        report_path=FileUtils.get_html_report_path() 
        file_map = self._get_toppic_files()
        col=st.columns(2)
        with col[0]:
            st.write("**详细文件查看**")
            st.write("请在`columns`侧边栏中选择您需要查看的列")
        with col[1]:
            if st.button("📑 打开Toppic报告"):
                self._display_toppic_report(report_path)
        tabs = st.tabs([f"📊 {display_name}" for display_name in self.file_suffixes.keys()])
        for idx, (display_name, suffix) in enumerate(self.file_suffixes.items()):
             with tabs[idx]:
                if suffix in file_map:
                    self._display_tab_content(file_map[suffix], suffix)
                else:
                    st.warning(f"⚠️ 目录中未找到 {suffix} 类型的文件")

    def _display_toppic_report(self, report_path):
        try:
            server_url = ServerControl.get_url()
            st.markdown(f"[IPv4访问地址]({server_url})")
        except Exception as e:
            st.error(f"服务器启动失败: {str(e)}")

    def _display_tab_content(self, file_path, suffix):
        df = pd.read_csv(file_path,sep='\t',skiprows=37)
        filename = os.path.basename(file_path)
            
        try:
            row_count = df.shape[0]
            st.markdown(f"✈ **表格条目数：** `{row_count:,}` 条")
            # 文件下载功能
            self._create_download_button(df, filename)
            
            # 表格显示配置
            self._configure_aggrid(df, suffix, filename)
        except Exception as e:
            st.error(f"加载 {filename} 失败: {str(e)}")

    def _create_download_button(self, df, filename):
        """创建下载按钮组件"""
        csv_data = df.to_csv(index=False, sep='\t').encode('utf-8')
        st.download_button(
            label=f"📥 下载 {filename}",
            data=csv_data,
            file_name=filename,
            mime='text/tab-separated-values',
            key=f'download_{filename}'
        )

    def _configure_aggrid(self, df, suffix, filename):
        """配置AgGrid表格显示"""
        default_cols = self.default_columns[suffix]
        grid_builder = GridOptionsBuilder.from_dataframe(df,enableValue=True,enableRowGroup=True,enablePivot=True)
        for col in df.columns:
            grid_builder.configure_column(
                field=col,
                hide=col not in default_cols
            )
            
        grid_builder.configure_side_bar(
            filters_panel=True, 
            columns_panel=True
        )
        # 渲染表格
        AgGrid(
            df,
            gridOptions=grid_builder.build(),
            height=500,
            theme='streamlit',
            enable_enterprise_modules=True,
            custom_css={
                ".ag-header-cell-label": {"justify-content": "center"},
                ".ag-cell": {"display": "flex", "align-items": "center"}
            },
            key=f"grid_{filename}"
        )