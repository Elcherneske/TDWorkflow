import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid,GridOptionsBuilder
from .FileUtils import FileUtils
from .ServerUtils import ServerControl
from . import FeaturePage,ToppicPage

class ReportPage():
    def __init__(self):
        self.selected_file = None
        self.df = None

    def run(self):
        self.show_report_page()
        
    def show_report_page(self):
        with st.sidebar:
            file_utils = FileUtils()
            samples = file_utils.list_samples()
            st.session_state["sample"]=st.selectbox("选择检测样品",samples)
            selected_file = st.session_state["user_select_file"]   

        #首先直接启动toppic服务
        html_path = FileUtils.get_html_report_path()
        ServerControl.start_report_server(html_path)
        
        st.title("报告界面")
        feature_files = self._get_feature_files(st.session_state['user_select_file'])
        report_tab,feature_tab,toppic_tab = st.tabs(["主报告界面", "Featuremap", "TOPPIC结果"])
        
        with report_tab:
            self._count_report_files()
            if feature_files:
                self.selected_file = st.selectbox("选择特征文件", feature_files)
            self.df = pd.read_csv(self.selected_file, sep='\t')
            self._display_data_grid()
            
        with feature_tab:
            feature=FeaturePage.Featuremap()
            feature.run()

        with toppic_tab:
            toppic=ToppicPage.ToppicShowPage()
            toppic.run()
        
    def _get_feature_files(self, files_path):
        """获取用户目录下所有特征文件"""
        if not os.path.exists(files_path):
            return []
        return [
            os.path.join(files_path, f) 
            for f in os.listdir(files_path) 
            if f.endswith('.feature') or f.endswith('.FEATURE') 
        ]

    def _count_report_files(self):
        """统计HTML报告相关文件数量"""
        html_path = FileUtils.get_html_report_path()
        try:
            base_path = os.path.join(
                html_path,
                "toppic_proteoform_cutoff",
                "data_js"
            )
            target_folders = [
                ("proteins", "蛋白"),
                ("proteoforms", "变体"), 
                ("prsms", "特征")
            ]
            results = []
            for folder, display_name in target_folders:
                folder_path = os.path.join(base_path, folder)
                if os.path.exists(folder_path):
                    file_count = len([
                        f for f in os.listdir(folder_path) 
                        if os.path.isfile(os.path.join(folder_path, f))
                    ])
                    results.append(f" **{display_name}**: {file_count} 个")
                else:
                    results.append(f"⚠️ {display_name}目录不存在")
            st.markdown("__本样品共检测到:__")
            st.markdown("\n".join(results))
        except Exception as e:
            st.sidebar.error(f"文件统计失败: {str(e)}")
            
    def _display_data_grid(self):
        """配置AgGrid列显示"""
        st.markdown(f"**当前文件:**  `{os.path.basename(self.selected_file)}`")
        # 文件下载按钮
        csv_data = self.df.to_csv(index=False, sep='\t').encode('utf-8')
        st.download_button(
            label="📥 下载选中文件",
            data=csv_data,
            file_name=os.path.basename(self.selected_file),
            mime='text/csv',
            key='btn_download_feature'
        )
        default_columns = ['Mass','Monoisotopic_mass','Precursor_monoisotopic_mz' 'Apex_time', 'Intensity','Precursor_intensity']  # 示例列名
        grid_builder = GridOptionsBuilder.from_dataframe(self.df,enableValue=True,enableRowGroup=True,enablePivot=True)
        for col in self.df.columns:
            grid_builder.configure_column(
                field=col,
                hide=col not in default_columns  # 关键配置
            )
        grid_builder.configure_side_bar(
            filters_panel=True,
            columns_panel=True
        )
        AgGrid(
            self.df, 
            enable_enterprise_modules=True,
            gridOptions=grid_builder.build(),
            height=500,
            theme='streamlit',
            custom_css={
                ".ag-header-cell-label": {"justify-content": "center"},
                ".ag-cell": {"display": "flex", "align-items": "center"}
            },
            key='aggrid_feature_show'
        )
        st.markdown(
            '''其他的数据被隐藏起来了,点击`columns`侧边栏即可找到
            后续进一步开发作图组件
            ''')
