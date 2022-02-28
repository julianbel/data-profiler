from pandas import read_csv  #, read_excel
from pandas.io.excel import read_excel
import plotly.graph_objects as go
import streamlit as st


@st.cache(show_spinner=True)
def get_data(file):
    """
    Returns a dataframe built from the data in the uploaded image.
    
    ------
    Params
    ------
    
        file [Engine]: None or UploadedFile (subclass of BytesIO).
    
    ------
    Returns
    ------
    
        df [pandas.DataFrame]
    
    """

    engine = {'xlsx': 'openpyxl', 'xls': 'xlrd'}

    ext = file.name.split('.')[-1]

    if ext == 'csv':
        df = read_csv(file)

    else:
        df = read_excel(file, sheet_name=0, engine=engine[ext])

    for col in df.columns:
        try:
            df[col] = df[col].str.replace(',', '.').astype('float64')
        except:
            continue

    return df


def stats(dataframe):
    """
    Generates the following statistics:
        - Number of rows.
        - Number of columns.
        - Number of Empty Cells.
        - Percentage of Empty Cells.
        - Number of duplicate rows.
        - Percentage of duplicate rows.
    
    ------
    Params
    ------
        
        dataframe [pandas.DataFrame]: dataframe with data from uploaded file.
    
    ------
    Returns
    ------
    
        stats_dict [dict]: dictionary with metric name (key) and calculated value.
    
    """
    rows_num = dataframe.shape[0]
    cols_num = dataframe.shape[1]
    null_num = dataframe.isnull().sum().sum()
    null_perc = dataframe.isnull().sum().sum() / (rows_num * cols_num)
    dups_num = dataframe.duplicated().sum()
    dups_perc = dataframe.duplicated().sum() / rows_num

    stats_dict = {
        'Rows': rows_num,
        'Columns': cols_num,
        'Empty Cells': null_num,
        '% Empty Cells': null_perc,
        'Duplicate Rows': dups_num,
        '% Duplicate Rows': dups_perc
    }

    return stats_dict


def indicator_int(stats_dict, kpi):
    """
    Generates a Plotly Indicator to visualize an integer.
    
    ------
    Params
    ------
    
        stats_dict [dict]: dictionary with metric name (key) and calculated value.
        kpi [string]: metric name.
    
    ------
    Returns
    ------

        fig [FigureWidget]: Plotly Indicator with value as integer and metric name.
        
    """
    fig = go.Figure(
        go.Indicator(mode="number",
                     value=stats_dict[kpi],
                     number={"font": {
                         "size": 65
                     }},
                     title={"text": kpi},
                     domain={
                         'x': [0, 1],
                         'y': [0, 1]
                     }))
    fig.update_layout(autosize=False,
                      width=500,
                      height=200,
                      margin=dict(l=10, r=10, b=0, t=10, pad=1))
    return fig


def indicator_perc(stats_dict, kpi):
    """
    Generates a Plotly Indicator to visualize a percentage.
    
    ------
    Params
    ------
    
        stats_dict [dict]: dictionary with metric name (key) and calculated value.
        kpi [string]: metric name.
    
    ------
    Returns
    ------
    
        fig [FigureWidget]: Plotly Indicator with value as a percentage and metric name.
    
    """
    fig = go.Figure(
        go.Indicator(mode="number",
                     value=stats_dict[kpi] * 100,
                     number={
                         "valueformat": ".1f",
                         "suffix": "%",
                         "font": {
                             "size": 65
                         }
                     },
                     title={"text": kpi},
                     domain={
                         'x': [0, 1],
                         'y': [0, 1]
                     }))
    fig.update_layout(autosize=False,
                      width=500,
                      height=200,
                      margin=dict(l=10, r=10, b=0, t=10, pad=1))
    return fig
