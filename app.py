import functions as funcs
from pandas_profiling import profile_report
from pathlib import Path
from PIL import Image
import streamlit as st
from streamlit_pandas_profiling import st_profile_report

############################# Environment Variables ###################################
FILEPATH = Path(__file__).parent
IMAGEPATH = Path(FILEPATH / 'images')

####################################### App ###########################################
logo = Image.open((IMAGEPATH / 'logo.png').resolve().as_posix())


def main():
    # Header
    st.set_page_config(page_title="Data Profiler",
                       page_icon=logo,
                       layout="wide",
                       initial_sidebar_state="auto")
    st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 100%;
        padding-top: 0rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 0rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )
    title = "🔎 Data Profiler 🔍"
    background_color = "#950808"
    font_color = "#FFFFFF"
    st.markdown(
        f'<p style="text-align:center;background-image: linear-gradient(to right,{background_color}, {background_color});color:{font_color};font-family:sans-serif;font-size:42px;font-weight:bold;">{title}</p>',
        unsafe_allow_html=True)
    
    # explainer
    with st.expander("App Usage"):
        st.write("""
            This is an app made to quickly explore a tabular dataset using Streamlit. It provides a view of the data in the shape of a pandas DataFrame while also providing basic statistics on the quality of the dataset.
            
            Additionally, it allows to generate a detailed report on the data of each column and their interactions using Pandas Profiling.
            
            Currently, it supports only CSV, XLS and XLSX files.
            
            To get started, drag a file or browse your local drive and select a file and click the "Upload 📤" button. If there is an issue reading an XLSX or XLS file, try converting it to CSV.
        """)

    # file uploader
    with st.form(key='upload'):
        uploaded_file = st.file_uploader("Upload a file",
                                         type=['csv', 'xlsx', 'xls'],
                                         accept_multiple_files=False)

        report = st.checkbox(
            label='Generate analytics report',
            value=True,
            help=
            'Depending on file size, the report can take a long time to complete.'
        )
        submitted = st.form_submit_button('Upload 📤')

    if submitted:
        # data upload
        if uploaded_file is not None:
            uploaded_file.seek(0)
            data = funcs.get_data(uploaded_file)

        # Dataset statistics
        with st.container():
            col4, col5, col6, col7, col8, col9 = st.columns(6)
            stats = funcs.stats(data)
            config = {'displayModeBar': False, 'responsive': False}
            with col4:
                st.plotly_chart(funcs.indicator_int(stats, 'Rows'),
                                use_container_width=True,
                                **{'config': config})
            with col5:
                st.plotly_chart(funcs.indicator_int(stats, 'Columns'),
                                use_container_width=True,
                                **{'config': config})
            with col6:
                st.plotly_chart(funcs.indicator_int(stats, 'Empty Cells'),
                                use_container_width=True,
                                **{'config': config})

            with col7:
                st.plotly_chart(funcs.indicator_perc(stats, '% Empty Cells'),
                                use_container_width=True,
                                **{'config': config})
            with col8:
                st.plotly_chart(funcs.indicator_int(stats, 'Duplicate Rows'),
                                use_container_width=True,
                                **{'config': config})
            with col9:
                st.plotly_chart(funcs.indicator_perc(stats,
                                                     '% Duplicate Rows'),
                                use_container_width=True,
                                **{'config': config})

        with st.container():
            st.dataframe(
                data=data,  #.style.set_sticky(axis=1),
                width=None,
                height=600)

        # Pandas Profiling Report
        if report:
            st.header('📊 Analytics Report')
            with st.container():
                pr = data.profile_report(
                    title=f"",
                    progress_bar=True,
                    config_file=(
                        FILEPATH /
                        'pandas_profiling_config.yml').resolve().as_posix())

                st_profile_report(pr, height=1000)


if __name__ == '__main__':
    main()
