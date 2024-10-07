


import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import math
from io import BytesIO
import zipfile
import altair as alt
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from fpdf import FPDF
from PIL import Image
import tempfile
import altair_saver
from selenium import webdriver


def remove_solo_values(lst):
    if len(lst) < 2:
        return lst  # If the list is too short, return as is

    result = []
    
    # Iterate through the list and check neighbors
    for i in range(len(lst)):
        if (i > 0 and lst[i] == lst[i-1] + 1) or (i < len(lst)-1 and lst[i] == lst[i+1] - 1):
            result.append(lst[i])

    return result
def merge_dicts_with_zero_values(dict_list):
    all_keys = set()
    for d in dict_list:
        all_keys.update(d.keys())
    merged_dicts = []
    for d in dict_list:
        new_dict = {key: 0 for key in all_keys}
        new_dict.update(d)
        merged_dicts.append(new_dict)

    return merged_dicts
def convert_input_state(inp):

    # Convert keys to lowercase for material_type
    material_input = {k.lower(): v for k, v in inp["material_type"].items()}

    # Convert keys to lowercase for product_type
    product_input = {k.lower(): v for k, v in inp["product_type"].items()}

    # No change needed for ni_plating_time
    nickel_input = inp["ni_plating_time"]

    # Aggregate all inputs into a list
    inpu = [material_input, product_input, nickel_input]
    return inpu
def plot_nt_pt(inp):
    inp=st.session_state.input_state
    nt = st.session_state.nt 
    pt = st.session_state.pt 
    plot_data_nt_pt=[]
    for i in list(inp[1].keys()):
        if inp[1][i]==False:
            continue
        else:
            for j in list(inp[2].keys()):
                if inp[2][j]==False:
                    continue
                else:
                    rh=[]
                    for k in range(len(pt[i])):
                        if list(pt[i]["BATCH ID"])[k] in list(nt[j]['BATCH ID']):
                            rh.append(list(pt[i]["RH mins"])[k])
                    if len(rh)==0:
                        rh_avg=0
                        rh_avg=0
                        rh_max=0
                        rh_min=0
                        batches=0
                    else:
                        rh_avg=sum(rh)/len(rh)
                        rh_max=max(rh)
                        rh_min=min(rh)
                        batches=len(rh)
                    plot_data_nt_pt.append([str(j),str(i),round(rh_avg,2),round(rh_max,2),round(rh_min,2),batches])   
    I_data=[x for x in plot_data_nt_pt if x[0]=="I_series"]
    II_data=[x for x in plot_data_nt_pt if x[0]=="II_series"]
    III_data=[x for x in plot_data_nt_pt if x[0]=="III_series"]
    if len(I_data)!=0 and len(II_data)!=0 and len(III_data)!=0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "RH Time": [x[2] for x in I_data],
            "Average RH Time": [x[2] for x in I_data],
            "Max RH Time": [x[3] for x in I_data],
            "Min RH Time": [x[4] for x in I_data],
            "Number of Batches": [x[5] for x in I_data]
        })
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "RH Time": [x[2] for x in II_data],
            "Average RH Time": [x[2] for x in II_data],
            "Max RH Time": [x[3] for x in II_data],
            "Min RH Time": [x[4] for x in II_data],
            "Number of Batches": [x[5] for x in II_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "RH Time": [x[2] for x in III_data],
            "Average RH Time": [x[2] for x in III_data],
            "Max RH Time": [x[3] for x in III_data],
            "Min RH Time": [x[4] for x in III_data],
            "Number of Batches": [x[5] for x in III_data]
        })

        dfm = pd.concat([d_I,d_II, d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(RH Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'II_data','III_data'], range=['#990040', '#ff0030','#ffaa30'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")

    elif len(I_data)!=0 and len(II_data)==0 and len(III_data)!=0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "RH Time": [x[2] for x in I_data],
            "Average RH Time": [x[2] for x in I_data],
            "Max RH Time": [x[3] for x in I_data],
            "Min RH Time": [x[4] for x in I_data],
            "Number of Batches": [x[5] for x in I_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "RH Time": [x[2] for x in III_data],
            "Average RH Time": [x[2] for x in III_data],
            "Max RH Time": [x[3] for x in III_data],
            "Min RH Time": [x[4] for x in III_data],
            "Number of Batches": [x[5] for x in III_data]
        })

        dfm = pd.concat([d_I,d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(RH Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'III_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    
    elif len(I_data)!=0 and len(II_data)!=0 and len(III_data)==0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "RH Time": [x[2] for x in I_data],
            "Average RH Time": [x[2] for x in I_data],
            "Max RH Time": [x[3] for x in I_data],
            "Min RH Time": [x[4] for x in I_data],
            "Number of Batches": [x[5] for x in I_data]
        })
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "RH Time": [x[2] for x in II_data],
            "Average RH Time": [x[2] for x in II_data],
            "Max RH Time": [x[3] for x in II_data],
            "Min RH Time": [x[4] for x in II_data],
            "Number of Batches": [x[5] for x in II_data]
        })

        dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(RH Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'II_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)!=0 and len(III_data)!=0:
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "RH Time": [x[2] for x in II_data],
            "Average RH Time": [x[2] for x in II_data],
            "Max RH Time": [x[3] for x in II_data],
            "Min RH Time": [x[4] for x in II_data],
            "Number of Batches": [x[5] for x in II_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "RH Time": [x[2] for x in III_data],
            "Average RH Time": [x[2] for x in III_data],
            "Max RH Time": [x[3] for x in III_data],
            "Min RH Time": [x[4] for x in III_data],
            "Number of Batches": [x[5] for x in III_data]
        })

        dfm = pd.concat([d_II,d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(RH Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['II_data', 'III_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)!=0 and len(II_data)==0 and len(III_data)==0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "RH Time": [x[2] for x in I_data],
            "Average RH Time": [x[2] for x in I_data],
            "Max RH Time": [x[3] for x in I_data],
            "Min RH Time": [x[4] for x in I_data],
            "Number of Batches": [x[5] for x in I_data]
        })

        #dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(d_I).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(RH Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)!=0 and len(III_data)==0:
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "RH Time": [x[2] for x in II_data],
            "Average RH Time": [x[2] for x in II_data],
            "Max RH Time": [x[3] for x in II_data],
            "Min RH Time": [x[4] for x in II_data],
            "Number of Batches": [x[5] for x in II_data]
        })

        #dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(d_II).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(RH Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['II_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)==0 and len(III_data)!=0:
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "RH Time": [x[2] for x in III_data],
            "Average RH Time": [x[2] for x in III_data],
            "Max RH Time": [x[3] for x in III_data],
            "Min RH Time": [x[4] for x in III_data],
            "Number of Batches": [x[5] for x in III_data]
        })

        chart = alt.Chart(d_III).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(RH Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['III_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_nt_pt_II(inp):
    inp=st.session_state.input_state
    nt = st.session_state.nt 
    pt = st.session_state.pt 
    plot_data_nt_pt=[]
    for i in list(inp[1].keys()):
        if inp[1][i]==False:
            continue
        else:
            for j in list(inp[2].keys()):
                if inp[2][j]==False:
                    continue
                else:
                    rh=[]
                    for k in range(len(pt[i])):
                        if list(pt[i]["BATCH ID"])[k] in list(nt[j]['BATCH ID']):
                            rh.append(list(pt[i]["H_II mins"])[k])
                    if len(rh)==0:
                        rh_avg=0
                        rh_avg=0
                        rh_max=0
                        rh_min=0
                        batches=0
                    else:
                        rh_avg=sum(rh)/len(rh)
                        rh_max=max(rh)
                        rh_min=min(rh)
                        batches=len(rh)
                    plot_data_nt_pt.append([str(j),str(i),round(rh_avg,2),round(rh_max,2),round(rh_min,2),batches])   
    I_data=[x for x in plot_data_nt_pt if x[0]=="I_series"]
    II_data=[x for x in plot_data_nt_pt if x[0]=="II_series"]
    III_data=[x for x in plot_data_nt_pt if x[0]=="III_series"]
    if len(I_data)!=0 and len(II_data)!=0 and len(III_data)!=0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "H_II Time": [x[2] for x in I_data],
            "Average H_II Time": [x[2] for x in I_data],
            "Max H_II Time": [x[3] for x in I_data],
            "Min H_II Time": [x[4] for x in I_data],
            "Number of Batches": [x[5] for x in I_data]
        })
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "H_II Time": [x[2] for x in II_data],
            "Average H_II Time": [x[2] for x in II_data],
            "Max H_II Time": [x[3] for x in II_data],
            "Min H_II Time": [x[4] for x in II_data],
            "Number of Batches": [x[5] for x in II_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "H_II Time": [x[2] for x in III_data],
            "Average H_II Time": [x[2] for x in III_data],
            "Max H_II Time": [x[3] for x in III_data],
            "Min H_II Time": [x[4] for x in III_data],
            "Number of Batches": [x[5] for x in III_data]
        })

        dfm = pd.concat([d_I,d_II, d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(H_II Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'II_data','III_data'], range=['#990040', '#ff0030','#ffaa30'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")

    elif len(I_data)!=0 and len(II_data)==0 and len(III_data)!=0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "H_II Time": [x[2] for x in I_data],
            "Average H_II Time": [x[2] for x in I_data],
            "Max H_II Time": [x[3] for x in I_data],
            "Min H_II Time": [x[4] for x in I_data],
            "Number of Batches": [x[5] for x in I_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "H_II Time": [x[2] for x in III_data],
            "Average H_II Time": [x[2] for x in III_data],
            "Max H_II Time": [x[3] for x in III_data],
            "Min H_II Time": [x[4] for x in III_data],
            "Number of Batches": [x[5] for x in III_data]
        })

        dfm = pd.concat([d_I,d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(H_II Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'III_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    
    elif len(I_data)!=0 and len(II_data)!=0 and len(III_data)==0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "H_II Time": [x[2] for x in I_data],
            "Average H_II Time": [x[2] for x in I_data],
            "Max H_II Time": [x[3] for x in I_data],
            "Min H_II Time": [x[4] for x in I_data],
            "Number of Batches": [x[5] for x in I_data]
        })
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "H_II Time": [x[2] for x in II_data],
            "Average H_II Time": [x[2] for x in II_data],
            "Max H_II Time": [x[3] for x in II_data],
            "Min H_II Time": [x[4] for x in II_data],
            "Number of Batches": [x[5] for x in II_data]
        })

        dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(H_II Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'II_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)!=0 and len(III_data)!=0:
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "H_II Time": [x[2] for x in II_data],
            "Average H_II Time": [x[2] for x in II_data],
            "Max H_II Time": [x[3] for x in II_data],
            "Min H_II Time": [x[4] for x in II_data],
            "Number of Batches": [x[5] for x in II_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "H_II Time": [x[2] for x in III_data],
            "Average H_II Time": [x[2] for x in III_data],
            "Max H_II Time": [x[3] for x in III_data],
            "Min H_II Time": [x[4] for x in III_data],
            "Number of Batches": [x[5] for x in III_data]
        })

        dfm = pd.concat([d_II,d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(H_II Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['II_data', 'III_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)!=0 and len(II_data)==0 and len(III_data)==0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "H_II Time": [x[2] for x in I_data],
            "Average H_II Time": [x[2] for x in I_data],
            "Max H_II Time": [x[3] for x in I_data],
            "Min H_II Time": [x[4] for x in I_data],
            "Number of Batches": [x[5] for x in I_data]
        })

        #dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(d_I).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(H_II Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)!=0 and len(III_data)==0:
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "H_II Time": [x[2] for x in II_data],
            "Average H_II Time": [x[2] for x in II_data],
            "Max H_II Time": [x[3] for x in II_data],
            "Min H_II Time": [x[4] for x in II_data],
            "Number of Batches": [x[5] for x in II_data]
        })

        #dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(d_II).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(H_II Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['II_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)==0 and len(III_data)!=0:
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "H_II Time": [x[2] for x in III_data],
            "Average H_II Time": [x[2] for x in III_data],
            "Max H_II Time": [x[3] for x in III_data],
            "Min H_II Time": [x[4] for x in III_data],
            "Number of Batches": [x[5] for x in III_data]
        })

        chart = alt.Chart(d_III).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='sum(H_II Time):Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['III_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_nt_pt_glow(inp):
    inp=st.session_state.input_state
    nt = st.session_state.nt 
    pt = st.session_state.pt 
    plot_data_nt_pt=[]
    for i in list(inp[1].keys()):
        if inp[1][i]==False:
            continue
        else:
            for j in list(inp[2].keys()):
                if inp[2][j]==False:
                    continue
                else:
                    count=[]
                    for k in range(len(pt[i])):
                        if list(pt[i]["BATCH ID"])[k] in list(nt[j]['BATCH ID']):
                            count.append(1)
                    batches=len(count)
                    plot_data_nt_pt.append([str(j),str(i),batches])   
    I_data=[x for x in plot_data_nt_pt if x[0]=="I_series"]
    II_data=[x for x in plot_data_nt_pt if x[0]=="II_series"]
    III_data=[x for x in plot_data_nt_pt if x[0]=="III_series"]
    if len(I_data)!=0 and len(II_data)!=0 and len(III_data)!=0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "Batches": [x[2] for x in I_data]
        })
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "Batches": [x[2] for x in II_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "Batches": [x[2] for x in III_data]
        })

        dfm = pd.concat([d_I,d_II, d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'II_data','III_data'], range=['#990040', '#ff0030','#ffaa30'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")

    elif len(I_data)!=0 and len(II_data)==0 and len(III_data)!=0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "Batches": [x[2] for x in I_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "Batches": [x[2] for x in III_data]
        })

        dfm = pd.concat([d_I,d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'III_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    
    elif len(I_data)!=0 and len(II_data)!=0 and len(III_data)==0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "Batches": [x[2] for x in I_data]
        })
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "Batches": [x[2] for x in II_data]
        })

        dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'II_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)!=0 and len(III_data)!=0:
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "Batches": [x[2] for x in II_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "Batches": [x[2] for x in III_data]
        })

        dfm = pd.concat([d_II,d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['II_data', 'III_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)!=0 and len(II_data)==0 and len(III_data)==0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "Batches": [x[2] for x in I_data]
        })

        #dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(d_I).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)!=0 and len(III_data)==0:
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "Batches": [x[2] for x in II_data]
        })

        #dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(d_II).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['II_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)==0 and len(III_data)!=0:
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "Batches": [x[2] for x in III_data]
        })

        chart = alt.Chart(d_III).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['III_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_nt_pt_ac(inp):
    inp=st.session_state.input_state
    nt = st.session_state.nt 
    pt = st.session_state.pt 
    plot_data_nt_pt=[]
    for i in list(inp[1].keys()):
        if inp[1][i]==False:
            continue
        else:
            for j in list(inp[2].keys()):
                if inp[2][j]==False:
                    continue
                else:
                    count=[]
                    for k in range(len(pt[i])):
                        if list(pt[i]["BATCH ID"])[k] in list(nt[j]['BATCH ID']):
                            count.append(1)
                    batches=len(count)
                    plot_data_nt_pt.append([str(j),str(i),batches])   
    I_data=[x for x in plot_data_nt_pt if x[0]=="I_series"]
    II_data=[x for x in plot_data_nt_pt if x[0]=="II_series"]
    III_data=[x for x in plot_data_nt_pt if x[0]=="III_series"]
    if len(I_data)!=0 and len(II_data)!=0 and len(III_data)!=0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "Batches": [x[2] for x in I_data]
        })
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "Batches": [x[2] for x in II_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "Batches": [x[2] for x in III_data]
        })

        dfm = pd.concat([d_I,d_II, d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'II_data','III_data'], range=['#990040', '#ff0030','#ffaa30'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")

    elif len(I_data)!=0 and len(II_data)==0 and len(III_data)!=0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "Batches": [x[2] for x in I_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "Batches": [x[2] for x in III_data]
        })

        dfm = pd.concat([d_I,d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'III_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    
    elif len(I_data)!=0 and len(II_data)!=0 and len(III_data)==0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "Batches": [x[2] for x in I_data]
        })
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "Batches": [x[2] for x in II_data]
        })

        dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data', 'II_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)!=0 and len(III_data)!=0:
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "Batches": [x[2] for x in II_data]
        })
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "Batches": [x[2] for x in III_data]
        })

        dfm = pd.concat([d_II,d_III], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['II_data', 'III_data'], range=['#990040', '#ff0030'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)!=0 and len(II_data)==0 and len(III_data)==0:
        d_I = pd.DataFrame({
            "Product Type": [x[1] for x in I_data],
            "Ni Plating Time": ["I_data"] * len(I_data),
            "Batches": [x[2] for x in I_data]
        })

        #dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(d_I).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['I_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)!=0 and len(III_data)==0:
        d_II = pd.DataFrame({
            "Product Type": [x[1] for x in II_data],
            "Ni Plating Time": ["II_data"] * len(II_data),
            "Batches": [x[2] for x in II_data]
        })

        #dfm = pd.concat([d_I,d_II], ignore_index=True)

        chart = alt.Chart(d_II).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['II_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(I_data)==0 and len(II_data)==0 and len(III_data)!=0:
        d_III = pd.DataFrame({
            "Product Type": [x[1] for x in III_data],
            "Ni Plating Time": ["III_data"] * len(III_data),
            "Batches": [x[2] for x in III_data]
        })

        chart = alt.Chart(d_III).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Ni Plating Time:N', scale=alt.Scale(domain=['III_data'], range=['#990040'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=50,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_mt_nt(inp):
    inp=st.session_state.input_state
    nt = st.session_state.nt 
    mt = st.session_state.mt 
    plot_data_mt_nt=[]
    for i in list(inp[2].keys()):
        if inp[2][i]==False:
            continue
        else:
            for j in list(inp[0].keys()):
                if inp[0][j]==False:
                    continue
                else:
                    rh=[]
                    for k in range(len(nt[i])):
                        if list(nt[i]["BATCH ID"])[k] in list(mt[j]['BATCH ID']):
                            rh.append(list(nt[i]["RH mins"])[k])
                    if len(rh)==0:
                        rh_avg=0
                        rh_max=0
                        rh_min=0
                        batches=0
                    else:
                        rh_avg=sum(rh)/len(rh)
                        rh_max=max(rh)
                        rh_min=min(rh)
                        batches=len(rh)
                    plot_data_mt_nt.append([str(j),str(i),round(rh_avg,2),round(rh_max,2),round(rh_min,2),batches])
    brass_data=[x for x in plot_data_mt_nt if x[0]=="brass"]
    ss_data=[x for x in plot_data_mt_nt if x[0]=="ss"]
    if len(brass_data)!=0 and len(ss_data)!=0:
        d_brass = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in brass_data],
            "Material Type": ["Brass"] * len(brass_data),
            "RH Time": [x[2] for x in brass_data],
            "Average RH Time": [x[2] for x in brass_data],
            "Max RH Time": [x[3] for x in brass_data],
            "Min RH Time": [x[4] for x in brass_data],
            "Number of Batches": [x[5] for x in brass_data]
        })

        d_ss = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in ss_data],
            "Material Type": ["SS"] * len(ss_data),
            "RH Time": [x[2] for x in ss_data],
            "Average RH Time": [x[2] for x in ss_data],
            "Max RH Time": [x[3] for x in ss_data],
            "Min RH Time": [x[4] for x in ss_data],
            "Number of Batches": [x[5] for x in ss_data]
        })

        dfm = pd.concat([d_brass, d_ss], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Material Type:N', title=None, axis=None),
            y='sum(RH Time):Q',
            color=alt.Color('Material Type:N', scale=alt.Scale(domain=['Brass', 'SS'], range=['#a07000', '#888888'])),
            column=alt.Column('Ni Plating Time:O'),
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Material Type:N', title='Material Type'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=150,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")

    elif len(brass_data) == 0 and len(ss_data) != 0:

        d_ss = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in ss_data],
            "RH Time": [x[2] for x in ss_data],
            "Average RH Time": [x[2] for x in ss_data],
            "Max RH Time": [x[3] for x in ss_data],
            "Min RH Time": [x[4] for x in ss_data],
            "Number of Batches": [x[5] for x in ss_data]
        })

        chart = alt.Chart(d_ss).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title='Ni Plating Time'),
            y='sum(RH Time):Q',
            color=alt.value('#888888'),  # Set color for SS bars
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=400,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")

    elif len(brass_data) != 0 and len(ss_data) == 0:
        d_brass = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in brass_data],
            "RH Time": [x[2] for x in brass_data],
            "Average RH Time": [x[2] for x in brass_data],
            "Max RH Time": [x[3] for x in brass_data],
            "Min RH Time": [x[4] for x in brass_data],
            "Number of Batches": [x[5] for x in brass_data]
        })

        chart = alt.Chart(d_brass).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title='Ni Plating Time'),
            y='sum(RH Time):Q',
            color=alt.value('#a07000'),  # Set color for Brass bars
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=400,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_mt_nt_II(inp):
    inp=st.session_state.input_state
    nt = st.session_state.nt 
    mt = st.session_state.mt 
    plot_data_mt_nt=[]
    for i in list(inp[2].keys()):
        if inp[2][i]==False:
            continue
        else:
            for j in list(inp[0].keys()):
                if inp[0][j]==False:
                    continue
                else:
                    rh=[]
                    for k in range(len(nt[i])):
                        if list(nt[i]["BATCH ID"])[k] in list(mt[j]['BATCH ID']):
                            rh.append(list(nt[i]["H_II mins"])[k])
                    if len(rh)==0:
                        rh_avg=0
                        rh_max=0
                        rh_min=0
                        batches=0
                    else:
                        rh_avg=sum(rh)/len(rh)
                        rh_max=max(rh)
                        rh_min=min(rh)
                        batches=len(rh)
                    plot_data_mt_nt.append([str(j),str(i),round(rh_avg,2),round(rh_max,2),round(rh_min,2),batches])
    brass_data=[x for x in plot_data_mt_nt if x[0]=="brass"]
    ss_data=[x for x in plot_data_mt_nt if x[0]=="ss"]
    if len(brass_data)!=0 and len(ss_data)!=0:
        d_brass = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in brass_data],
            "Material Type": ["Brass"] * len(brass_data),
            "H_II Time": [x[2] for x in brass_data],
            "Average H_II Time": [x[2] for x in brass_data],
            "Max H_II Time": [x[3] for x in brass_data],
            "Min H_II Time": [x[4] for x in brass_data],
            "Number of Batches": [x[5] for x in brass_data]
        })

        d_ss = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in ss_data],
            "Material Type": ["SS"] * len(ss_data),
            "H_II Time": [x[2] for x in ss_data],
            "Average H_II Time": [x[2] for x in ss_data],
            "Max H_II Time": [x[3] for x in ss_data],
            "Min H_II Time": [x[4] for x in ss_data],
            "Number of Batches": [x[5] for x in ss_data]
        })

        dfm = pd.concat([d_brass, d_ss], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Material Type:N', title=None, axis=None),
            y='sum(H_II Time):Q',
            color=alt.Color('Material Type:N', scale=alt.Scale(domain=['Brass', 'SS'], range=['#a07000', '#888888'])),
            column=alt.Column('Ni Plating Time:O'),
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Material Type:N', title='Material Type'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=150,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_mt_nt_glow(inp):
    inp=st.session_state.input_state
    nt = st.session_state.nt 
    mt = st.session_state.mt 
    plot_data_mt_nt=[]
    for i in list(inp[2].keys()):
        if inp[2][i]==False:
            continue
        else:
            for j in list(inp[0].keys()):
                if inp[0][j]==False:
                    continue
                else:
                    count=[]
                    for k in range(len(nt[i])):
                        if list(nt[i]["BATCH ID"])[k] in list(mt[j]['BATCH ID']):
                            count.append(1)
                    batches=len(count)
                    plot_data_mt_nt.append([str(j),str(i),batches])
    brass_data=[x for x in plot_data_mt_nt if x[0]=="brass"]
    ss_data=[x for x in plot_data_mt_nt if x[0]=="ss"]
    if len(brass_data)!=0 and len(ss_data)!=0:
        d_brass = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in brass_data],
            "Material Type": ["Brass"] * len(brass_data),
            "Batches": [x[2] for x in brass_data]
        })

        d_ss = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in ss_data],
            "Material Type": ["SS"] * len(ss_data),
            "Batches": [x[2] for x in ss_data]
        })

        dfm = pd.concat([d_brass, d_ss], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Material Type:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Material Type:N', scale=alt.Scale(domain=['Brass', 'SS'], range=['#a07000', '#888888'])),
            column=alt.Column('Ni Plating Time:O'),
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Material Type:N', title='Material Type'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=150,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(brass_data) == 0 and len(ss_data) != 0:

        d_ss = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in ss_data],
            "Material Type": ["SS"] * len(ss_data),
            "Batches": [x[2] for x in ss_data]
        })

        chart = alt.Chart(d_ss).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title='Ni Plating Time'),
            y='Batches:Q',
            color=alt.value('#888888'),  # Set color for SS bars
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=400,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")

    elif len(brass_data) != 0 and len(ss_data) == 0:
        d_brass = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in brass_data],
            "Material Type": ["Brass"] * len(brass_data),
            "Batches": [x[2] for x in brass_data]
        })

        chart = alt.Chart(d_brass).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title='Ni Plating Time'),
            y='Batches:Q',
            color=alt.value('#a07000'),  # Set color for Brass bars
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=400,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_mt_nt_ac(inp):
    inp=st.session_state.input_state
    nt = st.session_state.nt 
    mt = st.session_state.mt 
    plot_data_mt_nt=[]
    for i in list(inp[2].keys()):
        if inp[2][i]==False:
            continue
        else:
            for j in list(inp[0].keys()):
                if inp[0][j]==False:
                    continue
                else:
                    count=[]
                    for k in range(len(nt[i])):
                        if list(nt[i]["BATCH ID"])[k] in list(mt[j]['BATCH ID']):
                            count.append(1)
                    batches=len(count)
                    plot_data_mt_nt.append([str(j),str(i),batches])
    brass_data=[x for x in plot_data_mt_nt if x[0]=="brass"]
    ss_data=[x for x in plot_data_mt_nt if x[0]=="ss"]
    if len(brass_data)!=0 and len(ss_data)!=0:
        d_brass = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in brass_data],
            "Material Type": ["Brass"] * len(brass_data),
            "Batches": [x[2] for x in brass_data]
        })

        d_ss = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in ss_data],
            "Material Type": ["SS"] * len(ss_data),
            "Batches": [x[2] for x in ss_data]
        })

        dfm = pd.concat([d_brass, d_ss], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Material Type:N', title=None, axis=None),
            y='Batches:Q',
            color=alt.Color('Material Type:N', scale=alt.Scale(domain=['Brass', 'SS'], range=['#a07000', '#888888'])),
            column=alt.Column('Ni Plating Time:O'),
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Material Type:N', title='Material Type'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=150,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
    elif len(brass_data) == 0 and len(ss_data) != 0:

        d_ss = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in ss_data],
            "Material Type": ["SS"] * len(ss_data),
            "Batches": [x[2] for x in ss_data]
        })

        chart = alt.Chart(d_ss).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title='Ni Plating Time'),
            y='Batches:Q',
            color=alt.value('#888888'),  # Set color for SS bars
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=400,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")

    elif len(brass_data) != 0 and len(ss_data) == 0:
        d_brass = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in brass_data],
            "Material Type": ["Brass"] * len(brass_data),
            "Batches": [x[2] for x in brass_data]
        })

        chart = alt.Chart(d_brass).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title='Ni Plating Time'),
            y='Batches:Q',
            color=alt.value('#a07000'),  # Set color for Brass bars
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=400,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
        st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_mt_pt(inp):
    inp=st.session_state.input_state
    pt = st.session_state.pt 
    mt = st.session_state.mt 
    plot_data_mt_pt=[]
    for i in list(inp[1].keys()):
        if inp[1][i]==False:
            continue
        else:
            for j in list(inp[0].keys()):
                if inp[0][j]==False:
                    continue
                else:
                    rh=[]
                    for k in range(len(pt[i])):
                        if list(pt[i]["BATCH ID"])[k] in list(mt[j]['BATCH ID']):
                            rh.append(list(pt[i]["RH mins"])[k])
                    if len(rh)==0:
                        rh_avg=0
                        rh_max=0
                        rh_min=0
                        batches=0
                    else:
                        rh_avg=sum(rh)/len(rh)
                        rh_max=max(rh)
                        rh_min=min(rh)
                        batches=len(rh)
                    plot_data_mt_pt.append([str(j),str(i),round(rh_avg,2),round(rh_max,2),round(rh_min,2),batches]) 
    brass_data=[x for x in plot_data_mt_pt if x[0]=="brass"]
    ss_data=[x for x in plot_data_mt_pt if x[0]=="ss"]
    if len(brass_data)!=0 and len(ss_data)!=0:
        d_brass = pd.DataFrame({
            "Product Type": [x[1] for x in brass_data],
            "Material Type": ["Brass"] * len(brass_data),
            "RH Time": [x[2] for x in brass_data],
            "Average RH Time": [x[2] for x in brass_data],
            "Max RH Time": [x[3] for x in brass_data],
            "Min RH Time": [x[4] for x in brass_data],
            "Number of Batches": [x[5] for x in brass_data]
        })

        d_ss = pd.DataFrame({
            "Product Type": [x[1] for x in ss_data],
            "Material Type": ["SS"] * len(ss_data),
            "RH Time": [x[2] for x in ss_data],
            "Average RH Time": [x[2] for x in ss_data],
            "Max RH Time": [x[3] for x in ss_data],
            "Min RH Time": [x[4] for x in ss_data],
            "Number of Batches": [x[5] for x in ss_data]
        })

        dfm = pd.concat([d_brass, d_ss], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Material Type:N', title=None, axis=None),
            y='sum(RH Time):Q',
            color=alt.Color('Material Type:N', scale=alt.Scale(domain=['Brass', 'SS'], range=['#a07000', '#888888'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Material Type:N', title='Material Type'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=40,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)

    elif len(brass_data) == 0 and len(ss_data) != 0:

        d_ss = pd.DataFrame({
            "Product Type": [x[1] for x in ss_data],
            "RH Time": [x[2] for x in ss_data],
            "Average RH Time": [x[2] for x in ss_data],
            "Max RH Time": [x[3] for x in ss_data],
            "Min RH Time": [x[4] for x in ss_data],
            "Number of Batches": [x[5] for x in ss_data]
        })

        chart = alt.Chart(d_ss).mark_bar().encode(
            x=alt.X('Product Type:N', title='Product Type'),
            y='sum(RH Time):Q',
            color=alt.value('#888888'),  # Set color for Brass bars
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=600,
            height=400
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)


    elif len(brass_data) != 0 and len(ss_data) == 0:
        d_brass = pd.DataFrame({
            "Product Type": [x[1] for x in brass_data],
            "RH Time": [x[2] for x in brass_data],
            "Average RH Time": [x[2] for x in brass_data],
            "Max RH Time": [x[3] for x in brass_data],
            "Min RH Time": [x[4] for x in brass_data],
            "Number of Batches": [x[5] for x in brass_data]
        })

        chart = alt.Chart(d_brass).mark_bar().encode(
            x=alt.X('Product Type:N', title='Product Type'),
            y='sum(RH Time):Q',
            color=alt.value('#a07000'),  # Set color for Brass bars
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Average RH Time:Q', title='Average RH Time'),
                alt.Tooltip('Max RH Time:Q', title='Max RH Time'),
                alt.Tooltip('Min RH Time:Q', title='Min RH Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=600,
            height=400
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
def plot_mt_pt_II(inp):
    inp=st.session_state.input_state
    pt = st.session_state.pt 
    mt = st.session_state.mt 
    plot_data_mt_pt=[]
    for i in list(inp[1].keys()):
        if inp[1][i]==False:
            continue
        else:
            for j in list(inp[0].keys()):
                if inp[0][j]==False:
                    continue
                else:
                    rh=[]
                    for k in range(len(pt[i])):
                        if list(pt[i]["BATCH ID"])[k] in list(mt[j]['BATCH ID']):
                            rh.append(list(pt[i]["H_II mins"])[k])
                    if len(rh)==0:
                        rh_avg=0
                        rh_max=0
                        rh_min=0
                        batches=0
                    else:
                        rh_avg=sum(rh)/len(rh)
                        rh_max=max(rh)
                        rh_min=min(rh)
                        batches=len(rh)
                    plot_data_mt_pt.append([str(j),str(i),round(rh_avg,2),round(rh_max,2),round(rh_min,2),batches]) 
    brass_data=[x for x in plot_data_mt_pt if x[0]=="brass"]
    ss_data=[x for x in plot_data_mt_pt if x[0]=="ss"]
    if len(brass_data)!=0 and len(ss_data)!=0:
        d_brass = pd.DataFrame({
            "Product Type": [x[1] for x in brass_data],
            "Material Type": ["Brass"] * len(brass_data),
            "H_II Time": [x[2] for x in brass_data],
            "Average H_II Time": [x[2] for x in brass_data],
            "Max H_II Time": [x[3] for x in brass_data],
            "Min H_II Time": [x[4] for x in brass_data],
            "Number of Batches": [x[5] for x in brass_data]
        })

        d_ss = pd.DataFrame({
            "Product Type": [x[1] for x in ss_data],
            "Material Type": ["SS"] * len(ss_data),
            "H_II Time": [x[2] for x in ss_data],
            "Average H_II Time": [x[2] for x in ss_data],
            "Max H_II Time": [x[3] for x in ss_data],
            "Min H_II Time": [x[4] for x in ss_data],
            "Number of Batches": [x[5] for x in ss_data]
        })

        dfm = pd.concat([d_brass, d_ss], ignore_index=True)

        chart = alt.Chart(dfm).mark_bar().encode(
            x=alt.X('Material Type:N', title=None, axis=None),
            y='sum(H_II Time):Q',
            color=alt.Color('Material Type:N', scale=alt.Scale(domain=['Brass', 'SS'], range=['#a07000', '#888888'])),
            column=alt.Column('Product Type:O'),
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Material Type:N', title='Material Type'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=40,
            height=300
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)

    elif len(brass_data) == 0 and len(ss_data) != 0:

        d_ss = pd.DataFrame({
            "Product Type": [x[1] for x in ss_data],
            "H_II Time": [x[2] for x in ss_data],
            "Average H_II Time": [x[2] for x in ss_data],
            "Max H_II Time": [x[3] for x in ss_data],
            "Min H_II Time": [x[4] for x in ss_data],
            "Number of Batches": [x[5] for x in ss_data]
        })

        chart = alt.Chart(d_ss).mark_bar().encode(
            x=alt.X('Product Type:N', title='Product Type'),
            y='sum(H_II Time):Q',
            color=alt.value('#888888'),  # Set color for Brass bars
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=600,
            height=400
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)


    elif len(brass_data) != 0 and len(ss_data) == 0:
        d_brass = pd.DataFrame({
            "Product Type": [x[1] for x in brass_data],
            "H_II Time": [x[2] for x in brass_data],
            "Average H_II Time": [x[2] for x in brass_data],
            "Max H_II Time": [x[3] for x in brass_data],
            "Min H_II Time": [x[4] for x in brass_data],
            "Number of Batches": [x[5] for x in brass_data]
        })

        chart = alt.Chart(d_brass).mark_bar().encode(
            x=alt.X('Product Type:N', title='Product Type'),
            y='sum(H_II Time):Q',
            color=alt.value('#a07000'),  # Set color for Brass bars
            tooltip=[
                alt.Tooltip('Product Type:N', title='Product Type'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
                alt.Tooltip('Number of Batches:Q', title='Number of Batches')
            ]
        ).properties(
            width=600,
            height=400
        ).configure_view(
            stroke='transparent'
        )

        st.altair_chart(chart)
def plot_mt_pt_glow(inp):
    inp=st.session_state.input_state
    pt = st.session_state.pt 
    mt = st.session_state.mt 
    pt_full = st.session_state.pt_full 
    mt_full = st.session_state.mt_full
    region_selections_glow=st.session_state.region_selections_glow
    plot_data_mt_pt=[]
    if region_selections_glow[0]==True:
        for i in list(inp[1].keys()):
            if inp[1][i]==False:
                continue
            else:
                for j in list(inp[0].keys()):
                    if inp[0][j]==False:
                        continue
                    else:
                        count=[]
                        #count_full=[]
                        for k in range(len(pt[i])):
                            if list(pt[i]["BATCH ID"])[k] in list(mt[j]['BATCH ID']):
                                count.append(1)
                            #if list(pt_full[i]["BATCH ID"])[k] in list(mt_full[j]['BATCH ID']):
                                #count_full.append(1)                        
                        batches=len(count)#/len(count_full)
                        plot_data_mt_pt.append([str(j),str(i),batches]) 
        brass_data=[x for x in plot_data_mt_pt if x[0]=="brass"]
        ss_data=[x for x in plot_data_mt_pt if x[0]=="ss"]
        if len(brass_data)!=0 and len(ss_data)!=0:
            d_brass = pd.DataFrame({
                "Product Type": [x[1] for x in brass_data],
                "Material Type": ["Brass"] * len(brass_data),
                "Batches": [x[2] for x in brass_data]
            })

            d_ss = pd.DataFrame({
                "Product Type": [x[1] for x in ss_data],
                "Material Type": ["SS"] * len(ss_data),
                "Batches": [x[2] for x in ss_data]
            })

            dfm = pd.concat([d_brass, d_ss], ignore_index=True)

            chart = alt.Chart(dfm).mark_bar().encode(
                x=alt.X('Material Type:N', title=None, axis=None),
                y='Batches:Q',
                color=alt.Color('Material Type:N', scale=alt.Scale(domain=['Brass', 'SS'], range=['#a07000', '#888888'])),
                column=alt.Column('Product Type:O'),
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Material Type:N', title='Material Type'),
                    alt.Tooltip('Batches:Q', title='Number of Batches')
                ]
            ).properties(
                width=40,
                height=300
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)

        elif len(brass_data) == 0 and len(ss_data) != 0:

            d_ss = pd.DataFrame({
                "Product Type": [x[1] for x in ss_data],
                "Material Type": ["SS"] * len(ss_data),
                "Batches": [x[2] for x in ss_data]
            })

            chart = alt.Chart(d_ss).mark_bar().encode(
                x=alt.X('Product Type:N', title='Product Type'),
                y='Batches:Q',
                color=alt.value('#888888'),  # Set color for Brass bars
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Batches:Q', title='Number of Batches')
                ]
            ).properties(
                width=600,
                height=400
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)
    else:
        for i in list(inp[1].keys()):
            if inp[1][i]==False:
                continue
            else:
                for j in list(inp[0].keys()):
                    if inp[0][j]==False:
                        continue
                    else:
                        count=[]
                        count_full=[]
                        for k in range(len(pt[i])):
                            if list(pt[i]["BATCH ID"])[k] in list(mt[j]['BATCH ID']):
                                count.append(1)
                            if list(pt_full[i]["BATCH ID"])[k] in list(mt_full[j]['BATCH ID']):
                                count_full.append(1)
                        if len(count_full)!=0:                    
                            batches=len(count)/len(count_full)
                        else:
                            batches=len(count)
                        plot_data_mt_pt.append([str(j),str(i),batches]) 
        brass_data=[x for x in plot_data_mt_pt if x[0]=="brass"]
        ss_data=[x for x in plot_data_mt_pt if x[0]=="ss"]
        if len(brass_data)!=0 and len(ss_data)!=0:
            d_brass = pd.DataFrame({
                "Product Type": [x[1] for x in brass_data],
                "Material Type": ["Brass"] * len(brass_data),
                "Batches": [x[2] for x in brass_data]
            })

            d_ss = pd.DataFrame({
                "Product Type": [x[1] for x in ss_data],
                "Material Type": ["SS"] * len(ss_data),
                "Batches": [x[2] for x in ss_data]
            })

            dfm = pd.concat([d_brass, d_ss], ignore_index=True)

            chart = alt.Chart(dfm).mark_bar().encode(
                x=alt.X('Material Type:N', title=None, axis=None),
                y='Batches:Q',
                color=alt.Color('Material Type:N', scale=alt.Scale(domain=['Brass', 'SS'], range=['#a07000', '#888888'])),
                column=alt.Column('Product Type:O'),
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Material Type:N', title='Material Type'),
                    alt.Tooltip('Batches:Q', title='Number of Batches')
                ]
            ).properties(
                width=40,
                height=300
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)

        elif len(brass_data) == 0 and len(ss_data) != 0:

            d_ss = pd.DataFrame({
                "Product Type": [x[1] for x in ss_data],
                "Material Type": ["SS"] * len(ss_data),
                "Batches": [x[2] for x in ss_data]
            })

            chart = alt.Chart(d_ss).mark_bar().encode(
                x=alt.X('Product Type:N', title='Product Type'),
                y='Batches:Q',
                color=alt.value('#888888'),  # Set color for Brass bars
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Batches:Q', title='Number of Batches')
                ]
            ).properties(
                width=600,
                height=400
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)

        elif len(brass_data) != 0 and len(ss_data) == 0:
            d_brass = pd.DataFrame({
                "Product Type": [x[1] for x in brass_data],
                "Material Type": ["Brass"] * len(brass_data),
                "Batches": [x[2] for x in brass_data]
            })

            chart = alt.Chart(d_brass).mark_bar().encode(
                x=alt.X('Product Type:N', title='Product Type'),
                y='Batches:Q',
                color=alt.value('#a07000'),  # Set color for Brass bars
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Batches:Q', title='Number of Batches')
                ]
            ).properties(
                width=600,
                height=400
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)
def plot_mt_pt_ac(inp):
    inp=st.session_state.input_state
    pt_full = st.session_state.pt_full
    mt_full = st.session_state.mt_full
    region_selections_ae=st.session_state.region_selections_ae
    region_selections_ac=st.session_state.region_selections_ac
    region_selections_ps=st.session_state.region_selections_ps
    region_selections_ti=st.session_state.region_selections_ti

    pt = st.session_state.pt 
    mt = st.session_state.mt 
    if (st.session_state.current_page == 'ac_isa' and region_selections_ac[0]==True) or (st.session_state.current_page == 'ae_isa' and region_selections_ae[1]=='All Batches') or (st.session_state.current_page == 'ps_isa' and region_selections_ps[0]=='All Batches')  or (st.session_state.current_page == 'ti_isa' and region_selections_ti[0]=='All Batches'):
        plot_data_mt_pt=[]
        for i in list(inp[1].keys()):
            if inp[1][i]==False:
                continue
            else:
                for j in list(inp[0].keys()):
                    if inp[0][j]==False:
                        continue
                    else:
                        count=[]
                        for k in range(len(pt[i])):
                            if list(pt[i]["BATCH ID"])[k] in list(mt[j]['BATCH ID']):
                                count.append(1)
                        batches=len(count)
                        plot_data_mt_pt.append([str(j),str(i),batches]) 
        brass_data=[x for x in plot_data_mt_pt if x[0]=="brass"]
        ss_data=[x for x in plot_data_mt_pt if x[0]=="ss"]
        if len(brass_data)!=0 and len(ss_data)!=0:
            d_brass = pd.DataFrame({
                "Product Type": [x[1] for x in brass_data],
                "Material Type": ["Brass"] * len(brass_data),
                "Batches": [x[2] for x in brass_data]
            })

            d_ss = pd.DataFrame({
                "Product Type": [x[1] for x in ss_data],
                "Material Type": ["SS"] * len(ss_data),
                "Batches": [x[2] for x in ss_data]
            })

            dfm = pd.concat([d_brass, d_ss], ignore_index=True)

            chart = alt.Chart(dfm).mark_bar().encode(
                x=alt.X('Material Type:N', title=None, axis=None),
                y='Batches:Q',
                color=alt.Color('Material Type:N', scale=alt.Scale(domain=['Brass', 'SS'], range=['#a07000', '#888888'])),
                column=alt.Column('Product Type:O'),
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Material Type:N', title='Material Type'),
                    alt.Tooltip('Batches:Q', title='Number of Batches')
                ]
            ).properties(
                width=40,
                height=300
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)

        elif len(brass_data) == 0 and len(ss_data) != 0:

            d_ss = pd.DataFrame({
                "Product Type": [x[1] for x in ss_data],
                "Material Type": ["SS"] * len(ss_data),
                "Batches": [x[2] for x in ss_data]
            })

            chart = alt.Chart(d_ss).mark_bar().encode(
                x=alt.X('Product Type:N', title='Product Type'),
                y='Batches:Q',
                color=alt.value('#888888'),  # Set color for Brass bars
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Batches:Q', title='Number of Batches')
                ]
            ).properties(
                width=600,
                height=400
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)


        elif len(brass_data) != 0 and len(ss_data) == 0:
            d_brass = pd.DataFrame({
                "Product Type": [x[1] for x in brass_data],
                "Material Type": ["Brass"] * len(brass_data),
                "Batches": [x[2] for x in brass_data]
            })

            chart = alt.Chart(d_brass).mark_bar().encode(
                x=alt.X('Product Type:N', title='Product Type'),
                y='Batches:Q',
                color=alt.value('#a07000'),  # Set color for Brass bars
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Batches:Q', title='Number of Batches')
                ]
            ).properties(
                width=600,
                height=400
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)
    elif (st.session_state.current_page == 'ac_isa' and region_selections_ac[0]==False) or (st.session_state.current_page == 'ae_isa' and (region_selections_ae[1]=='Irregular Batches' or region_selections_ae[1]=='Good Batches')) or (st.session_state.current_page == 'ps_isa' and (region_selections_ps[0]=='Irregular Batches' or region_selections_ps[0]=='Good Batches')) or (st.session_state.current_page == 'ti_isa' and (region_selections_ti[0]=='Irregular Batches' or region_selections_ti[0]=='Good Batches')):
        plot_data_mt_pt=[]
        for i in list(inp[1].keys()):
            if inp[1][i]==False:
                continue
            else:
                for j in list(inp[0].keys()):
                    if inp[0][j]==False:
                        continue
                    else:
                        count=[]
                        count_full=[]
                        for k in range(len(pt[i])):
                            if list(pt[i]["BATCH ID"])[k] in list(mt[j]['BATCH ID']):
                                count.append(1)
                        for k in range(len(pt_full[i])):
                            if list(pt_full[i]["BATCH ID"])[k] in list(mt_full[j]['BATCH ID']):
                                count_full.append(1)
                        if len(count_full)!=0:
                            batches=len(count)/len(count_full)
                        else:
                            batches=len(count)
                        plot_data_mt_pt.append([str(j),str(i),np.round(batches,2),len(count),len(count_full)]) 
        brass_data=[x for x in plot_data_mt_pt if x[0]=="brass"]
        ss_data=[x for x in plot_data_mt_pt if x[0]=="ss"]
        if len(brass_data)!=0 and len(ss_data)!=0:
            d_brass = pd.DataFrame({
                "Product Type": [x[1] for x in brass_data],
                "Material Type": ["Brass"] * len(brass_data),
                "Batches": [x[2] for x in brass_data],
                "Part Batches": [x[3] for x in brass_data],
                "Full Batches": [x[4] for x in brass_data]
            })

            d_ss = pd.DataFrame({
                "Product Type": [x[1] for x in ss_data],
                "Material Type": ["SS"] * len(ss_data),
                "Batches": [x[2] for x in ss_data],
                "Part Batches": [x[3] for x in ss_data],
                "Full Batches": [x[4] for x in ss_data]
            })

            dfm = pd.concat([d_brass, d_ss], ignore_index=True)

            chart = alt.Chart(dfm).mark_bar().encode(
                x=alt.X('Material Type:N', title=None, axis=None),
                y='Batches:Q',
                color=alt.Color('Material Type:N', scale=alt.Scale(domain=['Brass', 'SS'], range=['#a07000', '#888888'])),
                column=alt.Column('Product Type:O'),
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Material Type:N', title='Material Type'),
                    alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                    alt.Tooltip('Part Batches:N', title='Filter Count'),
                    alt.Tooltip('Full Batches:Q', title='Total Count')
                ]
            ).properties(
                width=40,
                height=300
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)

        elif len(brass_data) == 0 and len(ss_data) != 0:

            d_ss = pd.DataFrame({
                "Product Type": [x[1] for x in ss_data],
                "Material Type": ["SS"] * len(ss_data),
                "Batches": [x[2] for x in ss_data],
                "Part Batches": [x[3] for x in ss_data],
                "Full Batches": [x[4] for x in ss_data]
            })

            chart = alt.Chart(d_ss).mark_bar().encode(
                x=alt.X('Product Type:N', title='Product Type'),
                y='Batches:Q',
                color=alt.value('#888888'),  # Set color for Brass bars
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                    alt.Tooltip('Part Batches:N', title='Filter Count'),
                    alt.Tooltip('Full Batches:Q', title='Total Count')
                ]
            ).properties(
                width=600,
                height=400
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)


        elif len(brass_data) != 0 and len(ss_data) == 0:
            d_brass = pd.DataFrame({
                "Product Type": [x[1] for x in brass_data],
                "Material Type": ["Brass"] * len(brass_data),
                "Batches": [x[2] for x in brass_data],
                "Part Batches": [x[3] for x in brass_data],
                "Full Batches": [x[4] for x in brass_data]
            })

            chart = alt.Chart(d_brass).mark_bar().encode(
                x=alt.X('Product Type:N', title='Product Type'),
                y='Batches:Q',
                color=alt.value('#a07000'),  # Set color for Brass bars
                tooltip=[
                    alt.Tooltip('Product Type:N', title='Product Type'),
                    alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                    alt.Tooltip('Part Batches:N', title='Filter Count'),
                    alt.Tooltip('Full Batches:Q', title='Total Count')
                ]
            ).properties(
                width=600,
                height=400
            ).configure_view(
                stroke='transparent'
            )

            st.altair_chart(chart)
def plot_pt(inp):
    inp=st.session_state.input_state
    pt = st.session_state.pt  # Ensure pt is defined in session state
    plot_data_pt = []

    for i in list(inp[1].keys()):
        if inp[1][i] == False:
            continue
        else:
            rh = []
            for k in range(len(pt[i])):
                rh.append(list(pt[i]["RH mins"])[k])
            if len(rh) == 0:
                rh_avg = 0
                rh_max = 0
                rh_min = 0
                batches = 0
            else:
                rh_avg = sum(rh) / len(rh)
                rh_max = max(rh)
                rh_min = min(rh)
                batches = len(rh)
            plot_data_pt.append([str(i), round(rh_avg, 2), round(rh_max, 2), round(rh_min, 2), batches])

    plot_df = pd.DataFrame(plot_data_pt, columns=["Product Type", "RH Avg", "RH Max", "RH Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Product Type:O', title='Product Type')
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('RH Avg:Q', title='RH Time (Mins)'),
        tooltip=[
            alt.Tooltip('Product Type:O', title='Product Type'),
            alt.Tooltip('RH Avg:Q', title='Average RH Time'),
            alt.Tooltip('RH Max:Q', title='Max RH Time'),
            alt.Tooltip('RH Min:Q', title='Min RH Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='RH Avg:Q'
    )

    chart = (bars + text).properties(
        title='Product Type vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_pt_II(inp):
    inp=st.session_state.input_state
    pt = st.session_state.pt  # Ensure pt is defined in session state
    plot_data_pt = []

    for i in list(inp[1].keys()):
        if inp[1][i] == False:
            continue
        else:
            rh = []
            for k in range(len(pt[i])):
                rh.append(list(pt[i]["H_II mins"])[k])
            if len(rh) == 0:
                rh_avg = 0
                rh_max = 0
                rh_min = 0
                batches = 0
            else:
                rh_avg = sum(rh) / len(rh)
                rh_max = max(rh)
                rh_min = min(rh)
                batches = len(rh)
            plot_data_pt.append([str(i), round(rh_avg, 2), round(rh_max, 2), round(rh_min, 2), batches])

    plot_df = pd.DataFrame(plot_data_pt, columns=["Product Type", "H_II Avg", "H_II Max", "H_II Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Product Type:O', title='Product Type')
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('H_II Avg:Q', title='H_II Time (Mins)'),
        tooltip=[
            alt.Tooltip('Product Type:O', title='Product Type'),
            alt.Tooltip('H_II Avg:Q', title='Average H_II Time'),
            alt.Tooltip('H_II Max:Q', title='Max H_II Time'),
            alt.Tooltip('H_II Min:Q', title='Min H_II Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='H_II Avg:Q'
    )

    chart = (bars + text).properties(
        title='Product Type vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_pt_glow(inp):
    inp=st.session_state.input_state
    pt = st.session_state.pt
    pt_full = st.session_state.pt_full
    region_selections_glow=st.session_state.region_selections_glow
    if region_selections_glow[0]==True:

        plot_data_pt = []

        for i in list(inp[1].keys()):
            if inp[1][i] == False:
                continue
            else:
                batches=len(pt[i])
                plot_data_pt.append([str(i), batches])

        plot_df = pd.DataFrame(plot_data_pt, columns=["Product Type", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Product Type:O', title='Product Type')
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Product Type:O', title='Product Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches')
            ]
        )

        chart = (bars).properties(
            title='Product Type vs Glow Discharge Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_pt = []

        for i in list(inp[1].keys()):
            if inp[1][i] == False:
                continue
            else:
                if len(pt_full[i])!=0:
                    batches=len(pt[i])/len(pt_full[i])
                else:
                    batches=len(pt[i])
                plot_data_pt.append([str(i), np.round(batches,2), len(pt[i]), len(pt_full[i])])

        plot_df = pd.DataFrame(plot_data_pt, columns=["Product Type", "Batches", "Part Batches", "Full Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Product Type:O', title='Product Type')
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Fraction from Total Batches',scale=alt.Scale(domain=[0, 1])),
            tooltip=[
                alt.Tooltip('Product Type:O', title='Product Type'),
                alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                alt.Tooltip('Part Batches:Q', title='Filter Count'),
                alt.Tooltip('Full Batches:Q', title='Total Count')            ]
        )

        chart = (bars).properties(
            title='Product Type vs Glow Discharge Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_pt_ac(inp):
    inp=st.session_state.input_state
    pt = st.session_state.pt
    pt_full = st.session_state.pt_full
    region_selections_ae=st.session_state.region_selections_ae
    region_selections_ac=st.session_state.region_selections_ac
    region_selections_ps=st.session_state.region_selections_ps
    region_selections_ti=st.session_state.region_selections_ti

    if (st.session_state.current_page == 'ac_isa' and region_selections_ac[0]==True) or (st.session_state.current_page == 'ae_isa' and region_selections_ae[1]=='All Batches') or (st.session_state.current_page == 'ps_isa' and region_selections_ps[0]=='All Batches')  or (st.session_state.current_page == 'ti_isa' and region_selections_ti[0]=='All Batches'):

        plot_data_pt = []

        for i in list(inp[1].keys()):
            if inp[1][i] == False:
                continue
            else:
                batches=len(pt[i])
                plot_data_pt.append([str(i), batches])

        plot_df = pd.DataFrame(plot_data_pt, columns=["Product Type", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Product Type:O', title='Product Type')
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Product Type:O', title='Product Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches')
            ]
        )

        chart = (bars).properties(
            title='Product Type',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    elif (st.session_state.current_page == 'ac_isa' and region_selections_ac[0]==False) or (st.session_state.current_page == 'ae_isa' and (region_selections_ae[1]=='Irregular Batches' or region_selections_ae[1]=='Good Batches')) or (st.session_state.current_page == 'ps_isa' and (region_selections_ps[0]=='Irregular Batches' or region_selections_ps[0]=='Good Batches')) or (st.session_state.current_page == 'ti_isa' and (region_selections_ti[0]=='Irregular Batches' or region_selections_ti[0]=='Good Batches')):
        plot_data_pt = []

        for i in list(inp[1].keys()):
            if inp[1][i] == False:
                continue
            else:
                if len(pt_full[i])!=0:
                    batches=len(pt[i])/len(pt_full[i])
                else:
                    batches=len(pt[i])
                plot_data_pt.append([str(i), np.round(batches,2), len(pt[i]), len(pt_full[i])])

        plot_df = pd.DataFrame(plot_data_pt, columns=["Product Type", "Batches", "Part Batches", "Full Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Product Type:O', title='Product Type')
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Fraction from Total Batches',scale=alt.Scale(domain=[0, 1])),
            tooltip=[
                alt.Tooltip('Product Type:O', title='Product Type'),
                alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                alt.Tooltip('Part Batches:Q', title='Filter Count'),
                alt.Tooltip('Full Batches:Q', title='Total Count')


            ]
        )

        chart = (bars).properties(
            title='Product Type',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_mt(inp):
    inp=st.session_state.input_state
    mt = st.session_state.mt
    plot_data_mt = []

    for i in list(inp[0].keys()):
        if inp[0][i] == False:
            continue
        else:
            rh = []
            for k in range(len(mt[i])):
                rh.append(list(mt[i]["RH mins"])[k])
            if len(rh) == 0:
                rh_avg = 0
                rh_max = 0
                rh_min = 0
                batches = 0
            else:
                rh_avg = sum(rh) / len(rh)
                rh_max = max(rh)
                rh_min = min(rh)
                batches = len(rh)
            plot_data_mt.append([str(i), round(rh_avg, 2), round(rh_max, 2), round(rh_min, 2), batches])

    plot_df = pd.DataFrame(plot_data_mt, columns=["Material Type", "RH Avg", "RH Max", "RH Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Material Type:O', title='Material Type')
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('RH Avg:Q', title='RH Time (Mins)'),
        tooltip=[
            alt.Tooltip('Material Type:O', title='Material Type'),
            alt.Tooltip('RH Avg:Q', title='Average RH Time'),
            alt.Tooltip('RH Max:Q', title='Max RH Time'),
            alt.Tooltip('RH Min:Q', title='Min RH Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='RH Avg:Q'
    )

    chart = (bars + text).properties(
        title='Material Type vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
    refined_df=st.session_state.refined_df

    ss_data=[refined_df["RH mins"][i] if refined_df["MATERIAL TYPE"][i]=="SS" else None for i in range(len(refined_df)) ]
    brass_data=[refined_df["RH mins"][i] if refined_df["MATERIAL TYPE"][i]=="Brass" else None for i in range(len(refined_df))]
    x=np.arange(0,len(refined_df),1)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(x,ss_data,label="SS batches",color="#008081")
    ax.scatter(x,brass_data, label="Brass batches",color="#f02071")
    ax.plot(x,np.full((len(refined_df)),np.average([i for i in ss_data if i!=None])),linestyle='dashed',color="#008081",label="SS Mean RH time ("+str(np.average([i for i in ss_data if i!=None]).round(2))+")")
    ax.plot(x,np.full((len(refined_df)),np.average([i for i in brass_data if i!=None])),linestyle='dashed',color="#f02071",label="Brass Mean RH time ("+str(np.average([i for i in brass_data if i!=None]).round(2))+")")
    ax.set_title("Brass vs SS Pumpdown Time Comparison "+refined_df["BATCH START TIME"][0][:10]+" - "+refined_df["BATCH START TIME"][len(refined_df)-1][:10],fontsize=10)
    ax.set_xlabel("Batches")
    ax.set_ylabel("RH Time (Mins)")
    ax.legend(loc='center right', bbox_to_anchor=(1.0, 0.15),fontsize=7)
    st.pyplot(fig)
def plot_mt_II(inp):
    inp=st.session_state.input_state
    mt = st.session_state.mt
    plot_data_mt = []

    for i in list(inp[0].keys()):
        if inp[0][i] == False:
            continue
        else:
            rh = []
            for k in range(len(mt[i])):
                rh.append(list(mt[i]["H_II mins"])[k])
            if len(rh) == 0:
                rh_avg = 0
                rh_max = 0
                rh_min = 0
                batches = 0
            else:
                rh_avg = sum(rh) / len(rh)
                rh_max = max(rh)
                rh_min = min(rh)
                batches = len(rh)
            plot_data_mt.append([str(i), round(rh_avg, 2), round(rh_max, 2), round(rh_min, 2), batches])

    plot_df = pd.DataFrame(plot_data_mt, columns=["Material Type", "H_II Avg", "H_II Max", "H_II Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Material Type:O', title='Material Type')
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('H_II Avg:Q', title='H_II Time (Mins)'),
        tooltip=[
            alt.Tooltip('Material Type:O', title='Material Type'),
            alt.Tooltip('H_II Avg:Q', title='Average H_II Time'),
            alt.Tooltip('H_II Max:Q', title='Max H_II Time'),
            alt.Tooltip('H_II Min:Q', title='Min H_II Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='H_II Avg:Q'
    )

    chart = (bars + text).properties(
        title='Material Type vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
    refined_df_II=st.session_state.refined_df_II

    ss_data=[refined_df_II["H_II mins"][i] if refined_df_II["MATERIAL TYPE"][i]=="SS" else None for i in range(len(refined_df_II)) ]
    brass_data=[refined_df_II["H_II mins"][i] if refined_df_II["MATERIAL TYPE"][i]=="Brass" else None for i in range(len(refined_df_II))]
    x=np.arange(0,len(refined_df_II),1)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(x,ss_data,label="SS batches",color="#008081")
    ax.scatter(x,brass_data, label="Brass batches",color="#f02071")
    ax.plot(x,np.full((len(refined_df_II)),np.average([i for i in ss_data if i!=None])),linestyle='dashed',color="#008081",label="SS Mean H_II time ("+str(np.average([i for i in ss_data if i!=None]).round(2))+")")
    ax.plot(x,np.full((len(refined_df_II)),np.average([i for i in brass_data if i!=None])),linestyle='dashed',color="#f02071",label="Brass Mean H_II time ("+str(np.average([i for i in brass_data if i!=None]).round(2))+")")
    ax.set_title("Brass vs SS Pumpdown II Time Comparison "+refined_df_II["BATCH START TIME"][0][:10]+" - "+refined_df_II["BATCH START TIME"][len(refined_df_II)-1][:10],fontsize=10)
    ax.set_xlabel("Batches")
    ax.set_ylabel("H_II Time (Mins)")
    ax.legend(loc='center right', bbox_to_anchor=(1.0, 0.15),fontsize=7)
    st.pyplot(fig)
def plot_mt_glow(inp):
    inp=st.session_state.input_state
    mt = st.session_state.mt
    mt_full = st.session_state.mt_full
    region_selections_glow=st.session_state.region_selections_glow
    if region_selections_glow[0]==True:
        plot_data_mt = []

        for i in list(inp[0].keys()):
            if inp[0][i] == False:
                continue
            else:
                batches=len(mt[i])
                plot_data_mt.append([str(i), batches])

        plot_df = pd.DataFrame(plot_data_mt, columns=["Material Type", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Material Type:O', title='Material Type')
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Material Type:O', title='Material Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches')
            ]
        )

        chart = (bars).properties(
            title='Material Type vs Glow Discharge Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_mt = []

        for i in list(inp[0].keys()):
            if inp[0][i] == False:
                continue
            else:
                batches=len(mt[i])/len(mt_full[i])
                plot_data_mt.append([str(i), np.round(batches,2), len(mt[i]), len(mt_full[i])])

        plot_df = pd.DataFrame(plot_data_mt, columns=["Material Type", "Batches", "Part Batches", "Full Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Material Type:O', title='Material Type')
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Fraction from Total Batches', scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Material Type:O', title='Material Type'),
                alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                alt.Tooltip('Part Batches:Q', title='Filter Count'),
                alt.Tooltip('Full Batches:Q', title='Total Count')            ]
        )

        chart = (bars).properties(
            title='Material Type vs Glow Discharge Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_mt_ac(inp):
    inp=st.session_state.input_state
    mt = st.session_state.mt
    mt_full = st.session_state.mt_full
    region_selections_ac=st.session_state.region_selections_ac
    region_selections_ae=st.session_state.region_selections_ae
    region_selections_ps=st.session_state.region_selections_ps
    region_selections_ti=st.session_state.region_selections_ti

    if (st.session_state.current_page == 'ac_isa' and region_selections_ac[0]==True) or (st.session_state.current_page == 'ae_isa' and region_selections_ae[1]=='All Batches') or (st.session_state.current_page == 'ps_isa' and region_selections_ps[0]=='All Batches')  or (st.session_state.current_page == 'ti_isa' and region_selections_ti[0]=='All Batches'):
        plot_data_mt = []

        for i in list(inp[0].keys()):
            if inp[0][i] == False:
                continue
            else:
                batches=len(mt[i])
                plot_data_mt.append([str(i), batches])

        plot_df = pd.DataFrame(plot_data_mt, columns=["Material Type", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Material Type:O', title='Material Type')
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Material Type:O', title='Material Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches')
            ]
        )

        chart = (bars).properties(
            title='Material Type',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    elif (st.session_state.current_page == 'ac_isa' and region_selections_ac[0]==False) or (st.session_state.current_page == 'ae_isa' and (region_selections_ae[1]=='Irregular Batches' or region_selections_ae[1]=='Good Batches')) or (st.session_state.current_page == 'ps_isa' and (region_selections_ps[0]=='Irregular Batches' or region_selections_ps[0]=='Good Batches')) or (st.session_state.current_page == 'ti_isa' and (region_selections_ti[0]=='Irregular Batches' or region_selections_ti[0]=='Good Batches')):
        plot_data_mt = []

        for i in list(inp[0].keys()):
            if inp[0][i] == False:
                continue
            else:
                if len(mt_full[i])!=0:
                    batches=len(mt[i])/len(mt_full[i])
                else:
                    batches=len(mt[i])
                plot_data_mt.append([str(i), np.round(batches,2), len(mt[i]), len(mt_full[i])])

        plot_df = pd.DataFrame(plot_data_mt, columns=["Material Type", "Batches", "Part Batches", "Full Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Material Type:O', title='Material Type')
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Fraction from Total Batches', scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Material Type:O', title='Material Type'),
                alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                alt.Tooltip('Part Batches:Q', title='Filter Count'),
                alt.Tooltip('Full Batches:Q', title='Total Count')            ]
        )

        chart = (bars).properties(
            title='Material Type',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)       
def plot_nt(inp):
    inp=st.session_state.input_state
    nt=st.session_state.nt
    plot_data_nt=[]
    for i in list(inp[2].keys()):
        if inp[2][i]==False:
            continue
        else:
            rh=[]
            for k in range(len(nt[i])):
                rh.append(list(nt[i]["RH mins"])[k])
            if len(rh)==0:
                rh_avg=0
                rh_max=0
                rh_min=0
                batches=0
            else:
                rh_avg=sum(rh)/len(rh)
                rh_max=max(rh)
                rh_min=min(rh)
                batches=len(rh)
            plot_data_nt.append([str(i),round(rh_avg,2),round(rh_max,2),round(rh_min,2),batches])
    plot_df = pd.DataFrame(plot_data_nt, columns=["Nickel Plating Time", "RH Avg", "RH Max", "RH Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Nickel Plating Time:O', title='Nickel Plating Time')
    )

    bars = base.mark_bar(color="#008081").encode(
        y=alt.Y('RH Avg:Q', title='RH Time (Mins)'),
        tooltip=[
            alt.Tooltip('Nickel Plating Time:O', title='Nickel Plating Time'),
            alt.Tooltip('RH Avg:Q', title='Average RH Time'),
            alt.Tooltip('RH Max:Q', title='Max RH Time'),
            alt.Tooltip('RH Min:Q', title='Min RH Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='RH Avg:Q'
    )

    chart = (bars + text).properties(
        title='Nickel Plating Time vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_nt_II(inp):
    inp=st.session_state.input_state
    nt=st.session_state.nt
    plot_data_nt=[]
    for i in list(inp[2].keys()):
        if inp[2][i]==False:
            continue
        else:
            rh=[]
            for k in range(len(nt[i])):
                rh.append(list(nt[i]["H_II mins"])[k])
            if len(rh)==0:
                rh_avg=0
                rh_max=0
                rh_min=0
                batches=0
            else:
                rh_avg=sum(rh)/len(rh)
                rh_max=max(rh)
                rh_min=min(rh)
                batches=len(rh)
            plot_data_nt.append([str(i),round(rh_avg,2),round(rh_max,2),round(rh_min,2),batches])
    plot_df = pd.DataFrame(plot_data_nt, columns=["Nickel Plating Time", "H_II Avg", "H_II Max", "H_II Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Nickel Plating Time:O', title='Nickel Plating Time')
    )

    bars = base.mark_bar(color="#008081").encode(
        y=alt.Y('H_II Avg:Q', title='H_II Time (Mins)'),
        tooltip=[
            alt.Tooltip('Nickel Plating Time:O', title='Nickel Plating Time'),
            alt.Tooltip('H_II Avg:Q', title='Average H_II Time'),
            alt.Tooltip('H_II Max:Q', title='Max H_II Time'),
            alt.Tooltip('H_II Min:Q', title='Min H_II Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='H_II Avg:Q'
    )

    chart = (bars + text).properties(
        title='Nickel Plating Time vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_nt_glow(inp):
    inp=st.session_state.input_state
    nt = st.session_state.nt
    plot_data_nt = []

    for i in list(inp[2].keys()):
        if inp[2][i] == False:
            continue
        else:
            batches=len(nt[i])
            plot_data_nt.append([str(i), batches])

    plot_df = pd.DataFrame(plot_data_nt, columns=["Ni Plating Time", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Ni Plating Time:O', title='Ni Plating Time')
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('Batches:Q', title='No. of Batches'),
        tooltip=[
            alt.Tooltip('Ni Plating Time:O', title='Ni Plating Time'),
            alt.Tooltip('Batches:Q', title='No. of Batches')
        ]
    )

    chart = (bars).properties(
        title='Ni Plating Time vs Glow Discharge Batches',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
    st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def plot_nt_ac(inp):
    inp=st.session_state.input_state
    nt = st.session_state.nt
    plot_data_nt = []

    for i in list(inp[2].keys()):
        if inp[2][i] == False:
            continue
        else:
            batches=len(nt[i])
            plot_data_nt.append([str(i), batches])

    plot_df = pd.DataFrame(plot_data_nt, columns=["Ni Plating Time", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Ni Plating Time:O', title='Ni Plating Time')
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('Batches:Q', title='No. of Batches'),
        tooltip=[
            alt.Tooltip('Ni Plating Time:O', title='Ni Plating Time'),
            alt.Tooltip('Batches:Q', title='No. of Batches')
        ]
    )

    chart = (bars).properties(
        title='Ni Plating Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
    st.write("I series : \nless than 2 hrs\n\nII series : \n2-8 hrs\n\nIII series : \ngreater than 8 hrs")
def submit_inputs(): 
    st.session_state.input_state = convert_input_state(st.session_state.input_state)
    inp=st.session_state.input_state
    if True not in list(inp[0].values()) and True not in list(inp[1].values()) and True not in list(inp[2].values()):
        pass
    elif True not in list(inp[0].values()) and True not in list(inp[1].values()):
        plot_nt(inp)
    elif True not in list(inp[1].values()) and True not in list(inp[2].values()):
        plot_mt(inp)
    elif True not in list(inp[0].values()) and True not in list(inp[2].values()):
        plot_pt(inp)
    elif True in list(inp[0].values()) and True in list(inp[1].values()):
        plot_mt_pt(inp)
    elif True in list(inp[1].values()) and True in list(inp[2].values()):
        plot_nt_pt(inp)
    elif True in list(inp[2].values()) and True in list(inp[0].values()):
        plot_mt_nt(inp)
def submit_inputs_II(): 
    st.session_state.input_state = convert_input_state(st.session_state.input_state)
    inp=st.session_state.input_state
    if True not in list(inp[0].values()) and True not in list(inp[1].values()) and True not in list(inp[2].values()):
        pass
    elif True not in list(inp[0].values()) and True not in list(inp[1].values()):
        plot_nt_II(inp)
    elif True not in list(inp[1].values()) and True not in list(inp[2].values()):
        plot_mt_II(inp)
    elif True not in list(inp[0].values()) and True not in list(inp[2].values()):
        plot_pt_II(inp)
    elif True in list(inp[0].values()) and True in list(inp[1].values()):
        plot_mt_pt_II(inp)
    elif True in list(inp[1].values()) and True in list(inp[2].values()):
        plot_nt_pt_II(inp)
    elif True in list(inp[2].values()) and True in list(inp[0].values()):
        plot_mt_nt_II(inp)
def submit_inputs_glow(): 
    st.session_state.input_state = convert_input_state(st.session_state.input_state)
    inp=st.session_state.input_state
    if True not in list(inp[0].values()) and True not in list(inp[1].values()) and True not in list(inp[2].values()):
        pass
    elif True not in list(inp[0].values()) and True not in list(inp[1].values()):
        plot_nt_glow(inp)
    elif True not in list(inp[1].values()) and True not in list(inp[2].values()):
        plot_mt_glow(inp)
    elif True not in list(inp[0].values()) and True not in list(inp[2].values()):
        plot_pt_glow(inp)
    elif True in list(inp[0].values()) and True in list(inp[1].values()):
        plot_mt_pt_glow(inp)
    elif True in list(inp[1].values()) and True in list(inp[2].values()):
        plot_nt_pt_glow(inp)
    elif True in list(inp[2].values()) and True in list(inp[0].values()):
        plot_mt_nt_glow(inp)
def submit_inputs_ac(): 
    st.session_state.input_state = convert_input_state(st.session_state.input_state)
    inp=st.session_state.input_state
    if True not in list(inp[0].values()) and True not in list(inp[1].values()) and True not in list(inp[2].values()):
        pass
    elif True not in list(inp[0].values()) and True not in list(inp[1].values()):
        plot_nt_ac(inp)
    elif True not in list(inp[1].values()) and True not in list(inp[2].values()):
        plot_mt_ac(inp)
    elif True not in list(inp[0].values()) and True not in list(inp[2].values()):
        plot_pt_ac(inp)
    elif True in list(inp[0].values()) and True in list(inp[1].values()):
        plot_mt_pt_ac(inp)
    elif True in list(inp[1].values()) and True in list(inp[2].values()):
        plot_nt_pt_ac(inp)
    elif True in list(inp[2].values()) and True in list(inp[0].values()):
        plot_mt_nt_ac(inp)
def handle_all_checkbox(section):
    if section not in st.session_state.open_sections:
        return 

    all_key = f"all_{section}"
    all_checked = st.sidebar.checkbox("All", key=all_key, value=all(st.session_state.input_state[section].values()))
    if all_checked:
        for key in st.session_state.input_state[section]:
            st.session_state.input_state[section][key] = True
    else:
        for key in st.session_state.input_state[section]:
            st.session_state.input_state[section][key] = st.sidebar.checkbox(
                key, value=st.session_state.input_state[section][key]
            )

# Function to handle opening and closing sections
def handle_section_toggle(section):
    if section in st.session_state.open_sections:
        st.session_state.open_sections.remove(section)
    elif len(st.session_state.open_sections) < 2:
        st.session_state.open_sections.append(section)

def reset_checkboxes(section):
    for key in st.session_state.input_state[section]:
        st.session_state.input_state[section][key] = False


def individual_plot(sample_no):
    
    df = st.session_state.df
    r_time_id = st.session_state.refined_df["R Idxs"]
    rh_time_id = st.session_state.refined_df["RH Idxs"]
    temp_time_id = st.session_state.refined_df["Temp Idxs"]
    #batch_data = st.session_state.batch_data
    refined_df=st.session_state.refined_df
    golden_index=st.session_state.golden_index
    idxs = st.session_state.refined_df["Idxs"]
    import streamlit.components.v1 as components
    refined_df["RH mins"] = pd.to_numeric(refined_df["RH mins"], errors='coerce')
    green_limit = st.session_state.green_limit_global
    yellow_limit= st.session_state.yellow_limit_global
    # Extract relevant columns
    pump_time = refined_df["RH mins"].tolist()
    date = np.array(refined_df["BATCH START TIME"])
    batch_id = refined_df['BATCH ID'].to_list()
    for i in range(len(date)):
        date[i]=date[i][:5]
    # Create DataFrame for Altair
    data2 = pd.DataFrame({
        'Batch': range(len(pump_time)),
        'BATCH ID': batch_id,
        'Pumpdown Time (minutes)': pump_time,
        'Date': date,
    })
    selection = alt.selection_single(fields=['Batch'], nearest=False, on='click', empty='none')
    # Categorize based on limits
    data2['Category'] = pd.cut(data2['Pumpdown Time (minutes)'],
                                bins=[-float('inf'), green_limit, yellow_limit, float('inf')],
                                labels=['green_pumptime', 'yellow_pumptime', 'red_pumptime'])
    scatter = alt.Chart(data2).mark_circle(size=60).encode(
        x='Batch:Q',
        y='Pumpdown Time (minutes):Q',
        color=alt.Color('Category:N', scale=alt.Scale(domain=['green_pumptime', 'yellow_pumptime', 'red_pumptime'],
                                                    range=['#00dd00', 'yellow', 'red']),legend=None),
        tooltip=['BATCH ID:N', 'Pumpdown Time (minutes):Q', 'Date:N']
    ).add_selection(
        selection
    ).interactive()
    base = alt.Chart(data2).encode(
        x=alt.X('Batch:Q', title='Batches', )
    )
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )
    # Horizontal lines
    line_green = alt.Chart(pd.DataFrame({'y': [green_limit]})).mark_rule(color='#00dd00',size=2,strokeDash=[5, 5]).encode(y='y:Q')
    line_yellow = alt.Chart(pd.DataFrame({'y': [yellow_limit]})).mark_rule(color='yellow',size=2,strokeDash=[5, 5]).encode(y='y:Q')

    # Combine scatter plot with lines
    chart2 = (scatter + line_green + line_yellow+text).properties(width=800, height=400)
    st.altair_chart(chart2, use_container_width=True)


    batch_options = [f"{st.session_state.df['BATCH ID'][i[0]]}  {st.session_state.df['DATE TIME'][i[0]]}" for i in st.session_state.refined_df['Idxs']]
    default_value = batch_options[golden_index]
    selected_batch = st.selectbox("Golden Batch :", batch_options, index=batch_options.index(default_value))
    arr=selected_batch.split(" ")
    golden_batch=arr[0]
    for i in range(len(refined_df)):
        if refined_df['BATCH ID'][i] == golden_batch:
            golden_index=i
    # Display the selected value (optional, for verification)
    st.write("Selected batch:", selected_batch)
    # Prepare the data for Altair
    time_values = np.arange(idxs[sample_no][0], rh_time_id[sample_no][1] + 100, 1)
    pressure_values = df['HIGH VACUM ACTUAL'][idxs[sample_no][0]:rh_time_id[sample_no][1] + 100].values
    pressure_values_golden=df['HIGH VACUM ACTUAL'][idxs[golden_index][0]:idxs[golden_index][0]+(rh_time_id[sample_no][1] + 100-idxs[sample_no][0])].values
    date_values = df['DATE TIME'][idxs[sample_no][0]:rh_time_id[sample_no][1] + 100].values

    data = pd.DataFrame({
        'Time': time_values,
        'Pressure': pressure_values,
        'Golden Pressure':pressure_values_golden,
        'Date': date_values
    })

    # Custom tick indices and labels
    tick_indices = np.arange(idxs[sample_no][0], rh_time_id[sample_no][1] + 100, int((rh_time_id[sample_no][1] + 100 - idxs[sample_no][0]) * 0.16))
    custom_labels = [str(x[11:]) for x in df['DATE TIME'][tick_indices]]

    # Prepare tick_labels_dict as a JS object string
    tick_labels_dict = {int(tick_indices[i]): custom_labels[i] for i in range(len(tick_indices))}
    tick_labels_js = str(tick_labels_dict).replace("'", "\"")
    label_expr = 'datum.label'
    for key, value in tick_labels_dict.items():
        label_expr = f"datum.value == {key} ? '{value}' : " + label_expr
    # Base chart
    base = alt.Chart(data).encode(
        x=alt.X('Time:Q', title='Time',  
                axis=alt.Axis(values=tick_indices,labelExpr=label_expr))
    )

    # Line chart
    line = base.mark_line(color="#008081").encode(
        y=alt.Y('Pressure:Q', title='Pressure log'),
        tooltip=alt.value(None)
    ).properties(
        title='Vacuum Pressure vs time: Batch ' + refined_df['BATCH ID'][sample_no] + "  " + str(st.session_state.df['DATE TIME'][refined_df['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    line_golden = base.mark_line(color="#dd9900").encode(
        y=alt.Y('Golden Pressure:Q', title='Pressure log'),
        tooltip=alt.value(None)
    ).properties(
        #title='Vacuum Pressure vs time: Batch ' + refined_df['BATCH ID'][sample_no] + "  " + str(st.session_state.df['DATE TIME'][refined_df['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )

    # Scatter points for R_Time, RH_Time, and Temp_Time
    r_time_point_golden = pd.DataFrame({
        'Time': [r_time_id[golden_index][1]-r_time_id[golden_index][0]+r_time_id[sample_no][0]],
        'Pressure': [df['HIGH VACUM ACTUAL'][r_time_id[golden_index][1]]],
        'Label': ['R_Time of Golden Batch']
    })

    rh_time_point_golden = pd.DataFrame({
        'Time': [rh_time_id[golden_index][1]-rh_time_id[golden_index][0]+rh_time_id[sample_no][0]],
        'Pressure': [df['HIGH VACUM ACTUAL'][rh_time_id[golden_index][1]]],
        'Label': ['RH_Time of Golden Batch']
    })

    temp_time_point_golden = pd.DataFrame({
        'Time': [temp_time_id[golden_index][1]-temp_time_id[golden_index][0]+temp_time_id[sample_no][0]],
        'Pressure': [df['HIGH VACUM ACTUAL'][temp_time_id[golden_index][1]]],
        'Label': ['Temp_Time of Golden Batch']
    })
    r_time_point = pd.DataFrame({
        'Time': [r_time_id[sample_no][1]],
        'Pressure': [df['HIGH VACUM ACTUAL'][r_time_id[sample_no][1]]],
        'Label': ['R_Time (rough vacuum ends, high vacuum starts)']
    })

    rh_time_point = pd.DataFrame({
        'Time': [rh_time_id[sample_no][1]],
        'Pressure': [df['HIGH VACUM ACTUAL'][rh_time_id[sample_no][1]]],
        'Label': ['RH_Time (Total rough and high vacuum time)']
    })

    temp_time_point = pd.DataFrame({
        'Time': [temp_time_id[sample_no][1]],
        'Pressure': [df['HIGH VACUM ACTUAL'][temp_time_id[sample_no][1]]],
        'Label': ['Temp_Time (Time to reach chamber set temperature)']
    })

    scatter_r = alt.Chart(r_time_point).mark_point(color='blue',size=100,filled=True).encode(
        x='Time:Q',
        y='Pressure:Q',
        tooltip=alt.TooltipValue(("R time :"+str(refined_df["R Time"][sample_no][0][2])+" mins "+str(refined_df["R Time"][sample_no][0][3])+" secs"))
    ).properties(width=600, height=400)

    scatter_rh = alt.Chart(rh_time_point).mark_point(color='red',size=100,filled=True).encode(
        x='Time:Q',
        y='Pressure:Q',
        tooltip=alt.TooltipValue(("RH time :"+str(refined_df["RH Time"][sample_no][0][2])+" mins "+str(refined_df["RH Time"][sample_no][0][3])+" secs"))
    ).properties(width=600, height=400)

    scatter_temp = alt.Chart(temp_time_point).mark_point(color='green',size=100,filled=True).encode(
        x='Time:Q',
        y='Pressure:Q',
        tooltip=alt.TooltipValue(("Temp time :"+str(refined_df["Temp Time"][sample_no][0][2])+" mins "+str(refined_df["Temp Time"][sample_no][0][3])+" secs"))
    ).properties(width=600, height=400)
    scatter_r_golden = alt.Chart(r_time_point_golden).mark_point(color='blue',size=100,filled=True).encode(
        x='Time:Q',
        y='Pressure:Q',
        tooltip=alt.TooltipValue(("R time of Golden Batch:"+str(refined_df["R Time"][golden_index][0][2])+" mins "+str(refined_df["R Time"][golden_index][0][3])+" secs"))
    ).properties(width=600, height=400)

    scatter_rh_golden = alt.Chart(rh_time_point_golden).mark_point(color='red',size=100,filled=True).encode(
        x='Time:Q',
        y='Pressure:Q',
        tooltip=alt.TooltipValue(("RH time of Golden Batch:"+str(refined_df["RH Time"][golden_index][0][2])+" mins "+str(refined_df["RH Time"][golden_index][0][3])+" secs"))
    ).properties(width=600, height=400)

    scatter_temp_golden = alt.Chart(temp_time_point_golden).mark_point(color='green',size=100,filled=True).encode(
        x='Time:Q',
        y='Pressure:Q',
        tooltip=alt.TooltipValue(("Temp time of Golden Batch:"+str(refined_df["Temp Time"][golden_index][0][2])+" mins "+str(refined_df["Temp Time"][golden_index][0][3])+" secs"))
    ).properties(width=600, height=400)

    # Combine the line chart and scatter plots
    chart = alt.layer(line, scatter_r, scatter_rh, scatter_temp).configure_legend(
        orient='bottom'
    ).configure_axisX(
        labelFontSize=10,
        labelAngle=0,
        titleFontSize=12
    )
    if st.checkbox("Show Golden Batch"):
        chart = alt.layer(line,line_golden, scatter_r, scatter_rh, scatter_temp,scatter_r_golden,scatter_rh_golden,scatter_temp_golden)

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    data = {
        ' ':['','🔴', '🔵','🟢','','','',''],
        #'Batch ID':[str(refined_df['BATCH ID'][sample_no]) + "  " + str(st.session_state.df['DATE TIME'][refined_df['Idxs'][sample_no][0]]),str(refined_df['BATCH ID'][golden_index]) + "  " + str(st.session_state.df['DATE TIME'][refined_df['Idxs'][golden_index][0]])],
        'Parameters': ['Batch ID','RH time', 'R time', 'Temp time','Material Type','Product Type','Pre Storage Type','Coating Type'],
        'Actual Batch': [str(refined_df['BATCH ID'][sample_no]) + "  " + str(st.session_state.df['DATE TIME'][refined_df['Idxs'][sample_no][0]]),str(refined_df["RH Time"][sample_no][0][2])+" mins "+str(refined_df["RH Time"][sample_no][0][3])+" secs", str(refined_df["R Time"][sample_no][0][2])+" mins "+str(refined_df["R Time"][sample_no][0][3])+" secs", str(refined_df["Temp Time"][sample_no][0][2])+" mins "+str(refined_df["Temp Time"][sample_no][0][3])+" secs", str(refined_df['MATERIAL TYPE'][sample_no]), str(refined_df['PRODUCT TYPE'][sample_no]), str(refined_df['PRE STORAGE'][sample_no]), str(refined_df['COATING TYPE'][sample_no])],
        'Golden Batch': [str(refined_df['BATCH ID'][golden_index]) + "  " + str(st.session_state.df['DATE TIME'][refined_df['Idxs'][golden_index][0]]),str(refined_df["RH Time"][golden_index][0][2])+" mins "+str(refined_df["RH Time"][golden_index][0][3])+" secs", str(refined_df["R Time"][golden_index][0][2])+" mins "+str(refined_df["R Time"][golden_index][0][3])+" secs", str(refined_df["Temp Time"][golden_index][0][2])+" mins "+str(refined_df["Temp Time"][golden_index][0][3])+" secs", str(refined_df['MATERIAL TYPE'][golden_index]), str(refined_df['PRODUCT TYPE'][golden_index]), str(refined_df['PRE STORAGE'][golden_index]), str(refined_df['COATING TYPE'][golden_index])]
    }
    table_df = pd.DataFrame(data)
    table_df = table_df.reset_index(drop=True)
    table_str = table_df.to_html(index=False, escape=False)

    # Display the table as HTML
    st.markdown(table_str, unsafe_allow_html=True)
    if st.button("Export Data"):
        from PIL import Image, ImageDraw, ImageFont
        chart = alt.layer(line,line_golden, scatter_r, scatter_rh, scatter_temp,scatter_r_golden,scatter_rh_golden,scatter_temp_golden).properties(
            width=600,
            height=300,
            background='white'
        ).configure_axis(
            labelColor='black',  # Set the font color for axis labels
            titleColor='black'   # Set the font color for axis titles
        ).configure_title(
            color='black'  # Set the font color for the chart title
        ).configure_legend(
            labelColor='black',  # Set the font color for legend labels
            titleColor='black'   # Set the font color for legend titles
        )
        chart.save('Pumpdown Curve alone.png', engine="vl-convert",ppi=200) 
        cell_width = 550
        cell_height = 50
        padding = 10
        font_path = "arial.ttf"  # Replace with the path to your font file
        font_size = 30  # Increase this for larger text
        font = ImageFont.truetype(font_path, font_size)

        # Calculate the image size
        img_width = cell_width * len(data) 
        img_height = cell_height * (len(data[' ']) + 1)  # +1 for the header

        # Create the image
        img = Image.new('RGB', (img_width, img_height), color='white')
        draw = ImageDraw.Draw(img)

        # Define the colors for the dots
        colors = [(255, 0, 0), (0, 0, 255), (0, 180, 40)]  # Red, Blue, Green

        # Draw the table content
        for i, key in enumerate(data.keys()):
            for j, value in enumerate(data[key]):
                if j == 0:  # Header
                    text_x = i * cell_width + padding
                    text_y = j * cell_height + padding
                    draw.text((text_x, text_y), key, font=ImageFont.truetype("arialbd.ttf" , font_size), fill='#222222')
                    draw.text((text_x, text_y + cell_height), value, font=font, fill='black')
                elif i == 0 and j > 0 and j<4:  # Draw circles instead of text
                    circle_x = i * cell_width + padding + 480
                    circle_y = j * cell_height + padding + cell_height+5
                    radius = 13
                    color = colors[j-1]
                    draw.ellipse([circle_x, circle_y, circle_x + 2 * radius, circle_y + 2 * radius], fill=color, outline=color)
                else:
                    text_x = i * cell_width + padding
                    text_y = j * cell_height + padding + cell_height
                    draw.text((text_x, text_y), value, font=font, fill='black')

        # Save the image
        img.save('table_image.png')
        image1 = Image.open('Pumpdown Curve alone.png')  # Replace with the path to your first image
        image2 = Image.open('table_image.png')  # Replace with the path to your second image

        # Get the dimensions of the images
        width1, height1 = image1.size
        width2, height2 = image2.size

        # Calculate the dimensions of the combined image
        combined_width = max(width1, width2)+50
        combined_height = height1 + height2+300

        # Create a new image with the calculated dimensions
        combined_image = Image.new('RGB', (combined_width, combined_height), color='white')

        # Paste the first image at the top
        combined_image.paste(image1, (50, 100))

        # Paste the second image below the first image
        combined_image.paste(image2, (-300, height1+200))

        # Save the combined image
        combined_image.save('Pumpdown Curve.png')
        import os
        if os.path.exists('Pumpdown Curve alone.png'):
            # Delete the file
            os.remove('Pumpdown Curve alone.png')
            os.remove('table_image.png')
        #st.altair_chart(chart, use_container_width=True)
def individual_plot_II(sample_no):
    
    df_II = st.session_state.df_II
    h_II_time_id = st.session_state.refined_df_II["H_II Idxs"]
    temp_II_time_id = st.session_state.refined_df_II["Temp_II Idxs"]
    #batch_data = st.session_state.batch_data
    refined_df_II=st.session_state.refined_df_II
    golden_index_II=st.session_state.golden_index_II
    idxs_II = st.session_state.refined_df_II["Idxs_II"]
    import streamlit.components.v1 as components
    refined_df_II["H_II mins"] = pd.to_numeric(refined_df_II["H_II mins"], errors='coerce')
    green_limit = st.session_state.green_limit_global_II
    yellow_limit= st.session_state.yellow_limit_global_II
    # Extract relevant columns
    pump_time = refined_df_II["H_II mins"].tolist()
    date = np.array(refined_df_II["BATCH START TIME"])
    batch_id = refined_df_II['BATCH ID'].to_list()
    for i in range(len(date)):
        date[i]=date[i][:5]
    # Create DataFrame for Altair
    data2 = pd.DataFrame({
        'Batch': range(len(pump_time)),
        'BATCH ID': batch_id,
        'Pumpdown Time (minutes)': pump_time,
        'Date': date,
    })
    selection = alt.selection_single(fields=['Batch'], nearest=False, on='click', empty='none')
    # Categorize based on limits
    data2['Category'] = pd.cut(data2['Pumpdown Time (minutes)'],
                                bins=[-float('inf'), green_limit, yellow_limit, float('inf')],
                                labels=['green_pumptime', 'yellow_pumptime', 'red_pumptime'])
    scatter = alt.Chart(data2).mark_circle(size=60).encode(
        x='Batch:Q',
        y='Pumpdown Time (minutes):Q',
        color=alt.Color('Category:N', scale=alt.Scale(domain=['green_pumptime', 'yellow_pumptime', 'red_pumptime'],
                                                    range=['#00dd00', 'yellow', 'red']),legend=None),
        tooltip=['BATCH ID:N', 'Pumpdown Time (minutes):Q', 'Date:N']
    ).add_selection(
        selection
    ).interactive()
    base = alt.Chart(data2).encode(
        x=alt.X('Batch:Q', title='Batches', )
    )
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )
    # Horizontal lines
    line_green = alt.Chart(pd.DataFrame({'y': [green_limit]})).mark_rule(color='#00dd00',size=2,strokeDash=[5, 5]).encode(y='y:Q')
    line_yellow = alt.Chart(pd.DataFrame({'y': [yellow_limit]})).mark_rule(color='yellow',size=2,strokeDash=[5, 5]).encode(y='y:Q')

    # Combine scatter plot with lines
    chart2 = (scatter + line_green + line_yellow+text).properties(width=800, height=400)
    st.altair_chart(chart2, use_container_width=True)


    batch_options = [f"{st.session_state.df_II['BATCH ID'][i[0]]}  {st.session_state.df_II['DATE TIME'][i[0]]}" for i in st.session_state.refined_df_II['Idxs_II']]
    default_value = batch_options[golden_index_II]
    selected_batch = st.selectbox("Golden Batch :", batch_options, index=batch_options.index(default_value))
    arr=selected_batch.split(" ")
    golden_batch_II=arr[0]
    for i in range(len(refined_df_II)):
        if refined_df_II['BATCH ID'][i] == golden_batch_II:
            golden_index_II=i
    # Display the selected value (optional, for verification)
    st.write("Selected batch:", selected_batch)
    # Prepare the data for Altair
    time_values = np.arange(idxs_II[sample_no][0],idxs_II[sample_no][1], 1)
    pressure_values = df_II['HIGH VACUUM II ACTUAL'][idxs_II[sample_no][0]:idxs_II[sample_no][1]].values
    if (idxs_II[sample_no][1] - idxs_II[sample_no][0])>(idxs_II[golden_index_II][1]-idxs_II[golden_index_II][0]):
        pressure_values_golden=df_II['HIGH VACUUM II ACTUAL'][idxs_II[golden_index_II][0]:idxs_II[golden_index_II][1]]
        nan_values = pd.Series([np.nan] * ((idxs_II[sample_no][1] - idxs_II[sample_no][0])-(idxs_II[golden_index_II][1]-idxs_II[golden_index_II][0])))
        pressure_values_golden = pd.concat([pressure_values_golden, nan_values], ignore_index=True)
    else:
        pressure_values_golden=df_II['HIGH VACUUM II ACTUAL'][idxs_II[golden_index_II][0]:idxs_II[sample_no][1]-idxs_II[sample_no][0]+idxs_II[golden_index_II][0]].values
    date_values = df_II['DATE TIME'][idxs_II[sample_no][0]:idxs_II[sample_no][1]].values

    data = pd.DataFrame({
        'Time': time_values,
        'Pressure': pressure_values,
        'Golden Pressure':pressure_values_golden,
        'Date': date_values
    })

    # Custom tick indices and labels
    tick_indices = np.arange(idxs_II[sample_no][0], idxs_II[sample_no][1], int((idxs_II[sample_no][1]- idxs_II[sample_no][0]) * 0.16))
    custom_labels = [str(x[11:]) for x in df_II['DATE TIME'][tick_indices]]

    # Prepare tick_labels_dict as a JS object string
    tick_labels_dict = {int(tick_indices[i]): custom_labels[i] for i in range(len(tick_indices))}
    tick_labels_js = str(tick_labels_dict).replace("'", "\"")
    label_expr = 'datum.label'
    for key, value in tick_labels_dict.items():
        label_expr = f"datum.value == {key} ? '{value}' : " + label_expr
    # Base chart
    base = alt.Chart(data).encode(
        x=alt.X('Time:Q', title='Time',  
                axis=alt.Axis(values=tick_indices,labelExpr=label_expr))
    )

    # Line chart
    line = base.mark_line(color="#008081").encode(
        y=alt.Y('Pressure:Q', title='Pressure log'),
        tooltip=alt.value(None)
    ).properties(
        title='Vacuum Pressure vs time: Batch ' + refined_df_II['BATCH ID'][sample_no] + "  " + str(st.session_state.df_II['DATE TIME'][refined_df_II['Idxs_II'][sample_no][0]]),
        width=600,
        height=400
    )
    line_golden = base.mark_line(color="#dd9900").encode(
        y=alt.Y('Golden Pressure:Q', title='Pressure log'),
        tooltip=alt.value(None)
    ).properties(
        #title='Vacuum Pressure vs time: Batch ' + refined_df_II['BATCH ID'][sample_no] + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['idxs_II'][sample_no][0]]),
        width=600,
        height=400
    )



    rh_time_point_golden = pd.DataFrame({
        'Time': [h_II_time_id[golden_index_II][1]-h_II_time_id[golden_index_II][0]+h_II_time_id[sample_no][0]],
        'Pressure': [df_II['HIGH VACUUM II ACTUAL'][h_II_time_id[golden_index_II][1]]],
        'Label': ['RH_Time of Golden Batch']
    })

    temp_time_point_golden = pd.DataFrame({
        'Time': [temp_II_time_id[golden_index_II][1]-temp_II_time_id[golden_index_II][0]+temp_II_time_id[sample_no][0]],
        'Pressure': [df_II['HIGH VACUUM II ACTUAL'][temp_II_time_id[golden_index_II][1]]],
        'Label': ['Temp_Time of Golden Batch']
    })


    rh_time_point = pd.DataFrame({
        'Time': [h_II_time_id[sample_no][1]],
        'Pressure': [df_II['HIGH VACUUM II ACTUAL'][h_II_time_id[sample_no][1]]],
        'Label': ['RH_Time (Total rough and high vacuum time)']
    })

    temp_time_point = pd.DataFrame({
        'Time': [temp_II_time_id[sample_no][1]],
        'Pressure': [df_II['HIGH VACUUM II ACTUAL'][temp_II_time_id[sample_no][1]]],
        'Label': ['Temp_Time (Time to reach chamber set temperature)']
    })



    scatter_rh = alt.Chart(rh_time_point).mark_point(color='red',size=100,filled=True).encode(
        x='Time:Q',
        y='Pressure:Q',
        tooltip=alt.TooltipValue(("H_II Time :"+str(refined_df_II["H_II Time"][sample_no][0][2])+" mins "+str(refined_df_II["H_II Time"][sample_no][0][3])+" secs"))
    ).properties(width=600, height=400)

    scatter_temp = alt.Chart(temp_time_point).mark_point(color='green',size=100,filled=True).encode(
        x='Time:Q',
        y='Pressure:Q',
        tooltip=alt.TooltipValue(("Temp_II Time :"+str(refined_df_II["Temp_II Time"][sample_no][0][2])+" mins "+str(refined_df_II["Temp_II Time"][sample_no][0][3])+" secs"))
    ).properties(width=600, height=400)


    scatter_rh_golden = alt.Chart(rh_time_point_golden).mark_point(color='red',size=100,filled=True).encode(
        x='Time:Q',
        y='Pressure:Q',
        tooltip=alt.TooltipValue(("H_II Time of Golden Batch:"+str(refined_df_II["H_II Time"][golden_index_II][0][2])+" mins "+str(refined_df_II["H_II Time"][golden_index_II][0][3])+" secs"))
    ).properties(width=600, height=400)

    scatter_temp_golden = alt.Chart(temp_time_point_golden).mark_point(color='green',size=100,filled=True).encode(
        x='Time:Q',
        y='Pressure:Q',
        tooltip=alt.TooltipValue(("Temp_II Time of Golden Batch:"+str(refined_df_II["Temp_II Time"][golden_index_II][0][2])+" mins "+str(refined_df_II["Temp_II Time"][golden_index_II][0][3])+" secs"))
    ).properties(width=600, height=400)

    # Combine the line chart and scatter plots
    chart = alt.layer(line, scatter_rh, scatter_temp).configure_legend(
        orient='bottom'
    ).configure_axisX(
        labelFontSize=10,
        labelAngle=0,
        titleFontSize=12
    )
    if st.checkbox("Show Golden Batch"):
        chart = alt.layer(line,line_golden, scatter_rh, scatter_temp,scatter_rh_golden,scatter_temp_golden)

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    data = {
        ' ':['','🔴','🟢','','','',''],
        #'Batch ID':[str(refined_df_II['BATCH ID'][sample_no]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][sample_no][0]]),str(refined_df_II['BATCH ID'][golden_index_II]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][golden_index_II][0]])],
        'Parameters': ['Batch ID','H_II Time', 'Temp_II Time','Material Type','Product Type','Pre Storage Type','Coating Type'],
        'Actual Batch': [str(refined_df_II['BATCH ID'][sample_no]) + "  " + str(st.session_state.df_II['DATE TIME'][refined_df_II['Idxs_II'][sample_no][0]]),str(refined_df_II["H_II Time"][sample_no][0][2])+" mins "+str(refined_df_II["H_II Time"][sample_no][0][3])+" secs", str(refined_df_II["Temp_II Time"][sample_no][0][2])+" mins "+str(refined_df_II["Temp_II Time"][sample_no][0][3])+" secs", str(refined_df_II['MATERIAL TYPE'][sample_no]), str(refined_df_II['PRODUCT TYPE'][sample_no]), str(refined_df_II['PRE STORAGE'][sample_no]), str(refined_df_II['COATING TYPE'][sample_no])],
        'Golden Batch': [str(refined_df_II['BATCH ID'][golden_index_II]) + "  " + str(st.session_state.df_II['DATE TIME'][refined_df_II['Idxs_II'][golden_index_II][0]]),str(refined_df_II["H_II Time"][golden_index_II][0][2])+" mins "+str(refined_df_II["H_II Time"][golden_index_II][0][3])+" secs", str(refined_df_II["Temp_II Time"][golden_index_II][0][2])+" mins "+str(refined_df_II["Temp_II Time"][golden_index_II][0][3])+" secs", str(refined_df_II['MATERIAL TYPE'][golden_index_II]), str(refined_df_II['PRODUCT TYPE'][golden_index_II]), str(refined_df_II['PRE STORAGE'][golden_index_II]), str(refined_df_II['COATING TYPE'][golden_index_II])]
    }
    table_df = pd.DataFrame(data)
    table_df = table_df.reset_index(drop=True)
    table_str = table_df.to_html(index=False, escape=False)

    # Display the table as HTML
    st.markdown(table_str, unsafe_allow_html=True)
def individual_plot_glow(sample_no):
    
    df_glow = st.session_state.df_glow

    #batch_data = st.session_state.batch_data
    refined_df_glow=st.session_state.refined_df_glow
    idxs=refined_df_glow['V Idxs']
    golden_glow_process=st.session_state.golden_glow_process
    import streamlit.components.v1 as components
    st.write("Selected batch:", selected_batch)
    # Prepare the data for Altair
    time_values = np.arange(idxs[sample_no][0],idxs[sample_no][1], 1)
    voltage_values = df_glow['BIAS INITIAL VOLTAGE ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    current_values = df_glow['BIAS CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    gas_values = df_glow['AR GAS ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    arc_values = df_glow['BIAS ARC COUNT'][idxs[sample_no][0]:idxs[sample_no][1]].values
    date_values = df_glow['DATE TIME'][idxs[sample_no][0]:idxs[sample_no][1]].values
    encoder_position=df_glow['ENCODER POSITION'][idxs[sample_no][0]:idxs[sample_no][1]].values
    encoder_position=encoder_position/360
    vacuum_values=df_glow['GLOW VACUUM ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    temp_values=df_glow['CHAMBER TEMP ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    tvp_values=df_glow['TVP POSITION ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values

    golden_voltage_values=golden_glow_process['BIAS INITIAL VOLTAGE ACTUAL'].values
    golden_current_values=golden_glow_process['BIAS CURRENT ACTUAL'].values
    golden_gas_values=golden_glow_process['AR GAS ACTUAL'].values
    golden_vacuum_values=golden_glow_process['GLOW VACUUM ACTUAL'].values
    golden_temp_values=golden_glow_process['CHAMBER TEMP ACTUAL'].values
    golden_tvp_values=golden_glow_process['TVP POSITION ACTUAL'].values

    data = pd.DataFrame({
        'Time': time_values,
        'Voltage': voltage_values,
        'Current': current_values,
        'Ar Gas': gas_values,
        'Bias Arc':arc_values,
        'Encoder Position':encoder_position,
        'Golden Voltage':golden_voltage_values,
        'Golden Current':golden_current_values,
        'Golden Ar Gas':golden_gas_values,
        'Date': date_values,
        'Vacuum': vacuum_values,
        'Golden Vacuum': golden_vacuum_values,
        'Temperature':temp_values,
        'Golden Temperature':golden_temp_values,
        'TVP':tvp_values,
        'Golden TVP':golden_tvp_values,

    })
    tick_indices = np.arange(idxs[sample_no][0], idxs[sample_no][1], int((idxs[sample_no][1]- idxs[sample_no][0]) * 0.16))
    custom_labels = [str(x[11:]) for x in df_glow['DATE TIME'][tick_indices]]

    # Prepare tick_labels_dict as a JS object string
    tick_labels_dict = {int(tick_indices[i]): custom_labels[i] for i in range(len(tick_indices))}
    tick_labels_js = str(tick_labels_dict).replace("'", "\"")
    label_expr = 'datum.label'
    for key, value in tick_labels_dict.items():
        label_expr = f"datum.value == {key} ? '{value}' : " + label_expr
    # Base chart
    base = alt.Chart(data).encode(
        x=alt.X('Time:Q', title='Time',  
                axis=alt.Axis(values=tick_indices,labelExpr=label_expr))
    )
    # Line chart
    empty_line = base.mark_line(color="black").encode(
        y=alt.Y('Current:Q'),
        tooltip=alt.value(None)
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    v_line = base.mark_line(color="#00a0a1").encode(
        y=alt.Y('Voltage:Q',title='Features'),
        tooltip=['Voltage','Date']
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_v_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Voltage:Q'),
        tooltip=alt.value(None)
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    c_line = base.mark_line(color="#40d081").encode(
        y=alt.Y('Current:Q'),
        tooltip=['Current','Date']
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_c_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Current:Q'),
        tooltip=alt.value(None)
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    g_line = base.mark_line(color="#d04071").encode(
        y=alt.Y('Ar Gas:Q'),
        tooltip=['Ar Gas','Date']
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_g_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Ar Gas:Q'),
        tooltip=alt.value(None)
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    arc_bar = base.mark_bar(color="#40a0a1").encode(
        y=alt.Y('Bias Arc:Q', title='Bias Arc'),
        tooltip=alt.value(None)
    ).properties(
        width=600,
        height=150
    )
    encoder_bar= base.mark_bar(color="#333333").encode(
        y=alt.Y('Encoder Position:Q', title='Encoder'),
        tooltip=alt.value(None)
    ).properties(
        width=600,
        height=150
    )
    vacuum_line = base.mark_line(color="#a0a0a1").encode(
        y=alt.Y('Vacuum:Q'),
        tooltip=['Vacuum','Date']
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_vacuum_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Vacuum:Q'),
        tooltip=alt.value(None)
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    t_line = base.mark_line(color="#a06001").encode(
        y=alt.Y('Temperature:Q'),
        tooltip=['Temperature','Date']
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_t_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Temperature:Q'),
        tooltip=alt.value(None)
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    tvp_line = base.mark_line(color="#a060a1").encode(
        y=alt.Y('TVP:Q'),
        tooltip=['TVP','Date']
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_tvp_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden TVP:Q'),
        tooltip=alt.value(None)
    ).properties(
        title='Glow Discharge: Batch ' + refined_df_glow['BATCH ID'][sample_no] + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    chart=empty_line
    golden_inp=st.checkbox("Show Golden Batch "+"("+str(list(golden_glow_process['BATCH ID'])[0])+" "+str(list(golden_glow_process['DATE TIME'])[0])+")")

    col1, col2, col3, col4,col5,col6 = st.columns(6)

    # Add checkboxes to each column
    with col1:
        bias_voltage = st.checkbox("Bias Voltage",value=True)

    with col2:
        bias_current = st.checkbox("Bias Current",value=True)

    with col3:
        ar_gas = st.checkbox("Ar Gas",value=True)
    with col4:
        vacuum = st.checkbox("Glow Vacuum",value=True)
    with col5:
        temperature = st.checkbox("Chamber Temperature",value=True)
    with col6:
        tvp = st.checkbox("TVP Position",value=True)
    chart=empty_line
    inps=[bias_voltage,bias_current,ar_gas,vacuum,temperature,tvp]
    plots=[[v_line,golden_v_line],[c_line,golden_c_line],[g_line,golden_g_line],[vacuum_line,golden_vacuum_line],[t_line,golden_t_line],[tvp_line,golden_tvp_line]]
    for i in range(len(inps)):
        if golden_inp==True:
            if inps[i]==True:
                chart+=plots[i][0]
                chart+=plots[i][1]
        else:
            if inps[i]==True:
                chart+=plots[i][0]
    st.altair_chart(chart,use_container_width=True)
    st.altair_chart(encoder_bar+arc_bar,use_container_width=True)
    golden_glow_details=st.session_state.golden_glow_details
    data = {
        #'Batch ID':[str(refined_df_II['BATCH ID'][sample_no]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][sample_no][0]]),str(refined_df_II['BATCH ID'][golden_index_II]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][golden_index_II][0]])],
        'Parameters': ['Batch ID','Voltage Irregularity', 'Current Irregularity','Ar Gas Irregularity','Bias Arc Count','Material Type','Product Type','Pre Storage Type','Coating Type'],
        'Actual Batch': [str(refined_df_glow['BATCH ID'][sample_no]) + "  " + str(st.session_state.df_glow['DATE TIME'][refined_df_glow['Idxs'][sample_no][0]]),str(refined_df_glow["V Irregulars"][sample_no]), str(refined_df_glow["I Irregulars"][sample_no]), str(refined_df_glow["Ar Gas Irregulars"][sample_no]),str(refined_df_glow["Arc total"][sample_no]),str(refined_df_glow['MATERIAL TYPE'][sample_no]), str(refined_df_glow['PRODUCT TYPE'][sample_no]), str(refined_df_glow['PRE STORAGE'][sample_no]), str(refined_df_glow['COATING TYPE'][sample_no])],
        'Golden Batch': [str(st.session_state.golden_glow_details['BATCH ID']) + "  " + str(golden_glow_details['BATCH START TIME']),str(golden_glow_details["V Irregulars"]), str(golden_glow_details["I Irregulars"]),str(golden_glow_details["Ar Gas Irregulars"]),str(golden_glow_details["Arc total"]), str(golden_glow_details['MATERIAL TYPE']), str(golden_glow_details['PRODUCT TYPE']), str(golden_glow_details['PRE STORAGE']), str(golden_glow_details['COATING TYPE'])]
    }
    table_df = pd.DataFrame(data)
    table_df = table_df.reset_index(drop=True)
    table_str = table_df.to_html(index=False, escape=False)

    # Display the table as HTML
    st.markdown(table_str, unsafe_allow_html=True)
def individual_plot_ac(sample_no):
    
    df_ac = st.session_state.df_ac

    #batch_data = st.session_state.batch_data
    refined_df_ac=st.session_state.refined_df_ac
    golden_ac_process=st.session_state.golden_ac_process
    import streamlit.components.v1 as components
    st.write("Selected batch:", selected_batch)
    # Prepare the data for Altair
    time_values = np.arange(idxs[sample_no][0],idxs[sample_no][1], 1)
    voltage_values = df_ac['BIAS VOLTAGE ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    current1_values = df_ac['ARC 1 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    current2_values = df_ac['ARC 2 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    current3_values = df_ac['ARC 3 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    gas_values = df_ac['AR GAS ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    arc_values = df_ac['BIAS ARC COUNT'][idxs[sample_no][0]:idxs[sample_no][1]].values
    date_values = df_ac['DATE TIME'][idxs[sample_no][0]:idxs[sample_no][1]].values
    #encoder_position=df_ac['ENCODER POSITION'][idxs[sample_no][0]:idxs[sample_no][1]].values
    #encoder_position=encoder_position/360
    vacuum_values=df_ac['GLOW VACUUM ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    temp_values=df_ac['CHAMBER TEMP ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
    tvp_values=df_ac['TVP POSITION ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values

    golden_voltage_values=golden_ac_process['BIAS VOLTAGE ACTUAL'].values
    golden_current1_values=golden_ac_process['ARC 1 CURRENT ACTUAL'].values
    golden_current2_values=golden_ac_process['ARC 2 CURRENT ACTUAL'].values
    golden_current3_values=golden_ac_process['ARC 3 CURRENT ACTUAL'].values
    golden_gas_values=golden_ac_process['AR GAS ACTUAL'].values
    golden_vacuum_values=golden_ac_process['GLOW VACUUM ACTUAL'].values
    golden_temp_values=golden_ac_process['CHAMBER TEMP ACTUAL'].values
    golden_tvp_values=golden_ac_process['TVP POSITION ACTUAL'].values

    if len(golden_voltage_values)>len(voltage_values):
        golden_voltage_values=golden_voltage_values[:len(voltage_values)]
        golden_current1_values=golden_current1_values[:len(voltage_values)]
        golden_current2_values=golden_current2_values[:len(voltage_values)]
        golden_current3_values=golden_current3_values[:len(voltage_values)]
        golden_gas_values=golden_gas_values[:len(voltage_values)]
        golden_vacuum_values=golden_vacuum_values[:len(voltage_values)]
        golden_temp_values=golden_temp_values[:len(voltage_values)]
        golden_tvp_values=golden_tvp_values[:len(voltage_values)]

    elif len(golden_voltage_values)<len(voltage_values):
        n=len(voltage_values)-len(golden_voltage_values)
        golden_voltage_values = np.append(golden_voltage_values, np.full(n, np.nan))
        golden_current1_values = np.append(golden_current1_values, np.full(n, np.nan))
        golden_current2_values = np.append(golden_current2_values, np.full(n, np.nan))
        golden_current3_values = np.append(golden_current3_values, np.full(n, np.nan))
        golden_gas_values = np.append(golden_gas_values, np.full(n, np.nan))
        golden_vacuum_values = np.append(golden_vacuum_values, np.full(n, np.nan))
        golden_temp_values = np.append(golden_temp_values, np.full(n, np.nan))
        golden_tvp_values = np.append(golden_tvp_values, np.full(n, np.nan))

    data = pd.DataFrame({
        'Time': time_values,
        'Voltage': voltage_values,
        'Arc 1 Current': current1_values,
        'Arc 2 Current': current2_values,
        'Arc 3 Current': current3_values,
        'Ar Gas': gas_values,
        'Bias Arc':arc_values,
        #'Encoder Position':encoder_position,
        'Golden Voltage':golden_voltage_values,
        'Golden Arc 1 Current':golden_current1_values,
        'Golden Arc 2 Current':golden_current2_values,
        'Golden Arc 3 Current':golden_current3_values,
        'Golden Ar Gas':golden_gas_values,
        'Date': date_values,
        'Vacuum': vacuum_values,
        'Golden Vacuum': golden_vacuum_values,
        'Temperature':temp_values,
        'Golden Temperature':golden_temp_values,
        'TVP':tvp_values,
        'Golden TVP':golden_tvp_values,

    })
    tick_indices = np.arange(idxs[sample_no][0], idxs[sample_no][1], int((idxs[sample_no][1]- idxs[sample_no][0]) * 0.16))
    custom_labels = [str(x[11:]) for x in df_ac['DATE TIME'][tick_indices]]

    # Prepare tick_labels_dict as a JS object string
    tick_labels_dict = {int(tick_indices[i]): custom_labels[i] for i in range(len(tick_indices))}
    tick_labels_js = str(tick_labels_dict).replace("'", "\"")
    label_expr = 'datum.label'
    for key, value in tick_labels_dict.items():
        label_expr = f"datum.value == {key} ? '{value}' : " + label_expr
    # Base chart
    base = alt.Chart(data).encode(
        x=alt.X('Time:Q', title='Time',  
                axis=alt.Axis(values=tick_indices,labelExpr=label_expr))
    )
    # Line chart
    empty_line = base.mark_line(color="black").encode(
        y=alt.Y('Current:Q'),
        tooltip=alt.value(None)
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    v_line = base.mark_line(color="#00a0a1").encode(
        y=alt.Y('Voltage:Q',title='Features'),
        tooltip=['Voltage','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_v_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Voltage:Q'),
        tooltip=alt.value(None)
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    c1_line = base.mark_line(color="#cc3300").encode(
        y=alt.Y('Arc 1 Current:Q',title='Features'),
        tooltip=['Arc 1 Current','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_c1_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Arc 1 Current:Q'),
        tooltip=['Golden Arc 1 Current','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    c2_line = base.mark_line(color="#44cc00").encode(
        y=alt.Y('Arc 2 Current:Q',title='Features'),
        tooltip=['Arc 2 Current','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_c2_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Arc 2 Current:Q'),
        tooltip=['Golden Arc 2 Current','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    c3_line = base.mark_line(color="#cccc00").encode(
        y=alt.Y('Arc 3 Current:Q',title='Features'),
        tooltip=['Arc 3 Current','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_c3_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Arc 3 Current:Q'),
        tooltip=['Golden Arc 3 Current','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    g_line = base.mark_line(color="#d04071").encode(
        y=alt.Y('Ar Gas:Q',title='Features'),
        tooltip=['Ar Gas','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_g_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Ar Gas:Q'),
        tooltip=['Golden Ar Gas','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    arc_bar = base.mark_bar(color="#40a0a1").encode(
        y=alt.Y('Bias Arc:Q', title='Bias Arc'),
        tooltip=alt.value(None)
    ).properties(
        width=600,
        height=150
    )
    golden_arc_bar = base.mark_bar(color="#a0a000").encode(
        y=alt.Y('Golden Bias Arc:Q', title='Bias Arc'),
        tooltip=alt.value(None)
    ).properties(
        width=600,
        height=150
    )
    vacuum_line = base.mark_line(color="#a0a0a1").encode(
        y=alt.Y('Vacuum:Q',title='Features'),
        tooltip=['Vacuum','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_vacuum_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Vacuum:Q'),
        tooltip=['Golden Vacuum','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    t_line = base.mark_line(color="#a06001").encode(
        y=alt.Y('Temperature:Q',title='Features'),
        tooltip=['Temperature','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_t_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden Temperature:Q'),
        tooltip=['Golden Temperature','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    tvp_line = base.mark_line(color="#a060a1").encode(
        y=alt.Y('TVP:Q',title='Features'),
        tooltip=['TVP','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    golden_tvp_line = base.mark_line(color="#a0a000").encode(
        y=alt.Y('Golden TVP:Q'),
        tooltip=['Golden TVP','Date']
    ).properties(
        title='Arc Cleaning: Batch ' + refined_df_ac['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),
        width=600,
        height=400
    )
    chart=empty_line
    #golden_inp=st.checkbox("Show Golden Batch")
    golden_inp=st.checkbox("Show Golden Batch "+"("+str(list(golden_ac_process['BATCH ID'])[0])+" "+str(list(golden_ac_process['DATE TIME'])[0])+")")

    col1, col2, col3, col4,col5,col6,col7,col8 = st.columns(8)

    # Add checkboxes to each column
    with col1:
        bias_voltage = st.checkbox("Bias Voltage",value=True)

    with col2:
        current1 = st.checkbox("Arc 1 Current",value=True)
    with col3:
        current2 = st.checkbox("Arc 2 Current",value=True)
    with col4:
        current3 = st.checkbox("Arc 3 Current",value=True)
    with col5:
        ar_gas = st.checkbox("Ar Gas",value=True)
    with col6:
        vacuum = st.checkbox("Glow Vacuum",value=True)
    with col7:
        temperature = st.checkbox("Chamber Temperature",value=True)
    with col8:
        tvp = st.checkbox("TVP Position",value=True)
    chart=empty_line
    inps=[bias_voltage,current1,current2,current3,ar_gas,vacuum,temperature,tvp]
    plots=[[v_line,golden_v_line],[c1_line,golden_c1_line],[c2_line,golden_c2_line],[c3_line,golden_c3_line],[g_line,golden_g_line],[vacuum_line,golden_vacuum_line],[t_line,golden_t_line],[tvp_line,golden_tvp_line]]
    for i in range(len(inps)):
        if golden_inp==True:
            if inps[i]==True:
                chart+=plots[i][0]
                chart+=plots[i][1]
        else:
            if inps[i]==True:
                chart+=plots[i][0]
    st.altair_chart(chart,use_container_width=True)
    st.altair_chart(arc_bar,use_container_width=True)
    golden_ac_details=st.session_state.golden_ac_details
    data = {
        #'Batch ID':[str(refined_df_II['BATCH ID'][sample_no]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][sample_no][0]]),str(refined_df_II['BATCH ID'][golden_index_II]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][golden_index_II][0]])],
        'Parameters': ['Batch ID','Voltage Irregularity', 'Arc 1 Current Irregularity', 'Arc 2 Current Irregularity', 'Arc 3 Current Irregularity','Ar Gas Irregularity','Bias Arc Count','Material Type','Product Type','Pre Storage Type','Coating Type'],
        'Actual Batch': [str(refined_df_ac['BATCH ID'][sample_no]) + "  " + str(st.session_state.df_ac['DATE TIME'][refined_df_ac['Idxs'][sample_no][0]]),str(refined_df_ac["V Irregulars"][sample_no]), str(refined_df_ac["I1 Irregulars"][sample_no]), str(refined_df_ac["I2 Irregulars"][sample_no]), str(refined_df_ac["I3 Irregulars"][sample_no]), str(refined_df_ac["Ar Gas Irregulars"][sample_no]),str(refined_df_ac["Arc total"][sample_no]),str(refined_df_ac['MATERIAL TYPE'][sample_no]), str(refined_df_ac['PRODUCT TYPE'][sample_no]), str(refined_df_ac['PRE STORAGE'][sample_no]), str(refined_df_ac['COATING TYPE'][sample_no])],
        'Golden Batch': [str(st.session_state.golden_ac_details['BATCH ID']) + "  " + str(golden_ac_details['BATCH START TIME']),str(golden_ac_details["V Irregulars"]), str(golden_ac_details["I1 Irregulars"]), str(golden_ac_details["I2 Irregulars"]), str(golden_ac_details["I3 Irregulars"]),str(golden_ac_details["Ar Gas Irregulars"]),str(golden_ac_details["Arc total"]), str(golden_ac_details['MATERIAL TYPE']), str(golden_ac_details['PRODUCT TYPE']), str(golden_ac_details['PRE STORAGE']), str(golden_ac_details['COATING TYPE'])]
    }
    table_df = pd.DataFrame(data)
    table_df = table_df.reset_index(drop=True)
    table_str = table_df.to_html(index=False, escape=False)

    # Display the table as HTML
    st.markdown(table_str, unsafe_allow_html=True)
def individual_plot_ae(sample_no):
    
    df_ae = st.session_state.df_ae

    #batch_data = st.session_state.batch_data
    refined_df_ae=st.session_state.refined_df_ae
    idxs=refined_df_ae['Idxs']
    golden_ae_process=st.session_state.golden_ae_process
    import streamlit.components.v1 as components
    st.write("Selected batch:", selected_batch)
    # Prepare the data for Altair
    if len(idxs[sample_no])==1:
        idxs=[item[0] for item in idxs]
        time_values = np.arange(idxs[sample_no][0],idxs[sample_no][1], 1)
        voltage_values = df_ae['BIAS VOLTAGE ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        current1_values = df_ae['ARC 1 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        current2_values = df_ae['ARC 2 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        current3_values = df_ae['ARC 3 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        gas_values = df_ae['AR GAS ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        arc_values = df_ae['BIAS ARC COUNT'][idxs[sample_no][0]:idxs[sample_no][1]].values
        date_values = df_ae['DATE TIME'][idxs[sample_no][0]:idxs[sample_no][1]].values
        #encoder_position=df_ae['ENCODER POSITION'][idxs[sample_no][0]:idxs[sample_no][1]].values
        #encoder_position=encoder_position/360
        vacuum_values=df_ae['GLOW VACUUM ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        temp_values=df_ae['CHAMBER TEMP ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        tvp_values=df_ae['TVP POSITION ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values

        golden_voltage_values=golden_ae_process['BIAS VOLTAGE ACTUAL'].values
        golden_current1_values=golden_ae_process['ARC 1 CURRENT ACTUAL'].values
        golden_current2_values=golden_ae_process['ARC 2 CURRENT ACTUAL'].values
        golden_current3_values=golden_ae_process['ARC 3 CURRENT ACTUAL'].values
        golden_gas_values=golden_ae_process['AR GAS ACTUAL'].values
        golden_vacuum_values=golden_ae_process['GLOW VACUUM ACTUAL'].values
        golden_temp_values=golden_ae_process['CHAMBER TEMP ACTUAL'].values
        golden_tvp_values=golden_ae_process['TVP POSITION ACTUAL'].values

        if len(golden_voltage_values)>len(voltage_values):
            golden_voltage_values=golden_voltage_values[:len(voltage_values)]
            golden_current1_values=golden_current1_values[:len(voltage_values)]
            golden_current2_values=golden_current2_values[:len(voltage_values)]
            golden_current3_values=golden_current3_values[:len(voltage_values)]
            golden_gas_values=golden_gas_values[:len(voltage_values)]
            golden_vacuum_values=golden_vacuum_values[:len(voltage_values)]
            golden_temp_values=golden_temp_values[:len(voltage_values)]
            golden_tvp_values=golden_tvp_values[:len(voltage_values)]

        elif len(golden_voltage_values)<len(voltage_values):
            n=len(voltage_values)-len(golden_voltage_values)
            golden_voltage_values = np.append(golden_voltage_values, np.full(n, np.nan))
            golden_current1_values = np.append(golden_current1_values, np.full(n, np.nan))
            golden_current2_values = np.append(golden_current2_values, np.full(n, np.nan))
            golden_current3_values = np.append(golden_current3_values, np.full(n, np.nan))
            golden_gas_values = np.append(golden_gas_values, np.full(n, np.nan))
            golden_vacuum_values = np.append(golden_vacuum_values, np.full(n, np.nan))
            golden_temp_values = np.append(golden_temp_values, np.full(n, np.nan))
            golden_tvp_values = np.append(golden_tvp_values, np.full(n, np.nan))

        data = pd.DataFrame({
            'Time': time_values,
            'Voltage': voltage_values,
            'Arc 1 Current': current1_values,
            'Arc 2 Current': current2_values,
            'Arc 3 Current': current3_values,
            'Ar Gas': gas_values,
            'Bias Arc':arc_values,
            #'Encoder Position':encoder_position,
            'Golden Voltage':golden_voltage_values,
            'Golden Arc 1 Current':golden_current1_values,
            'Golden Arc 2 Current':golden_current2_values,
            'Golden Arc 3 Current':golden_current3_values,
            'Golden Ar Gas':golden_gas_values,
            'Date': date_values,
            'Vacuum': vacuum_values,
            'Golden Vacuum': golden_vacuum_values,
            'Temperature':temp_values,
            'Golden Temperature':golden_temp_values,
            'TVP':tvp_values,
            'Golden TVP':golden_tvp_values,

        })
        tick_indices = np.arange(idxs[sample_no][0], idxs[sample_no][1], int((idxs[sample_no][1]- idxs[sample_no][0]) * 0.3))
        custom_labels = [str(x[11:]) for x in df_ae['DATE TIME'][tick_indices]]

        # Prepare tick_labels_dict as a JS object string
        tick_labels_dict = {int(tick_indices[i]): custom_labels[i] for i in range(len(tick_indices))}
        tick_labels_js = str(tick_labels_dict).replace("'", "\"")
        label_expr = 'datum.label'
        for key, value in tick_labels_dict.items():
            label_expr = f"datum.value == {key} ? '{value}' : " + label_expr
        # Base chart
        base = alt.Chart(data).encode(
            x=alt.X('Time:Q', title='Time',  
                    axis=alt.Axis(values=tick_indices,labelExpr=label_expr))
        )
        # Line chart
        empty_line = base.mark_line(color="black").encode(
            y=alt.Y('Current:Q'),
            tooltip=alt.value(None)
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        v_line = base.mark_line(color="#00a0a1").encode(
            y=alt.Y('Voltage:Q',title='Features'),
            tooltip=['Voltage','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_v_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Voltage:Q'),
            tooltip=alt.value(None)
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        c1_line = base.mark_line(color="#cc3300").encode(
            y=alt.Y('Arc 1 Current:Q',title='Features'),
            tooltip=['Arc 1 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_c1_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Arc 1 Current:Q'),
            tooltip=['Golden Arc 1 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        c2_line = base.mark_line(color="#44cc00").encode(
            y=alt.Y('Arc 2 Current:Q',title='Features'),
            tooltip=['Arc 2 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_c2_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Arc 2 Current:Q'),
            tooltip=['Golden Arc 2 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        c3_line = base.mark_line(color="#cccc00").encode(
            y=alt.Y('Arc 3 Current:Q',title='Features'),
            tooltip=['Arc 3 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_c3_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Arc 3 Current:Q'),
            tooltip=['Golden Arc 3 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        g_line = base.mark_line(color="#d04071").encode(
            y=alt.Y('Ar Gas:Q',title='Features'),
            tooltip=['Ar Gas','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_g_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Ar Gas:Q'),
            tooltip=['Golden Ar Gas','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        arc_bar = base.mark_bar(color="#40a0a1").encode(
            y=alt.Y('Bias Arc:Q', title='Bias Arc'),
            tooltip=alt.value(None)
        ).properties(
            width=600,
            height=150
        )
        golden_arc_bar = base.mark_bar(color="#a0a000").encode(
            y=alt.Y('Golden Bias Arc:Q', title='Bias Arc'),
            tooltip=alt.value(None)
        ).properties(
            width=600,
            height=150
        )
        vacuum_line = base.mark_line(color="#a0a0a1").encode(
            y=alt.Y('Vacuum:Q',title='Features'),
            tooltip=['Vacuum','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_vacuum_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Vacuum:Q'),
            tooltip=['Golden Vacuum','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        t_line = base.mark_line(color="#a06001").encode(
            y=alt.Y('Temperature:Q',title='Features'),
            tooltip=['Temperature','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_t_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Temperature:Q'),
            tooltip=['Golden Temperature','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        tvp_line = base.mark_line(color="#a060a1").encode(
            y=alt.Y('TVP:Q',title='Features'),
            tooltip=['TVP','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_tvp_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden TVP:Q'),
            tooltip=['Golden TVP','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        chart=empty_line
        #golden_inp=st.checkbox("Show Golden Batch")
        golden_inp=st.checkbox("Show Golden Batch "+"("+str(list(golden_ae_process['BATCH ID'])[0])+" "+str(list(golden_ae_process['DATE TIME'])[0])+")")

        col1, col2, col3, col4,col5,col6,col7,col8 = st.columns(8)

        # Add checkboxes to each column
        with col1:
            bias_voltage = st.checkbox("Bias voltage",value=True)

        with col2:
            current1 = st.checkbox("Arc 1 current",value=True)
        with col3:
            current2 = st.checkbox("Arc 2 current",value=True)
        with col4:
            current3 = st.checkbox("Arc 3 current",value=True)
        with col5:
            ar_gas = st.checkbox("Ar gas",value=True)
        with col6:
            vacuum = st.checkbox("Glow vacuum",value=True)
        with col7:
            temperature = st.checkbox("Chamber temperature",value=True)
        with col8:
            tvp = st.checkbox("TVP position",value=True)
        chart=empty_line
        inps=[bias_voltage,current1,current2,current3,ar_gas,vacuum,temperature,tvp]
        plots=[[v_line,golden_v_line],[c1_line,golden_c1_line],[c2_line,golden_c2_line],[c3_line,golden_c3_line],[g_line,golden_g_line],[vacuum_line,golden_vacuum_line],[t_line,golden_t_line],[tvp_line,golden_tvp_line]]
        for i in range(len(inps)):
            if golden_inp==True:
                if inps[i]==True:
                    chart+=plots[i][0]
                    chart+=plots[i][1]
            else:
                if inps[i]==True:
                    chart+=plots[i][0]
        st.altair_chart(chart,use_container_width=True)
        st.altair_chart(arc_bar,use_container_width=True)
        golden_ae_details=st.session_state.golden_ae_details
        data = {
            #'Batch ID':[str(refined_df_II['BATCH ID'][sample_no]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][sample_no][0]]),str(refined_df_II['BATCH ID'][golden_index_II]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][golden_index_II][0]])],
            'Parameters': ['Batch ID','Voltage Irregularity', 'Arc 1 Current Irregularity', 'Arc 2 Current Irregularity', 'Arc 3 Current Irregularity','Ar Gas Irregularity','Bias Arc Count','Material Type','Product Type','Pre Storage Type','Coating Type'],
            'Actual Batch': [str(refined_df_ae['BATCH ID'][sample_no]) + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),str(refined_df_ae["V Irregulars"][sample_no]), str(refined_df_ae["I1 Irregulars"][sample_no]), str(refined_df_ae["I2 Irregulars"][sample_no]), str(refined_df_ae["I3 Irregulars"][sample_no]), str(refined_df_ae["Ar Gas Irregulars"][sample_no]),str(refined_df_ae["Arc total"][sample_no]),str(refined_df_ae['MATERIAL TYPE'][sample_no]), str(refined_df_ae['PRODUCT TYPE'][sample_no]), str(refined_df_ae['PRE STORAGE'][sample_no]), str(refined_df_ae['COATING TYPE'][sample_no])],
            'Golden Batch': [str(st.session_state.golden_ae_details['BATCH ID']) + "  " + str(golden_ae_details['BATCH START TIME']),str(golden_ae_details["V Irregulars"]), str(golden_ae_details["I1 Irregulars"]), str(golden_ae_details["I2 Irregulars"]), str(golden_ae_details["I3 Irregulars"]),str(golden_ae_details["Ar Gas Irregulars"]),str(golden_ae_details["Arc total"]), str(golden_ae_details['MATERIAL TYPE']), str(golden_ae_details['PRODUCT TYPE']), str(golden_ae_details['PRE STORAGE']), str(golden_ae_details['COATING TYPE'])]
        }
        table_df = pd.DataFrame(data)
        table_df = table_df.reset_index(drop=True)
        table_str = table_df.to_html(index=False, escape=False)

        # Display the table as HTML
        st.markdown(table_str, unsafe_allow_html=True)

    elif len(idxs[sample_no])==2:
        idxs=[item[0] for item in idxs]
        time_values = np.arange(idxs[sample_no][0],idxs[sample_no][1], 1)
        voltage_values = df_ae['BIAS VOLTAGE ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        current1_values = df_ae['ARC 1 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        current2_values = df_ae['ARC 2 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        current3_values = df_ae['ARC 3 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        gas_values = df_ae['AR GAS ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        arc_values = df_ae['BIAS ARC COUNT'][idxs[sample_no][0]:idxs[sample_no][1]].values
        date_values = df_ae['DATE TIME'][idxs[sample_no][0]:idxs[sample_no][1]].values
        #encoder_position=df_ae['ENCODER POSITION'][idxs[sample_no][0]:idxs[sample_no][1]].values
        #encoder_position=encoder_position/360
        vacuum_values=df_ae['GLOW VACUUM ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        temp_values=df_ae['CHAMBER TEMP ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        tvp_values=df_ae['TVP POSITION ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values

        golden_voltage_values=golden_ae_process['BIAS VOLTAGE ACTUAL'].values
        golden_current1_values=golden_ae_process['ARC 1 CURRENT ACTUAL'].values
        golden_current2_values=golden_ae_process['ARC 2 CURRENT ACTUAL'].values
        golden_current3_values=golden_ae_process['ARC 3 CURRENT ACTUAL'].values
        golden_gas_values=golden_ae_process['AR GAS ACTUAL'].values
        golden_vacuum_values=golden_ae_process['GLOW VACUUM ACTUAL'].values
        golden_temp_values=golden_ae_process['CHAMBER TEMP ACTUAL'].values
        golden_tvp_values=golden_ae_process['TVP POSITION ACTUAL'].values

        if len(golden_voltage_values)>len(voltage_values):
            golden_voltage_values=golden_voltage_values[:len(voltage_values)]
            golden_current1_values=golden_current1_values[:len(voltage_values)]
            golden_current2_values=golden_current2_values[:len(voltage_values)]
            golden_current3_values=golden_current3_values[:len(voltage_values)]
            golden_gas_values=golden_gas_values[:len(voltage_values)]
            golden_vacuum_values=golden_vacuum_values[:len(voltage_values)]
            golden_temp_values=golden_temp_values[:len(voltage_values)]
            golden_tvp_values=golden_tvp_values[:len(voltage_values)]

        elif len(golden_voltage_values)<len(voltage_values):
            n=len(voltage_values)-len(golden_voltage_values)
            golden_voltage_values = np.append(golden_voltage_values, np.full(n, np.nan))
            golden_current1_values = np.append(golden_current1_values, np.full(n, np.nan))
            golden_current2_values = np.append(golden_current2_values, np.full(n, np.nan))
            golden_current3_values = np.append(golden_current3_values, np.full(n, np.nan))
            golden_gas_values = np.append(golden_gas_values, np.full(n, np.nan))
            golden_vacuum_values = np.append(golden_vacuum_values, np.full(n, np.nan))
            golden_temp_values = np.append(golden_temp_values, np.full(n, np.nan))
            golden_tvp_values = np.append(golden_tvp_values, np.full(n, np.nan))

        data = pd.DataFrame({
            'Time': time_values,
            'Voltage': voltage_values,
            'Arc 1 Current': current1_values,
            'Arc 2 Current': current2_values,
            'Arc 3 Current': current3_values,
            'Ar Gas': gas_values,
            'Bias Arc':arc_values,
            #'Encoder Position':encoder_position,
            'Golden Voltage':golden_voltage_values,
            'Golden Arc 1 Current':golden_current1_values,
            'Golden Arc 2 Current':golden_current2_values,
            'Golden Arc 3 Current':golden_current3_values,
            'Golden Ar Gas':golden_gas_values,
            'Date': date_values,
            'Vacuum': vacuum_values,
            'Golden Vacuum': golden_vacuum_values,
            'Temperature':temp_values,
            'Golden Temperature':golden_temp_values,
            'TVP':tvp_values,
            'Golden TVP':golden_tvp_values,

        })
        tick_indices = np.arange(idxs[sample_no][0], idxs[sample_no][1], int((idxs[sample_no][1]- idxs[sample_no][0]) * 0.3))
        custom_labels = [str(x[11:]) for x in df_ae['DATE TIME'][tick_indices]]

        # Prepare tick_labels_dict as a JS object string
        tick_labels_dict = {int(tick_indices[i]): custom_labels[i] for i in range(len(tick_indices))}
        tick_labels_js = str(tick_labels_dict).replace("'", "\"")
        label_expr = 'datum.label'
        for key, value in tick_labels_dict.items():
            label_expr = f"datum.value == {key} ? '{value}' : " + label_expr
        # Base chart
        base = alt.Chart(data).encode(
            x=alt.X('Time:Q', title='Time',  
                    axis=alt.Axis(values=tick_indices,labelExpr=label_expr))
        )
        # Line chart
        empty_line = base.mark_line(color="black").encode(
            y=alt.Y('Current:Q'),
            tooltip=alt.value(None)
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        v_line = base.mark_line(color="#00a0a1").encode(
            y=alt.Y('Voltage:Q',title='Features'),
            tooltip=['Voltage','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        golden_v_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Voltage:Q'),
            tooltip=alt.value(None)
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        c1_line = base.mark_line(color="#cc3300").encode(
            y=alt.Y('Arc 1 Current:Q',title='Features'),
            tooltip=['Arc 1 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        golden_c1_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Arc 1 Current:Q'),
            tooltip=['Golden Arc 1 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        c2_line = base.mark_line(color="#44cc00").encode(
            y=alt.Y('Arc 2 Current:Q',title='Features'),
            tooltip=['Arc 2 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        golden_c2_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Arc 2 Current:Q'),
            tooltip=['Golden Arc 2 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        c3_line = base.mark_line(color="#cccc00").encode(
            y=alt.Y('Arc 3 Current:Q',title='Features'),
            tooltip=['Arc 3 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        golden_c3_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Arc 3 Current:Q'),
            tooltip=['Golden Arc 3 Current','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        g_line = base.mark_line(color="#d04071").encode(
            y=alt.Y('Ar Gas:Q',title='Features'),
            tooltip=['Ar Gas','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        golden_g_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Ar Gas:Q'),
            tooltip=['Golden Ar Gas','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        arc_bar_1 = base.mark_bar(color="#40a0a1").encode(
            y=alt.Y('Bias Arc:Q', title='Bias Arc'),
            tooltip=alt.value(None)
        ).properties(
            width=400,
            height=150
        )
        golden_arc_bar = base.mark_bar(color="#a0a000").encode(
            y=alt.Y('Golden Bias Arc:Q', title='Bias Arc'),
            tooltip=alt.value(None)
        ).properties(
            width=400,
            height=150
        )
        vacuum_line = base.mark_line(color="#a0a0a1").encode(
            y=alt.Y('Vacuum:Q',title='Features'),
            tooltip=['Vacuum','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        golden_vacuum_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Vacuum:Q'),
            tooltip=['Golden Vacuum','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        t_line = base.mark_line(color="#a06001").encode(
            y=alt.Y('Temperature:Q',title='Features'),
            tooltip=['Temperature','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        golden_t_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Temperature:Q'),
            tooltip=['Golden Temperature','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        tvp_line = base.mark_line(color="#a060a1").encode(
            y=alt.Y('TVP:Q',title='Features'),
            tooltip=['TVP','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        golden_tvp_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden TVP:Q'),
            tooltip=['Golden TVP','Date']
        ).properties(
            title='Arc Etching: Batch ' + refined_df_ae['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),
            width=400,
            height=280
        )
        chart=empty_line
        #golden_inp=st.checkbox("Show Golden Batch")
        golden_inp=st.checkbox("Show Golden Batch "+"("+str(list(golden_ae_process['BATCH ID'])[0])+" "+str(list(golden_ae_process['DATE TIME'])[0])+")")

        col1, col2, col3, col4,col5,col6,col7,col8 = st.columns(8)

        # Add checkboxes to each column
        with col1:
            bias_voltage = st.checkbox("Bias voltage",value=True)

        with col2:
            current1 = st.checkbox("Arc 1 current",value=True)
        with col3:
            current2 = st.checkbox("Arc 2 current",value=True)
        with col4:
            current3 = st.checkbox("Arc 3 current",value=True)
        with col5:
            ar_gas = st.checkbox("Ar gas",value=True)
        with col6:
            vacuum = st.checkbox("Glow vacuum",value=True)
        with col7:
            temperature = st.checkbox("Chamber temperature",value=True)
        with col8:
            tvp = st.checkbox("TVP position",value=True)
        chart_1=empty_line
        inps=[bias_voltage,current1,current2,current3,ar_gas,vacuum,temperature,tvp]
        plots=[[v_line,golden_v_line],[c1_line,golden_c1_line],[c2_line,golden_c2_line],[c3_line,golden_c3_line],[g_line,golden_g_line],[vacuum_line,golden_vacuum_line],[t_line,golden_t_line],[tvp_line,golden_tvp_line]]
        for i in range(len(inps)):
            if golden_inp==True:
                if inps[i]==True:
                    chart_1+=plots[i][0]
                    chart_1+=plots[i][1]
            else:
                if inps[i]==True:
                    chart_1+=plots[i][0]
        #st.altair_chart(chart_1,use_container_width=True)
        #st.altair_chart(arc_bar_1,use_container_width=True)

        idxs=refined_df_ae['Idxs']
        idxs=[item[1] for item in idxs]
        time_values = np.arange(idxs[sample_no][0],idxs[sample_no][1], 1)
        voltage_values = df_ae['BIAS VOLTAGE ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        current1_values = df_ae['ARC 1 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        current2_values = df_ae['ARC 2 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        current3_values = df_ae['ARC 3 CURRENT ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        gas_values = df_ae['AR GAS ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        arc_values = df_ae['BIAS ARC COUNT'][idxs[sample_no][0]:idxs[sample_no][1]].values
        date_values = df_ae['DATE TIME'][idxs[sample_no][0]:idxs[sample_no][1]].values
        #encoder_position=df_ae['ENCODER POSITION'][idxs[sample_no][0]:idxs[sample_no][1]].values
        #encoder_position=encoder_position/360
        vacuum_values=df_ae['GLOW VACUUM ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        temp_values=df_ae['CHAMBER TEMP ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        tvp_values=df_ae['TVP POSITION ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values

        golden_voltage_values=golden_ae_process['BIAS VOLTAGE ACTUAL'].values
        golden_current1_values=golden_ae_process['ARC 1 CURRENT ACTUAL'].values
        golden_current2_values=golden_ae_process['ARC 2 CURRENT ACTUAL'].values
        golden_current3_values=golden_ae_process['ARC 3 CURRENT ACTUAL'].values
        golden_gas_values=golden_ae_process['AR GAS ACTUAL'].values
        golden_vacuum_values=golden_ae_process['GLOW VACUUM ACTUAL'].values
        golden_temp_values=golden_ae_process['CHAMBER TEMP ACTUAL'].values
        golden_tvp_values=golden_ae_process['TVP POSITION ACTUAL'].values

        if len(golden_voltage_values)>len(voltage_values):
            golden_voltage_values=golden_voltage_values[:len(voltage_values)]
            golden_current1_values=golden_current1_values[:len(voltage_values)]
            golden_current2_values=golden_current2_values[:len(voltage_values)]
            golden_current3_values=golden_current3_values[:len(voltage_values)]
            golden_gas_values=golden_gas_values[:len(voltage_values)]
            golden_vacuum_values=golden_vacuum_values[:len(voltage_values)]
            golden_temp_values=golden_temp_values[:len(voltage_values)]
            golden_tvp_values=golden_tvp_values[:len(voltage_values)]

        elif len(golden_voltage_values)<len(voltage_values):
            n=len(voltage_values)-len(golden_voltage_values)
            golden_voltage_values = np.append(golden_voltage_values, np.full(n, np.nan))
            golden_current1_values = np.append(golden_current1_values, np.full(n, np.nan))
            golden_current2_values = np.append(golden_current2_values, np.full(n, np.nan))
            golden_current3_values = np.append(golden_current3_values, np.full(n, np.nan))
            golden_gas_values = np.append(golden_gas_values, np.full(n, np.nan))
            golden_vacuum_values = np.append(golden_vacuum_values, np.full(n, np.nan))
            golden_temp_values = np.append(golden_temp_values, np.full(n, np.nan))
            golden_tvp_values = np.append(golden_tvp_values, np.full(n, np.nan))

        data = pd.DataFrame({
            'Time': time_values,
            'Voltage': voltage_values,
            'Arc 1 Current': current1_values,
            'Arc 2 Current': current2_values,
            'Arc 3 Current': current3_values,
            'Ar Gas': gas_values,
            'Bias Arc':arc_values,
            #'Encoder Position':encoder_position,
            'Golden Voltage':golden_voltage_values,
            'Golden Arc 1 Current':golden_current1_values,
            'Golden Arc 2 Current':golden_current2_values,
            'Golden Arc 3 Current':golden_current3_values,
            'Golden Ar Gas':golden_gas_values,
            'Date': date_values,
            'Vacuum': vacuum_values,
            'Golden Vacuum': golden_vacuum_values,
            'Temperature':temp_values,
            'Golden Temperature':golden_temp_values,
            'TVP':tvp_values,
            'Golden TVP':golden_tvp_values,

        })
        tick_indices = np.arange(idxs[sample_no][0], idxs[sample_no][1], int((idxs[sample_no][1]- idxs[sample_no][0]) * 0.3))
        custom_labels = [str(x[11:]) for x in df_ae['DATE TIME'][tick_indices]]

        # Prepare tick_labels_dict as a JS object string
        tick_labels_dict = {int(tick_indices[i]): custom_labels[i] for i in range(len(tick_indices))}
        tick_labels_js = str(tick_labels_dict).replace("'", "\"")
        label_expr = 'datum.label'
        for key, value in tick_labels_dict.items():
            label_expr = f"datum.value == {key} ? '{value}' : " + label_expr
        # Base chart
        base = alt.Chart(data).encode(
            x=alt.X('Time:Q', title='Time',  
                    axis=alt.Axis(values=tick_indices,labelExpr=label_expr))
        )
        # Line chart
        empty_line = base.mark_line(color="black").encode(
            y=alt.Y('Current:Q'),
            tooltip=alt.value(None)
        ).properties(
            title='',
            width=400,
            height=280
        )
        v_line = base.mark_line(color="#00a0a1").encode(
            y=alt.Y('Voltage:Q',axis=alt.Axis(title=None, labels=False)),
            tooltip=['Voltage','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        golden_v_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Voltage:Q'),
            tooltip=alt.value(None)
        ).properties(
            title='',
            width=400,
            height=280
        )
        c1_line = base.mark_line(color="#cc3300").encode(
            y=alt.Y('Arc 1 Current:Q',title='Features'),
            tooltip=['Arc 1 Current','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        golden_c1_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Arc 1 Current:Q'),
            tooltip=['Golden Arc 1 Current','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        c2_line = base.mark_line(color="#44cc00").encode(
            y=alt.Y('Arc 2 Current:Q',title='Features'),
            tooltip=['Arc 2 Current','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        golden_c2_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Arc 2 Current:Q'),
            tooltip=['Golden Arc 2 Current','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        c3_line = base.mark_line(color="#cccc00").encode(
            y=alt.Y('Arc 3 Current:Q',title='Features'),
            tooltip=['Arc 3 Current','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        golden_c3_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Arc 3 Current:Q'),
            tooltip=['Golden Arc 3 Current','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        g_line = base.mark_line(color="#d04071").encode(
            y=alt.Y('Ar Gas:Q',title='Features'),
            tooltip=['Ar Gas','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        golden_g_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Ar Gas:Q'),
            tooltip=['Golden Ar Gas','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        arc_bar_2 = base.mark_bar(color="#40a0a1").encode(
            y=alt.Y('Bias Arc:Q', title='Bias Arc'),
            tooltip=alt.value(None)
        ).properties(
            width=400,
            height=150
        )
        golden_arc_bar = base.mark_bar(color="#a0a000").encode(
            y=alt.Y('Golden Bias Arc:Q', title='Bias Arc'),
            tooltip=alt.value(None)
        ).properties(
            width=400,
            height=150
        )
        vacuum_line = base.mark_line(color="#a0a0a1").encode(
            y=alt.Y('Vacuum:Q',title='Features'),
            tooltip=['Vacuum','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        golden_vacuum_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Vacuum:Q'),
            tooltip=['Golden Vacuum','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        t_line = base.mark_line(color="#a06001").encode(
            y=alt.Y('Temperature:Q',title='Features'),
            tooltip=['Temperature','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        golden_t_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Temperature:Q'),
            tooltip=['Golden Temperature','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        tvp_line = base.mark_line(color="#a060a1").encode(
            y=alt.Y('TVP:Q',title='Features'),
            tooltip=['TVP','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        golden_tvp_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden TVP:Q'),
            tooltip=['Golden TVP','Date']
        ).properties(
            title='',
            width=400,
            height=280
        )
        chart_2=empty_line
        inps=[bias_voltage,current1,current2,current3,ar_gas,vacuum,temperature,tvp]
        plots=[[v_line,golden_v_line],[c1_line,golden_c1_line],[c2_line,golden_c2_line],[c3_line,golden_c3_line],[g_line,golden_g_line],[vacuum_line,golden_vacuum_line],[t_line,golden_t_line],[tvp_line,golden_tvp_line]]
        for i in range(len(inps)):
            if golden_inp==True:
                if inps[i]==True:
                    chart_2+=plots[i][0]
                    chart_2+=plots[i][1]
            else:
                if inps[i]==True:
                    chart_2+=plots[i][0]

        st.altair_chart(chart_1 | chart_2,use_container_width=True)
        st.altair_chart(arc_bar_1 | arc_bar_2,use_container_width=True)
        golden_ae_details=st.session_state.golden_ae_details
        data = {
            #'Batch ID':[str(refined_df_II['BATCH ID'][sample_no]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][sample_no][0]]),str(refined_df_II['BATCH ID'][golden_index_II]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][golden_index_II][0]])],
            'Parameters': ['Batch ID','Voltage Irregularity', 'Arc 1 Current Irregularity', 'Arc 2 Current Irregularity', 'Arc 3 Current Irregularity','Ar Gas Irregularity','Bias Arc Count','Material Type','Product Type','Pre Storage Type','Coating Type'],
            'Actual Batch': [str(refined_df_ae['BATCH ID'][sample_no]) + "  " + str(st.session_state.df_ae['DATE TIME'][refined_df_ae['Idxs'][sample_no][0][0]]),str(refined_df_ae["V Irregulars"][sample_no]), str(refined_df_ae["I1 Irregulars"][sample_no]), str(refined_df_ae["I2 Irregulars"][sample_no]), str(refined_df_ae["I3 Irregulars"][sample_no]), str(refined_df_ae["Ar Gas Irregulars"][sample_no]),str(refined_df_ae["Arc total"][sample_no]),str(refined_df_ae['MATERIAL TYPE'][sample_no]), str(refined_df_ae['PRODUCT TYPE'][sample_no]), str(refined_df_ae['PRE STORAGE'][sample_no]), str(refined_df_ae['COATING TYPE'][sample_no])],
            'Golden Batch': [str(st.session_state.golden_ae_details['BATCH ID']) + "  " + str(golden_ae_details['BATCH START TIME']),str(golden_ae_details["V Irregulars"]), str(golden_ae_details["I1 Irregulars"]), str(golden_ae_details["I2 Irregulars"]), str(golden_ae_details["I3 Irregulars"]),str(golden_ae_details["Ar Gas Irregulars"]),str(golden_ae_details["Arc total"]), str(golden_ae_details['MATERIAL TYPE']), str(golden_ae_details['PRODUCT TYPE']), str(golden_ae_details['PRE STORAGE']), str(golden_ae_details['COATING TYPE'])]
        }
        table_df = pd.DataFrame(data)
        table_df = table_df.reset_index(drop=True)
        table_str = table_df.to_html(index=False, escape=False)

        # Display the table as HTML
        st.markdown(table_str, unsafe_allow_html=True)
def individual_plot_ps(sample_no):
    
    df_ps = st.session_state.df_ps

    #batch_data = st.session_state.batch_data
    refined_df_ps=st.session_state.refined_df_ps
    idxs=refined_df_ps['Idxs']
    golden_ps_process=st.session_state.golden_ps_process
    import streamlit.components.v1 as components
    st.write("Selected batch:", selected_batch)
    # Prepare the data for Altair
    if len(idxs[sample_no])==1:
        idxs=[item[0] for item in idxs]
        time_values = np.arange(idxs[sample_no][0],idxs[sample_no][1], 1)
        voltage_values = df_ps['BIAS VOLTAGE ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        mfp1_values = df_ps['MFP1 POWER ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        mfp2_values = df_ps['MFP2 POWER ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        gas_values = df_ps['AR GAS ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        arc_values = df_ps['BIAS ARC COUNT'][idxs[sample_no][0]:idxs[sample_no][1]].values
        date_values = df_ps['DATE TIME'][idxs[sample_no][0]:idxs[sample_no][1]].values
        encoder_position=df_ps['ENCODER POSITION'][idxs[sample_no][0]:idxs[sample_no][1]].values
        encoder_position=encoder_position/360
        vacuum_values=df_ps['VACUUM PRESSURE ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        temp_values=df_ps['CHAMBER TEMP ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values

        golden_voltage_values=golden_ps_process['BIAS VOLTAGE ACTUAL'].values
        golden_mfp1_values=golden_ps_process['MFP1 POWER ACTUAL'].values
        golden_mfp2_values=golden_ps_process['MFP2 POWER ACTUAL'].values
        golden_gas_values=golden_ps_process['AR GAS ACTUAL'].values
        golden_vacuum_values=golden_ps_process['VACUUM PRESSURE ACTUAL'].values
        golden_temp_values=golden_ps_process['CHAMBER TEMP ACTUAL'].values

        if len(golden_voltage_values)>len(voltage_values):
            golden_voltage_values=golden_voltage_values[:len(voltage_values)]
            golden_mfp1_values=golden_mfp1_values[:len(voltage_values)]
            golden_mfp2_values=golden_mfp2_values[:len(voltage_values)]
            golden_gas_values=golden_gas_values[:len(voltage_values)]
            golden_vacuum_values=golden_vacuum_values[:len(voltage_values)]
            golden_temp_values=golden_temp_values[:len(voltage_values)]

        elif len(golden_voltage_values)<len(voltage_values):
            n=len(voltage_values)-len(golden_voltage_values)
            golden_voltage_values = np.append(golden_voltage_values, np.full(n, np.nan))
            golden_mfp1_values = np.append(golden_mfp1_values, np.full(n, np.nan))
            golden_mfp2_values = np.append(golden_mfp2_values, np.full(n, np.nan))
            golden_gas_values = np.append(golden_gas_values, np.full(n, np.nan))
            golden_vacuum_values = np.append(golden_vacuum_values, np.full(n, np.nan))
            golden_temp_values = np.append(golden_temp_values, np.full(n, np.nan))

        data = pd.DataFrame({
            'Time': time_values,
            'Voltage': voltage_values,
            'MFP1 POWER': mfp1_values,
            'MFP2 POWER': mfp2_values,
            'Ar Gas': gas_values,
            'Bias Arc':arc_values,
            #'Encoder Position':encoder_position,
            'Golden Voltage':golden_voltage_values,
            'Golden MFP1 POWER':golden_mfp1_values,
            'Golden MFP2 POWER':golden_mfp2_values,
            'Golden Ar Gas':golden_gas_values,
            'Date': date_values,
            'Vacuum': vacuum_values,
            'Golden Vacuum': golden_vacuum_values,
            'Temperature':temp_values,
            'Golden Temperature':golden_temp_values,

        })
        tick_indices = np.arange(idxs[sample_no][0], idxs[sample_no][1], int((idxs[sample_no][1]- idxs[sample_no][0]) * 0.3))
        custom_labels = [str(x[11:]) for x in df_ps['DATE TIME'][tick_indices]]

        # Prepare tick_labels_dict as a JS object string
        tick_labels_dict = {int(tick_indices[i]): custom_labels[i] for i in range(len(tick_indices))}
        tick_labels_js = str(tick_labels_dict).replace("'", "\"")
        label_expr = 'datum.label'
        for key, value in tick_labels_dict.items():
            label_expr = f"datum.value == {key} ? '{value}' : " + label_expr
        # Base chart
        base = alt.Chart(data).encode(
            x=alt.X('Time:Q', title='Time',  
                    axis=alt.Axis(values=tick_indices,labelExpr=label_expr))
        )
        # Line chart
        empty_line = base.mark_line(color="black").encode(
            y=alt.Y('Current:Q'),
            tooltip=alt.value(None)
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        v_line = base.mark_line(color="#00a0a1").encode(
            y=alt.Y('Voltage:Q',title='Features'),
            tooltip=['Voltage','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_v_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Voltage:Q'),
            tooltip=alt.value(None)
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        mfp1_line = base.mark_line(color="#cc3300").encode(
            y=alt.Y('MFP1 POWER:Q',title='Features'),
            tooltip=['MFP1 POWER','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_mfp1_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden MFP1 POWER:Q'),
            tooltip=['Golden MFP1 POWER','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        mfp2_line = base.mark_line(color="#44cc00").encode(
            y=alt.Y('MFP2 POWER:Q',title='Features'),
            tooltip=['MFP2 POWER','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_mfp2_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden MFP2 POWER:Q'),
            tooltip=['Golden MFP2 POWER','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        g_line = base.mark_line(color="#d04071").encode(
            y=alt.Y('Ar Gas:Q',title='Features'),
            tooltip=['Ar Gas','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_g_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Ar Gas:Q'),
            tooltip=['Golden Ar Gas','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        arc_bar = base.mark_bar(color="#40a0a1").encode(
            y=alt.Y('Bias Arc:Q', title='Bias Arc'),
            tooltip=alt.value(None)
        ).properties(
            width=600,
            height=150
        )
        golden_arc_bar = base.mark_bar(color="#a0a000").encode(
            y=alt.Y('Golden Bias Arc:Q', title='Bias Arc'),
            tooltip=alt.value(None)
        ).properties(
            width=600,
            height=150
        )
        vacuum_line = base.mark_line(color="#a0a0a1").encode(
            y=alt.Y('Vacuum:Q',title='Features'),
            tooltip=['Vacuum','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_vacuum_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Vacuum:Q'),
            tooltip=['Golden Vacuum','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        t_line = base.mark_line(color="#a06001").encode(
            y=alt.Y('Temperature:Q',title='Features'),
            tooltip=['Temperature','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_t_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Temperature:Q'),
            tooltip=['Golden Temperature','Date']
        ).properties(
            title='Pre Sputtering: Batch ' + refined_df_ps['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        chart=empty_line
        #golden_inp=st.checkbox("Show Golden Batch")
        golden_inp=st.checkbox("Show Golden Batch "+"("+str(list(golden_ps_process['BATCH ID'])[0])+" "+str(list(golden_ps_process['DATE TIME'])[0])+")")

        col1, col2, col3, col4,col5,col6 = st.columns(6)

        # Add checkboxes to each column
        with col1:
            bias_voltage = st.checkbox("Bias voltage",value=True)

        with col2:
            mfp1 = st.checkbox("MFP1 POWER",value=True)
        with col3:
            mfp2 = st.checkbox("MFP2 POWER",value=True)
        with col4:
            ar_gas = st.checkbox("Ar gas",value=True)
        with col5:
            vacuum = st.checkbox("Vacuum",value=True)
        with col6:
            temperature = st.checkbox("Chamber temperature",value=True)

        chart=empty_line
        inps=[bias_voltage,mfp1,mfp2,ar_gas,vacuum,temperature]
        plots=[[v_line,golden_v_line],[mfp1_line,golden_mfp1_line],[mfp2_line,golden_mfp2_line],[g_line,golden_g_line],[vacuum_line,golden_vacuum_line],[t_line,golden_t_line]]
        for i in range(len(inps)):
            if golden_inp==True:
                if inps[i]==True:
                    chart+=plots[i][0]
                    chart+=plots[i][1]
            else:
                if inps[i]==True:
                    chart+=plots[i][0]
        st.altair_chart(chart,use_container_width=True)
        st.altair_chart(arc_bar,use_container_width=True)
        golden_ps_details=st.session_state.golden_ps_details
        data = {
            #'Batch ID':[str(refined_df_II['BATCH ID'][sample_no]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][sample_no][0]]),str(refined_df_II['BATCH ID'][golden_index_II]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][golden_index_II][0]])],
            'Parameters': ['Batch ID','Voltage Irregularity', 'MFP1 POWER Irregularity', 'MFP2 POWER Irregularity','Ar Gas Irregularity','Bias Arc Count','Material Type','Product Type','Pre Storage Type','Coating Type'],
            'Actual Batch': [str(refined_df_ps['BATCH ID'][sample_no]) + "  " + str(st.session_state.df_ps['DATE TIME'][refined_df_ps['Idxs'][sample_no][0][0]]),str(refined_df_ps["V Irregulars"][sample_no]), str(refined_df_ps["MFP1 Irregulars"][sample_no]), str(refined_df_ps["MFP2 Irregulars"][sample_no]), str(refined_df_ps["Ar Gas Irregulars"][sample_no]),str(refined_df_ps["Arc total"][sample_no]),str(refined_df_ps['MATERIAL TYPE'][sample_no]), str(refined_df_ps['PRODUCT TYPE'][sample_no]), str(refined_df_ps['PRE STORAGE'][sample_no]), str(refined_df_ps['COATING TYPE'][sample_no])],
            'Golden Batch': [str(st.session_state.golden_ps_details['BATCH ID']) + "  " + str(golden_ps_details['BATCH START TIME']),str(golden_ps_details["V Irregulars"]), str(golden_ps_details["MFP1 Irregulars"]), str(golden_ps_details["MFP2 Irregulars"]),str(golden_ps_details["Ar Gas Irregulars"]),str(golden_ps_details["Arc total"]), str(golden_ps_details['MATERIAL TYPE']), str(golden_ps_details['PRODUCT TYPE']), str(golden_ps_details['PRE STORAGE']), str(golden_ps_details['COATING TYPE'])]
        }
        table_df = pd.DataFrame(data)
        table_df = table_df.reset_index(drop=True)
        table_str = table_df.to_html(index=False, escape=False)

        # Display the table as HTML
        st.markdown(table_str, unsafe_allow_html=True)
def individual_plot_ti(sample_no):
    
    df_ti = st.session_state.df_ti

    #batch_data = st.session_state.batch_data
    refined_df_ti=st.session_state.refined_df_ti
    idxs=refined_df_ti['Idxs']
    golden_ti_process=st.session_state.golden_ti_process
    import streamlit.components.v1 as components
    st.write("Selected batch:", selected_batch)
    # Prepare the data for Altair
    if len(idxs[sample_no])==1:
        idxs=[item[0] for item in idxs]
        time_values = np.arange(idxs[sample_no][0],idxs[sample_no][1], 1)
        voltage_values = df_ti['BIAS VOLTAGE ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        mfp1_values = df_ti['MFP1 POWER ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        mfp2_values = df_ti['MFP2 POWER ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        gas_values = df_ti['AR GAS ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        arc_values = df_ti['BIAS ARC COUNT'][idxs[sample_no][0]:idxs[sample_no][1]].values
        date_values = df_ti['DATE TIME'][idxs[sample_no][0]:idxs[sample_no][1]].values
        encoder_position=df_ti['ENCODER POSITION'][idxs[sample_no][0]:idxs[sample_no][1]].values
        encoder_position=encoder_position/360
        vacuum_values=df_ti['VACUUM PRESSURE ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values
        temp_values=df_ti['CHAMBER TEMP ACTUAL'][idxs[sample_no][0]:idxs[sample_no][1]].values

        golden_voltage_values=golden_ti_process['BIAS VOLTAGE ACTUAL'].values
        golden_mfp1_values=golden_ti_process['MFP1 POWER ACTUAL'].values
        golden_mfp2_values=golden_ti_process['MFP2 POWER ACTUAL'].values
        golden_gas_values=golden_ti_process['AR GAS ACTUAL'].values
        golden_vacuum_values=golden_ti_process['VACUUM PRESSURE ACTUAL'].values
        golden_temp_values=golden_ti_process['CHAMBER TEMP ACTUAL'].values

        if len(golden_voltage_values)>len(voltage_values):
            golden_voltage_values=golden_voltage_values[:len(voltage_values)]
            golden_mfp1_values=golden_mfp1_values[:len(voltage_values)]
            golden_mfp2_values=golden_mfp2_values[:len(voltage_values)]
            golden_gas_values=golden_gas_values[:len(voltage_values)]
            golden_vacuum_values=golden_vacuum_values[:len(voltage_values)]
            golden_temp_values=golden_temp_values[:len(voltage_values)]

        elif len(golden_voltage_values)<len(voltage_values):
            n=len(voltage_values)-len(golden_voltage_values)
            golden_voltage_values = np.append(golden_voltage_values, np.full(n, np.nan))
            golden_mfp1_values = np.append(golden_mfp1_values, np.full(n, np.nan))
            golden_mfp2_values = np.append(golden_mfp2_values, np.full(n, np.nan))
            golden_gas_values = np.append(golden_gas_values, np.full(n, np.nan))
            golden_vacuum_values = np.append(golden_vacuum_values, np.full(n, np.nan))
            golden_temp_values = np.append(golden_temp_values, np.full(n, np.nan))

        data = pd.DataFrame({
            'Time': time_values,
            'Voltage': voltage_values,
            'MFP1 POWER': mfp1_values,
            'MFP2 POWER': mfp2_values,
            'Ar Gas': gas_values,
            'Bias Arc':arc_values,
            #'Encoder Position':encoder_position,
            'Golden Voltage':golden_voltage_values,
            'Golden MFP1 POWER':golden_mfp1_values,
            'Golden MFP2 POWER':golden_mfp2_values,
            'Golden Ar Gas':golden_gas_values,
            'Date': date_values,
            'Vacuum': vacuum_values,
            'Golden Vacuum': golden_vacuum_values,
            'Temperature':temp_values,
            'Golden Temperature':golden_temp_values,

        })
        tick_indices = np.arange(idxs[sample_no][0], idxs[sample_no][1], int((idxs[sample_no][1]- idxs[sample_no][0]) * 0.3))
        custom_labels = [str(x[11:]) for x in df_ti['DATE TIME'][tick_indices]]

        # Prepare tick_labels_dict as a JS object string
        tick_labels_dict = {int(tick_indices[i]): custom_labels[i] for i in range(len(tick_indices))}
        tick_labels_js = str(tick_labels_dict).replace("'", "\"")
        label_expr = 'datum.label'
        for key, value in tick_labels_dict.items():
            label_expr = f"datum.value == {key} ? '{value}' : " + label_expr
        # Base chart
        base = alt.Chart(data).encode(
            x=alt.X('Time:Q', title='Time',  
                    axis=alt.Axis(values=tick_indices,labelExpr=label_expr))
        )
        # Line chart
        empty_line = base.mark_line(color="black").encode(
            y=alt.Y('Current:Q'),
            tooltip=alt.value(None)
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        v_line = base.mark_line(color="#00a0a1").encode(
            y=alt.Y('Voltage:Q',title='Features'),
            tooltip=['Voltage','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_v_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Voltage:Q'),
            tooltip=alt.value(None)
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        mfp1_line = base.mark_line(color="#cc3300").encode(
            y=alt.Y('MFP1 POWER:Q',title='Features'),
            tooltip=['MFP1 POWER','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_mfp1_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden MFP1 POWER:Q'),
            tooltip=['Golden MFP1 POWER','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        mfp2_line = base.mark_line(color="#44cc00").encode(
            y=alt.Y('MFP2 POWER:Q',title='Features'),
            tooltip=['MFP2 POWER','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_mfp2_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden MFP2 POWER:Q'),
            tooltip=['Golden MFP2 POWER','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        g_line = base.mark_line(color="#d04071").encode(
            y=alt.Y('Ar Gas:Q',title='Features'),
            tooltip=['Ar Gas','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_g_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Ar Gas:Q'),
            tooltip=['Golden Ar Gas','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        arc_bar = base.mark_bar(color="#40a0a1").encode(
            y=alt.Y('Bias Arc:Q', title='Bias Arc'),
            tooltip=alt.value(None)
        ).properties(
            width=600,
            height=150
        )
        golden_arc_bar = base.mark_bar(color="#a0a000").encode(
            y=alt.Y('Golden Bias Arc:Q', title='Bias Arc'),
            tooltip=alt.value(None)
        ).properties(
            width=600,
            height=150
        )
        vacuum_line = base.mark_line(color="#a0a0a1").encode(
            y=alt.Y('Vacuum:Q',title='Features'),
            tooltip=['Vacuum','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_vacuum_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Vacuum:Q'),
            tooltip=['Golden Vacuum','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        t_line = base.mark_line(color="#a06001").encode(
            y=alt.Y('Temperature:Q',title='Features'),
            tooltip=['Temperature','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        golden_t_line = base.mark_line(color="#a0a000").encode(
            y=alt.Y('Golden Temperature:Q'),
            tooltip=['Golden Temperature','Date']
        ).properties(
            title='Ti Coating: Batch ' + refined_df_ti['BATCH ID'][sample_no] + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),
            width=600,
            height=400
        )
        chart=empty_line
        #golden_inp=st.checkbox("Show Golden Batch")
        golden_inp=st.checkbox("Show Golden Batch "+"("+str(list(golden_ti_process['BATCH ID'])[0])+" "+str(list(golden_ti_process['DATE TIME'])[0])+")")

        col1, col2, col3, col4,col5,col6 = st.columns(6)

        # Add checkboxes to each column
        with col1:
            bias_voltage = st.checkbox("Bias voltage",value=True)

        with col2:
            mfp1 = st.checkbox("MFP1 POWER",value=True)
        with col3:
            mfp2 = st.checkbox("MFP2 POWER",value=True)
        with col4:
            ar_gas = st.checkbox("Ar gas",value=True)
        with col5:
            vacuum = st.checkbox("Vacuum",value=True)
        with col6:
            temperature = st.checkbox("Chamber temperature",value=True)

        chart=empty_line
        inps=[bias_voltage,mfp1,mfp2,ar_gas,vacuum,temperature]
        plots=[[v_line,golden_v_line],[mfp1_line,golden_mfp1_line],[mfp2_line,golden_mfp2_line],[g_line,golden_g_line],[vacuum_line,golden_vacuum_line],[t_line,golden_t_line]]
        for i in range(len(inps)):
            if golden_inp==True:
                if inps[i]==True:
                    chart+=plots[i][0]
                    chart+=plots[i][1]
            else:
                if inps[i]==True:
                    chart+=plots[i][0]
        st.altair_chart(chart,use_container_width=True)
        st.altair_chart(arc_bar,use_container_width=True)
        golden_ti_details=st.session_state.golden_ti_details
        data = {
            #'Batch ID':[str(refined_df_II['BATCH ID'][sample_no]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][sample_no][0]]),str(refined_df_II['BATCH ID'][golden_index_II]) + "  " + str(st.session_state.df['DATE TIME'][refined_df_II['Idxs'][golden_index_II][0]])],
            'Parameters': ['Batch ID','Voltage Irregularity', 'MFP1 POWER Irregularity', 'MFP2 POWER Irregularity','Ar Gas Irregularity','Bias Arc Count','Material Type','Product Type','Pre Storage Type','Coating Type'],
            'Actual Batch': [str(refined_df_ti['BATCH ID'][sample_no]) + "  " + str(st.session_state.df_ti['DATE TIME'][refined_df_ti['Idxs'][sample_no][0][0]]),str(refined_df_ti["V Irregulars"][sample_no]), str(refined_df_ti["MFP1 Irregulars"][sample_no]), str(refined_df_ti["MFP2 Irregulars"][sample_no]), str(refined_df_ti["Ar Gas Irregulars"][sample_no]),str(refined_df_ti["Arc total"][sample_no]),str(refined_df_ti['MATERIAL TYPE'][sample_no]), str(refined_df_ti['PRODUCT TYPE'][sample_no]), str(refined_df_ti['PRE STORAGE'][sample_no]), str(refined_df_ti['COATING TYPE'][sample_no])],
            'Golden Batch': [str(st.session_state.golden_ti_details['BATCH ID']) + "  " + str(golden_ti_details['BATCH START TIME']),str(golden_ti_details["V Irregulars"]), str(golden_ti_details["MFP1 Irregulars"]), str(golden_ti_details["MFP2 Irregulars"]),str(golden_ti_details["Ar Gas Irregulars"]),str(golden_ti_details["Arc total"]), str(golden_ti_details['MATERIAL TYPE']), str(golden_ti_details['PRODUCT TYPE']), str(golden_ti_details['PRE STORAGE']), str(golden_ti_details['COATING TYPE'])]
        }
        table_df = pd.DataFrame(data)
        table_df = table_df.reset_index(drop=True)
        table_str = table_df.to_html(index=False, escape=False)

        # Display the table as HTML
        st.markdown(table_str, unsafe_allow_html=True)
def plot_corr():
    refined_df=st.session_state.refined_df
    pre_storage=[]
    for i in range(len(refined_df)):
        if refined_df['PRE STORAGE'][i]!=None and type(refined_df['PRE STORAGE'][i])!=float:
            pre_storage.append([refined_df['PRE STORAGE'][i],refined_df['RH mins'][i]])
    x=[pre_storage[i][0] for i in range(len(pre_storage))]
    pre_storage_time=[pre_storage[i][1] for i in range(len(pre_storage))]
    pre_storage_category = [1 if x[i]=="Open" else 0 for i in range(len(x))]
    load_time=[]
    for i in range(len(refined_df)):
        if refined_df['PVD MACHINE LOADING TIME'][i]!=None and type(refined_df['PVD MACHINE LOADING TIME'][i])!=float and ":" not in refined_df['PVD MACHINE LOADING TIME'][i] and "#" not in refined_df['PVD MACHINE LOADING TIME'][i] and refined_df['PVD MACHINE LOADING TIME'][i]!='0':
            load_time.append([float(refined_df['PVD MACHINE LOADING TIME'][i]),refined_df['RH mins'][i]])
    # Assume refined_df is already defined and available in the scope
    ni_refined_df = refined_df.sort_values(by="Ni hours")
    drop_labels = []
    for i in range(len(ni_refined_df)):
        if ni_refined_df["Ni hours"][i] < 0:
            drop_labels.append(i)
    ni_refined_df = ni_refined_df.drop(labels=drop_labels, axis=0)
    ni_refined_df = ni_refined_df.reset_index(drop=True)
    material_category = (ni_refined_df['MATERIAL TYPE'] == 'Brass').astype(int)
    
    x_axis_names = ["Temp time", "Ni hours", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        #np.corrcoef(ni_refined_df["R mins"], ni_refined_df["RH mins"])[0, 1],
        np.corrcoef(ni_refined_df["T mins"], ni_refined_df["RH mins"])[0, 1],
        np.corrcoef(ni_refined_df["Ni hours"], ni_refined_df["RH mins"])[0, 1],
        np.corrcoef(material_category, ni_refined_df["RH mins"])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[1] for item in load_time])[0, 1],
        np.corrcoef(pre_storage_category, pre_storage_time)[0, 1]
    ]

    # Prepare the data for Altair
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with RH mins (Total Pumpdown Time)',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
def plot_corr_II():
    refined_df_II=st.session_state.refined_df_II
    pre_storage=[]
    for i in range(len(refined_df_II)):
        if refined_df_II['PRE STORAGE'][i]!=None and type(refined_df_II['PRE STORAGE'][i])!=float:
            pre_storage.append([refined_df_II['PRE STORAGE'][i],refined_df_II['H_II mins'][i]])
    x=[pre_storage[i][0] for i in range(len(pre_storage))]
    pre_storage_time=[pre_storage[i][1] for i in range(len(pre_storage))]
    pre_storage_category = [1 if x[i]=="Open" else 0 for i in range(len(x))]
    load_time=[]
    for i in range(len(refined_df_II)):
        if refined_df_II['PVD MACHINE LOADING TIME'][i]!=None and type(refined_df_II['PVD MACHINE LOADING TIME'][i])!=float and ":" not in str(refined_df_II['PVD MACHINE LOADING TIME'][i]) and "#" not in str(refined_df_II['PVD MACHINE LOADING TIME'][i]) and refined_df_II['PVD MACHINE LOADING TIME'][i]!='0':
            load_time.append([float(refined_df_II['PVD MACHINE LOADING TIME'][i]),refined_df_II['H_II mins'][i]])
    # Assume refined_df_II is already defined and available in the scope
    ni_refined_df_II = refined_df_II.sort_values(by="Ni hours")
    drop_labels = []
    for i in range(len(ni_refined_df_II)):
        if ni_refined_df_II["Ni hours"][i] < 0:
            drop_labels.append(i)
    ni_refined_df_II = ni_refined_df_II.drop(labels=drop_labels, axis=0)
    ni_refined_df_II = ni_refined_df_II.reset_index(drop=True)
    material_category = (ni_refined_df_II['MATERIAL TYPE'] == 'Brass').astype(int)
    
    x_axis_names = ["Temp_II time", "Ni hours", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        #np.corrcoef(ni_refined_df_II["R mins"], ni_refined_df_II["H_II mins"])[0, 1],
        np.corrcoef(ni_refined_df_II["T_II mins"], ni_refined_df_II["H_II mins"])[0, 1],
        np.corrcoef(ni_refined_df_II["Ni hours"], ni_refined_df_II["H_II mins"])[0, 1],
        np.corrcoef(material_category, ni_refined_df_II["H_II mins"])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[1] for item in load_time])[0, 1],
        np.corrcoef(pre_storage_category, pre_storage_time)[0, 1]
    ]
    if 'refined_df' in st.session_state:    
        x_axis_names.append('HV I time')
        y_corr.append(np.corrcoef(st.session_state.I_II_df["RH mins"], st.session_state.I_II_df["H_II mins"])[0, 1])
    # Prepare the data for Altair
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with H_II mins (Total Pumpdown Time)',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
def plot_corr_glow():
    from scipy.stats import chi2_contingency
    refined_df_glow=st.session_state.refined_df_glow
    pre_storage=[]
    for i in range(len(refined_df_glow)):
        if refined_df_glow['PRE STORAGE'][i]!=None and type(refined_df_glow['PRE STORAGE'][i])!=float:
            pre_storage.append([(refined_df_glow['PRE STORAGE']=='Open').astype(int)[i],(refined_df_glow['V Irregulars']==True).astype(int)[i],(refined_df_glow['Bias Arc Irregulars']==True).astype(int)[i]])
    load_time=[]
    for i in range(len(refined_df_glow)):
        if refined_df_glow['PVD MACHINE LOADING TIME'][i]!=None and type(refined_df_glow['PVD MACHINE LOADING TIME'][i])!=float and ":" not in str(refined_df_glow['PVD MACHINE LOADING TIME'][i]) and "#" not in str(refined_df_glow['PVD MACHINE LOADING TIME'][i]) and refined_df_glow['PVD MACHINE LOADING TIME'][i]!='0':
            load_time.append([float(refined_df_glow['PVD MACHINE LOADING TIME'][i]),(refined_df_glow['V Irregulars']==True).astype(int)[i],(refined_df_glow['Bias Arc Irregulars']==True).astype(int)[i]])
    material_category=[]
    for i in range(len(refined_df_glow)):
        material_category.append([(refined_df_glow['MATERIAL TYPE'] == 'Brass').astype(int)[i],(refined_df_glow['V Irregulars']==True).astype(int)[i],(refined_df_glow['Bias Arc Irregulars']==True).astype(int)[i]])
    contingency_table = pd.crosstab(refined_df_glow['SHIFT TYPE'], refined_df_glow['Bias Arc Irregulars'].astype(int))

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1

    cramers_arc = np.sqrt(chi2 / (n * min_dim))
    x_axis_names = ["Shift Type", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        cramers_arc,
        np.corrcoef([item[0] for item in material_category], [item[2] for item in material_category])[0, 1],
        np.corrcoef([item[0] for item in pre_storage], [item[2] for item in pre_storage])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[2] for item in load_time])[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with Bias Arc Irregularities',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
    contingency_table = pd.crosstab(refined_df_glow['SHIFT TYPE'], refined_df_glow['V Irregulars'].astype(int))

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1

    cramers_v = np.sqrt(chi2 / (n * min_dim))
    x_axis_names = ["Shift Type", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        cramers_v,
        np.corrcoef([item[0] for item in material_category], [item[1] for item in material_category])[0, 1],
        np.corrcoef([item[0] for item in pre_storage], [item[1] for item in pre_storage])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[1] for item in load_time])[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with Voltage Irregularities',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
    df_glow=st.session_state.df_glow
    x_axis_names = ["V vs Arc", "I vs Arc","V vs I","Encoder vs Arc","Ar vs Arc"]
    y_corr = [
        np.corrcoef([item[1] for item in material_category], [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_glow['I total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_glow['V total'].astype(float)), refined_df_glow['I total'].astype(float))[0, 1],
        np.corrcoef(np.array(df_glow['ENCODER POSITION'].astype(float)), df_glow['BIAS ARC COUNT'].astype(float))[0, 1],
        np.corrcoef(np.array(df_glow['AR GAS ACTUAL'].astype(float)), df_glow['BIAS ARC COUNT'].astype(float))[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Process features Correlations',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
def plot_corr_ac():
    from scipy.stats import chi2_contingency
    refined_df_ac=st.session_state.refined_df_ac
    pre_storage=[]
    for i in range(len(refined_df_ac)):
        if refined_df_ac['PRE STORAGE'][i]!=None and type(refined_df_ac['PRE STORAGE'][i])!=float:
            pre_storage.append([(refined_df_ac['PRE STORAGE']=='Open').astype(int)[i],(refined_df_ac['V Irregulars']==True).astype(int)[i],(refined_df_ac['Bias Arc Irregulars']==True).astype(int)[i]])
    load_time=[]
    for i in range(len(refined_df_ac)):
        if refined_df_ac['PVD MACHINE LOADING TIME'][i]!=None and type(refined_df_ac['PVD MACHINE LOADING TIME'][i])!=float and ":" not in str(refined_df_ac['PVD MACHINE LOADING TIME'][i]) and "#" not in str(refined_df_ac['PVD MACHINE LOADING TIME'][i]) and refined_df_ac['PVD MACHINE LOADING TIME'][i]!='0':
            load_time.append([float(refined_df_ac['PVD MACHINE LOADING TIME'][i]),(refined_df_ac['V Irregulars']==True).astype(int)[i],(refined_df_ac['Bias Arc Irregulars']==True).astype(int)[i]])
    material_category=[]
    for i in range(len(refined_df_ac)):
        material_category.append([(refined_df_ac['MATERIAL TYPE'] == 'Brass').astype(int)[i],(refined_df_ac['V Irregulars']==True).astype(int)[i],(refined_df_ac['Bias Arc Irregulars']==True).astype(int)[i]])
    contingency_table = pd.crosstab(refined_df_ac['SHIFT TYPE'], refined_df_ac['Bias Arc Irregulars'].astype(int))

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1

    cramers_arc = np.sqrt(chi2 / (n * min_dim))
    x_axis_names = ["Shift Type", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        cramers_arc,
        np.corrcoef([item[0] for item in material_category], [item[2] for item in material_category])[0, 1],
        np.corrcoef([item[0] for item in pre_storage], [item[2] for item in pre_storage])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[2] for item in load_time])[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with Bias Arc Irregularities',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
    contingency_table = pd.crosstab(refined_df_ac['SHIFT TYPE'], refined_df_ac['V Irregulars'].astype(int))

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1

    cramers_v = np.sqrt(chi2 / (n * min_dim))
    x_axis_names = ["Shift Type", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        cramers_v,
        np.corrcoef([item[0] for item in material_category], [item[1] for item in material_category])[0, 1],
        np.corrcoef([item[0] for item in pre_storage], [item[1] for item in pre_storage])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[1] for item in load_time])[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with Voltage Irregularities',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
    df_ac=st.session_state.df_ac
    x_axis_names = ["V vs Arc", "I1 vs Arc", "I2 vs Arc", "I3 vs Arc","Ar vs Arc"]
    y_corr = [
        np.corrcoef([item[1] for item in material_category], [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_ac['I1 total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_ac['I2 total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_ac['I3 total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(df_ac['AR GAS ACTUAL'].astype(float)), df_ac['BIAS ARC COUNT'].astype(float))[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Process features Correlations',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
def plot_corr_ae():
    from scipy.stats import chi2_contingency
    refined_df_ae=st.session_state.refined_df_ae
    pre_storage=[]
    for i in range(len(refined_df_ae)):
        if refined_df_ae['PRE STORAGE'][i]!=None and type(refined_df_ae['PRE STORAGE'][i])!=float:
            pre_storage.append([(refined_df_ae['PRE STORAGE']=='Open').astype(int)[i],(refined_df_ae['V Irregulars']==True).astype(int)[i],(refined_df_ae['Bias Arc Irregulars']==True).astype(int)[i]])
    load_time=[]
    for i in range(len(refined_df_ae)):
        if refined_df_ae['PVD MACHINE LOADING TIME'][i]!=None and type(refined_df_ae['PVD MACHINE LOADING TIME'][i])!=float and ":" not in str(refined_df_ae['PVD MACHINE LOADING TIME'][i]) and "#" not in str(refined_df_ae['PVD MACHINE LOADING TIME'][i]) and refined_df_ae['PVD MACHINE LOADING TIME'][i]!='0':
            load_time.append([float(refined_df_ae['PVD MACHINE LOADING TIME'][i]),(refined_df_ae['V Irregulars']==True).astype(int)[i],(refined_df_ae['Bias Arc Irregulars']==True).astype(int)[i]])
    material_category=[]
    for i in range(len(refined_df_ae)):
        material_category.append([(refined_df_ae['MATERIAL TYPE'] == 'Brass').astype(int)[i],(refined_df_ae['V Irregulars']==True).astype(int)[i],(refined_df_ae['Bias Arc Irregulars']==True).astype(int)[i]])
    contingency_table = pd.crosstab(refined_df_ae['SHIFT TYPE'], refined_df_ae['Bias Arc Irregulars'].astype(int))

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1

    cramers_arc = np.sqrt(chi2 / (n * min_dim))
    x_axis_names = ["Shift Type", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        cramers_arc,
        np.corrcoef([item[0] for item in material_category], [item[2] for item in material_category])[0, 1],
        np.corrcoef([item[0] for item in pre_storage], [item[2] for item in pre_storage])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[2] for item in load_time])[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with Bias Arc Irregularities',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
    contingency_table = pd.crosstab(refined_df_ae['SHIFT TYPE'], refined_df_ae['V Irregulars'].astype(int))

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1

    cramers_v = np.sqrt(chi2 / (n * min_dim))
    x_axis_names = ["Shift Type", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        cramers_v,
        np.corrcoef([item[0] for item in material_category], [item[1] for item in material_category])[0, 1],
        np.corrcoef([item[0] for item in pre_storage], [item[1] for item in pre_storage])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[1] for item in load_time])[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with Voltage Irregularities',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
    df_ae=st.session_state.df_ae
    x_axis_names = ["V vs Arc", "I1 vs Arc", "I2 vs Arc", "I3 vs Arc","Ar vs Arc"]
    y_corr = [
        np.corrcoef([item[1] for item in material_category], [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_ae['I1 total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_ae['I2 total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_ae['I3 total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(df_ae['AR GAS ACTUAL'].astype(float)), df_ae['BIAS ARC COUNT'].astype(float))[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Process features Correlations',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
def plot_corr_ps():
    from scipy.stats import chi2_contingency
    refined_df_ps=st.session_state.refined_df_ps
    pre_storage=[]
    for i in range(len(refined_df_ps)):
        if refined_df_ps['PRE STORAGE'][i]!=None and type(refined_df_ps['PRE STORAGE'][i])!=float:
            pre_storage.append([(refined_df_ps['PRE STORAGE']=='Open').astype(int)[i],(refined_df_ps['V Irregulars']==True).astype(int)[i],(refined_df_ps['Bias Arc Irregulars']==True).astype(int)[i]])
    load_time=[]
    for i in range(len(refined_df_ps)):
        if refined_df_ps['PVD MACHINE LOADING TIME'][i]!=None and type(refined_df_ps['PVD MACHINE LOADING TIME'][i])!=float and ":" not in str(refined_df_ps['PVD MACHINE LOADING TIME'][i]) and "#" not in str(refined_df_ps['PVD MACHINE LOADING TIME'][i]) and refined_df_ps['PVD MACHINE LOADING TIME'][i]!='0':
            load_time.append([float(refined_df_ps['PVD MACHINE LOADING TIME'][i]),(refined_df_ps['V Irregulars']==True).astype(int)[i],(refined_df_ps['Bias Arc Irregulars']==True).astype(int)[i]])
    material_category=[]
    for i in range(len(refined_df_ps)):
        material_category.append([(refined_df_ps['MATERIAL TYPE'] == 'Brass').astype(int)[i],(refined_df_ps['V Irregulars']==True).astype(int)[i],(refined_df_ps['Bias Arc Irregulars']==True).astype(int)[i]])
    contingency_table = pd.crosstab(refined_df_ps['SHIFT TYPE'], refined_df_ps['Bias Arc Irregulars'].astype(int))

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1

    cramers_arc = np.sqrt(chi2 / (n * min_dim))
    x_axis_names = ["Shift Type", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        cramers_arc,
        np.corrcoef([item[0] for item in material_category], [item[2] for item in material_category])[0, 1],
        np.corrcoef([item[0] for item in pre_storage], [item[2] for item in pre_storage])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[2] for item in load_time])[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with Bias Arc Irregularities',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
    contingency_table = pd.crosstab(refined_df_ps['SHIFT TYPE'], refined_df_ps['V Irregulars'].astype(int))

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1

    cramers_v = np.sqrt(chi2 / (n * min_dim))
    x_axis_names = ["Shift Type", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        cramers_v,
        np.corrcoef([item[0] for item in material_category], [item[1] for item in material_category])[0, 1],
        np.corrcoef([item[0] for item in pre_storage], [item[1] for item in pre_storage])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[1] for item in load_time])[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with Voltage Irregularities',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
    df_ps=st.session_state.df_ps
    x_axis_names = ["V vs Arc", "MFP1 vs Arc", "MFP2 vs Arc","Ar vs Arc"]
    y_corr = [
        np.corrcoef([item[1] for item in material_category], [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_ps['MFP1 total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_ps['MFP2 total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(df_ps['AR GAS ACTUAL'].astype(float)), df_ps['BIAS ARC COUNT'].astype(float))[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Process features Correlations',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
def plot_corr_ti():
    from scipy.stats import chi2_contingency
    refined_df_ti=st.session_state.refined_df_ti
    pre_storage=[]
    for i in range(len(refined_df_ti)):
        if refined_df_ti['PRE STORAGE'][i]!=None and type(refined_df_ti['PRE STORAGE'][i])!=float:
            pre_storage.append([(refined_df_ti['PRE STORAGE']=='Open').astype(int)[i],(refined_df_ti['V Irregulars']==True).astype(int)[i],(refined_df_ti['Bias Arc Irregulars']==True).astype(int)[i]])
    load_time=[]
    for i in range(len(refined_df_ti)):
        if refined_df_ti['PVD MACHINE LOADING TIME'][i]!=None and type(refined_df_ti['PVD MACHINE LOADING TIME'][i])!=float and ":" not in str(refined_df_ti['PVD MACHINE LOADING TIME'][i]) and "#" not in str(refined_df_ti['PVD MACHINE LOADING TIME'][i]) and refined_df_ti['PVD MACHINE LOADING TIME'][i]!='0':
            load_time.append([float(refined_df_ti['PVD MACHINE LOADING TIME'][i]),(refined_df_ti['V Irregulars']==True).astype(int)[i],(refined_df_ti['Bias Arc Irregulars']==True).astype(int)[i]])
    material_category=[]
    for i in range(len(refined_df_ti)):
        material_category.append([(refined_df_ti['MATERIAL TYPE'] == 'Brass').astype(int)[i],(refined_df_ti['V Irregulars']==True).astype(int)[i],(refined_df_ti['Bias Arc Irregulars']==True).astype(int)[i]])
    contingency_table = pd.crosstab(refined_df_ti['SHIFT TYPE'], refined_df_ti['Bias Arc Irregulars'].astype(int))

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1

    cramers_arc = np.sqrt(chi2 / (n * min_dim))
    x_axis_names = ["Shift Type", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        cramers_arc,
        np.corrcoef([item[0] for item in material_category], [item[2] for item in material_category])[0, 1],
        np.corrcoef([item[0] for item in pre_storage], [item[2] for item in pre_storage])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[2] for item in load_time])[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with Bias Arc Irregularities',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
    contingency_table = pd.crosstab(refined_df_ti['SHIFT TYPE'], refined_df_ti['V Irregulars'].astype(int))

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Calculate Cramér's V
    n = contingency_table.sum().sum()  # Total number of observations
    min_dim = min(contingency_table.shape) - 1

    cramers_v = np.sqrt(chi2 / (n * min_dim))
    x_axis_names = ["Shift Type", "Material Type","Load Time","Pre Storage Type"]
    y_corr = [
        cramers_v,
        np.corrcoef([item[0] for item in material_category], [item[1] for item in material_category])[0, 1],
        np.corrcoef([item[0] for item in pre_storage], [item[1] for item in pre_storage])[0, 1],
        np.corrcoef([item[0] for item in load_time], [item[1] for item in load_time])[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with Voltage Irregularities',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
    df_ti=st.session_state.df_ti
    x_axis_names = ["V vs Arc", "MFP1 vs Arc", "MFP2 vs Arc","Ar vs Arc"]
    y_corr = [
        np.corrcoef([item[1] for item in material_category], [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_ti['MFP1 total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(refined_df_ti['MFP2 total'].astype(float)), [item[2] for item in material_category])[0, 1],
        np.corrcoef(np.array(df_ti['AR GAS ACTUAL'].astype(float)), df_ti['BIAS ARC COUNT'].astype(float))[0, 1],
    ]
    data = pd.DataFrame({
        'Variable': x_axis_names,
        'Correlation': y_corr
    })

    # Separate positive and negative correlations
    data['Correlation Type'] = np.where(data['Correlation'] < 0, 'Negative', 'Positive')
    data['Abs Correlation'] = data['Correlation'].abs()

    # Create the Altair chart
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Abs Correlation:Q',scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Process features Correlations',
        width=600,
        height=300
    )

    st.altair_chart(chart, use_container_width=True)
def plot_glow_irr():
    refined_df_glow=st.session_state.refined_df_glow
    data = pd.DataFrame({
        'Irregularities': ["V Irregulars", "Bias Arc Irregulars", "I Irregulars", "Ar Gas Irregulars"],
        'Count': [
            refined_df_glow['V Irregulars'].sum(),
            refined_df_glow['Bias Arc Irregulars'].sum(),
            refined_df_glow['I Irregulars'].sum(),
            refined_df_glow['Ar Gas Irregulars'].sum()
        ]
    })

    # Create the bar chart
    chart = alt.Chart(data).mark_bar(color='#008081').encode(
        x=alt.X('Count:Q', title='Number of Batches',scale=alt.Scale(domain=[0, len(refined_df_glow)])),
        y=alt.Y('Irregularities:N', sort='-x', title='Irregularities'),
    ).properties(
        title='Count of True Values for Different Irregularities',
        width=500,
        height=300
    )
    st.altair_chart(chart, use_container_width=True)
def plot_ac_irr():
    refined_df_ac=st.session_state.refined_df_ac
    data = pd.DataFrame({
        'Irregularities': ["V Irregulars", "Bias Arc Irregulars", "I1 Irregulars", "I2 Irregulars", "I3 Irregulars", "Ar Gas Irregulars"],
        'Count': [
            refined_df_ac['V Irregulars'].sum(),
            refined_df_ac['Bias Arc Irregulars'].sum(),
            refined_df_ac['I1 Irregulars'].sum(),
            refined_df_ac['I2 Irregulars'].sum(),
            refined_df_ac['I3 Irregulars'].sum(),
            refined_df_ac['Ar Gas Irregulars'].sum()
        ]
    })

    # Create the bar chart
    chart = alt.Chart(data).mark_bar(color='#008081').encode(
        x=alt.X('Count:Q', title='Number of Batches',scale=alt.Scale(domain=[0, len(refined_df_ac)])),
        y=alt.Y('Irregularities:N', sort='-x', title='Irregularities'),
    ).properties(
        title='Count of True Values for Different Irregularities',
        width=500,
        height=300
    )
    st.altair_chart(chart, use_container_width=True)
def plot_ae_irr(region_selections):
    refined_df_ae=st.session_state.refined_df_ae
    if region_selections[1]=='All Batches' or region_selections[1]=='Irregular Batches':
        data = pd.DataFrame({
            'Irregularities': ["V Irregulars", "Bias Arc Irregulars", "I1 Irregulars", "I2 Irregulars", "I3 Irregulars", "Ar Gas Irregulars"],
            'Count': [
                refined_df_ae['V Irregulars'].sum(),
                refined_df_ae['Bias Arc Irregulars'].sum(),
                refined_df_ae['I1 Irregulars'].sum(),
                refined_df_ae['I2 Irregulars'].sum(),
                refined_df_ae['I3 Irregulars'].sum(),
                refined_df_ae['Ar Gas Irregulars'].sum()
            ]
        })

        # Create the bar chart
        chart = alt.Chart(data).mark_bar(color='#008081').encode(
            x=alt.X('Count:Q', title='Number of Batches',scale=alt.Scale(domain=[0, len(refined_df_ae)])),
            y=alt.Y('Irregularities:N', sort='-x', title='Irregularities'),
        ).properties(
            title='Count of True Values for Different Irregularities',
            width=500,
            height=300
        )
        st.altair_chart(chart, use_container_width=True)
    elif region_selections[1]=='Good Batches':
        data = pd.DataFrame({
            'Good Batches': ["Voltage", "Bias Arc", "Arc 1 Current", "Arc 2 Current", "Arc 3 Current", "Ar Gas"],
            'Count': [
                len(refined_df_ae)-refined_df_ae['V Irregulars'].sum(),
                len(refined_df_ae)-refined_df_ae['Bias Arc Irregulars'].sum(),
                len(refined_df_ae)-refined_df_ae['I1 Irregulars'].sum(),
                len(refined_df_ae)-refined_df_ae['I2 Irregulars'].sum(),
                len(refined_df_ae)-refined_df_ae['I3 Irregulars'].sum(),
                len(refined_df_ae)-refined_df_ae['Ar Gas Irregulars'].sum()
            ]
        })

        # Create the bar chart
        chart = alt.Chart(data).mark_bar(color='#008081').encode(
            x=alt.X('Count:Q', title='Number of Batches',scale=alt.Scale(domain=[0, len(refined_df_ae)])),
            y=alt.Y('Good Batches:N', sort='-x', title='Good Batches'),
        ).properties(
            title='Count of True Values for Different Categories',
            width=500,
            height=300
        )
        st.altair_chart(chart, use_container_width=True)
def plot_ps_irr(region_selections):
    refined_df_ps=st.session_state.refined_df_ps
    if region_selections[0]=='All Batches' or region_selections[0]=='Irregular Batches':
        data = pd.DataFrame({
            'Irregularities': ["V Irregulars", "Bias Arc Irregulars", "MFP1 Irregulars", "MFP2 Irregulars", "Ar Gas Irregulars"],
            'Count': [
                refined_df_ps['V Irregulars'].sum(),
                refined_df_ps['Bias Arc Irregulars'].sum(),
                refined_df_ps['MFP1 Irregulars'].sum(),
                refined_df_ps['MFP2 Irregulars'].sum(),
                refined_df_ps['Ar Gas Irregulars'].sum()
            ]
        })

        # Create the bar chart
        chart = alt.Chart(data).mark_bar(color='#008081').encode(
            x=alt.X('Count:Q', title='Number of Batches',scale=alt.Scale(domain=[0, len(refined_df_ps)])),
            y=alt.Y('Irregularities:N', sort='-x', title='Irregularities'),
        ).properties(
            title='Count of True Values for Different Irregularities',
            width=500,
            height=300
        )
        st.altair_chart(chart, use_container_width=True)
    elif region_selections[0]=='Good Batches':
        data = pd.DataFrame({
            'Good Batches': ["Voltage", "Bias Arc", "MFP1 Power", "MFP2 Power", "Ar Gas"],
            'Count': [
                len(refined_df_ps)-refined_df_ps['V Irregulars'].sum(),
                len(refined_df_ps)-refined_df_ps['Bias Arc Irregulars'].sum(),
                len(refined_df_ps)-refined_df_ps['MFP1 Irregulars'].sum(),
                len(refined_df_ps)-refined_df_ps['MFP2 Irregulars'].sum(),
                len(refined_df_ps)-refined_df_ps['Ar Gas Irregulars'].sum()
            ]
        })

        # Create the bar chart
        chart = alt.Chart(data).mark_bar(color='#008081').encode(
            x=alt.X('Count:Q', title='Number of Batches',scale=alt.Scale(domain=[0, len(refined_df_ps)])),
            y=alt.Y('Good Batches:N', sort='-x', title='Good Batches'),
        ).properties(
            title='Count of True Values for Different Categories',
            width=500,
            height=300
        )
        st.altair_chart(chart, use_container_width=True)
def plot_ti_irr(region_selections):
    refined_df_ti=st.session_state.refined_df_ti
    if region_selections[0]=='All Batches' or region_selections[0]=='Irregular Batches':
        data = pd.DataFrame({
            'Irregularities': ["V Irregulars", "Bias Arc Irregulars", "MFP1 Irregulars", "MFP2 Irregulars", "Ar Gas Irregulars"],
            'Count': [
                refined_df_ti['V Irregulars'].sum(),
                refined_df_ti['Bias Arc Irregulars'].sum(),
                refined_df_ti['MFP1 Irregulars'].sum(),
                refined_df_ti['MFP2 Irregulars'].sum(),
                refined_df_ti['Ar Gas Irregulars'].sum()
            ]
        })

        # Create the bar chart
        chart = alt.Chart(data).mark_bar(color='#008081').encode(
            x=alt.X('Count:Q', title='Number of Batches',scale=alt.Scale(domain=[0, len(refined_df_ti)])),
            y=alt.Y('Irregularities:N', sort='-x', title='Irregularities'),
        ).properties(
            title='Count of True Values for Different Irregularities',
            width=500,
            height=300
        )
        st.altair_chart(chart, use_container_width=True)
    elif region_selections[0]=='Good Batches':
        data = pd.DataFrame({
            'Good Batches': ["Voltage", "Bias Arc", "MFP1 Power", "MFP2 Power", "Ar Gas"],
            'Count': [
                len(refined_df_ti)-refined_df_ti['V Irregulars'].sum(),
                len(refined_df_ti)-refined_df_ti['Bias Arc Irregulars'].sum(),
                len(refined_df_ti)-refined_df_ti['MFP1 Irregulars'].sum(),
                len(refined_df_ti)-refined_df_ti['MFP2 Irregulars'].sum(),
                len(refined_df_ti)-refined_df_ti['Ar Gas Irregulars'].sum()
            ]
        })

        # Create the bar chart
        chart = alt.Chart(data).mark_bar(color='#008081').encode(
            x=alt.X('Count:Q', title='Number of Batches',scale=alt.Scale(domain=[0, len(refined_df_ti)])),
            y=alt.Y('Good Batches:N', sort='-x', title='Good Batches'),
        ).properties(
            title='Count of True Values for Different Categories',
            width=500,
            height=300
        )
        st.altair_chart(chart, use_container_width=True)
def sig_mv(signal, window_size):
    mvs=signal
    window = np.ones(window_size) / float(window_size)
    mv_values = np.convolve(mvs, window, 'valid') 
    pad_size = window_size // 2
    padded_ma_array = np.concatenate([np.full(pad_size-1, np.nan), mv_values, np.full(pad_size, np.nan)])
    return padded_ma_array

def plot_trend():
    window_size = st.sidebar.number_input("Baseline window size (no.of Batches)", min_value=10, max_value=120, step=10, value=30) 
    green_limit = st.sidebar.number_input("Green region Pumpdown time limit (mins)", min_value=11, max_value=30, step=1, value=st.session_state.green_limit_global)
    yellow_limit = st.sidebar.number_input("Yellow region Pumpdown time limit (mins)", min_value=11, max_value=40, step=1, value=st.session_state.yellow_limit_global) 
    if st.sidebar.button("Save Region Limits"):
        st.session_state.green_limit_global=green_limit
        st.session_state.yellow_limit_global=yellow_limit

    #green_limit=st.session_state.green_limit_global
    #yellow_limit=st.session_state.yellow_limit_global
    refined_df=st.session_state.refined_df
    pump_time = refined_df["RH mins"].tolist()
    date=np.array(refined_df["BATCH START TIME"])
    mv_pumptime=sig_mv(pump_time,window_size)
    for i in range(len(date)):
        date[i]=date[i][:5]
    greens=[]
    yellows=[]
    reds=[]
    green_start=[]
    yellow_start=[]
    green_end=[]
    yellow_end=[]
    red_start=[]
    red_end=[]
    for i in range(len(mv_pumptime)):
        if mv_pumptime[i]==None:
            pass
        elif mv_pumptime[i]<=green_limit:
            greens.append(i)
        elif mv_pumptime[i]>green_limit and mv_pumptime[i]<=yellow_limit:
            yellows.append(i)
        elif mv_pumptime[i]>yellow_limit:
            reds.append(i)

    for i in range(len(greens)):
        if i==0:
            green_start.append(greens[i])
        elif greens[i]-greens[i-1]>2:
            green_start.append(greens[i])
            green_end.append(greens[i-1])
        if i==len(greens)-1:
            green_end.append(greens[i])
    for i in range(len(yellows)):
        if i==0:
            yellow_start.append(yellows[i]-1)
        elif yellows[i]-yellows[i-1]>2:
            yellow_start.append(yellows[i]-1)
            yellow_end.append(yellows[i-1]+1)
        if i==len(yellows)-1:
            yellow_end.append(yellows[i]+1)
    #print(yellows[0],yellows[-1])
    #print(yellow_start,yellow_end,len(yellow_start),len(yellow_end))
    for i in range(len(reds)):
        if i==0:
            red_start.append(reds[i])
        elif reds[i]-reds[i-1]>2:
            red_start.append(reds[i])
            red_end.append(reds[i-1])
        if i==len(reds)-1:
            red_end.append(reds[i])
    # Prepare the data for Altair
    #print(len(pump_time),len(mv_pumptime))
    data = pd.DataFrame({
        'Batch': range(len(pump_time)),
        'BATCH ID':refined_df['BATCH ID'].to_list(),
        'Pumpdown Time (minutes)': pump_time,
        'Date':date,
        "MV":mv_pumptime
    })
    # Create the Altair chart
    base = alt.Chart(data).encode(
        x=alt.X('Batch:Q', title='Batches', )
    )

    # Line chart
    line = base.mark_line(color="#808081").encode(
        y=alt.Y('Pumpdown Time (minutes):Q', title='Pumpdown Time (minutes)'),
        tooltip=['Date:N', 'Pumpdown Time (minutes):Q','BATCH ID:N']
    ).properties(
        title='Trend of Total Pumpdown Time',
        width=600,
        height=400
    ).interactive()
    line2 = base.mark_line(color='white').encode(
        y=alt.Y('MV:Q'),
        tooltip=['MV:Q']
    ).properties(
        width=600,
        height=400
    )

    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
    background_green = alt.Chart(pd.DataFrame({
        'x': green_start,
        'x2': green_end
    })).mark_rect(
        color='rgb(0,255,0,0.15)'  # Green, red, green
    ).encode(
        x='x:Q',
        x2='x2:Q',
        tooltip=alt.value(None)
    )
    background_yellow = alt.Chart(pd.DataFrame({
        'x': yellow_start,
        'x2': yellow_end
    })).mark_rect(
        color='rgb(255,255,0,0.15)'  # Green, red, green
    ).encode(
        x='x:Q',
        x2='x2:Q',
        tooltip=alt.value(None)
    )
    background_red = alt.Chart(pd.DataFrame({
        'x': red_start,
        'x2': red_end
    })).mark_rect(
        color='rgb(255,0,0,0.15)'  # Green, red, green
    ).encode(
        x='x:Q',
        x2='x2:Q',
        tooltip=alt.value(None)
    )
    # Combine the line chart and text layer
   
    shield=[]
    for i in range(1,len(refined_df)):
        if refined_df['INTERVENSIONS'][i]!=None and "shield_change" in refined_df['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df)):
        if refined_df['INTERVENSIONS'][i]!=None and "target_change" in refined_df['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(background_red,background_green,background_yellow,line, text, line2)     

    # Add shield and target lines based on sidebar inputs
    if st.checkbox('Interventions'):
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

    import streamlit.components.v1 as components
    refined_df["RH mins"] = pd.to_numeric(refined_df["RH mins"], errors='coerce')

    # Extract relevant columns
    pump_time = refined_df["RH mins"].tolist()
    date = np.array(refined_df["BATCH START TIME"])
    batch_id = refined_df['BATCH ID'].to_list()

    # Create DataFrame for Altair
    data2 = pd.DataFrame({
        'Batch': range(len(pump_time)),
        'BATCH ID': batch_id,
        'Pumpdown Time (minutes)': pump_time,
        'Date': date,
    })
    selection = alt.selection_single(fields=['Batch'], nearest=False, on='click', empty='none')
    # Categorize based on limits
    data2['Category'] = pd.cut(data2['Pumpdown Time (minutes)'],
                                bins=[-float('inf'), green_limit, yellow_limit, float('inf')],
                                labels=['green_pumptime', 'yellow_pumptime', 'red_pumptime'])
    scatter = alt.Chart(data2).mark_circle(size=60).encode(
        x='Batch:Q',
        y='Pumpdown Time (minutes):Q',
        color=alt.Color('Category:N', scale=alt.Scale(domain=['green_pumptime', 'yellow_pumptime', 'red_pumptime'],
                                                    range=['#00dd00', 'yellow', 'red']),legend=None),
        tooltip=['BATCH ID:N', 'Pumpdown Time (minutes):Q', 'Date:N']
    ).add_selection(
        selection
    ).interactive()

    # Horizontal lines
    line_green = alt.Chart(pd.DataFrame({'y': [green_limit]})).mark_rule(color='#00dd00',size=2,strokeDash=[5, 5]).encode(y='y:Q')
    line_yellow = alt.Chart(pd.DataFrame({'y': [yellow_limit]})).mark_rule(color='yellow',size=2,strokeDash=[5, 5]).encode(y='y:Q')

    # Combine scatter plot with lines
    chart2 = (scatter + line_green + line_yellow+text).properties(width=800, height=400)

    # Display the chart in Streamlit
    st.altair_chart(chart2, use_container_width=True)
    green_batches_length=len(data2[data2['Category'] == 'green_pumptime'])
    yellow_batches_length=len(data2[data2['Category'] == 'yellow_pumptime'])
    red_batches_length=len(data2[data2['Category'] == 'red_pumptime'])
    sum_batches=green_batches_length+yellow_batches_length+red_batches_length
    horizontal_limit_data={"Region":["Green Region","Yellow Region","Red Region"],
                        "Number of Batches":[green_batches_length,yellow_batches_length,red_batches_length],
                        "Percentage":[str(round((green_batches_length*100/sum_batches),2))+"%",str(round((yellow_batches_length*100/sum_batches),1))+"%",str(round((red_batches_length*100/sum_batches),2))+"%"]}
    #limit_data={"Green Region":["< "+str(green_limit)+" mins"],"Yellow Region":[str(green_limit)+"-"+str(yellow_limit)+" mins"],"Red Region":["> "+str(yellow_limit)+" mins"]}
    horizontal_limit_data=pd.DataFrame(horizontal_limit_data)
    st.table(horizontal_limit_data)

    if st.button('Export Plot'):
        base = alt.Chart(data).encode(
            x=alt.X('Batch:Q', title='Batches', axis=alt.Axis(grid=False))
        )

        # Line chart
        line = base.mark_line(color="#999999",size=1.5).encode(
            y=alt.Y('Pumpdown Time (minutes):Q', title='Pumpdown Time (minutes)'),
            tooltip=['Date:N', 'Pumpdown Time (minutes):Q']
        ).properties(
            width=600,
            height=400,
        )
        line2 = base.mark_line(color='#333333').encode(
            y=alt.Y('MV:Q')
        ).properties(
            width=600,
            height=400
        )

        # Text layer
        text = base.transform_filter(
            alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
        ).mark_text(
            align='left',
            baseline='middle',
            angle=270,  # Vertical text
            dx=-130,  # Adjust horizontal position
            dy=5,  # Adjust vertical position
            color='black'
        ).encode(
            text='Date:N'
        )

        # Background for the first and last thirds of the chart (green) and middle third (red)
        background_green = alt.Chart(pd.DataFrame({
            'x': green_start,
            'x2': green_end
        })).mark_rect(
            color='rgb(0,255,0,0.15)'  # Green, red, green
        ).encode(
            x='x:Q',
            x2='x2:Q',
            tooltip=alt.value(None)
        )
        background_yellow = alt.Chart(pd.DataFrame({
            'x': yellow_start,
            'x2': yellow_end
        })).mark_rect(
            color='rgb(255,255,0,0.15)'  # Green, red, green
        ).encode(
            x='x:Q',
            x2='x2:Q',
            tooltip=alt.value(None)
        )
        background_red = alt.Chart(pd.DataFrame({
            'x': red_start,
            'x2': red_end
        })).mark_rect(
            color='rgb(255,0,0,0.15)'  # Green, red, green
        ).encode(
            x='x:Q',
            x2='x2:Q',
            tooltip=alt.value(None)
        )
        # Combine the line chart and text layer
    
        shield=[]
        for i in range(1,len(refined_df)):
            if refined_df['INTERVENSIONS'][i]!=None and "shield_change" in refined_df['INTERVENSIONS'][i]:
                shield.append(i)
        target=[]
        for i in range(1,len(refined_df)):
            if refined_df['INTERVENSIONS'][i]!=None and "target_change" in refined_df['INTERVENSIONS'][i]:
                target.append(i)
        shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
        target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
        shield_line = alt.Chart(shield_df).mark_rule(
            color='#ff0070', size=2,strokeDash=[5, 5]
        ).encode(
            x='x:Q',
            color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#770077']), legend=alt.Legend(title='Interventions')),
            tooltip=alt.TooltipValue('Shield Change')
        )
        chart = alt.layer(background_red,background_green,background_yellow,line, text, line2,shield_line).properties(width=600,height=300,background='white',title={'text':'Trend of Total Pumpdown Time',"anchor": "middle"}).configure_axis(
            labelColor='black',  # Set the font color for axis labels
            titleColor='black'   # Set the font color for axis titles
        ).configure_title(
            color='black'  # Set the font color for the chart title
        ).configure_legend(
            labelColor='black',  # Set the font color for legend labels
            titleColor='black'   # Set the font color for legend titles
        )
        limit_data={"":["Start Date","End Date","Green Region","Yellow Region","Red Region"],"Values":[refined_df["BATCH START TIME"][0],refined_df["BATCH START TIME"][len(refined_df)-1],"< "+str(green_limit)+" mins",str(green_limit)+"-"+str(yellow_limit)+" mins","> "+str(yellow_limit)+" mins"]}
        #limit_data={"Green Region":["< "+str(green_limit)+" mins"],"Yellow Region":[str(green_limit)+"-"+str(yellow_limit)+" mins"],"Red Region":["> "+str(yellow_limit)+" mins"]}
        limit_df=pd.DataFrame(limit_data)
        st.table(limit_df)
        fig, ax = plt.subplots()
        ax.axis('tight')
        ax.axis('off')

        # Create the table
        table = ax.table(cellText=limit_df.values, colLabels=limit_df.columns, loc='center', cellLoc='center')

        # Customize the font size and make it bold
        table.auto_set_font_size(False)
        table.set_fontsize(6)
        table.scale(1, 1)
        chart.save('Pumpdown Trend alone.png', engine="vl-convert",ppi=200) 

        # Save the table as an image
        plt.savefig('limit_table.png', bbox_inches='tight', dpi=300)
        image1 = Image.open('Pumpdown Trend alone.png')  # Replace with the path to your first image
        image2 = Image.open('limit_table.png')  # Replace with the path to your second image

        # Get the dimensions of the images
        width1, height1 = image1.size
        width2, height2 = image2.size

        # Calculate the dimensions of the combined image
        combined_width = max(width1, width2)+100
        combined_height = height1 + height2-400

        # Create a new image with the calculated dimensions
        combined_image = Image.new('RGB', (combined_width, combined_height), color='white')

        # Paste the first image at the top
        combined_image.paste(image2, (125, height1-250))
        combined_image.paste(image1, (50, 100))
        

        # Save the combined image
        combined_image.save('Pumpdown Trend.png')
        import os
        if os.path.exists('Pumpdown Trend alone.png'):
            # Delete the file
            os.remove('Pumpdown Trend alone.png')
            os.remove('limit_table.png')
        #st.altair_chart(chart, use_container_width=True)
def plot_trend_II():
    window_size = st.sidebar.number_input("Baseline window size (no.of Batches)", min_value=10, max_value=80, step=10, value=20) 
    green_limit = st.sidebar.number_input("Green region Pumpdown time limit (mins)", min_value=1, max_value=10, step=1, value=st.session_state.green_limit_global_II)
    yellow_limit = st.sidebar.number_input("Yellow region Pumpdown time limit (mins)", min_value=3, max_value=18, step=1, value=st.session_state.yellow_limit_global_II) 
    if st.sidebar.button("Save Region Limits"):
        st.session_state.green_limit_global_II=green_limit
        st.session_state.yellow_limit_global_II=yellow_limit

    #green_limit=st.session_state.green_limit_global
    #yellow_limit=st.session_state.yellow_limit_global
    refined_df_II=st.session_state.refined_df_II
    pump_time = refined_df_II["H_II mins"].tolist()
    date=np.array(refined_df_II["BATCH START TIME"])
    mv_pumptime=sig_mv(pump_time,window_size)
    for i in range(len(date)):
        date[i]=date[i][:5]
    greens=[]
    yellows=[]
    reds=[]
    green_start=[]
    yellow_start=[]
    green_end=[]
    yellow_end=[]
    red_start=[]
    red_end=[]
    for i in range(len(mv_pumptime)):
        if mv_pumptime[i]==None:
            pass
        elif mv_pumptime[i]<=green_limit:
            greens.append(i)
        elif mv_pumptime[i]>green_limit and mv_pumptime[i]<=yellow_limit:
            yellows.append(i)
        elif mv_pumptime[i]>yellow_limit:
            reds.append(i)

    for i in range(len(greens)):
        if i==0:
            green_start.append(greens[i])
        elif greens[i]-greens[i-1]>2:
            green_start.append(greens[i])
            green_end.append(greens[i-1])
        if i==len(greens)-1:
            green_end.append(greens[i])
    for i in range(len(yellows)):
        if i==0:
            yellow_start.append(yellows[i]-1)
        elif yellows[i]-yellows[i-1]>2:
            yellow_start.append(yellows[i]-1)
            yellow_end.append(yellows[i-1]+1)
        if i==len(yellows)-1:
            yellow_end.append(yellows[i]+1)
    #print(yellows[0],yellows[-1])
    #print(yellow_start,yellow_end,len(yellow_start),len(yellow_end))
    for i in range(len(reds)):
        if i==0:
            red_start.append(reds[i])
        elif reds[i]-reds[i-1]>2:
            red_start.append(reds[i])
            red_end.append(reds[i-1])
        if i==len(reds)-1:
            red_end.append(reds[i])
    # Prepare the data for Altair
    #print(len(pump_time),len(mv_pumptime))
    data = pd.DataFrame({
        'Batch': range(len(pump_time)),
        'BATCH ID':refined_df_II['BATCH ID'].to_list(),
        'Pumpdown Time (minutes)': pump_time,
        'Date':date,
        "MV":mv_pumptime
    })
    # Create the Altair chart
    base = alt.Chart(data).encode(
        x=alt.X('Batch:Q', title='Batches', )
    )

    # Line chart
    line = base.mark_line(color="#808081").encode(
        y=alt.Y('Pumpdown Time (minutes):Q', title='Pumpdown Time (minutes)'),
        tooltip=['Date:N', 'Pumpdown Time (minutes):Q','BATCH ID:N']
    ).properties(
        title='Trend of Total Pumpdown Time',
        width=600,
        height=400
    ).interactive()
    line2 = base.mark_line(color='white').encode(
        y=alt.Y('MV:Q'),
        tooltip=['MV:Q']
    ).properties(
        width=600,
        height=400
    )

    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
    background_green = alt.Chart(pd.DataFrame({
        'x': green_start,
        'x2': green_end
    })).mark_rect(
        color='rgb(0,255,0,0.15)'  # Green, red, green
    ).encode(
        x='x:Q',
        x2='x2:Q',
        tooltip=alt.value(None)
    )
    background_yellow = alt.Chart(pd.DataFrame({
        'x': yellow_start,
        'x2': yellow_end
    })).mark_rect(
        color='rgb(255,255,0,0.15)'  # Green, red, green
    ).encode(
        x='x:Q',
        x2='x2:Q',
        tooltip=alt.value(None)
    )
    background_red = alt.Chart(pd.DataFrame({
        'x': red_start,
        'x2': red_end
    })).mark_rect(
        color='rgb(255,0,0,0.15)'  # Green, red, green
    ).encode(
        x='x:Q',
        x2='x2:Q',
        tooltip=alt.value(None)
    )
    # Combine the line chart and text layer
   
    shield=[]
    for i in range(1,len(refined_df_II)):
        if refined_df_II['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_II['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_II)):
        if refined_df_II['INTERVENSIONS'][i]!=None and "target_change" in refined_df_II['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(background_red,background_green,background_yellow,line, text, line2)     

    # Add shield and target lines based on sidebar inputs
    if st.checkbox('Interventions'):
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

    import streamlit.components.v1 as components
    refined_df_II["H_II mins"] = pd.to_numeric(refined_df_II["H_II mins"], errors='coerce')

    # Extract relevant columns
    pump_time = refined_df_II["H_II mins"].tolist()
    date = np.array(refined_df_II["BATCH START TIME"])
    batch_id = refined_df_II['BATCH ID'].to_list()

    # Create DataFrame for Altair
    data2 = pd.DataFrame({
        'Batch': range(len(pump_time)),
        'BATCH ID': batch_id,
        'Pumpdown Time (minutes)': pump_time,
        'Date': date,
    })
    selection = alt.selection_single(fields=['Batch'], nearest=False, on='click', empty='none')
    # Categorize based on limits
    data2['Category'] = pd.cut(data2['Pumpdown Time (minutes)'],
                                bins=[-float('inf'), green_limit, yellow_limit, float('inf')],
                                labels=['green_pumptime', 'yellow_pumptime', 'red_pumptime'])
    scatter = alt.Chart(data2).mark_circle(size=60).encode(
        x='Batch:Q',
        y='Pumpdown Time (minutes):Q',
        color=alt.Color('Category:N', scale=alt.Scale(domain=['green_pumptime', 'yellow_pumptime', 'red_pumptime'],
                                                    range=['#00dd00', 'yellow', 'red']),legend=None),
        tooltip=['BATCH ID:N', 'Pumpdown Time (minutes):Q', 'Date:N']
    ).add_selection(
        selection
    ).interactive()

    # Horizontal lines
    line_green = alt.Chart(pd.DataFrame({'y': [green_limit]})).mark_rule(color='#00dd00',size=2,strokeDash=[5, 5]).encode(y='y:Q')
    line_yellow = alt.Chart(pd.DataFrame({'y': [yellow_limit]})).mark_rule(color='yellow',size=2,strokeDash=[5, 5]).encode(y='y:Q')

    # Combine scatter plot with lines
    chart2 = (scatter + line_green + line_yellow+text).properties(width=800, height=400)

    # Display the chart in Streamlit
    st.altair_chart(chart2, use_container_width=True)
    green_batches_length=len(data2[data2['Category'] == 'green_pumptime'])
    yellow_batches_length=len(data2[data2['Category'] == 'yellow_pumptime'])
    red_batches_length=len(data2[data2['Category'] == 'red_pumptime'])
    sum_batches=green_batches_length+yellow_batches_length+red_batches_length
    horizontal_limit_data={"Region":["Green Region","Yellow Region","Red Region"],
                        "Number of Batches":[green_batches_length,yellow_batches_length,red_batches_length],
                        "Percentage":[str(round((green_batches_length*100/sum_batches),2))+"%",str(round((yellow_batches_length*100/sum_batches),1))+"%",str(round((red_batches_length*100/sum_batches),2))+"%"]}
    #limit_data={"Green Region":["< "+str(green_limit)+" mins"],"Yellow Region":[str(green_limit)+"-"+str(yellow_limit)+" mins"],"Red Region":["> "+str(yellow_limit)+" mins"]}
    horizontal_limit_data=pd.DataFrame(horizontal_limit_data)
    st.table(horizontal_limit_data)
def plot_trend_glow():
    window_size = st.sidebar.number_input("Baseline window size (no.of Batches)", min_value=10, max_value=80, step=10, value=20) 
    #green_limit=st.session_state.green_limit_global
    #yellow_limit=st.session_state.yellow_limit_global
    refined_df_glow=st.session_state.refined_df_glow
    v_tot = refined_df_glow["V total"].tolist()
    v_irr = refined_df_glow["V Irregulars"].tolist()
    c_tot = refined_df_glow["I total"].tolist()
    g_tot = refined_df_glow["Gas total"].tolist()
    arc_tot = refined_df_glow["Arc total"].tolist()
    date=np.array(refined_df_glow["BATCH START TIME"])
    v_irr_scat = [v_tot[i] if v_irr[i] == True else None for i in range(len(v_irr))]
    mv_v_tot=sig_mv(v_tot,window_size)
    mv_c_tot=sig_mv(c_tot,window_size)
    mv_g_tot=sig_mv(g_tot,window_size)
    for i in range(len(date)):
        date[i]=date[i][:5]
    # Prepare the data for Altair
    data = pd.DataFrame({
        'Batch': range(len(v_tot)),
        'BATCH ID':refined_df_glow['BATCH ID'].to_list(),
        'Voltage Integral': v_tot,
        'Voltage Irregular':v_irr_scat,
        'Current Integral': c_tot,
        'Ar Gas Integral': g_tot,
        'Bias Arc Count': arc_tot,
        'Date':date,
        "Voltage MV":mv_v_tot,
        "Current MV":mv_c_tot,
        "Ar Gas MV":mv_g_tot,

    })
    # Create the Altair chart
    base = alt.Chart(data).encode(
        x=alt.X('Batch:Q', title='Batches', )
    )

    # Line chart
    v_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Voltage Integral:Q', title='Voltage Integral', scale=alt.Scale(domain=[74800, 75800])),
        tooltip=['Date:N', 'Voltage Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Voltage Integral',
        width=600,
        height=400
    )
    v_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Voltage MV:Q'),
        tooltip=['Voltage MV:Q']
    ).properties(
        width=600,
        height=400
    )
    v_scatter = base.mark_circle(size=60,color='red').encode(
        y='Voltage Irregular:Q',
        tooltip=['BATCH ID:N', 'Voltage Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_glow)):
        if refined_df_glow['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_glow['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_glow)):
        if refined_df_glow['INTERVENSIONS'][i]!=None and "target_change" in refined_df_glow['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(v_tot_line, text,v_scatter)     

    # Add shield and target lines based on sidebar inputs
    Interventions= st.checkbox('Interventions')
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    arc_count = base.mark_bar(color="white").encode(
        y=alt.Y('Bias Arc Count:Q', title='Bias Arc Count'),
        tooltip=['Date:N', 'Bias Arc Count:Q','BATCH ID:N']
    ).properties(
        title='Trend of Bias Arc Count',
        width=600,
        height=250
    )

    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_glow)):
        if refined_df_glow['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_glow['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_glow)):
        if refined_df_glow['INTERVENSIONS'][i]!=None and "target_change" in refined_df_glow['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(arc_count)  
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    c_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Current Integral:Q', title='Current Integral', scale=alt.Scale(domain=[0, 1800])),
        tooltip=['Date:N', 'Current Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Current Integral',
        width=600,
        height=400
    )
    c_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Current MV:Q'),
        tooltip=['Current MV:Q']
    ).properties(
        width=600,
        height=400
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_glow)):
        if refined_df_glow['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_glow['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_glow)):
        if refined_df_glow['INTERVENSIONS'][i]!=None and "target_change" in refined_df_glow['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(c_tot_line, text, c_mv_line)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    g_tot_line = base.mark_line(color="white").encode(
        y=alt.Y('Ar Gas Integral:Q', title='Ar Gas Integral', scale=alt.Scale(domain=[42000, 42050])),
        tooltip=['Date:N', 'Ar Gas Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Ar Gas Integral',
        width=600,
        height=400
    )
    g_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Ar Gas MV:Q'),
        tooltip=['Ar Gas MV:Q']
    ).properties(
        width=600,
        height=400
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_glow)):
        if refined_df_glow['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_glow['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_glow)):
        if refined_df_glow['INTERVENSIONS'][i]!=None and "target_change" in refined_df_glow['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(g_tot_line, text)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

def plot_trend_ac():
    window_size = st.sidebar.number_input("Baseline window size (no.of Batches)", min_value=10, max_value=80, step=10, value=20) 
    #green_limit=st.session_state.green_limit_global
    #yellow_limit=st.session_state.yellow_limit_global
    refined_df_ac=st.session_state.refined_df_ac
    v_tot = refined_df_ac["V total"].tolist()
    v_irr = refined_df_ac["V Irregulars"].tolist()
    c1_irr = refined_df_ac["I1 Irregulars"].tolist()
    c2_irr = refined_df_ac["I2 Irregulars"].tolist()
    c3_irr = refined_df_ac["I3 Irregulars"].tolist()

    c1_tot = refined_df_ac["I1 total"].tolist()
    c2_tot = refined_df_ac["I2 total"].tolist()
    c3_tot = refined_df_ac["I3 total"].tolist()

    g_tot = refined_df_ac["Ar Gas total"].tolist()
    arc_tot = refined_df_ac["Arc total"].tolist()
    date=np.array(refined_df_ac["BATCH START TIME"])
    v_irr_scat = [v_tot[i] if v_irr[i] == True else None for i in range(len(v_irr))]
    c1_irr_scat = [c1_tot[i] if c1_irr[i] == True else None for i in range(len(c1_irr))]
    c2_irr_scat = [c2_tot[i] if c2_irr[i] == True else None for i in range(len(c2_irr))]
    c3_irr_scat = [c3_tot[i] if c3_irr[i] == True else None for i in range(len(c3_irr))]

    mv_v_tot=sig_mv(v_tot,window_size)
    mv_c1_tot=sig_mv(c1_tot,window_size)
    mv_c2_tot=sig_mv(c2_tot,window_size)
    mv_c3_tot=sig_mv(c3_tot,window_size)
    mv_g_tot=sig_mv(g_tot,window_size)

    for i in range(len(date)):
        date[i]=date[i][:5]
    # Prepare the data for Altair
    data = pd.DataFrame({
        'Batch': range(len(v_tot)),
        'BATCH ID':refined_df_ac['BATCH ID'].to_list(),
        'Voltage Integral': v_tot,
        'Voltage Irregular':v_irr_scat,
        'Arc 1 Current Irregular': c1_irr_scat,
        'Arc 2 Current Irregular': c2_irr_scat,
        'Arc 3 Current Irregular': c3_irr_scat,
        'Arc 1 Current Integral': c1_tot,
        'Arc 2 Current Integral': c2_tot,
        'Arc 3 Current Integral': c3_tot,
        'Ar Gas Integral': g_tot,
        'Bias Arc Count': arc_tot,
        'Date':date,
        "Voltage MV":mv_v_tot,
        "Arc 1 Current MV":mv_c1_tot,
        "Arc 2 Current MV":mv_c2_tot,
        "Arc 3 Current MV":mv_c3_tot,
        "Ar Gas MV":mv_g_tot,

    })
    # Create the Altair chart
    base = alt.Chart(data).encode(
        x=alt.X('Batch:Q', title='Batches', )
    )
    c1_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Arc 1 Current Integral:Q', title='Arc 1 Current Integral', scale=alt.Scale(domain=[0, 11000])),
        tooltip=['Date:N', 'Arc 1 Current Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Arc 1 Current Integral',
        width=600,
        height=400
    )
    c1_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Arc 1 Current MV:Q'),
        tooltip=['Arc 1 Current MV:Q']
    ).properties(
        width=600,
        height=400
    )
    c1_scatter = base.mark_circle(size=60,color='red').encode(
        y='Arc 1 Current Irregular:Q',
        tooltip=['BATCH ID:N', 'Arc 1 Current Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )   
   
    shield=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ac['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ac['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(c1_tot_line, text,c1_scatter)     

    # Add shield and target lines based on sidebar inputs
    Interventions= st.checkbox('Interventions')
    if Interventions==True:
        #print(refined_df_ac[refined_df_ac['INTERVENSIONS']!=None])
        chart = alt.layer(chart, shield_line)
    st.altair_chart(chart, use_container_width=True)

    c2_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Arc 2 Current Integral:Q', title='Arc 2 Current Integral', scale=alt.Scale(domain=[0, 11000])),
        tooltip=['Date:N', 'Arc 2 Current Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Arc 2 Current Integral',
        width=600,
        height=400
    )
    c2_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Arc 2 Current MV:Q'),
        tooltip=['Arc 2 Current MV:Q']
    ).properties(
        width=600,
        height=400
    )
    c2_scatter = base.mark_circle(size=60,color='red').encode(
        y='Arc 2 Current Irregular:Q',
        tooltip=['BATCH ID:N', 'Arc 2 Current Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ac['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ac['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(c2_tot_line, text, c2_mv_line,c2_scatter)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    c3_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Arc 3 Current Integral:Q', title='Arc 3 Current Integral', scale=alt.Scale(domain=[0, 11000])),
        tooltip=['Date:N', 'Arc 3 Current Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Arc 3 Current Integral',
        width=600,
        height=400
    )
    c3_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Arc 3 Current MV:Q'),
        tooltip=['Arc 3 Current MV:Q']
    ).properties(
        width=600,
        height=400
    )
    c3_scatter = base.mark_circle(size=60,color='red').encode(
        y='Arc 3 Current Irregular:Q',
        tooltip=['BATCH ID:N', 'Arc 3 Current Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ac['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ac['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(c3_tot_line, text, c3_mv_line,c3_scatter)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    # Line chart
    v_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Voltage Integral:Q', title='Voltage Integral', scale=alt.Scale(domain=[1000, 11000])),
        tooltip=['Date:N', 'Voltage Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Voltage Integral',
        width=600,
        height=400
    )
    v_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Voltage MV:Q'),
        tooltip=['Voltage MV:Q']
    ).properties(
        width=600,
        height=400
    )
    v_scatter = base.mark_circle(size=60,color='red').encode(
        y='Voltage Irregular:Q',
        tooltip=['BATCH ID:N', 'Voltage Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ac['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ac['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(v_tot_line, text,v_scatter)     

    # Add shield and target lines based on sidebar inputs

    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    arc_count = base.mark_bar(color="white").encode(
        y=alt.Y('Bias Arc Count:Q', title='Bias Arc Count'),
        tooltip=['Date:N', 'Bias Arc Count:Q','BATCH ID:N']
    ).properties(
        title='Trend of Bias Arc Count',
        width=600,
        height=250
    )

    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ac['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ac['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(arc_count)  
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
   
    g_tot_line = base.mark_line(color="white").encode(
        y=alt.Y('Ar Gas Integral:Q', title='Ar Gas Integral'),
        tooltip=['Date:N', 'Ar Gas Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Ar Gas Integral',
        width=600,
        height=400
    )
    g_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Ar Gas MV:Q'),
        tooltip=['Ar Gas MV:Q']
    ).properties(
        width=600,
        height=400
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ac['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ac)):
        if refined_df_ac['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ac['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(g_tot_line, text)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
def plot_trend_ae():
    window_size = st.sidebar.number_input("Baseline window size (no.of Batches)", min_value=10, max_value=80, step=10, value=20) 
    #green_limit=st.session_state.green_limit_global
    #yellow_limit=st.session_state.yellow_limit_global
    refined_df_ae=st.session_state.refined_df_ae
    v_tot = refined_df_ae["V total"].tolist()
    v_irr = refined_df_ae["V Irregulars"].tolist()
    c1_irr = refined_df_ae["I1 Irregulars"].tolist()
    c2_irr = refined_df_ae["I2 Irregulars"].tolist()
    c3_irr = refined_df_ae["I3 Irregulars"].tolist()

    c1_tot = refined_df_ae["I1 total"].tolist()
    c2_tot = refined_df_ae["I2 total"].tolist()
    c3_tot = refined_df_ae["I3 total"].tolist()
    g_irr = refined_df_ae["Ar Gas Irregulars"].tolist()
    g_tot = refined_df_ae["Ar Gas total"].tolist()
    arc_tot = refined_df_ae["Arc total"].tolist()
    date=np.array(refined_df_ae["BATCH START TIME"])
    v_irr_scat = [v_tot[i] if v_irr[i] == True else None for i in range(len(v_irr))]
    c1_irr_scat = [c1_tot[i] if c1_irr[i] == True else None for i in range(len(c1_irr))]
    c2_irr_scat = [c2_tot[i] if c2_irr[i] == True else None for i in range(len(c2_irr))]
    c3_irr_scat = [c3_tot[i] if c3_irr[i] == True else None for i in range(len(c3_irr))]
    g_irr_scat = [g_tot[i] if g_irr[i] == True else None for i in range(len(g_irr))]
    mv_v_tot=sig_mv(v_tot,window_size)
    mv_c1_tot=sig_mv(c1_tot,window_size)
    mv_c2_tot=sig_mv(c2_tot,window_size)
    mv_c3_tot=sig_mv(c3_tot,window_size)
    mv_g_tot=sig_mv(g_tot,window_size)

    for i in range(len(date)):
        date[i]=date[i][:5]
    # Prepare the data for Altair
    data = pd.DataFrame({
        'Batch': range(len(v_tot)),
        'BATCH ID':refined_df_ae['BATCH ID'].to_list(),
        'Voltage Integral': v_tot,
        'Voltage Irregular':v_irr_scat,
        'Arc 1 Current Irregular': c1_irr_scat,
        'Arc 2 Current Irregular': c2_irr_scat,
        'Arc 3 Current Irregular': c3_irr_scat,
        'Arc 1 Current Integral': c1_tot,
        'Arc 2 Current Integral': c2_tot,
        'Arc 3 Current Integral': c3_tot,
        'Ar Gas Integral': g_tot,
        'Ar Gas Irregular':g_irr_scat,
        'Bias Arc Count': arc_tot,
        'Date':date,
        "Voltage MV":mv_v_tot,
        "Arc 1 Current MV":mv_c1_tot,
        "Arc 2 Current MV":mv_c2_tot,
        "Arc 3 Current MV":mv_c3_tot,
        "Ar Gas MV":mv_g_tot,

    })
    # Create the Altair chart
    base = alt.Chart(data).encode(
        x=alt.X('Batch:Q', title='Batches', )
    )
    c1_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Arc 1 Current Integral:Q', title='Arc 1 Current Integral', scale=alt.Scale(domain=[min(c1_tot), max(c1_tot)])),
        tooltip=['Date:N', 'Arc 1 Current Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Arc 1 Current Integral',
        width=600,
        height=400
    )
    c1_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Arc 1 Current MV:Q'),
        tooltip=['Arc 1 Current MV:Q']
    ).properties(
        width=600,
        height=400
    )
    c1_scatter = base.mark_circle(size=60,color='red').encode(
        y='Arc 1 Current Irregular:Q',
        tooltip=['BATCH ID:N', 'Arc 1 Current Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )   
   
    shield=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ae['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ae['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(c1_tot_line, text,c1_scatter)     

    # Add shield and target lines based on sidebar inputs
    Interventions= st.checkbox('Interventions')
    if Interventions==True:
        #print(refined_df_ae[refined_df_ae['INTERVENSIONS']!=None])
        chart = alt.layer(chart, shield_line)
    st.altair_chart(chart, use_container_width=True)

    c2_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Arc 2 Current Integral:Q', title='Arc 2 Current Integral', scale=alt.Scale(domain=[min(c2_tot), max(c2_tot)])),
        tooltip=['Date:N', 'Arc 2 Current Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Arc 2 Current Integral',
        width=600,
        height=400
    )
    c2_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Arc 2 Current MV:Q'),
        tooltip=['Arc 2 Current MV:Q']
    ).properties(
        width=600,
        height=400
    )
    c2_scatter = base.mark_circle(size=60,color='red').encode(
        y='Arc 2 Current Irregular:Q',
        tooltip=['BATCH ID:N', 'Arc 2 Current Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ae['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ae['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(c2_tot_line, text, c2_mv_line,c2_scatter)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    st.altair_chart(chart, use_container_width=True)
    c3_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Arc 3 Current Integral:Q', title='Arc 3 Current Integral', scale=alt.Scale(domain=[min(c3_tot), max(c3_tot)])),
        tooltip=['Date:N', 'Arc 3 Current Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Arc 3 Current Integral',
        width=600,
        height=400
    )
    c3_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Arc 3 Current MV:Q'),
        tooltip=['Arc 3 Current MV:Q']
    ).properties(
        width=600,
        height=400
    )
    c3_scatter = base.mark_circle(size=60,color='red').encode(
        y='Arc 3 Current Irregular:Q',
        tooltip=['BATCH ID:N', 'Arc 3 Current Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ae['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ae['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(c3_tot_line, text, c3_mv_line,c3_scatter)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    # Line chart
    v_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Voltage Integral:Q', title='Voltage Integral', scale=alt.Scale(domain=[min(v_tot), max(v_tot)])),
        tooltip=['Date:N', 'Voltage Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Voltage Integral',
        width=600,
        height=400
    )
    v_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Voltage MV:Q'),
        tooltip=['Voltage MV:Q']
    ).properties(
        width=600,
        height=400
    )
    v_scatter = base.mark_circle(size=60,color='red').encode(
        y='Voltage Irregular:Q',
        tooltip=['BATCH ID:N', 'Voltage Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ae['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ae['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(v_tot_line, text,v_scatter)     

    # Add shield and target lines based on sidebar inputs

    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    arc_count = base.mark_bar(color="white").encode(
        y=alt.Y('Bias Arc Count:Q', title='Bias Arc Count'),
        tooltip=['Date:N', 'Bias Arc Count:Q','BATCH ID:N']
    ).properties(
        title='Trend of Bias Arc Count',
        width=600,
        height=250
    )

    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ae['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ae['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(arc_count)  
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
   
    g_tot_line = base.mark_line(color="white").encode(
        y=alt.Y('Ar Gas Integral:Q', title='Ar Gas Integral'),
        tooltip=['Date:N', 'Ar Gas Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Ar Gas Integral',
        width=600,
        height=400
    )
    g_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Ar Gas MV:Q'),
        tooltip=['Ar Gas MV:Q']
    ).properties(
        width=600,
        height=400
    )
    g_scatter = base.mark_circle(size=60,color='red').encode(
        y='Ar Gas Irregular:Q',
        tooltip=['BATCH ID:N', 'Ar Gas Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ae['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ae)):
        if refined_df_ae['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ae['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(g_tot_line, text, g_scatter)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
def plot_trend_ps():
    window_size = st.sidebar.number_input("Baseline window size (no.of Batches)", min_value=10, max_value=80, step=10, value=10) 
    #green_limit=st.session_state.green_limit_global
    #yellow_limit=st.session_state.yellow_limit_global
    refined_df_ps=st.session_state.refined_df_ps
    v_tot = refined_df_ps["V total"].tolist()
    v_irr = refined_df_ps["V Irregulars"].tolist()
    mfp1_irr = refined_df_ps["MFP1 Irregulars"].tolist()
    mfp2_irr = refined_df_ps["MFP2 Irregulars"].tolist()

    mfp1_tot = refined_df_ps["MFP1 total"].tolist()
    mfp2_tot = refined_df_ps["MFP2 total"].tolist()

    g_tot = refined_df_ps["Ar Gas total"].tolist()
    g_irr = refined_df_ps["Ar Gas Irregulars"].tolist()
    arc_tot = refined_df_ps["Arc total"].tolist()
    date=np.array(refined_df_ps["BATCH START TIME"])
    v_irr_scat = [v_tot[i] if v_irr[i] == True else None for i in range(len(v_irr))]
    mfp1_irr_scat = [mfp1_tot[i] if mfp1_irr[i] == True else None for i in range(len(mfp1_irr))]
    mfp2_irr_scat = [mfp2_tot[i] if mfp2_irr[i] == True else None for i in range(len(mfp2_irr))]
    g_irr_scat = [g_tot[i] if g_irr[i] == True else None for i in range(len(g_irr))]

    mv_v_tot=sig_mv(v_tot,window_size)
    mv_mfp1_tot=sig_mv(mfp1_tot,window_size)
    mv_mfp2_tot=sig_mv(mfp2_tot,window_size)
    mv_g_tot=sig_mv(g_tot,window_size)

    for i in range(len(date)):
        date[i]=date[i][:5]
    # Prepare the data for Altair
    data = pd.DataFrame({
        'Batch': range(len(v_tot)),
        'BATCH ID':refined_df_ps['BATCH ID'].to_list(),
        'Voltage Integral': v_tot,
        'Voltage Irregular':v_irr_scat,
        'MFP1 Power Irregular': mfp1_irr_scat,
        'MFP2 Power Irregular': mfp2_irr_scat,
        'MFP1 Power Integral': mfp1_tot,
        'MFP2 Power Integral': mfp2_tot,
        'Ar Gas Integral': g_tot,
        'Ar Gas Irregular': g_irr_scat,
        'Bias Arc Count': arc_tot,
        'Date':date,
        "Voltage MV":mv_v_tot,
        "MFP1 Power MV":mv_mfp1_tot,
        "MFP2 Power MV":mv_mfp2_tot,
        "Ar Gas MV":mv_g_tot,

    })
    # Create the Altair chart
    base = alt.Chart(data).encode(
        x=alt.X('Batch:Q', title='Batches', )
    )
    mfp1_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('MFP1 Power Integral:Q', title='MFP1 Power Integral', scale=alt.Scale(domain=[min(mfp1_tot), max(mfp1_tot)])),
        tooltip=['Date:N', 'MFP1 Power Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of MFP1 Power Integral',
        width=600,
        height=400
    )
    mfp1_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('MFP1 Power MV:Q'),
        tooltip=['MFP1 Power MV:Q']
    ).properties(
        width=600,
        height=400
    )
    mfp1_scatter = base.mark_circle(size=60,color='red').encode(
        y='MFP1 Power Irregular:Q',
        tooltip=['BATCH ID:N', 'MFP1 Power Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )   
   
    shield=[]
    for i in range(1,len(refined_df_ps)):
        if refined_df_ps['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ps['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ps)):
        if refined_df_ps['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ps['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(mfp1_tot_line, text,mfp1_scatter)     

    # Add shield and target lines based on sidebar inputs
    Interventions= st.checkbox('Interventions')
    if Interventions==True:
        #print(refined_df_ps[refined_df_ps['INTERVENSIONS']!=None])
        chart = alt.layer(chart, shield_line)
    st.altair_chart(chart, use_container_width=True)

    mfp2_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('MFP2 Power Integral:Q', title='MFP2 Power Integral', scale=alt.Scale(domain=[min(mfp2_tot), max(mfp2_tot)])),
        tooltip=['Date:N', 'MFP2 Power Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of MFP2 Power Integral',
        width=600,
        height=400
    )
    mfp2_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('MFP2 Power MV:Q'),
        tooltip=['MFP2 Power MV:Q']
    ).properties(
        width=600,
        height=400
    )
    mfp2_scatter = base.mark_circle(size=60,color='red').encode(
        y='MFP2 Power Irregular:Q',
        tooltip=['BATCH ID:N', 'MFP2 Power Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ps)):
        if refined_df_ps['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ps['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ps)):
        if refined_df_ps['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ps['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(mfp2_tot_line, text, mfp2_mv_line,mfp2_scatter)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    st.altair_chart(chart, use_container_width=True)
    # Line chart
    v_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Voltage Integral:Q', title='Voltage Integral', scale=alt.Scale(domain=[min(v_tot), max(v_tot)])),
        tooltip=['Date:N', 'Voltage Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Voltage Integral',
        width=600,
        height=400
    )
    v_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Voltage MV:Q'),
        tooltip=['Voltage MV:Q']
    ).properties(
        width=600,
        height=400
    )
    v_scatter = base.mark_circle(size=60,color='red').encode(
        y='Voltage Irregular:Q',
        tooltip=['BATCH ID:N', 'Voltage Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ps)):
        if refined_df_ps['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ps['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ps)):
        if refined_df_ps['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ps['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(v_tot_line, text,v_scatter)     

    # Add shield and target lines based on sidebar inputs

    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    arc_count = base.mark_bar(color="white").encode(
        y=alt.Y('Bias Arc Count:Q', title='Bias Arc Count'),
        tooltip=['Date:N', 'Bias Arc Count:Q','BATCH ID:N']
    ).properties(
        title='Trend of Bias Arc Count',
        width=600,
        height=250
    )

    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ps)):
        if refined_df_ps['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ps['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ps)):
        if refined_df_ps['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ps['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(arc_count)  
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
   
    g_tot_line = base.mark_line(color="white").encode(
        y=alt.Y('Ar Gas Integral:Q', title='Ar Gas Integral'),
        tooltip=['Date:N', 'Ar Gas Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Ar Gas Integral',
        width=600,
        height=400
    )
    g_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Ar Gas MV:Q'),
        tooltip=['Ar Gas MV:Q']
    ).properties(
        width=600,
        height=400
    )
    g_scatter = base.mark_circle(size=60,color='red').encode(
        y='Ar Gas Irregular:Q',
        tooltip=['BATCH ID:N', 'Ar Gas Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ps)):
        if refined_df_ps['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ps['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ps)):
        if refined_df_ps['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ps['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(g_tot_line, text, g_scatter)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
def plot_trend_ti():
    window_size = st.sidebar.number_input("Baseline window size (no.of Batches)", min_value=10, max_value=80, step=10, value=10) 
    #green_limit=st.session_state.green_limit_global
    #yellow_limit=st.session_state.yellow_limit_global
    refined_df_ti=st.session_state.refined_df_ti
    v_tot = refined_df_ti["V total"].tolist()
    v_irr = refined_df_ti["V Irregulars"].tolist()
    mfp1_irr = refined_df_ti["MFP1 Irregulars"].tolist()
    mfp2_irr = refined_df_ti["MFP2 Irregulars"].tolist()

    mfp1_tot = refined_df_ti["MFP1 total"].tolist()
    mfp2_tot = refined_df_ti["MFP2 total"].tolist()

    g_tot = refined_df_ti["Ar Gas total"].tolist()
    g_irr = refined_df_ti["Ar Gas Irregulars"].tolist()
    arc_tot = refined_df_ti["Arc total"].tolist()
    date=np.array(refined_df_ti["BATCH START TIME"])
    v_irr_scat = [v_tot[i] if v_irr[i] == True else None for i in range(len(v_irr))]
    mfp1_irr_scat = [mfp1_tot[i] if mfp1_irr[i] == True else None for i in range(len(mfp1_irr))]
    mfp2_irr_scat = [mfp2_tot[i] if mfp2_irr[i] == True else None for i in range(len(mfp2_irr))]
    g_irr_scat = [g_tot[i] if g_irr[i] == True else None for i in range(len(g_irr))]

    mv_v_tot=sig_mv(v_tot,window_size)
    mv_mfp1_tot=sig_mv(mfp1_tot,window_size)
    mv_mfp2_tot=sig_mv(mfp2_tot,window_size)
    mv_g_tot=sig_mv(g_tot,window_size)

    for i in range(len(date)):
        date[i]=date[i][:5]
    # Prepare the data for Altair
    data = pd.DataFrame({
        'Batch': range(len(v_tot)),
        'BATCH ID':refined_df_ti['BATCH ID'].to_list(),
        'Voltage Integral': v_tot,
        'Voltage Irregular':v_irr_scat,
        'MFP1 Power Irregular': mfp1_irr_scat,
        'MFP2 Power Irregular': mfp2_irr_scat,
        'MFP1 Power Integral': mfp1_tot,
        'MFP2 Power Integral': mfp2_tot,
        'Ar Gas Integral': g_tot,
        'Ar Gas Irregular': g_irr_scat,
        'Bias Arc Count': arc_tot,
        'Date':date,
        "Voltage MV":mv_v_tot,
        "MFP1 Power MV":mv_mfp1_tot,
        "MFP2 Power MV":mv_mfp2_tot,
        "Ar Gas MV":mv_g_tot,

    })
    # Create the Altair chart
    base = alt.Chart(data).encode(
        x=alt.X('Batch:Q', title='Batches', )
    )
    mfp1_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('MFP1 Power Integral:Q', title='MFP1 Power Integral', scale=alt.Scale(domain=[min(mfp1_tot), max(mfp1_tot)])),
        tooltip=['Date:N', 'MFP1 Power Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of MFP1 Power Integral',
        width=600,
        height=400
    )
    mfp1_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('MFP1 Power MV:Q'),
        tooltip=['MFP1 Power MV:Q']
    ).properties(
        width=600,
        height=400
    )
    mfp1_scatter = base.mark_circle(size=60,color='red').encode(
        y='MFP1 Power Irregular:Q',
        tooltip=['BATCH ID:N', 'MFP1 Power Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )   
   
    shield=[]
    for i in range(1,len(refined_df_ti)):
        if refined_df_ti['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ti['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ti)):
        if refined_df_ti['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ti['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(mfp1_tot_line, text,mfp1_scatter)     

    # Add shield and target lines based on sidebar inputs
    Interventions= st.checkbox('Interventions')
    if Interventions==True:
        #print(refined_df_ti[refined_df_ti['INTERVENSIONS']!=None])
        chart = alt.layer(chart, shield_line)
    st.altair_chart(chart, use_container_width=True)

    mfp2_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('MFP2 Power Integral:Q', title='MFP2 Power Integral', scale=alt.Scale(domain=[min(mfp2_tot), max(mfp2_tot)])),
        tooltip=['Date:N', 'MFP2 Power Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of MFP2 Power Integral',
        width=600,
        height=400
    )
    mfp2_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('MFP2 Power MV:Q'),
        tooltip=['MFP2 Power MV:Q']
    ).properties(
        width=600,
        height=400
    )
    mfp2_scatter = base.mark_circle(size=60,color='red').encode(
        y='MFP2 Power Irregular:Q',
        tooltip=['BATCH ID:N', 'MFP2 Power Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ti)):
        if refined_df_ti['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ti['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ti)):
        if refined_df_ti['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ti['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(mfp2_tot_line, text, mfp2_mv_line,mfp2_scatter)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    st.altair_chart(chart, use_container_width=True)
    # Line chart
    v_tot_line = base.mark_line(color="#808081").encode(
        y=alt.Y('Voltage Integral:Q', title='Voltage Integral', scale=alt.Scale(domain=[min(v_tot), max(v_tot)])),
        tooltip=['Date:N', 'Voltage Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Voltage Integral',
        width=600,
        height=400
    )
    v_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Voltage MV:Q'),
        tooltip=['Voltage MV:Q']
    ).properties(
        width=600,
        height=400
    )
    v_scatter = base.mark_circle(size=60,color='red').encode(
        y='Voltage Irregular:Q',
        tooltip=['BATCH ID:N', 'Voltage Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ti)):
        if refined_df_ti['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ti['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ti)):
        if refined_df_ti['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ti['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(v_tot_line, text,v_scatter)     

    # Add shield and target lines based on sidebar inputs

    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
    arc_count = base.mark_bar(color="white").encode(
        y=alt.Y('Bias Arc Count:Q', title='Bias Arc Count'),
        tooltip=['Date:N', 'Bias Arc Count:Q','BATCH ID:N']
    ).properties(
        title='Trend of Bias Arc Count',
        width=600,
        height=250
    )

    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ti)):
        if refined_df_ti['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ti['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ti)):
        if refined_df_ti['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ti['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(arc_count)  
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
   
    g_tot_line = base.mark_line(color="white").encode(
        y=alt.Y('Ar Gas Integral:Q', title='Ar Gas Integral'),
        tooltip=['Date:N', 'Ar Gas Integral:Q','BATCH ID:N']
    ).properties(
        title='Trend of Ar Gas Integral',
        width=600,
        height=400
    )
    g_mv_line = base.mark_line(size=1,color='white').encode(
        y=alt.Y('Ar Gas MV:Q'),
        tooltip=['Ar Gas MV:Q']
    ).properties(
        width=600,
        height=400
    )
    g_scatter = base.mark_circle(size=60,color='red').encode(
        y='Ar Gas Irregular:Q',
        tooltip=['BATCH ID:N', 'Ar Gas Irregular:Q', 'Date:N']
    )
    # Text layer
    text = base.transform_filter(
        alt.datum.Batch % 7 == 0  # Filter to show one label for every ten batches
    ).mark_text(
        align='left',
        baseline='middle',
        angle=270,  # Vertical text
        dx=-130,  # Adjust horizontal position
        dy=5,  # Adjust vertical position
        color='white'
    ).encode(
        text='Date:N'
    )

    # Background for the first and last thirds of the chart (green) and middle third (red)
   
   
    shield=[]
    for i in range(1,len(refined_df_ti)):
        if refined_df_ti['INTERVENSIONS'][i]!=None and "shield_change" in refined_df_ti['INTERVENSIONS'][i]:
            shield.append(i)
    target=[]
    for i in range(1,len(refined_df_ti)):
        if refined_df_ti['INTERVENSIONS'][i]!=None and "target_change" in refined_df_ti['INTERVENSIONS'][i]:
            target.append(i)
    shield_df = pd.DataFrame({'x': shield+target, 'Type': ['Shield Change']*len(shield)+['Target Change']*len(target)})
    target_df = pd.DataFrame({'Target': target, 'TypeT': 'Target Change'})
    shield_line = alt.Chart(shield_df).mark_rule(
        color='#ff0070', size=2,strokeDash=[5, 5]
    ).encode(
        x='x:Q',
        color=alt.Color('Type:N', scale=alt.Scale(domain=['Shield Change','Target Change'], range=['#ff0070','#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Shield Change')
    )

    target_line = alt.Chart(target_df).mark_rule(
        color='#ffa000', size=2,strokeDash=[5, 5]
    ).encode(
        x='Target:Q',
        color=alt.Color('TypeT:N', scale=alt.Scale(domain=['Target Change'], range=['#ffa000']), legend=alt.Legend(title='Interventions')),
        tooltip=alt.TooltipValue('Target Change')
    )

    # Combine all layers and display
    chart = alt.layer(g_tot_line, text, g_scatter)     

    # Add shield and target lines based on sidebar inputs
    if Interventions==True:
        chart = alt.layer(chart, shield_line)
    #chart = chart.properties(
    #    background='white'
    #)
    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
def plot_bellcurve():
    rh_mins=st.session_state.rh_mins
    data_points = rh_mins

    # Calculate PMF
    hist, bins = np.histogram(data_points, bins=np.arange(1, 40))
    pmf = hist / np.sum(hist)
    
    # Prepare data for Altair
    pmf_data = pd.DataFrame({
        'Pumpdown Time (mins)': bins[:-1],
        'Probability': pmf
    })

    pmf_chart = alt.Chart(pmf_data).mark_bar(width=8,color="#00bbab").encode(
        x='Pumpdown Time (mins):Q',
        y='Probability:Q'
    ).properties(
        title='Probability Mass Function of Pumpdown Time',
        width=400,
        height=300
    )

    # Prepare data for the bell curve
    x_grid = np.linspace(min(data_points), max(data_points), 1000)
    mu, sigma = np.mean(data_points), np.std(data_points)
    gaussian_curve = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(x_grid - mu) ** 2 / (2 * sigma ** 2))
    
    bell_curve_data = pd.DataFrame({
        'Pumpdown Time (mins)': x_grid,
        'Density': gaussian_curve
    })

    scatter_data = pd.DataFrame({
        'Pumpdown Time (mins)': data_points,
        'Density': np.zeros_like(data_points)
    })

    scatter_chart = alt.Chart(scatter_data).mark_point(filled=True, opacity=0.5).encode(
        x='Pumpdown Time (mins):Q',
        y='Density:Q'
    ).properties(
        width=400,
        height=300
    )

    bell_curve_chart = alt.Chart(bell_curve_data).mark_line(color='#00ddc7', strokeDash=[5, 5]).encode(
        x='Pumpdown Time (mins):Q',
        y='Density:Q'
    ).properties(
        title=f'Bell Curve depicting occurrences of total Pumpdown time (mean={mu.round(1)}, std={sigma.round(1)})',
        width=400,
        height=300
    )

    combined_chart = alt.layer(scatter_chart, bell_curve_chart).resolve_scale(
        y='independent'
    )

    st.altair_chart(pmf_chart | combined_chart, use_container_width=True)

def plot_bellcurve_II():
    h_II_mins=st.session_state.h_II_mins
    data_points = h_II_mins

    # Calculate PMF
    hist, bins = np.histogram(data_points, bins=np.arange(1, 40))
    pmf = hist / np.sum(hist)
    
    # Prepare data for Altair
    pmf_data = pd.DataFrame({
        'Pumpdown II Time (mins)': bins[:-1],
        'Probability': pmf
    })

    pmf_chart = alt.Chart(pmf_data).mark_bar(width=8,color="#00bbab").encode(
        x='Pumpdown II Time (mins):Q',
        y='Probability:Q'
    ).properties(
        title='Probability Mass Function of Pumpdown Time',
        width=400,
        height=300
    )

    # Prepare data for the bell curve
    x_grid = np.linspace(min(data_points), max(data_points), 1000)
    mu, sigma = np.mean(data_points), np.std(data_points)
    gaussian_curve = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-(x_grid - mu) ** 2 / (2 * sigma ** 2))
    
    bell_curve_data = pd.DataFrame({
        'Pumpdown II Time (mins)': x_grid,
        'Density': gaussian_curve
    })

    scatter_data = pd.DataFrame({
        'Pumpdown II Time (mins)': data_points,
        'Density': np.zeros_like(data_points)
    })

    scatter_chart = alt.Chart(scatter_data).mark_point(filled=True, opacity=0.5).encode(
        x='Pumpdown II Time (mins):Q',
        y='Density:Q'
    ).properties(
        width=400,
        height=300
    )

    bell_curve_chart = alt.Chart(bell_curve_data).mark_line(color='#00ddc7', strokeDash=[5, 5]).encode(
        x='Pumpdown II Time (mins):Q',
        y='Density:Q'
    ).properties(
        title=f'Bell Curve depicting occurrences of total Pumpdown II time (mean={mu.round(1)}, std={sigma.round(1)})',
        width=400,
        height=300
    )

    combined_chart = alt.layer(scatter_chart, bell_curve_chart).resolve_scale(
        y='independent'
    )

    st.altair_chart(pmf_chart | combined_chart, use_container_width=True)
def list_to_matrix(lst, elements_per_subarray):
    matrix = [lst[i:i + elements_per_subarray] for i in range(0, len(lst), elements_per_subarray)]
    return matrix
def calculate_time_difference(datetime_str1, datetime_str2):
    from datetime import datetime
    format_str = "%d/%m/%Y %H:%M:%S"
    dt1 = datetime.strptime(datetime_str1, format_str)
    dt2 = datetime.strptime(datetime_str2, format_str)
    time_elapsed = dt2 - dt1
    days = time_elapsed.days
    seconds = time_elapsed.seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return days, hours, minutes, seconds
def plot_coating_type():
    refined_df=st.session_state.refined_df
    coating_types=np.array(refined_df['COATING TYPE'].unique())
    coating_dict={}
    for i in coating_types:    
        if str(i) =="nan" or i == None:
            continue
        else:
            coating_dict[str(i)]=np.array(refined_df[refined_df['COATING TYPE'] == i]['RH mins'])
    plot_data_coat=[]
    for i in coating_dict.keys():
        plot_data_coat.append([str(i),round(np.average(coating_dict[i]), 2), round(np.max(coating_dict[i]), 2), round(np.min(coating_dict[i]),2), len(coating_dict[i])])
    plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "RH Avg", "RH Max", "RH Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('RH Avg:Q', title='RH Time (Mins)'),
        tooltip=[
            alt.Tooltip('Coating Type:O', title='Coating'),
            alt.Tooltip('RH Avg:Q', title='Average RH Time'),
            alt.Tooltip('RH Max:Q', title='Max RH Time'),
            alt.Tooltip('RH Min:Q', title='Min RH Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='RH Avg:Q'
    )

    chart = (bars + text).properties(
        title='Coating Type vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_coating_type_II():
    refined_df_II=st.session_state.refined_df_II
    coating_types=np.array(refined_df_II['COATING TYPE'].unique())
    coating_dict={}
    for i in coating_types:    
        if str(i) =="nan" or i == None:
            continue
        else:
            coating_dict[str(i)]=np.array(refined_df_II[refined_df_II['COATING TYPE'] == i]['H_II mins'])
    plot_data_coat=[]
    for i in coating_dict.keys():
        plot_data_coat.append([str(i),round(np.average(coating_dict[i]), 2), round(np.max(coating_dict[i]), 2), round(np.min(coating_dict[i]),2), len(coating_dict[i])])
    plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "H_II Avg", "H_II Max", "H_II Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('H_II Avg:Q', title='H_II Time (Mins)'),
        tooltip=[
            alt.Tooltip('Coating Type:O', title='Coating'),
            alt.Tooltip('H_II Avg:Q', title='Average H_II Time'),
            alt.Tooltip('H_II Max:Q', title='Max H_II Time'),
            alt.Tooltip('H_II Min:Q', title='Min H_II Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='H_II Avg:Q'
    )

    chart = (bars + text).properties(
        title='Coating Type vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_coating_type_glow():
    refined_df_glow=st.session_state.refined_df_glow
    complete_refined_df_glow=st.session_state.complete_refined_df_glow
    region_selections_glow=st.session_state.region_selections_glow

    if region_selections_glow[0]==True:
        coating_types=np.array(refined_df_glow['COATING TYPE'].unique())
        coating_dict={}
        for i in coating_types:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict[str(i)]=len(refined_df_glow[refined_df_glow['COATING TYPE'] == i])
        plot_data_coat=[]
        for i in coating_dict.keys():
            plot_data_coat.append([str(i),coating_dict[str(i)]])
        plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Coating Type:O', title='Coating'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        )

    else:
        coating_types=np.array(refined_df_glow['COATING TYPE'].unique())
        coating_dict={}
        for i in coating_types:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict[str(i)]=len(refined_df_glow[refined_df_glow['COATING TYPE'] == i])
        coating_types_full=np.array(complete_refined_df_glow['COATING TYPE'].unique())
        coating_dict_full={}
        for i in coating_types_full:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict_full[str(i)]=len(complete_refined_df_glow[complete_refined_df_glow['COATING TYPE'] == i])
        plot_data_coat=[]
        for i in coating_dict.keys():
            plot_data_coat.append([str(i),np.round(coating_dict[str(i)]/coating_dict_full[str(i)],2),coating_dict[str(i)],coating_dict_full[str(i)]])
        plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "Batches", "filter batch", 'full batch'])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Batches', scale=alt.Scale(domain=[0,1]) ),
            tooltip=[
                alt.Tooltip('Coating Type:O', title='Coating'),
                alt.Tooltip('Batches:Q', title='Fraction from total batches'),
                alt.Tooltip('filter batch:Q', title='Number of Filtered Batches'),
                alt.Tooltip('full batch:Q', title='Number of Total batches')

            ]
        )

    chart = (bars).properties(
        title='Coating Type vs Arc Etching Batches',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_coating_type_ac():
    refined_df_ac=st.session_state.refined_df_ac
    complete_refined_df_ac=st.session_state.complete_refined_df_ac
    region_selections_ac=st.session_state.region_selections_ac

    if region_selections_ac[0]==True:
        coating_types=np.array(refined_df_ac['COATING TYPE'].unique())
        coating_dict={}
        for i in coating_types:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict[str(i)]=len(refined_df_ac[refined_df_ac['COATING TYPE'] == i])
        plot_data_coat=[]
        for i in coating_dict.keys():
            plot_data_coat.append([str(i),coating_dict[str(i)]])
        plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Coating Type:O', title='Coating'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        )

    else:
        coating_types=np.array(refined_df_ac['COATING TYPE'].unique())
        coating_dict={}
        for i in coating_types:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict[str(i)]=len(refined_df_ac[refined_df_ac['COATING TYPE'] == i])
        coating_types_full=np.array(complete_refined_df_ac['COATING TYPE'].unique())
        coating_dict_full={}
        for i in coating_types_full:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict_full[str(i)]=len(complete_refined_df_ac[complete_refined_df_ac['COATING TYPE'] == i])
        plot_data_coat=[]
        for i in coating_dict.keys():
            plot_data_coat.append([str(i),np.round(coating_dict[str(i)]/coating_dict_full[str(i)],2),coating_dict[str(i)],coating_dict_full[str(i)]])
        plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "Batches", "filter batch", 'full batch'])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Batches', scale=alt.Scale(domain=[0,1]) ),
            tooltip=[
                alt.Tooltip('Coating Type:O', title='Coating'),
                alt.Tooltip('Batches:Q', title='Fraction from total batches'),
                alt.Tooltip('filter batch:Q', title='Number of Filtered Batches'),
                alt.Tooltip('full batch:Q', title='Number of Total batches')

            ]
        )

    chart = (bars).properties(
        title='Coating Type vs Arc Etching Batches',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_coating_type_ae():
    refined_df_ae=st.session_state.refined_df_ae
    complete_refined_df_ae=st.session_state.complete_refined_df_ae
    region_selections_ae=st.session_state.region_selections_ae

    if region_selections_ae[1]=='All Batches':
        coating_types=np.array(refined_df_ae['COATING TYPE'].unique())
        coating_dict={}
        for i in coating_types:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict[str(i)]=len(refined_df_ae[refined_df_ae['COATING TYPE'] == i])
        plot_data_coat=[]
        for i in coating_dict.keys():
            plot_data_coat.append([str(i),coating_dict[str(i)]])
        plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Coating Type:O', title='Coating'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        )

    else:
        coating_types=np.array(refined_df_ae['COATING TYPE'].unique())
        coating_dict={}
        for i in coating_types:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict[str(i)]=len(refined_df_ae[refined_df_ae['COATING TYPE'] == i])
        coating_types_full=np.array(complete_refined_df_ae['COATING TYPE'].unique())
        coating_dict_full={}
        for i in coating_types_full:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict_full[str(i)]=len(complete_refined_df_ae[complete_refined_df_ae['COATING TYPE'] == i])
        plot_data_coat=[]
        for i in coating_dict.keys():
            plot_data_coat.append([str(i),np.round(coating_dict[str(i)]/coating_dict_full[str(i)],2),coating_dict[str(i)],coating_dict_full[str(i)]])
        plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "Batches", "filter batch", 'full batch'])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Batches', scale=alt.Scale(domain=[0,1]) ),
            tooltip=[
                alt.Tooltip('Coating Type:O', title='Coating'),
                alt.Tooltip('Batches:Q', title='Fraction from total batches'),
                alt.Tooltip('filter batch:Q', title='Number of Filtered Batches'),
                alt.Tooltip('full batch:Q', title='Number of Total batches')

            ]
        )

    chart = (bars).properties(
        title='Coating Type vs Arc Etching Batches',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_coating_type_ps():
    refined_df_ps=st.session_state.refined_df_ps
    complete_refined_df_ps=st.session_state.complete_refined_df_ps
    region_selections_ps=st.session_state.region_selections_ps

    if region_selections_ps[0]=='All Batches':
        coating_types=np.array(refined_df_ps['COATING TYPE'].unique())
        coating_dict={}
        for i in coating_types:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict[str(i)]=len(refined_df_ps[refined_df_ps['COATING TYPE'] == i])
        plot_data_coat=[]
        for i in coating_dict.keys():
            plot_data_coat.append([str(i),coating_dict[str(i)]])
        plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Coating Type:O', title='Coating'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        )

    else:
        coating_types=np.array(refined_df_ps['COATING TYPE'].unique())
        coating_dict={}
        for i in coating_types:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict[str(i)]=len(refined_df_ps[refined_df_ps['COATING TYPE'] == i])
        coating_types_full=np.array(complete_refined_df_ps['COATING TYPE'].unique())
        coating_dict_full={}
        for i in coating_types_full:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict_full[str(i)]=len(complete_refined_df_ps[complete_refined_df_ps['COATING TYPE'] == i])
        plot_data_coat=[]
        for i in coating_dict.keys():
            plot_data_coat.append([str(i),np.round(coating_dict[str(i)]/coating_dict_full[str(i)],2),coating_dict[str(i)],coating_dict_full[str(i)]])
        plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "Batches", "filter batch", 'full batch'])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Batches', scale=alt.Scale(domain=[0,1]) ),
            tooltip=[
                alt.Tooltip('Coating Type:O', title='Coating'),
                alt.Tooltip('Batches:Q', title='Fraction from total batches'),
                alt.Tooltip('filter batch:Q', title='Number of Filtered Batches'),
                alt.Tooltip('full batch:Q', title='Number of Total batches')

            ]
        )

    chart = (bars).properties(
        title='Coating Type vs Pre Sputtering Batches',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_coating_type_ti():
    refined_df_ti=st.session_state.refined_df_ti
    complete_refined_df_ti=st.session_state.complete_refined_df_ti
    region_selections_ti=st.session_state.region_selections_ti

    if region_selections_ti[0]=='All Batches':
        coating_types=np.array(refined_df_ti['COATING TYPE'].unique())
        coating_dict={}
        for i in coating_types:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict[str(i)]=len(refined_df_ti[refined_df_ti['COATING TYPE'] == i])
        plot_data_coat=[]
        for i in coating_dict.keys():
            plot_data_coat.append([str(i),coating_dict[str(i)]])
        plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Coating Type:O', title='Coating'),
                alt.Tooltip('Batches:Q', title='Number of Batches')
            ]
        )

    else:
        coating_types=np.array(refined_df_ti['COATING TYPE'].unique())
        coating_dict={}
        for i in coating_types:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict[str(i)]=len(refined_df_ti[refined_df_ti['COATING TYPE'] == i])
        coating_types_full=np.array(complete_refined_df_ti['COATING TYPE'].unique())
        coating_dict_full={}
        for i in coating_types_full:    
            if str(i) =="nan" or i == None:
                continue
            else:
                coating_dict_full[str(i)]=len(complete_refined_df_ti[complete_refined_df_ti['COATING TYPE'] == i])
        plot_data_coat=[]
        for i in coating_dict.keys():
            plot_data_coat.append([str(i),np.round(coating_dict[str(i)]/coating_dict_full[str(i)],2),coating_dict[str(i)],coating_dict_full[str(i)]])
        plot_df = pd.DataFrame(plot_data_coat, columns=["Coating Type", "Batches", "filter batch", 'full batch'])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Coating Type:O', title='Coating Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Batches', scale=alt.Scale(domain=[0,1]) ),
            tooltip=[
                alt.Tooltip('Coating Type:O', title='Coating'),
                alt.Tooltip('Batches:Q', title='Fraction from total batches'),
                alt.Tooltip('filter batch:Q', title='Number of Filtered Batches'),
                alt.Tooltip('full batch:Q', title='Number of Total batches')

            ]
        )

    chart = (bars).properties(
        title='Coating Type vs Ti Coating Batches',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_shifts():
    refined_df=st.session_state.refined_df
    plot_data_shift = []
    shift1_plot=[]
    shift2_plot=[]
    shift3_plot=[]
    for i in range(len(refined_df)):
        if int(refined_df['BATCH START TIME'][i][11:13])<6 or int(refined_df['BATCH START TIME'][i][11:13])>=23:
            shift1_plot.append(refined_df['RH mins'][i])
        elif int(refined_df['BATCH START TIME'][i][11:13])<15 and int(refined_df['BATCH START TIME'][i][11:13])>=6:
            if refined_df['BATCH START TIME'][i][11:13]==14:
                if int(refined_df['BATCH START TIME'][i][14:16])<=30:
                    shift2_plot.append(refined_df['RH mins'][i])
                else:
                    pass
            else:
                shift2_plot.append(refined_df['RH mins'][i])
        elif int(refined_df['BATCH START TIME'][i][11:13])<23 and int(refined_df['BATCH START TIME'][i][11:13])>=14 :
            if refined_df['BATCH START TIME'][i][11:13]==14:
                if int(refined_df['BATCH START TIME'][i][14:16])>30:
                    shift3_plot.append(refined_df['RH mins'][i])
                else:
                    pass
            else:
                shift3_plot.append(refined_df['RH mins'][i])
    plot_data_shift.append(["11 PM to 6 AM", round(np.average(shift1_plot), 2), round(np.max(shift1_plot), 2), round(np.min(shift1_plot),2), len(shift1_plot)])
    plot_data_shift.append(["6 AM to 2:30 PM", round(np.average(shift2_plot), 2), round(np.max(shift2_plot), 2), round(np.min(shift2_plot),2), len(shift2_plot)])
    plot_data_shift.append(["2:30 PM to 11 PM", round(np.average(shift3_plot), 2), round(np.max(shift3_plot), 2), round(np.min(shift3_plot),2), len(shift3_plot)])
    plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "RH Avg", "RH Max", "RH Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('RH Avg:Q', title='RH Time (Mins)'),
        tooltip=[
            alt.Tooltip('Shift:O', title='Shift Type'),
            alt.Tooltip('RH Avg:Q', title='Average RH Time'),
            alt.Tooltip('RH Max:Q', title='Max RH Time'),
            alt.Tooltip('RH Min:Q', title='Min RH Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='RH Avg:Q'
    )

    chart = (bars + text).properties(
        title='Shift Type vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_shifts_II():
    refined_df_II=st.session_state.refined_df_II
    plot_data_shift = []
    shift1_plot=[]
    shift2_plot=[]
    shift3_plot=[]
    for i in range(len(refined_df_II)):
        if int(refined_df_II['BATCH START TIME'][i][11:13])<6 or int(refined_df_II['BATCH START TIME'][i][11:13])>=23:
            shift1_plot.append(refined_df_II['H_II mins'][i])
        elif int(refined_df_II['BATCH START TIME'][i][11:13])<15 and int(refined_df_II['BATCH START TIME'][i][11:13])>=6:
            if refined_df_II['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_II['BATCH START TIME'][i][14:16])<=30:
                    shift2_plot.append(refined_df_II['H_II mins'][i])
                else:
                    pass
            else:
                shift2_plot.append(refined_df_II['H_II mins'][i])
        elif int(refined_df_II['BATCH START TIME'][i][11:13])<23 and int(refined_df_II['BATCH START TIME'][i][11:13])>=14 :
            if refined_df_II['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_II['BATCH START TIME'][i][14:16])>30:
                    shift3_plot.append(refined_df_II['H_II mins'][i])
                else:
                    pass
            else:
                shift3_plot.append(refined_df_II['H_II mins'][i])
    plot_data_shift.append(["11 PM to 6 AM", round(np.average(shift1_plot), 2), round(np.max(shift1_plot), 2), round(np.min(shift1_plot),2), len(shift1_plot)])
    plot_data_shift.append(["6 AM to 2:30 PM", round(np.average(shift2_plot), 2), round(np.max(shift2_plot), 2), round(np.min(shift2_plot),2), len(shift2_plot)])
    plot_data_shift.append(["2:30 PM to 11 PM", round(np.average(shift3_plot), 2), round(np.max(shift3_plot), 2), round(np.min(shift3_plot),2), len(shift3_plot)])
    plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "H_II Avg", "H_II Max", "H_II Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('H_II Avg:Q', title='H_II Time (Mins)'),
        tooltip=[
            alt.Tooltip('Shift:O', title='Shift Type'),
            alt.Tooltip('H_II Avg:Q', title='Average H_II Time'),
            alt.Tooltip('H_II Max:Q', title='Max H_II Time'),
            alt.Tooltip('H_II Min:Q', title='Min H_II Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='H_II Avg:Q'
    )

    chart = (bars + text).properties(
        title='Shift Type vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
def plot_shifts_glow():
    refined_df_glow=st.session_state.refined_df_glow
    complete_refined_df_glow=st.session_state.complete_refined_df_glow
    region_selections_glow=st.session_state.region_selections_glow

    if region_selections_glow[0]==True:
        plot_data_shift = []
        plot_data_shift.append(["6 AM to 2:30 PM", len(refined_df_glow[refined_df_glow['SHIFT TYPE']=='Shift 1'])])
        plot_data_shift.append(["2:30 PM to 11 PM", len(refined_df_glow[refined_df_glow['SHIFT TYPE']=='Shift 2'])])
        plot_data_shift.append(["11 PM to 6 AM", len(refined_df_glow[refined_df_glow['SHIFT TYPE']=='Shift 3'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Shift:O', title='Shift Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches')
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Shift Type vs Glow Discharge Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_shift = []
        plot_data_shift.append(["6 AM to 2:30 PM", np.round(len(refined_df_glow[refined_df_glow['SHIFT TYPE']=='Shift 1'])/ len(complete_refined_df_glow[complete_refined_df_glow['SHIFT TYPE']=='Shift 1']),2),len(refined_df_glow[refined_df_glow['SHIFT TYPE']=='Shift 1']), len(complete_refined_df_glow[complete_refined_df_glow['SHIFT TYPE']=='Shift 1'])])
        plot_data_shift.append(["2:30 PM to 11 PM", np.round(len(refined_df_glow[refined_df_glow['SHIFT TYPE']=='Shift 2'])/ len(complete_refined_df_glow[complete_refined_df_glow['SHIFT TYPE']=='Shift 2']),2),len(refined_df_glow[refined_df_glow['SHIFT TYPE']=='Shift 2']), len(complete_refined_df_glow[complete_refined_df_glow['SHIFT TYPE']=='Shift 2'])])
        plot_data_shift.append(["11 PM to 6 AM", np.round(len(refined_df_glow[refined_df_glow['SHIFT TYPE']=='Shift 3'])/ len(complete_refined_df_glow[complete_refined_df_glow['SHIFT TYPE']=='Shift 3']),2),len(refined_df_glow[refined_df_glow['SHIFT TYPE']=='Shift 3']), len(complete_refined_df_glow[complete_refined_df_glow['SHIFT TYPE']=='Shift 3'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "Batches", "filter batches", "full batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Batches',scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Shift:O', title='Shift Type'),
                alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                alt.Tooltip('filter batches:Q', title='No. of Filtered Batches'),
                alt.Tooltip('full batches:Q', title='No. of Total Batches')

            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Shift Type vs Glow Discharge Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_shifts_ac():
    refined_df_ac=st.session_state.refined_df_ac
    complete_refined_df_ac=st.session_state.complete_refined_df_ac
    region_selections_ac=st.session_state.region_selections_ac

    if region_selections_ac[0]==True:
        plot_data_shift = []
        plot_data_shift.append(["6 AM to 2:30 PM", len(refined_df_ac[refined_df_ac['SHIFT TYPE']=='Shift 1'])])
        plot_data_shift.append(["2:30 PM to 11 PM", len(refined_df_ac[refined_df_ac['SHIFT TYPE']=='Shift 2'])])
        plot_data_shift.append(["11 PM to 6 AM", len(refined_df_ac[refined_df_ac['SHIFT TYPE']=='Shift 3'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Shift:O', title='Shift Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches')
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Shift Type vs Arc Cleaning Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_shift = []
        plot_data_shift.append(["6 AM to 2:30 PM", np.round(len(refined_df_ac[refined_df_ac['SHIFT TYPE']=='Shift 1'])/ len(complete_refined_df_ac[complete_refined_df_ac['SHIFT TYPE']=='Shift 1']),2),len(refined_df_ac[refined_df_ac['SHIFT TYPE']=='Shift 1']), len(complete_refined_df_ac[complete_refined_df_ac['SHIFT TYPE']=='Shift 1'])])
        plot_data_shift.append(["2:30 PM to 11 PM", np.round(len(refined_df_ac[refined_df_ac['SHIFT TYPE']=='Shift 2'])/ len(complete_refined_df_ac[complete_refined_df_ac['SHIFT TYPE']=='Shift 2']),2),len(refined_df_ac[refined_df_ac['SHIFT TYPE']=='Shift 2']), len(complete_refined_df_ac[complete_refined_df_ac['SHIFT TYPE']=='Shift 2'])])
        plot_data_shift.append(["11 PM to 6 AM", np.round(len(refined_df_ac[refined_df_ac['SHIFT TYPE']=='Shift 3'])/ len(complete_refined_df_ac[complete_refined_df_ac['SHIFT TYPE']=='Shift 3']),2),len(refined_df_ac[refined_df_ac['SHIFT TYPE']=='Shift 3']), len(complete_refined_df_ac[complete_refined_df_ac['SHIFT TYPE']=='Shift 3'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "Batches", "filter batches", "full batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Batches',scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Shift:O', title='Shift Type'),
                alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                alt.Tooltip('filter batches:Q', title='No. of Filtered Batches'),
                alt.Tooltip('full batches:Q', title='No. of Total Batches')

            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Shift Type vs Arc Cleaning Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_shifts_ae():
    refined_df_ae=st.session_state.refined_df_ae
    complete_refined_df_ae=st.session_state.complete_refined_df_ae
    region_selections_ae=st.session_state.region_selections_ae

    if region_selections_ae[1]=='All Batches':
        plot_data_shift = []
        plot_data_shift.append(["6 AM to 2:30 PM", len(refined_df_ae[refined_df_ae['SHIFT TYPE']=='Shift 1'])])
        plot_data_shift.append(["2:30 PM to 11 PM", len(refined_df_ae[refined_df_ae['SHIFT TYPE']=='Shift 2'])])
        plot_data_shift.append(["11 PM to 6 AM", len(refined_df_ae[refined_df_ae['SHIFT TYPE']=='Shift 3'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Shift:O', title='Shift Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches')
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Shift Type vs Arc Etching Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_shift = []
        plot_data_shift.append(["6 AM to 2:30 PM", np.round(len(refined_df_ae[refined_df_ae['SHIFT TYPE']=='Shift 1'])/ len(complete_refined_df_ae[complete_refined_df_ae['SHIFT TYPE']=='Shift 1']),2),len(refined_df_ae[refined_df_ae['SHIFT TYPE']=='Shift 1']), len(complete_refined_df_ae[complete_refined_df_ae['SHIFT TYPE']=='Shift 1'])])
        plot_data_shift.append(["2:30 PM to 11 PM", np.round(len(refined_df_ae[refined_df_ae['SHIFT TYPE']=='Shift 2'])/ len(complete_refined_df_ae[complete_refined_df_ae['SHIFT TYPE']=='Shift 2']),2),len(refined_df_ae[refined_df_ae['SHIFT TYPE']=='Shift 2']), len(complete_refined_df_ae[complete_refined_df_ae['SHIFT TYPE']=='Shift 2'])])
        plot_data_shift.append(["11 PM to 6 AM", np.round(len(refined_df_ae[refined_df_ae['SHIFT TYPE']=='Shift 3'])/ len(complete_refined_df_ae[complete_refined_df_ae['SHIFT TYPE']=='Shift 3']),2),len(refined_df_ae[refined_df_ae['SHIFT TYPE']=='Shift 3']), len(complete_refined_df_ae[complete_refined_df_ae['SHIFT TYPE']=='Shift 3'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "Batches", "filter batches", "full batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Batches',scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Shift:O', title='Shift Type'),
                alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                alt.Tooltip('filter batches:Q', title='No. of Filtered Batches'),
                alt.Tooltip('full batches:Q', title='No. of Total Batches')

            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Shift Type vs Arc Etching Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_shifts_ps():
    refined_df_ps=st.session_state.refined_df_ps
    complete_refined_df_ps=st.session_state.complete_refined_df_ps
    region_selections_ps=st.session_state.region_selections_ps

    if region_selections_ps[0]=='All Batches':
        plot_data_shift = []
        plot_data_shift.append(["6 AM to 2:30 PM", len(refined_df_ps[refined_df_ps['SHIFT TYPE']=='Shift 1'])])
        plot_data_shift.append(["2:30 PM to 11 PM", len(refined_df_ps[refined_df_ps['SHIFT TYPE']=='Shift 2'])])
        plot_data_shift.append(["11 PM to 6 AM", len(refined_df_ps[refined_df_ps['SHIFT TYPE']=='Shift 3'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Shift:O', title='Shift Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches')
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Shift Type vs Pre Sputtering Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_shift = []
        plot_data_shift.append(["6 AM to 2:30 PM", np.round(len(refined_df_ps[refined_df_ps['SHIFT TYPE']=='Shift 1'])/ len(complete_refined_df_ps[complete_refined_df_ps['SHIFT TYPE']=='Shift 1']),2),len(refined_df_ps[refined_df_ps['SHIFT TYPE']=='Shift 1']), len(complete_refined_df_ps[complete_refined_df_ps['SHIFT TYPE']=='Shift 1'])])
        plot_data_shift.append(["2:30 PM to 11 PM", np.round(len(refined_df_ps[refined_df_ps['SHIFT TYPE']=='Shift 2'])/ len(complete_refined_df_ps[complete_refined_df_ps['SHIFT TYPE']=='Shift 2']),2),len(refined_df_ps[refined_df_ps['SHIFT TYPE']=='Shift 2']), len(complete_refined_df_ps[complete_refined_df_ps['SHIFT TYPE']=='Shift 2'])])
        plot_data_shift.append(["11 PM to 6 AM", np.round(len(refined_df_ps[refined_df_ps['SHIFT TYPE']=='Shift 3'])/ len(complete_refined_df_ps[complete_refined_df_ps['SHIFT TYPE']=='Shift 3']),2),len(refined_df_ps[refined_df_ps['SHIFT TYPE']=='Shift 3']), len(complete_refined_df_ps[complete_refined_df_ps['SHIFT TYPE']=='Shift 3'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "Batches", "filter batches", "full batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Batches',scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Shift:O', title='Shift Type'),
                alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                alt.Tooltip('filter batches:Q', title='No. of Filtered Batches'),
                alt.Tooltip('full batches:Q', title='No. of Total Batches')

            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Shift Type vs Pre Sputtering Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_shifts_ti():
    refined_df_ti=st.session_state.refined_df_ti
    complete_refined_df_ti=st.session_state.complete_refined_df_ti
    region_selections_ti=st.session_state.region_selections_ti

    if region_selections_ti[0]=='All Batches':
        plot_data_shift = []
        plot_data_shift.append(["6 AM to 2:30 PM", len(refined_df_ti[refined_df_ti['SHIFT TYPE']=='Shift 1'])])
        plot_data_shift.append(["2:30 PM to 11 PM", len(refined_df_ti[refined_df_ti['SHIFT TYPE']=='Shift 2'])])
        plot_data_shift.append(["11 PM to 6 AM", len(refined_df_ti[refined_df_ti['SHIFT TYPE']=='Shift 3'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Shift:O', title='Shift Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches')
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Shift Type vs Pre Sputtering Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_shift = []
        plot_data_shift.append(["6 AM to 2:30 PM", np.round(len(refined_df_ti[refined_df_ti['SHIFT TYPE']=='Shift 1'])/ len(complete_refined_df_ti[complete_refined_df_ti['SHIFT TYPE']=='Shift 1']),2),len(refined_df_ti[refined_df_ti['SHIFT TYPE']=='Shift 1']), len(complete_refined_df_ti[complete_refined_df_ti['SHIFT TYPE']=='Shift 1'])])
        plot_data_shift.append(["2:30 PM to 11 PM", np.round(len(refined_df_ti[refined_df_ti['SHIFT TYPE']=='Shift 2'])/ len(complete_refined_df_ti[complete_refined_df_ti['SHIFT TYPE']=='Shift 2']),2),len(refined_df_ti[refined_df_ti['SHIFT TYPE']=='Shift 2']), len(complete_refined_df_ti[complete_refined_df_ti['SHIFT TYPE']=='Shift 2'])])
        plot_data_shift.append(["11 PM to 6 AM", np.round(len(refined_df_ti[refined_df_ti['SHIFT TYPE']=='Shift 3'])/ len(complete_refined_df_ti[complete_refined_df_ti['SHIFT TYPE']=='Shift 3']),2),len(refined_df_ti[refined_df_ti['SHIFT TYPE']=='Shift 3']), len(complete_refined_df_ti[complete_refined_df_ti['SHIFT TYPE']=='Shift 3'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Shift", "Batches", "filter batches", "full batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Shift:O', title='Shift Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='Batches',scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Shift:O', title='Shift Type'),
                alt.Tooltip('Batches:Q', title='Fraction from Total Batches'),
                alt.Tooltip('filter batches:Q', title='No. of Filtered Batches'),
                alt.Tooltip('full batches:Q', title='No. of Total Batches')

            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Shift Type vs Pre Sputtering Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_pre_storage_glow():
    refined_df_glow=st.session_state.refined_df_glow
    complete_refined_df_glow=st.session_state.complete_refined_df_glow
    region_selections_glow=st.session_state.region_selections_glow
    if region_selections_glow[0]==True:
        plot_data_shift = []
        plot_data_shift.append(["Open", len(refined_df_glow[refined_df_glow['PRE STORAGE']=='Open'])])
        plot_data_shift.append(["Enclosure", len(refined_df_glow[refined_df_glow['PRE STORAGE']=='Enclosure'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Pre Storage", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Pre Storage:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Pre Storage:O', title='Pre Storage Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches'),
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Pre Storage Type vs Glow Discharge Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_shift = []
        plot_data_shift.append(["Open", np.round(len(refined_df_glow[refined_df_glow['PRE STORAGE']=='Open'])/len(complete_refined_df_glow[complete_refined_df_glow['PRE STORAGE']=='Open']),2),len(complete_refined_df_glow[complete_refined_df_glow['PRE STORAGE']=='Open']),len(refined_df_glow[refined_df_glow['PRE STORAGE']=='Open'])])
        plot_data_shift.append(["Enclosure", np.round(len(refined_df_glow[refined_df_glow['PRE STORAGE']=='Enclosure'])/len(complete_refined_df_glow[complete_refined_df_glow['PRE STORAGE']=='Enclosure']),2),len(complete_refined_df_glow[complete_refined_df_glow['PRE STORAGE']=='Enclosure']),len(refined_df_glow[refined_df_glow['PRE STORAGE']=='Enclosure'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Pre Storage", "Batches", "full batches", "filter batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Pre Storage:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches', scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Pre Storage:O', title='Pre Storage Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches'),
                alt.Tooltip('filter batches:Q', title='No. of Filtered Batches'),
                alt.Tooltip('full batches:Q', title='No. of Total Batches')
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Pre Storage Type vs Glow Discharge Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_pre_storage_ac():
    refined_df_ac=st.session_state.refined_df_ac
    complete_refined_df_ac=st.session_state.complete_refined_df_ac
    region_selections_ac=st.session_state.region_selections_ac
    if region_selections_ac[0]==True:
        plot_data_shift = []
        plot_data_shift.append(["Open", len(refined_df_ac[refined_df_ac['PRE STORAGE']=='Open'])])
        plot_data_shift.append(["Enclosure", len(refined_df_ac[refined_df_ac['PRE STORAGE']=='Enclosure'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Pre Storage", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Pre Storage:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Pre Storage:O', title='Pre Storage Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches'),
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Pre Storage Type vs Arc Cleaning Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_shift = []
        plot_data_shift.append(["Open", np.round(len(refined_df_ac[refined_df_ac['PRE STORAGE']=='Open'])/len(complete_refined_df_ac[complete_refined_df_ac['PRE STORAGE']=='Open']),2),len(complete_refined_df_ac[complete_refined_df_ac['PRE STORAGE']=='Open']),len(refined_df_ac[refined_df_ac['PRE STORAGE']=='Open'])])
        plot_data_shift.append(["Enclosure", np.round(len(refined_df_ac[refined_df_ac['PRE STORAGE']=='Enclosure'])/len(complete_refined_df_ac[complete_refined_df_ac['PRE STORAGE']=='Enclosure']),2),len(complete_refined_df_ac[complete_refined_df_ac['PRE STORAGE']=='Enclosure']),len(refined_df_ac[refined_df_ac['PRE STORAGE']=='Enclosure'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Pre Storage", "Batches", "full batches", "filter batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Pre Storage:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches', scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Pre Storage:O', title='Pre Storage Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches'),
                alt.Tooltip('filter batches:Q', title='No. of Filtered Batches'),
                alt.Tooltip('full batches:Q', title='No. of Total Batches')
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Pre Storage Type vs Arc Cleaning Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_pre_storage_ae():
    refined_df_ae=st.session_state.refined_df_ae
    complete_refined_df_ae=st.session_state.complete_refined_df_ae
    region_selections_ae=st.session_state.region_selections_ae
    if region_selections_ae[1]=='All Batches':
        plot_data_shift = []
        plot_data_shift.append(["Open", len(refined_df_ae[refined_df_ae['PRE STORAGE']=='Open'])])
        plot_data_shift.append(["Enclosure", len(refined_df_ae[refined_df_ae['PRE STORAGE']=='Enclosure'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Pre Storage", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Pre Storage:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Pre Storage:O', title='Pre Storage Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches'),
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Pre Storage Type vs Arc Etching Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_shift = []
        plot_data_shift.append(["Open", np.round(len(refined_df_ae[refined_df_ae['PRE STORAGE']=='Open'])/len(complete_refined_df_ae[complete_refined_df_ae['PRE STORAGE']=='Open']),2),len(complete_refined_df_ae[complete_refined_df_ae['PRE STORAGE']=='Open']),len(refined_df_ae[refined_df_ae['PRE STORAGE']=='Open'])])
        plot_data_shift.append(["Enclosure", np.round(len(refined_df_ae[refined_df_ae['PRE STORAGE']=='Enclosure'])/len(complete_refined_df_ae[complete_refined_df_ae['PRE STORAGE']=='Enclosure']),2),len(complete_refined_df_ae[complete_refined_df_ae['PRE STORAGE']=='Enclosure']),len(refined_df_ae[refined_df_ae['PRE STORAGE']=='Enclosure'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Pre Storage", "Batches", "full batches", "filter batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Pre Storage:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches', scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Pre Storage:O', title='Pre Storage Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches'),
                alt.Tooltip('filter batches:Q', title='No. of Filtered Batches'),
                alt.Tooltip('full batches:Q', title='No. of Total Batches')
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Pre Storage Type vs Arc Etching Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_pre_storage_ps():
    refined_df_ps=st.session_state.refined_df_ps
    complete_refined_df_ps=st.session_state.complete_refined_df_ps
    region_selections_ps=st.session_state.region_selections_ps
    if region_selections_ps[0]=='All Batches':
        plot_data_shift = []
        plot_data_shift.append(["Open", len(refined_df_ps[refined_df_ps['PRE STORAGE']=='Open'])])
        plot_data_shift.append(["Enclosure", len(refined_df_ps[refined_df_ps['PRE STORAGE']=='Enclosure'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Pre Storage", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Pre Storage:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Pre Storage:O', title='Pre Storage Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches'),
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Pre Storage Type vs Pre Sputtering Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_shift = []
        plot_data_shift.append(["Open", np.round(len(refined_df_ps[refined_df_ps['PRE STORAGE']=='Open'])/len(complete_refined_df_ps[complete_refined_df_ps['PRE STORAGE']=='Open']),2),len(complete_refined_df_ps[complete_refined_df_ps['PRE STORAGE']=='Open']),len(refined_df_ps[refined_df_ps['PRE STORAGE']=='Open'])])
        plot_data_shift.append(["Enclosure", np.round(len(refined_df_ps[refined_df_ps['PRE STORAGE']=='Enclosure'])/len(complete_refined_df_ps[complete_refined_df_ps['PRE STORAGE']=='Enclosure']),2),len(complete_refined_df_ps[complete_refined_df_ps['PRE STORAGE']=='Enclosure']),len(refined_df_ps[refined_df_ps['PRE STORAGE']=='Enclosure'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Pre Storage", "Batches", "full batches", "filter batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Pre Storage:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches', scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Pre Storage:O', title='Pre Storage Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches'),
                alt.Tooltip('filter batches:Q', title='No. of Filtered Batches'),
                alt.Tooltip('full batches:Q', title='No. of Total Batches')
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Pre Storage Type vs Pre Sputtering Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_pre_storage_ti():
    refined_df_ti=st.session_state.refined_df_ti
    complete_refined_df_ti=st.session_state.complete_refined_df_ti
    region_selections_ti=st.session_state.region_selections_ti
    if region_selections_ti[0]=='All Batches':
        plot_data_shift = []
        plot_data_shift.append(["Open", len(refined_df_ti[refined_df_ti['PRE STORAGE']=='Open'])])
        plot_data_shift.append(["Enclosure", len(refined_df_ti[refined_df_ti['PRE STORAGE']=='Enclosure'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Pre Storage", "Batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Pre Storage:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches'),
            tooltip=[
                alt.Tooltip('Pre Storage:O', title='Pre Storage Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches'),
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Pre Storage Type vs Ti Coating Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
    else:
        plot_data_shift = []
        plot_data_shift.append(["Open", np.round(len(refined_df_ti[refined_df_ti['PRE STORAGE']=='Open'])/len(complete_refined_df_ti[complete_refined_df_ti['PRE STORAGE']=='Open']),2),len(complete_refined_df_ti[complete_refined_df_ti['PRE STORAGE']=='Open']),len(refined_df_ti[refined_df_ti['PRE STORAGE']=='Open'])])
        plot_data_shift.append(["Enclosure", np.round(len(refined_df_ti[refined_df_ti['PRE STORAGE']=='Enclosure'])/len(complete_refined_df_ti[complete_refined_df_ti['PRE STORAGE']=='Enclosure']),2),len(complete_refined_df_ti[complete_refined_df_ti['PRE STORAGE']=='Enclosure']),len(refined_df_ti[refined_df_ti['PRE STORAGE']=='Enclosure'])])
        plot_df = pd.DataFrame(plot_data_shift, columns=["Pre Storage", "Batches", "full batches", "filter batches"])

        base = alt.Chart(plot_df).encode(
            x=alt.X('Pre Storage:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
        )

        bars = base.mark_bar(color="#00aeae").encode(
            y=alt.Y('Batches:Q', title='No. of Batches', scale=alt.Scale(domain=[0,1])),
            tooltip=[
                alt.Tooltip('Pre Storage:O', title='Pre Storage Type'),
                alt.Tooltip('Batches:Q', title='No. of Batches'),
                alt.Tooltip('filter batches:Q', title='No. of Filtered Batches'),
                alt.Tooltip('full batches:Q', title='No. of Total Batches')
            ]
        )

        text = base.mark_text(
            align='center',
            baseline='middle',
            dy=-10,
            color='black'
        ).encode(
            text='Batches:Q'
        )

        chart = (bars).properties(
            title='Pre Storage Type vs Ti Coating Batches',
            width=600,
            height=400
        )

        st.altair_chart(chart, use_container_width=True)
def plot_pre_storage():
    refined_df=st.session_state.refined_df
    pre_storage=[]
    for i in range(len(refined_df)):
        if refined_df['PRE STORAGE'][i]!=None and type(refined_df['PRE STORAGE'][i])!=float:
            pre_storage.append([refined_df['PRE STORAGE'][i],refined_df['RH mins'][i]])
    plot_data_pre = []
    opn_plot=[]
    encl_plot=[]
    for i in range(len(pre_storage)):
        if pre_storage[i][0]=="Open":
            opn_plot.append(pre_storage[i][1])
        elif pre_storage[i][0]=="Enclosure":
            encl_plot.append(pre_storage[i][1])
    plot_data_pre.append(["Open", round(np.average(opn_plot), 2), round(np.max(opn_plot), 2), round(np.min(opn_plot),2), len(opn_plot)])
    plot_data_pre.append(["Enclosure", round(np.average(encl_plot), 2), round(np.max(encl_plot), 2), round(np.min(encl_plot),2), len(encl_plot)])

    plot_df = pd.DataFrame(plot_data_pre, columns=["Pre Storage Type", "RH Avg", "RH Max", "RH Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Pre Storage Type:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('RH Avg:Q', title='RH Time (Mins)'),
        tooltip=[
            alt.Tooltip('Pre Storage Type:O', title='Pre Storage Type'),
            alt.Tooltip('RH Avg:Q', title='Average RH Time'),
            alt.Tooltip('RH Max:Q', title='Max RH Time'),
            alt.Tooltip('RH Min:Q', title='Min RH Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='RH Avg:Q'
    )

    chart = (bars + text).properties(
        title='Pre Storage Type vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
    pre_storage=[]
    for i in range(len(refined_df)):
        if refined_df['PRE STORAGE'][i]!=None and type(refined_df['PRE STORAGE'][i])!=float:
            pre_storage.append([refined_df['PRE STORAGE'][i],refined_df['RH mins'][i]])
    encl=[pre_storage[i][1] if pre_storage[i][0]=="Enclosure" else None for i in range(len(pre_storage)) ]
    opn=[pre_storage[i][1] if pre_storage[i][0]=="Open" else None for i in range(len(pre_storage)) ]
    x=np.arange(0,len(pre_storage),1)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(x,encl,label="Enclosed Batches",color="#008081")
    ax.scatter(x,opn, label="Open batches",color="#f02071")
    ax.plot(x,np.full((len(pre_storage)),np.average([i for i in encl if i!=None])),linestyle='dashed',color="#008081",label="Enlcosed Batches Mean RH time ("+str(np.average([i for i in encl if i!=None]).round(2))+")")
    ax.plot(x,np.full((len(pre_storage)),np.average([i for i in opn if i!=None])),linestyle='dashed',color="#f02071",label="Open Batches Mean RH time ("+str(np.average([i for i in opn if i!=None]).round(2))+")")
    ax.set_title("Open batches vs Enclosed Batches RH Time Comparison",fontsize=10)
    ax.set_xlabel("Batches")
    ax.set_ylabel("RH Time (Mins)")
    ax.legend(loc='center right', bbox_to_anchor=(1.0, 0.15),fontsize=7)
    st.pyplot(fig)
def plot_pre_storage_II():
    refined_df_II=st.session_state.refined_df_II
    pre_storage=[]
    for i in range(len(refined_df_II)):
        if refined_df_II['PRE STORAGE'][i]!=None and type(refined_df_II['PRE STORAGE'][i])!=float:
            pre_storage.append([refined_df_II['PRE STORAGE'][i],refined_df_II['H_II mins'][i]])
    plot_data_pre = []
    opn_plot=[]
    encl_plot=[]
    for i in range(len(pre_storage)):
        if pre_storage[i][0]=="Open":
            opn_plot.append(pre_storage[i][1])
        elif pre_storage[i][0]=="Enclosure":
            encl_plot.append(pre_storage[i][1])
    plot_data_pre.append(["Open", round(np.average(opn_plot), 2), round(np.max(opn_plot), 2), round(np.min(opn_plot),2), len(opn_plot)])
    plot_data_pre.append(["Enclosure", round(np.average(encl_plot), 2), round(np.max(encl_plot), 2), round(np.min(encl_plot),2), len(encl_plot)])

    plot_df = pd.DataFrame(plot_data_pre, columns=["Pre Storage Type", "H_II Avg", "H_II Max", "H_II Min", "Batches"])

    base = alt.Chart(plot_df).encode(
        x=alt.X('Pre Storage Type:O', title='Pre Storage Type', axis=alt.Axis(labelAngle=0))
    )

    bars = base.mark_bar(color="#00aeae").encode(
        y=alt.Y('H_II Avg:Q', title='H_II Time (Mins)'),
        tooltip=[
            alt.Tooltip('Pre Storage Type:O', title='Pre Storage Type'),
            alt.Tooltip('H_II Avg:Q', title='Average H_II Time'),
            alt.Tooltip('H_II Max:Q', title='Max H_II Time'),
            alt.Tooltip('H_II Min:Q', title='Min H_II Time'),
            alt.Tooltip('Batches:Q', title='Number of Batches')
        ]
    )

    text = base.mark_text(
        align='center',
        baseline='middle',
        dy=-10,
        color='black'
    ).encode(
        text='H_II Avg:Q'
    )

    chart = (bars + text).properties(
        title='Pre Storage Type vs Pumpdown Time',
        width=600,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
    pre_storage=[]
    for i in range(len(refined_df_II)):
        if refined_df_II['PRE STORAGE'][i]!=None and type(refined_df_II['PRE STORAGE'][i])!=float:
            pre_storage.append([refined_df_II['PRE STORAGE'][i],refined_df_II['H_II mins'][i]])
    encl=[pre_storage[i][1] if pre_storage[i][0]=="Enclosure" else None for i in range(len(pre_storage)) ]
    opn=[pre_storage[i][1] if pre_storage[i][0]=="Open" else None for i in range(len(pre_storage)) ]
    x=np.arange(0,len(pre_storage),1)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(x,encl,label="Enclosed Batches",color="#008081")
    ax.scatter(x,opn, label="Open batches",color="#f02071")
    ax.plot(x,np.full((len(pre_storage)),np.average([i for i in encl if i!=None])),linestyle='dashed',color="#008081",label="Enlcosed Batches Mean H_II time ("+str(np.average([i for i in encl if i!=None]).round(2))+")")
    ax.plot(x,np.full((len(pre_storage)),np.average([i for i in opn if i!=None])),linestyle='dashed',color="#f02071",label="Open Batches Mean H_II time ("+str(np.average([i for i in opn if i!=None]).round(2))+")")
    ax.set_title("Open batches vs Enclosed Batches H_II Time Comparison",fontsize=10)
    ax.set_xlabel("Batches")
    ax.set_ylabel("H_II Time (Mins)")
    ax.legend(loc='center right', bbox_to_anchor=(1.0, 0.15),fontsize=7)
    st.pyplot(fig)
# Define a safe converter function
def safe_parse_list(value):
    try:
        # Check if the value is a string and looks like a list format
        if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
            return ast.literal_eval(value)  # Attempt to convert to a Python list
        else:
            return value  # Return the value unchanged if not in expected format
    except (ValueError, SyntaxError):
        return value 
def compute(add_data,process_data,io_data):
    global df 
    df_old=pd.read_pickle('df.pkl')
    refined_df_old=pd.read_pickle('refined_df.pkl')
    import ast
    #columns_to_convert = ['R Time', 'RH Time', 'Temp Time','Idxs','R Idxs','RH Idxs','Temp Idxs','Ni_plating_diff']  # Add the names of all 7 columns here
    #Convert the specified columns using ast.literal_eval
    #for col in columns_to_convert:
        #refined_df[col] = refined_df[col].apply(safe_parse_list)
    #refined_df['R Time'] = refined_df['R Time'].apply(ast.literal_eval)
    #refined_df['RH Time'] = refined_df['RH Time'].apply(ast.literal_eval)

    if add_data==True:
        df = pd.DataFrame()
        df=df.dropna(how='all')
        df = pd.concat([df,process_data], ignore_index=True)

        a=np.array(df['DATE TIME'] )
        for i in range(len(a)):
            a[i]=str(a[i])
        df['DATE TIME'] = a
        startendtime=[]
        global idxs
        idxs=[]
        a=np.array(df['BATCH ID'])
        startendtime.append([a[0], a[0],0])
        idxs.append(0)
        for i in range(1,len(df)):
            if a[i]!=a[i]:
                continue
            elif i==(len(df)-1):
                startendtime.append([a[i], a[i],i])
                idxs.append(i)
            elif a[i]==a[i-1]:
                continue
            else:
                startendtime.append([a[i-1], a[i-1],i-1])
                startendtime.append([a[i], a[i],i])
                idxs.append(i-1)
                idxs.append(i)
        idxs=list_to_matrix(idxs,2)
        for i in idxs:
            if i[0]==i[1]:
                idxs.remove(i)
        global r_time_id
        r_time_id=[]
        for j in range(0,len(idxs)):
            if idxs[j][1]>=20+idxs[j][0]:
                for i in range(20+idxs[j][0], idxs[j][1]):
                    if i==idxs[j][1]-1:
                        r_time_id.append([idxs[j][0],idxs[j][0]])
                        break
                    elif df['HIGH VACUM ACTUAL'][i]>=1600:
                        continue
                    elif df['HIGH VACUM ACTUAL'][i]<1600:
                        r_time_id.append([idxs[j][0],i-1])
                        break
            else:
                r_time_id.append([idxs[j][0],idxs[j][0]])  
        global rh_time_id
        rh_time_id=[]
        for j in range(0,len(idxs)):

            for i in range(math.floor((idxs[j][1]-idxs[j][0])/12)+idxs[j][0], idxs[j][1]):
                if i==idxs[j][1]-1:
                    rh_time_id.append([idxs[j][0],i])
                    break
                elif df['HIGH VACUM ACTUAL'][i]>=720:
                    continue
                elif df['HIGH VACUM ACTUAL'][i]<720:
                    rh_time_id.append([idxs[j][0],i])
                    break
        global temp_time_id
        temp_time_id=[]
        for j in range(0,len(idxs)):

            for i in range(idxs[j][0], idxs[j][1]):
                if i==idxs[j][1]-1:
                    temp_time_id.append([idxs[j][0],i])
                    break
                elif df['HEATER TEMP ACTUAL'][i]<=240:
                    continue
                else:
                    temp_time_id.append([idxs[j][0],i])
                    break
        a=np.array(df['DATE TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        df['DATE TIME']=a
        r_time=[]
        for i in range(0,len(r_time_id)):
            r_time.append([calculate_time_difference(df['DATE TIME'][r_time_id[i][0]], df['DATE TIME'][r_time_id[i][1]])])
        rh_time=[]
        for i in range(0,len(rh_time_id)):
            rh_time.append([calculate_time_difference(df['DATE TIME'][rh_time_id[i][0]], df['DATE TIME'][rh_time_id[i][1]])])
        t_time=[]
        for i in range(0,len(temp_time_id)):
            t_time.append([calculate_time_difference(df['DATE TIME'][temp_time_id[i][0]], df['DATE TIME'][temp_time_id[i][1]])])
        h_time=[]
        for i in range(0,len(rh_time_id)):
            h_time.append([calculate_time_difference(df['DATE TIME'][r_time_id[i][1]], df['DATE TIME'][rh_time_id[i][1]])])
        column_headers=["DATE TIME","BATCH ID", "Idxs","R Idxs","RH Idxs","Temp Idxs","R Time","H Time","Temp Time","RH Time"]
        global batch_data
        batch_data=pd.DataFrame(columns=column_headers)
        for i in range(len(idxs)):
            batch_data.loc[i, 'DATE TIME'] = df['DATE TIME'][idxs[i][0]+1]
            batch_data.loc[i, 'BATCH ID'] = df['BATCH ID'][idxs[i][0]+3]
            batch_data.loc[i, 'Idxs'] = idxs[i]
            batch_data.loc[i, 'R Idxs'] = r_time_id[i]
            batch_data.loc[i, 'H Time'] = h_time[i]
            batch_data.loc[i, 'RH Idxs'] = rh_time_id[i]
            batch_data.loc[i, 'Temp Idxs'] = temp_time_id[i]
            batch_data.loc[i, 'R Time'] = r_time[i]
            batch_data.loc[i, 'RH Time'] = rh_time[i]
            batch_data.loc[i, 'Temp Time'] = t_time[i]
        batch_data=batch_data.drop_duplicates(subset=['BATCH ID'])
        batch_data.reset_index(drop=True, inplace=True)
        batch_data['DATE TIME']=pd.to_datetime(batch_data['DATE TIME'], format='%d/%m/%Y %H:%M:%S')
        batch_data = batch_data.sort_values(by='DATE TIME')
        batch_data = batch_data.reset_index(drop=True)
        batch_data['DATE TIME']=batch_data['DATE TIME'].astype(str)
        idxs=np.array(batch_data["Idxs"])
        rh_time_id=np.array(batch_data["RH Idxs"])
        r_time_id=np.array(batch_data["R Idxs"])
        temp_time_id=np.array(batch_data["Temp Idxs"])
        rh_time=np.array(batch_data["RH Time"])
        r_time=np.array(batch_data["R Time"])
        t_time=np.array(batch_data["Temp Time"])
        h_time=np.array(batch_data["H Time"])
        df2 = io_data
        new_header = df2.iloc[0]
        in_df = df2[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        columns_to_select = ["BATCH ID", "R Time", "RH Time", "Temp Time","Idxs","RH Idxs","R Idxs","Temp Idxs"]
        merged_df = pd.merge(in_df, batch_data[columns_to_select], on="BATCH ID", how="inner")
        merged_df=merged_df[merged_df["PROCESS TYPE"]=='Coating']
        merged_df.reset_index(drop=True, inplace=True)
        import json
        for i in range(len(merged_df)):
            s=merged_df["INTERVENSIONS"][i]
            d = json.loads(s)
            if "Yes" in d.values():
                merged_df["INTERVENSIONS"][i]=d
            else:
                merged_df["INTERVENSIONS"][i]=None

        for i in range(len(merged_df)):
            merged_df['NI PLATING DATE TIME'][i]=str(merged_df['NI PLATING DATE TIME'][i])
            merged_df['BATCH START TIME'][i]=str(merged_df['BATCH START TIME'][i])
            merged_df['BATCH END TIME'][i]=str(merged_df['BATCH END TIME'][i])
        for i in range(len(merged_df)):
            if "-" in merged_df['NI PLATING DATE TIME'][i]:
                string=merged_df['NI PLATING DATE TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df['NI PLATING DATE TIME'][i]=string2
        for i in range(len(merged_df)):
            if "-" in merged_df['BATCH START TIME'][i]:
                string=merged_df['BATCH START TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df['BATCH START TIME'][i]=string2
        for i in range(len(merged_df)):
            if "-" in merged_df['BATCH END TIME'][i]:
                string=merged_df['BATCH END TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df['BATCH END TIME'][i]=string2
        Ni_plating_diff=[]
        for i in range(0,len(merged_df['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df['NI PLATING DATE TIME'][i],merged_df['BATCH START TIME'][i])])
        merged_df["Ni_plating_diff"]=Ni_plating_diff
        #merged_df.to_excel("IO 37 batches merged.xlsx")
        Ni_plating_diff=[]
        for i in range(0,len(merged_df['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df['NI PLATING DATE TIME'][i],merged_df['BATCH START TIME'][i])])
        ni_hrs=[]
        for i in range(len(merged_df)):
            ni_hrs.append(Ni_plating_diff[i][0][0]*24+Ni_plating_diff[i][0][1]+Ni_plating_diff[i][0][2]/60+Ni_plating_diff[i][0][3]/3600)
        global rh_mins    
        rh_mins=[]
        for i in range(len(merged_df)):
            rh_mins.append(merged_df["RH Time"][i][0][1]*60+merged_df["RH Time"][i][0][2]+merged_df["RH Time"][i][0][3]/60)
        global r_mins
        r_mins=[]
        for i in range(len(merged_df)):
            r_mins.append(merged_df["R Time"][i][0][1]*60+merged_df["R Time"][i][0][2]+merged_df["R Time"][i][0][3]/60)
        global t_mins
        t_mins=[]
        for i in range(len(merged_df)):
            t_mins.append(merged_df["Temp Time"][i][0][1]*60+merged_df["Temp Time"][i][0][2]+merged_df["Temp Time"][i][0][3]/60)
        drop_labels=[]
        for i in range(len(merged_df)):
            if r_mins[i]<5 or r_mins[i]>30 or rh_mins[i]<8 or rh_mins[i]>33:
                drop_labels.append(i)
        
        refined_df=merged_df.drop(labels=drop_labels, axis=0)
        refined_df=refined_df.reset_index(drop=True)
        last_index_old_df = df_old.index[-1] if not df_old.empty else -1  # Handles empty old_df case
        new_start_index = last_index_old_df + 1
        columns_to_select = ["Idxs","RH Idxs","R Idxs","Temp Idxs"]
        for col in columns_to_select:
            for i in range(len(refined_df)):
                refined_df[col][i][0]=refined_df[col][i][0]+new_start_index
                refined_df[col][i][1]=refined_df[col][i][1]+new_start_index

        df_old = pd.concat([df_old, df], ignore_index=True)
        refined_df_old = pd.concat([refined_df_old, refined_df], ignore_index=True)

    df=df_old
    refined_df=refined_df_old
    refined_df=refined_df.drop_duplicates(subset=['BATCH ID'])
    refined_df.reset_index(drop=True, inplace=True)
    #df.to_pickle('df.pkl')
    #refined_df.to_pickle('refined_df.pkl')
    a=refined_df
    a['BATCH START TIME']=pd.to_datetime(a['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    a = a.sort_values(by='BATCH START TIME')
    a = a.reset_index(drop=True)
    start=pd.to_datetime(a['BATCH START TIME'][0], format='%d/%m/%Y %H:%M:%S')
    stop=pd.to_datetime(a['BATCH START TIME'][len(refined_df)-1], format='%d/%m/%Y %H:%M:%S')
    st.session_state.start_date = start
    st.session_state.end_date = stop

    st.session_state.df =df
    #st.session_state.batch_data=batch_data
    st.session_state.refined_df=refined_df
    st.session_state.complete_refined_df=refined_df
    region_selections = [True, True, True]
    st.session_state.green_limit_global=19
    st.session_state.yellow_limit_global=23
    change_date(st.session_state.start_date,st.session_state.end_date,region_selections)

def compute_II(add_data,process_data_II,io_data_II):
    global df_II 
    df_II_old=pd.read_pickle('df_II.pkl')
    refined_df_II_old=pd.read_pickle('refined_df_II.pkl')
    import ast
    if add_data==True:
        df_II = pd.DataFrame()
        df_II=df_II.dropna(how='all')
        df_II = pd.concat([df_II,process_data_II], ignore_index=True)
        a=np.array(df_II['DATE TIME'] )
        for i in range(len(a)):
            a[i]=str(a[i])
        df_II['DATE TIME'] = a
        startendtime=[]
        global idxs_II
        idxs_II=[]
        a=np.array(df_II['BATCH ID'])
        startendtime.append([a[0], a[0],0])
        idxs_II.append(0)
        for i in range(1,len(df_II)):
            if a[i]!=a[i]:
                continue
            elif i==(len(df_II)-1):
                startendtime.append([a[i], a[i],i])
                idxs_II.append(i)
            elif a[i]==a[i-1]:
                continue
            else:
                startendtime.append([a[i-1], a[i-1],i-1])
                startendtime.append([a[i], a[i],i])
                idxs_II.append(i-1)
                idxs_II.append(i)
        idxs_II=list_to_matrix(idxs_II,2)
        for i in idxs_II:
            if i[0]==i[1]:
                idxs_II.remove(i)

        global h_II_time_id
        h_II_time_id=[]
        for j in range(0,len(idxs_II)):

            for i in range(idxs_II[j][0], idxs_II[j][1]+1):
                if i==idxs_II[j][1]:
                    h_II_time_id.append([idxs_II[j][0],i])
                    break
                elif df_II['HIGH VACUUM II ACTUAL'][i]>460:
                    continue
                elif df_II['HIGH VACUUM II ACTUAL'][i]<=460:
                    h_II_time_id.append([idxs_II[j][0],i])
                    break
        global temp_II_time_id
        temp_II_time_id=[]
        for j in range(0,len(idxs_II)):

            for i in range(idxs_II[j][0], idxs_II[j][1]):
                if i==idxs_II[j][1]-1:
                    temp_II_time_id.append([idxs_II[j][0],i])
                    break
                elif df_II['HEATER TEMP ACTUAL'][i]<240:
                    continue
                else:
                    temp_II_time_id.append([idxs_II[j][0],i])
                    break
        a=np.array(df_II['DATE TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        df_II['DATE TIME']=a
        h_II_time=[]
        for i in range(0,len(h_II_time_id)):
            h_II_time.append([calculate_time_difference(df_II['DATE TIME'][h_II_time_id[i][0]], df_II['DATE TIME'][h_II_time_id[i][1]])])
        t_II_time=[]
        for i in range(0,len(temp_II_time_id)):
            t_II_time.append([calculate_time_difference(df_II['DATE TIME'][temp_II_time_id[i][0]], df_II['DATE TIME'][temp_II_time_id[i][1]])])
        column_headers=["DATE TIME","BATCH ID", "Idxs_II","H_II Idxs","Temp_II Idxs","Temp_II Time","H_II Time"]
        global batch_data_II
        batch_data_II=pd.DataFrame(columns=column_headers)
        for i in range(len(idxs_II)):
            batch_data_II.loc[i, 'DATE TIME'] = df_II['DATE TIME'][idxs_II[i][0]+1]
            batch_data_II.loc[i, 'BATCH ID'] = df_II['BATCH ID'][idxs_II[i][0]+3]
            batch_data_II.loc[i, 'Idxs_II'] = idxs_II[i]
            batch_data_II.loc[i, 'H_II Idxs'] = h_II_time_id[i]
            batch_data_II.loc[i, 'Temp_II Idxs'] = temp_II_time_id[i]
            batch_data_II.loc[i, 'H_II Time'] = h_II_time[i]
            batch_data_II.loc[i, 'Temp_II Time'] = t_II_time[i]
        batch_data_II=batch_data_II.drop_duplicates(subset=['BATCH ID'])
        batch_data_II.reset_index(drop=True, inplace=True)
        batch_data_II['DATE TIME']=pd.to_datetime(batch_data_II['DATE TIME'], format='%d/%m/%Y %H:%M:%S')
        batch_data_II = batch_data_II.sort_values(by='DATE TIME')
        batch_data_II = batch_data_II.reset_index(drop=True)
        batch_data_II['DATE TIME']=batch_data_II['DATE TIME'].astype(str)
        idxs_II=np.array(batch_data_II["Idxs_II"])
        h_II_time_id=np.array(batch_data_II["H_II Idxs"])
        temp_II_time_id=np.array(batch_data_II["Temp_II Idxs"])
        h_II_time=np.array(batch_data_II["H_II Time"])
        t_II_time=np.array(batch_data_II["Temp_II Time"])
        df2_II = io_data_II
        new_header = df2_II.iloc[0]
        in_df = df2_II[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        columns_to_select = ["BATCH ID", "H_II Time", "Temp_II Time","Idxs_II","H_II Idxs","Temp_II Idxs"]
        merged_df_II = pd.merge(in_df, batch_data_II[columns_to_select], on="BATCH ID", how="inner")
        merged_df_II=merged_df_II[merged_df_II["PROCESS TYPE"]=='Coating']
        merged_df_II.reset_index(drop=True, inplace=True)
        import json
        for i in range(len(merged_df_II)):
            s=merged_df_II["INTERVENSIONS"][i]
            d = json.loads(s)
            if "Yes" in d.values():
                merged_df_II["INTERVENSIONS"][i]=d
            else:
                merged_df_II["INTERVENSIONS"][i]=None

        for i in range(len(merged_df_II)):
            merged_df_II['NI PLATING DATE TIME'][i]=str(merged_df_II['NI PLATING DATE TIME'][i])
            merged_df_II['BATCH START TIME'][i]=str(merged_df_II['BATCH START TIME'][i])
            merged_df_II['BATCH END TIME'][i]=str(merged_df_II['BATCH END TIME'][i])
        for i in range(len(merged_df_II)):
            if "-" in merged_df_II['NI PLATING DATE TIME'][i]:
                string=merged_df_II['NI PLATING DATE TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_II['NI PLATING DATE TIME'][i]=string2
        for i in range(len(merged_df_II)):
            if "-" in merged_df_II['BATCH START TIME'][i]:
                string=merged_df_II['BATCH START TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_II['BATCH START TIME'][i]=string2
        for i in range(len(merged_df_II)):
            if "-" in merged_df_II['BATCH END TIME'][i]:
                string=merged_df_II['BATCH END TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_II['BATCH END TIME'][i]=string2
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_II['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_II['NI PLATING DATE TIME'][i],merged_df_II['BATCH START TIME'][i])])
        merged_df_II["Ni_plating_diff"]=Ni_plating_diff
        #merged_df_II.to_excel("IO 37 batches merged.xlsx")
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_II['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_II['NI PLATING DATE TIME'][i],merged_df_II['BATCH START TIME'][i])])
        ni_hrs=[]
        for i in range(len(merged_df_II)):
            ni_hrs.append(Ni_plating_diff[i][0][0]*24+Ni_plating_diff[i][0][1]+Ni_plating_diff[i][0][2]/60+Ni_plating_diff[i][0][3]/3600)
        global h_II_mins    
        h_II_mins=[]
        for i in range(len(merged_df_II)):
            h_II_mins.append(merged_df_II["H_II Time"][i][0][1]*60+merged_df_II["H_II Time"][i][0][2]+merged_df_II["H_II Time"][i][0][3]/60)
        global t_II_mins
        t_II_mins=[]
        for i in range(len(merged_df_II)):
            t_II_mins.append(merged_df_II["Temp_II Time"][i][0][1]*60+merged_df_II["Temp_II Time"][i][0][2]+merged_df_II["Temp_II Time"][i][0][3]/60)
        drop_labels=[]
        for i in range(len(merged_df_II)):
            if h_II_mins[i]<0.1 or h_II_mins[i]>24:
                drop_labels.append(i)
        
        global refined_df_II
        refined_df_II=merged_df_II.drop(labels=drop_labels, axis=0)
        refined_df_II=refined_df_II.reset_index(drop=True)
        last_index_old_df_II = df_II_old.index[-1] if not df_II_old.empty else -1  # Handles empty old_df case
        new_start_index = last_index_old_df_II + 1
        columns_to_select = ["Idxs_II","H_II Idxs","Temp_II Idxs"]
        for col in columns_to_select:
            for i in range(len(refined_df_II)):
                refined_df_II[col][i][0]=refined_df_II[col][i][0]+new_start_index
                refined_df_II[col][i][1]=refined_df_II[col][i][1]+new_start_index

        df_II_old = pd.concat([df_II_old, df_II], ignore_index=True)
        refined_df_II_old = pd.concat([refined_df_II_old, refined_df_II], ignore_index=True)
    df_II=df_II_old
    refined_df_II=refined_df_II_old
    refined_df_II=refined_df_II.drop_duplicates(subset=['BATCH ID'])
    refined_df_II.reset_index(drop=True, inplace=True)
    #df_II.to_pickle('df_II.pkl')
    #refined_df_II.to_pickle('refined_df_II.pkl')
    a=refined_df_II
    a['BATCH START TIME']=pd.to_datetime(a['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    a = a.sort_values(by='BATCH START TIME')
    a = a.reset_index(drop=True)
    start=pd.to_datetime(a['BATCH START TIME'][0], format='%d/%m/%Y %H:%M:%S')
    stop=pd.to_datetime(a['BATCH START TIME'][len(refined_df_II)-1], format='%d/%m/%Y %H:%M:%S')
    st.session_state.start_date_II = start
    st.session_state.end_date_II = stop

    st.session_state.df_II =df_II
    #st.session_state.batch_data_II=batch_data_II
    st.session_state.refined_df_II=refined_df_II 
    st.session_state.complete_refined_df_II=refined_df_II
    region_selections_II = [True, True, True]
    st.session_state.green_limit_global_II=2
    st.session_state.yellow_limit_global_II=6

    change_date_II(st.session_state.start_date_II,st.session_state.end_date_II,region_selections_II)
def compute_glow(add_data,process_data_glow,io_data_glow):
    global df_glow
    df_glow_old=pd.read_pickle('df_glow.pkl')
    refined_df_glow_old=pd.read_pickle('refined_df_glow.pkl')
    import ast
    if add_data==True:
        df_glow = process_data_glow
        a=np.array(df_glow['DATE TIME'] )
        for i in range(len(a)):
            a[i]=str(a[i])
        df_glow['DATE TIME'] = a
        startendtime=[]
        global idxs_glow
        idxs_glow=[]
        a=np.array(df_glow['BATCH ID'])
        startendtime.append([a[0], a[0],0])
        idxs_glow.append(0)
        for i in range(1,len(df_glow)):
            if a[i]!=a[i]:
                continue
            elif i==(len(df_glow)-1):
                startendtime.append([a[i], a[i],i])
                idxs_glow.append(i)
            elif a[i]==a[i-1]:
                continue
            else:
                startendtime.append([a[i-1], a[i-1],i-1])
                startendtime.append([a[i], a[i],i])
                idxs_glow.append(i-1)
                idxs_glow.append(i)
        idxs_glow=list_to_matrix(idxs_glow,2)
        for i in idxs_glow:
            if i[0]==i[1]:
                idxs_glow.remove(i)
        for i in idxs_glow:
            if i[1]-i[0]<144:
                idxs_glow.remove(i)
        for i in idxs_glow:
            if int(str(df_glow['DATE TIME'][i[1]])[11:13])-int(str(df_glow['DATE TIME'][i[0]])[11:13])>2:
                idxs_glow.remove(i)
        global v_time_id
        v_time_id=[]
        for i in range(len(idxs_glow)):
            for j in range(idxs_glow[i][0],idxs_glow[i][1]):
                if df_glow['BIAS INITIAL VOLTAGE ACTUAL'][j]>=450:
                    v_time_id.append([j,j+144])
                    break
        v_total=[]
        for i in v_time_id:
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_glow['BIAS INITIAL VOLTAGE ACTUAL'][j]
                check.append(i)
            v_total.append(tot) 
        v_time_id_in=[]
        for i in range(len(v_time_id)):
            a=[]
            for j in range(idxs_glow[i][0],idxs_glow[i][1]):
                if df_glow['BIAS INITIAL VOLTAGE ACTUAL'][j]>=450:
                    a.append(j)
                    break
            for j in range(idxs_glow[i][0],idxs_glow[i][1]):
                if df_glow['BIAS INITIAL VOLTAGE ACTUAL'][j]>=550:
                    a.append(j)
                    break
            v_time_id_in.append(a)
        v_time_in=[]
        #for i in v_time_id_in:
            #v_time_in.append((i[1]-i[0]-1)*5)
        v_irr_diff=[]
        for i in range(len(v_time_id)):
            check=0
            for j in range(v_time_id[i][0],v_time_id[i][1]):
                if j==v_time_id[i][0]:
                    pass
                elif abs(df_glow['BIAS INITIAL VOLTAGE ACTUAL'][j-1]-df_glow['BIAS INITIAL VOLTAGE ACTUAL'][j])>10:
                    x=df_glow['BIAS INITIAL VOLTAGE ACTUAL'][v_time_id[i][0]:v_time_id[i][1]]
                    check=1
                    break
            if check==1:
                v_irr_diff.append(True)
            else:
                v_irr_diff.append(False)
        v_irr_tot=[]
        for i in range(len(v_total)):
            if v_total[i]<75250:
                v_irr_tot.append(True)
            else:
                v_irr_tot.append(False)
        v_irr=[]
        for i in range(len(v_irr_diff)):
            if v_irr_diff[i]==True or v_irr_tot==True:
                v_irr.append(True)
            else:
                v_irr.append(False)
        arc_count=[]
        for i in range(len(v_time_id)):
            count=[]
            for j in range(v_time_id[i][0],v_time_id[i][1]):
                if df_glow["BIAS ARC COUNT"][j]==1:
                    count.append(1)
            arc_count.append(len(count))
        arc_irr=[]
        for i in range(len(arc_count)):
            if arc_count[i]==0:
                arc_irr.append(False)
            else:
                arc_irr.append(True)
        c_total=[]
        for i in v_time_id:
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_glow['BIAS CURRENT ACTUAL'][j]
                check.append(i)
            c_total.append(tot) 
        g_total=[]
        for i in v_time_id:
            tot=0
            check=[]
            for j in range(i[0]+3,i[1]):
                tot+=df_glow['AR GAS ACTUAL'][j]
                check.append(i)
            g_total.append(tot)  
        g_irr=[]
        for i in range(len(g_total)):
            if g_total[i]<42000:
                g_irr.append(True)
            else:
                g_irr.append(False)
        c_irr=[False for i in range(len(g_irr))]



        a=np.array(df_glow['DATE TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        df_glow['DATE TIME']=a

        column_headers=["DATE TIME","BATCH ID", "Idxs","V Idxs","V Irregulars","Bias Arc Irregulars","I Irregulars","Ar Gas Irregulars","V total","I total","Arc total","Gas total"]
        batch_data_glow=pd.DataFrame(columns=column_headers)
        for i in range(len(v_time_id)):
            batch_data_glow.loc[i, 'DATE TIME'] = df_glow['DATE TIME'][idxs_glow[i][0]+1]
            batch_data_glow.loc[i, 'BATCH ID'] = df_glow['BATCH ID'][idxs_glow[i][0]+3]
            batch_data_glow.loc[i, 'Idxs'] = idxs_glow[i]
            batch_data_glow.loc[i, 'V Idxs'] = v_time_id[i]
            batch_data_glow.loc[i, 'V Irregulars'] = v_irr[i]
            batch_data_glow.loc[i, 'Bias Arc Irregulars'] = arc_irr[i]
            batch_data_glow.loc[i, 'I Irregulars'] = c_irr[i]
            batch_data_glow.loc[i, 'Ar Gas Irregulars'] = g_irr[i]
            batch_data_glow.loc[i, 'V total'] = v_total[i]
            batch_data_glow.loc[i, 'I total'] = c_total[i]
            batch_data_glow.loc[i, 'Gas total'] = g_total[i]
            batch_data_glow.loc[i, 'Arc total'] = arc_count[i]

        batch_data_glow=batch_data_glow.drop_duplicates(subset=['BATCH ID'])
        batch_data_glow.reset_index(drop=True, inplace=True)
        batch_data_glow['DATE TIME']=pd.to_datetime(batch_data_glow['DATE TIME'], format='%d/%m/%Y %H:%M:%S')
        batch_data_glow = batch_data_glow.sort_values(by='DATE TIME')
        batch_data_glow = batch_data_glow.reset_index(drop=True)
        batch_data_glow['DATE TIME']=batch_data_glow['DATE TIME'].astype(str)
        idxs_glow=np.array(batch_data_glow["Idxs"])
        v_time_id=np.array(batch_data_glow["V Idxs"])
        v_irr=np.array(batch_data_glow["V Irregulars"])
        arc_irr=np.array(batch_data_glow["Bias Arc Irregulars"])
        c_irr=np.array(batch_data_glow["I Irregulars"])
        g_irr=np.array(batch_data_glow["Ar Gas Irregulars"])
        v_total=np.array(batch_data_glow["V total"])
        c_total=np.array(batch_data_glow["I total"])
        g_total=np.array(batch_data_glow["Gas total"])
        arc_total=np.array(batch_data_glow["Arc total"])
        df2_glow = io_data_glow 
        new_header = df2_glow.iloc[0]
        in_df = df2_glow[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        columns_to_select = ["DATE TIME","BATCH ID", "Idxs","V Idxs","V Irregulars","Bias Arc Irregulars","I Irregulars","Ar Gas Irregulars","V total","I total","Gas total","Arc total"]
        merged_df_glow = pd.merge(in_df, batch_data_glow[columns_to_select], on="BATCH ID", how="inner")
        merged_df_glow=merged_df_glow[merged_df_glow["PROCESS TYPE"]=='Coating']
        merged_df_glow.reset_index(drop=True, inplace=True)
        import json
        for i in range(len(merged_df_glow)):
            s=merged_df_glow["INTERVENSIONS"][i]
            d = json.loads(s)
            if "Yes" in d.values():
                merged_df_glow["INTERVENSIONS"][i]=d
            else:
                merged_df_glow["INTERVENSIONS"][i]=None

        for i in range(len(merged_df_glow)):
            merged_df_glow['NI PLATING DATE TIME'][i]=str(merged_df_glow['NI PLATING DATE TIME'][i])
            merged_df_glow['BATCH START TIME'][i]=str(merged_df_glow['BATCH START TIME'][i])
            merged_df_glow['BATCH END TIME'][i]=str(merged_df_glow['BATCH END TIME'][i])
        for i in range(len(merged_df_glow)):
            if "-" in merged_df_glow['NI PLATING DATE TIME'][i]:
                string=merged_df_glow['NI PLATING DATE TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_glow['NI PLATING DATE TIME'][i]=string2
        for i in range(len(merged_df_glow)):
            if "-" in merged_df_glow['BATCH START TIME'][i]:
                string=merged_df_glow['BATCH START TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_glow['BATCH START TIME'][i]=string2
        for i in range(len(merged_df_glow)):
            if "-" in merged_df_glow['BATCH END TIME'][i]:
                string=merged_df_glow['BATCH END TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_glow['BATCH END TIME'][i]=string2
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_glow['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_glow['NI PLATING DATE TIME'][i],merged_df_glow['BATCH START TIME'][i])])
        merged_df_glow["Ni_plating_diff"]=Ni_plating_diff
        #merged_df_glow.to_excel("IO 37 batches merged.xlsx")
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_glow['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_glow['NI PLATING DATE TIME'][i],merged_df_glow['BATCH START TIME'][i])])
        
        global refined_df_glow
        refined_df_glow=merged_df_glow
        last_index_old_df_glow = df_glow_old.index[-1] if not df_glow_old.empty else -1  # Handles empty old_df case
        new_start_index = last_index_old_df_glow + 1
        columns_to_select = ["Idxs","V Idxs"]
        for col in columns_to_select:
            for i in range(len(refined_df_glow)):
                refined_df_glow[col][i][0]=refined_df_glow[col][i][0]+new_start_index
                refined_df_glow[col][i][1]=refined_df_glow[col][i][1]+new_start_index

        df_glow_old = pd.concat([df_glow_old, df_glow], ignore_index=True)
        refined_df_glow_old = pd.concat([refined_df_glow_old, refined_df_glow], ignore_index=True)

    df_glow=df_glow_old
    refined_df_glow=refined_df_glow_old
    refined_df_glow=refined_df_glow.drop_duplicates(subset=['BATCH ID'])
    refined_df_glow.reset_index(drop=True, inplace=True)
    #df_glow.to_pickle('df_glow.pkl')
    #refined_df_glow.to_pickle('refined_df_glow.pkl')

    a=refined_df_glow
    a['BATCH START TIME']=pd.to_datetime(a['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    a = a.sort_values(by='BATCH START TIME')
    a = a.reset_index(drop=True)
    start=pd.to_datetime(a['BATCH START TIME'][0], format='%d/%m/%Y %H:%M:%S')
    stop=pd.to_datetime(a['BATCH START TIME'][len(refined_df_glow)-1], format='%d/%m/%Y %H:%M:%S')
    st.session_state.start_date_glow = start
    st.session_state.end_date_glow = stop

    st.session_state.df_glow =df_glow
    #st.session_state.batch_data_glow=batch_data_glow
    st.session_state.refined_df_glow=refined_df_glow  
    st.session_state.complete_refined_df_glow=refined_df_glow
    golden_index_glow = 1
    golden_batch_glow=refined_df_glow['BATCH ID'][golden_index_glow]
    golden_glow_details=refined_df_glow.iloc[golden_index_glow]
    golden_glow_process=df_glow[refined_df_glow['V Idxs'][golden_index_glow][0]:refined_df_glow['V Idxs'][golden_index_glow][1]]
    st.session_state.golden_batch_glow=golden_batch_glow
    st.session_state.golden_index_glow=golden_index_glow
    st.session_state.golden_glow_details=golden_glow_details
    st.session_state.golden_glow_process=golden_glow_process

    region_selections_glow = [True, False, False, False, False]

    change_date_glow(st.session_state.start_date_glow,st.session_state.end_date_glow,region_selections_glow)

def compute_ac(add_data,process_data_ac,io_data_ac):
    global df_ac
    df_ac_old=pd.read_pickle('df_ac.pkl')
    refined_df_ac_old=pd.read_pickle('refined_df_ac.pkl')
    import ast
    if add_data==True:
        df_ac = process_data_ac
        a=np.array(df_ac['DATE TIME'] )
        for i in range(len(a)):
            a[i]=str(a[i])
        df_ac['DATE TIME'] = a
        print(len(df_ac))
        startendtime=[]
        idxs_ac=[]
        a=np.array(df_ac['BATCH ID'])
        startendtime.append([a[0], a[0],0])
        idxs_ac.append(0)
        for i in range(1,len(df_ac)):
            if a[i]!=a[i]:
                continue
            elif i==(len(df_ac)-1):
                startendtime.append([a[i], a[i],i])
                idxs_ac.append(i)
            elif a[i]==a[i-1]:
                continue
            else:
                startendtime.append([a[i-1], a[i-1],i-1])
                startendtime.append([a[i], a[i],i])
                idxs_ac.append(i-1)
                idxs_ac.append(i)
        idxs_ac=list_to_matrix(idxs_ac,2)
        for i in idxs_ac:
            if i[0]==i[1]:
                idxs_ac.remove(i)
        for i in idxs_ac:
            if i[1]-i[0]>200:
                idxs_ac.remove(i)
        for i in idxs_ac:
            if int(str(df_ac['DATE TIME'][i[1]])[11:13])-int(str(df_ac['DATE TIME'][i[0]])[11:13])>2:
                idxs_ac.remove(i)
        print(len(idxs_ac))
        global step2_idxs
        step2_idxs=[]
        for i in idxs_ac:
            temp=[]
            for j in range(i[0],i[1]):
                if df_ac['ACTUAL STEP NO'][j]==2:
                    temp.append(j)
                    break
            for j in range(i[0],i[1]):
                if df_ac['ACTUAL STEP NO'][j]==3:
                    temp.append(j-1)
                    break
            step2_idxs.append(temp)
        drops=[]
        for i in range(len(step2_idxs)):
            if (step2_idxs[i][1]-step2_idxs[i][0])<10:
                drops.append(i)
        idxs_ac = [item for idx, item in enumerate(idxs_ac) if idx not in drops]
        step2_idxs = [item for idx, item in enumerate(step2_idxs) if idx not in drops]
        print(len(idxs_ac),len(step2_idxs))
        v_total=[]
        for i in step2_idxs:
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ac['BIAS VOLTAGE ACTUAL'][j]
                check.append(i)
            v_total.append(tot)  
        v_irr=[]
        for i in range(len(v_total)):
            if v_total[i]<8500:
                v_irr.append(True)
            else:
                v_irr.append(False)
        arc_count=[]
        for i in range(len(step2_idxs)):
            count=[]
            for j in range(step2_idxs[i][0],step2_idxs[i][1]):
                if df_ac["BIAS ARC COUNT"][j]==1:
                    count.append(1)
            arc_count.append(len(count))
        arc_irr=[]
        for i in range(len(arc_count)):
            if arc_count[i]==0:
                arc_irr.append(False)
            else:
                arc_irr.append(True)
        c1_total=[]
        for i in step2_idxs:
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ac['ARC 1 CURRENT ACTUAL'][j]
                check.append(i)
            c1_total.append(tot)  
        c1_irr=[]
        for i in range(len(c1_total)):
            if c1_total[i]<8500:
                c1_irr.append(True)
            else:
                c1_irr.append(False)
        c2_total=[]
        for i in step2_idxs:
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ac['ARC 2 CURRENT ACTUAL'][j]
                check.append(i)
            c2_total.append(tot) 
        c2_irr=[]
        for i in range(len(c2_total)):
            if c2_total[i]<8500:
                c2_irr.append(True)
            else:
                c2_irr.append(False)
        c3_total=[]
        for i in step2_idxs:
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ac['ARC 3 CURRENT ACTUAL'][j]
                check.append(i)
            c3_total.append(tot) 
        c3_irr=[]
        for i in range(len(c3_total)):
            if c3_total[i]<8500:
                c3_irr.append(True)
            else:
                c3_irr.append(False)

        g_total=[]
        for i in step2_idxs:
            tot=0
            check=[]
            for j in range(i[0]+3,i[1]):
                tot+=df_ac['AR GAS ACTUAL'][j]
                check.append(i)
            g_total.append(tot)   
        g_irr=[]
        for i in range(len(g_total)):
            if g_total[i]<1750:
                g_irr.append(True)
            else:
                g_irr.append(False)



        a=np.array(df_ac['DATE TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        df_ac['DATE TIME']=a

        column_headers=["DATE TIME","BATCH ID", "Idxs","Step2 Idxs","V Irregulars","Bias Arc Irregulars","I1 Irregulars","I2 Irregulars","I3 Irregulars","Ar Gas Irregulars","V total","I1 total","I2 total","I3 total","Arc total","Ar Gas total"]
        batch_data_ac=pd.DataFrame(columns=column_headers)
        for i in range(len(idxs_ac)):
            batch_data_ac.loc[i, 'DATE TIME'] = df_ac['DATE TIME'][idxs_ac[i][0]+1]
            batch_data_ac.loc[i, 'BATCH ID'] = df_ac['BATCH ID'][idxs_ac[i][0]+3]
            batch_data_ac.loc[i, 'Idxs'] = idxs_ac[i]
            batch_data_ac.loc[i, 'Step2 Idxs'] = step2_idxs[i]
            batch_data_ac.loc[i, 'V Irregulars'] = v_irr[i]
            batch_data_ac.loc[i, 'Bias Arc Irregulars'] = arc_irr[i]
            batch_data_ac.loc[i, 'I1 Irregulars'] = c1_irr[i]
            batch_data_ac.loc[i, 'I2 Irregulars'] = c2_irr[i]
            batch_data_ac.loc[i, 'I3 Irregulars'] = c3_irr[i]
            batch_data_ac.loc[i, 'Ar Gas Irregulars'] = g_irr[i]
            batch_data_ac.loc[i, 'V total'] = v_total[i]
            batch_data_ac.loc[i, 'I1 total'] = c1_total[i]
            batch_data_ac.loc[i, 'I2 total'] = c2_total[i]
            batch_data_ac.loc[i, 'I3 total'] = c3_total[i]
            batch_data_ac.loc[i, 'Ar Gas total'] = g_total[i]
            batch_data_ac.loc[i, 'Arc total'] = arc_count[i]

        batch_data_ac=batch_data_ac.drop_duplicates(subset=['BATCH ID'])
        batch_data_ac.reset_index(drop=True, inplace=True)
        batch_data_ac['DATE TIME']=pd.to_datetime(batch_data_ac['DATE TIME'], format='%d/%m/%Y %H:%M:%S')
        batch_data_ac = batch_data_ac.sort_values(by='DATE TIME')
        batch_data_ac = batch_data_ac.reset_index(drop=True)
        batch_data_ac['DATE TIME']=batch_data_ac['DATE TIME'].astype(str)
        idxs_ac=np.array(batch_data_ac["Idxs"])
        step2_idxs=np.array(batch_data_ac["Step2 Idxs"])
        v_irr=np.array(batch_data_ac["V Irregulars"])
        arc_irr=np.array(batch_data_ac["Bias Arc Irregulars"])
        c1_irr=np.array(batch_data_ac["I1 Irregulars"])
        c2_irr=np.array(batch_data_ac["I2 Irregulars"])
        c3_irr=np.array(batch_data_ac["I3 Irregulars"])
        g_irr=np.array(batch_data_ac["Ar Gas Irregulars"])
        v_total=np.array(batch_data_ac["V total"])
        c1_total=np.array(batch_data_ac["I1 total"])
        c2_total=np.array(batch_data_ac["I2 total"])
        c3_total=np.array(batch_data_ac["I3 total"])
        g_total=np.array(batch_data_ac["Ar Gas total"])
        arc_total=np.array(batch_data_ac["Arc total"])
        df2_ac =io_data_ac
        new_header = df2_ac.iloc[0]
        in_df = df2_ac[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        columns_to_select = ["DATE TIME","BATCH ID", "Idxs","Step2 Idxs","V Irregulars","Bias Arc Irregulars","I1 Irregulars","I2 Irregulars","I3 Irregulars","Ar Gas Irregulars","V total","I1 total","I2 total","I3 total","Arc total","Ar Gas total"]
        merged_df_ac = pd.merge(batch_data_ac[columns_to_select],in_df, on="BATCH ID", how="inner")
        merged_df_ac=merged_df_ac[merged_df_ac["PROCESS TYPE"]=='Coating']
        merged_df_ac.reset_index(drop=True, inplace=True)
        import json
        for i in range(len(merged_df_ac)):
            s=merged_df_ac["INTERVENSIONS"][i]
            d = json.loads(s)
            if "Yes" in d.values():
                merged_df_ac["INTERVENSIONS"][i]=d
            else:
                merged_df_ac["INTERVENSIONS"][i]=None

        for i in range(len(merged_df_ac)):
            merged_df_ac['NI PLATING DATE TIME'][i]=str(merged_df_ac['NI PLATING DATE TIME'][i])
            merged_df_ac['BATCH START TIME'][i]=str(merged_df_ac['BATCH START TIME'][i])
            merged_df_ac['BATCH END TIME'][i]=str(merged_df_ac['BATCH END TIME'][i])
        for i in range(len(merged_df_ac)):
            if "-" in merged_df_ac['NI PLATING DATE TIME'][i]:
                string=merged_df_ac['NI PLATING DATE TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ac['NI PLATING DATE TIME'][i]=string2
        for i in range(len(merged_df_ac)):
            if "-" in merged_df_ac['BATCH START TIME'][i]:
                string=merged_df_ac['BATCH START TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ac['BATCH START TIME'][i]=string2
        for i in range(len(merged_df_ac)):
            if "-" in merged_df_ac['BATCH END TIME'][i]:
                string=merged_df_ac['BATCH END TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ac['BATCH END TIME'][i]=string2
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_ac['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_ac['NI PLATING DATE TIME'][i],merged_df_ac['BATCH START TIME'][i])])
        merged_df_ac["Ni_plating_diff"]=Ni_plating_diff
        #merged_df_ac.to_excel("IO 37 batches merged.xlsx")
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_ac['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_ac['NI PLATING DATE TIME'][i],merged_df_ac['BATCH START TIME'][i])])
        
        global refined_df_ac
        refined_df_ac=merged_df_ac
        last_index_old_df_ac = df_ac_old.index[-1] if not df_ac_old.empty else -1  # Handles empty old_df case
        new_start_index = last_index_old_df_ac + 1
        columns_to_select = ["Idxs","Step2 Idxs"]
        for col in columns_to_select:
            for i in range(len(refined_df_ac)):
                refined_df_ac[col][i][0]=refined_df_ac[col][i][0]+new_start_index
                refined_df_ac[col][i][1]=refined_df_ac[col][i][1]+new_start_index

        df_ac_old = pd.concat([df_ac_old, df_ac], ignore_index=True)
        refined_df_ac_old = pd.concat([refined_df_ac_old, refined_df_ac], ignore_index=True)

    df_ac=df_ac_old
    refined_df_ac=refined_df_ac_old
    refined_df_ac=refined_df_ac.drop_duplicates(subset=['BATCH ID'])
    refined_df_ac.reset_index(drop=True, inplace=True)
    #df_ac.to_pickle('df_ac.pkl')
    #refined_df_ac.to_pickle('refined_df_ac.pkl')
    a=refined_df_ac
    a['BATCH START TIME']=pd.to_datetime(a['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    a = a.sort_values(by='BATCH START TIME')
    a = a.reset_index(drop=True)
    start=pd.to_datetime(a['BATCH START TIME'][0], format='%d/%m/%Y %H:%M:%S')
    stop=pd.to_datetime(a['BATCH START TIME'][len(refined_df_ac)-1], format='%d/%m/%Y %H:%M:%S')
    st.session_state.start_date_ac = start
    st.session_state.end_date_ac = stop

    st.session_state.df_ac =df_ac
    #st.session_state.batch_data_ac=batch_data_ac
    st.session_state.refined_df_ac=refined_df_ac
    
    #st.session_state.idxs_ac =idxs_ac
  
    st.session_state.complete_refined_df_ac=refined_df_ac
    golden_index_ac = 0
    golden_batch_ac=refined_df_ac['BATCH ID'][golden_index_ac]
    golden_ac_details=refined_df_ac.iloc[golden_index_ac]
    golden_ac_process=df_ac[refined_df_ac['Step2 Idxs'][golden_index_ac][0]:refined_df_ac['Step2 Idxs'][golden_index_ac][1]]
    st.session_state.golden_batch_ac=golden_batch_ac
    st.session_state.golden_index_ac=golden_index_ac
    st.session_state.golden_ac_details=golden_ac_details
    st.session_state.golden_ac_process=golden_ac_process

    region_selections_ac = [True, False, False, False,False,False, False]
    change_date_ac(st.session_state.start_date_ac,st.session_state.end_date_ac,region_selections_ac)
def compute_ae(add_data,process_data_ae,io_data_ae):
    global df_ae
    df_ae_old=pd.read_pickle('df_ae.pkl')
    refined_df_ae_old=pd.read_pickle('refined_df_ae.pkl')
    import ast
    if add_data==True:
        df_ae = process_data_ae
        a=np.array(df_ae['DATE TIME'] )
        for i in range(len(a)):
            a[i]=str(a[i])
        df_ae['DATE TIME'] = a
        print(len(df_ae))
        startendtime=[]
        idxs_ae=[]
        a=np.array(df_ae['BATCH ID'])
        startendtime.append([a[0], a[0],0])
        idxs_ae.append(0)
        for i in range(1,len(df_ae)):
            if a[i]!=a[i]:
                continue
            elif i==(len(df_ae)-1):
                startendtime.append([a[i], a[i],i])
                idxs_ae.append(i)
            elif a[i]==a[i-1]:
                continue
            else:
                startendtime.append([a[i-1], a[i-1],i-1])
                startendtime.append([a[i], a[i],i])
                idxs_ae.append(i-1)
                idxs_ae.append(i)
        idxs_ae=list_to_matrix(idxs_ae,2)
        for i in idxs_ae:
            if i[0]==i[1]:
                idxs_ae.remove(i)
        drops=[]
        for i in range(len(idxs_ae)):
            if idxs_ae[i][1]-idxs_ae[i][0]<130:
                drops.append(i)
            elif idxs_ae[i][1]-idxs_ae[i][0]>270:
                drops.append(i)

        idxs_ae = [item for idx, item in enumerate(idxs_ae) if idx not in drops]
        drops=[]
        for i in range(len(idxs_ae)):
            if abs(int(str(df_ae['DATE TIME'][idxs_ae[i][1]])[11:13])-int(str(df_ae['DATE TIME'][idxs_ae[i][0]])[11:13]))>2:
                drops.append(i)
        idxs_ae = [item for idx, item in enumerate(idxs_ae) if idx not in drops]
        step_6=[]
        for i in range(len(idxs_ae)):
            temp=[]
            for j in range(idxs_ae[i][0],idxs_ae[i][1]+1):
                if df_ae["ACTUAL STEP NO"][j]==6:
                    temp.append(1)
            step_6.append(len(temp))
        step7_start=[]
        for i in range(len(idxs_ae)):
            for j in range(idxs_ae[i][0],idxs_ae[i][1]+1):
                if df_ae["ACTUAL STEP NO"][j]==7:
                    step7_start.append(j)
                    break
        recipe=[]
        rec_idxs=[]
        for i in range(len(idxs_ae)):
            if step_6[i]>20:
                rec_idxs.append([idxs_ae[i][0],idxs_ae[i][1]])
                recipe.append('New')
            else:
                rec_idxs.append([step7_start[i],idxs_ae[i][1]])
                recipe.append('Old')       

        v_total=[]
        for i in rec_idxs:
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ae['BIAS VOLTAGE ACTUAL'][j]
                check.append(i)
            v_total.append(tot)  
        v_irr=[]
        for i in range(len(v_total)):
            if recipe[i]=='Old':
                if v_total[i]<=87500:
                    v_irr.append(True)
                else:
                    v_irr.append(False)
            elif recipe[i]=='New':
                if v_total[i]<=113000:
                    v_irr.append(True)
                else:
                    v_irr.append(False)
        arc_count=[]
        for i in range(len(rec_idxs)):
            count=[]
            for j in range(rec_idxs[i][0],rec_idxs[i][1]):
                if df_ae["BIAS ARC COUNT"][j]==1:
                    count.append(1)
            arc_count.append(len(count))
        arc_irr=[]
        for i in range(len(arc_count)):
            if arc_count[i]==0:
                arc_irr.append(False)
            else:
                arc_irr.append(True)
        c1_total=[]
        for j,i in enumerate(rec_idxs):    
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ae['ARC 1 CURRENT ACTUAL'][j]
                check.append(i)
            c1_total.append(tot) 
        c1_irr=[]
        for i in range(len(c1_total)):
            if c1_total[i]<40000:
                c1_irr.append(True)
            else:
                c1_irr.append(False)
        c3_total=[]
        for j,i in enumerate(rec_idxs):    
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ae['ARC 3 CURRENT ACTUAL'][j]
                check.append(i)
            c3_total.append(tot)
        c3_irr=[]
        for i in range(len(c3_total)):
            if c3_total[i]<40000:
                c3_irr.append(True)
            else:
                c3_irr.append(False)
        c2_total=[]
        for j,i in enumerate(rec_idxs):    
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ae['ARC 2 CURRENT ACTUAL'][j]
                check.append(i)
            c2_total.append(tot)
        c2_irr=[]
        for i in range(len(c2_total)):
            if recipe[i]=='New':
                if c2_total[i]<55000:
                    c2_irr.append(True)
                else:
                    c2_irr.append(False)
            elif recipe[i]=='Old':
                if c2_total[i]<40000:
                    c2_irr.append(True)
                else:
                    c2_irr.append(False)

        g_total=[]
        for i in rec_idxs:
            tot=0
            check=[]
            for j in range(i[0]+3,i[1]):
                tot+=df_ae['AR GAS ACTUAL'][j]
                check.append(i)
            g_total.append(tot)   
        g_irr=[]
        for i in range(len(g_total)):
            if recipe[i]=='New':
                if g_total[i]<25000:
                    g_irr.append(True)
                else:
                    g_irr.append(False)
            elif recipe[i]=='Old':
                if g_total[i]<20000:
                    g_irr.append(True)
                else:
                    g_irr.append(False)   
        step_dict={"6":[],"7":[],"8":[],"9":[],"10":[]}
        for key in step_dict.keys():
            id_list=[]
            for i in range(len(idxs_ae)):
                temp=[]
                for j in range(idxs_ae[i][0],idxs_ae[i][1]+1):
                    if df_ae["ACTUAL STEP NO"][j]==int(key):
                        temp.append(j)
                temp=remove_solo_values(temp)
                state=0
                for i in range(1,len(temp)):
                    if temp[i]-temp[i-1]>1:
                        state=i
                        break
                    else:
                        pass
                if state==0:
                    id_list.append([[temp[0],temp[len(temp)-1]]])
                elif state==i:
                    if temp[len(temp)-1]==temp[i]:
                        id_list.append([[temp[0],temp[len(temp)-1]]])
                    else:
                        id_list.append([[temp[0],temp[i-1]],[temp[i],temp[len(temp)-1]]])
            step_dict[key]=id_list
        step_v_total={"6":[],"7":[],"8":[],"9":[],"10":[]}
        for l in step_v_total.keys():
            for k in step_dict[l]:   
                tot=0
                for j,i in enumerate(k):
                    for j in range(i[0],i[1]):
                        tot+=df_ae['BIAS VOLTAGE ACTUAL'][j]
                step_v_total[l].append(tot)  
        step_v_irr={"6":[],"7":[],"8":[],"9":[],"10":[]}
        from scipy import stats as stat
        for l in step_v_total.keys():
            for i in range(len(step_v_total[l])):
                if recipe[i]=='Old':
                    temp = [step_v_total[l][m] for m in range(len(step_v_total[l])) if recipe[m] == 'Old']
                    if step_v_total[l][i]<np.median(temp)-2*np.std(temp) or step_v_total[l][i]>np.median(temp)+2*np.std(temp):
                        step_v_irr[l].append(True)
                    else:
                        step_v_irr[l].append(False)
                elif recipe[i]=='New':
                    temp = [step_v_total[l][m] for m in range(len(step_v_total[l])) if recipe[m] == 'New']
                    if step_v_total[l][i]<np.median(temp)-2*np.std(temp) or step_v_total[l][i]>np.median(temp)+2*np.std(temp):
                        step_v_irr[l].append(True)
                    else:
                        step_v_irr[l].append(False)
        step_c_total={"1":{},"2":{},"3":{}}
        for m in step_c_total.keys():
            step_c_total[m]={"6":[],"7":[],"8":[],"9":[],"10":[]}
            for l in step_c_total[m].keys():
                str1='ARC '+str(m)+" CURRENT ACTUAL"
                for k in step_dict[l]:   
                    tot=0
                    for j,i in enumerate(k):
                        for j in range(i[0],i[1]):
                            tot+=df_ae[str1][j]
                    step_c_total[m][l].append(tot)  
        step_c_irr={"1":{},"2":{},"3":{}}
        for m in step_c_irr.keys():
            step_c_irr[m]={"6":[],"7":[],"8":[],"9":[],"10":[]}
            for l in step_c_irr[m].keys():
                for i in range(len(step_c_total[m][l])):
                    if recipe[i]=='Old':
                        temp = [step_c_total[m][l][n] for n in range(len(step_c_total[m][l])) if recipe[n] == 'Old']
                        if step_c_total[m][l][i]<np.median(temp)-2*np.std(temp) or step_c_total[m][l][i]>np.median(temp)+2*np.std(temp):
                            step_c_irr[m][l].append(True)
                        else:
                            step_c_irr[m][l].append(False)
                    elif recipe[i]=='New':
                        temp = [step_c_total[m][l][n] for n in range(len(step_c_total[m][l])) if recipe[n] == 'New']
                        if step_c_total[m][l][i]<np.median(temp)-2*np.std(temp) or step_c_total[m][l][i]>np.median(temp)+2*np.std(temp):
                            step_c_irr[m][l].append(True)
                        else:
                            step_c_irr[m][l].append(False)
        step_arc_count={"6":[],"7":[],"8":[],"9":[],"10":[]}
        for l in step_arc_count.keys():
            for k in step_dict[l]:   
                count=[]
                for j,i in enumerate(k):
                    for j in range(i[0],i[1]):
                        if df_ae["BIAS ARC COUNT"][j]==1:
                            count.append(1)
                step_arc_count[l].append(len(count))
        step_arc_irr={"6":[],"7":[],"8":[],"9":[],"10":[]}
        for l in step_arc_irr.keys():
            for i in range(len(step_arc_count[l])):
                if step_arc_count[l][i]==0:
                    step_arc_irr[l].append(False)
                else:
                    step_arc_irr[l].append(True)
        step_g_total={"6":[],"7":[],"8":[],"9":[],"10":[]}
        for l in step_g_total.keys():
            for k in step_dict[l]:   
                tot=0
                for j,i in enumerate(k):  
                    for j in range(i[0],i[1]):
                        tot+=df_ae['AR GAS ACTUAL'][j]
                step_g_total[l].append(tot)  
        step_g_irr={"6":[],"7":[],"8":[],"9":[],"10":[]}
        for l in step_g_total.keys():
            for i in range(len(step_g_total[l])):
                if recipe[i]=='Old':
                    temp = [step_g_total[l][m] for m in range(len(step_g_total[l])) if recipe[m] == 'Old']
                    if step_g_total[l][i]<np.median(temp)-2*np.std(temp) or step_g_total[l][i]>np.median(temp)+2*np.std(temp):
                        step_g_irr[l].append(True)
                    else:
                        step_g_irr[l].append(False)
                elif recipe[i]=='New':
                    temp = [step_g_total[l][m] for m in range(len(step_g_total[l])) if recipe[m] == 'New']
                    if step_g_total[l][i]<np.median(temp)-2*np.std(temp) or step_g_total[l][i]>np.median(temp)+2*np.std(temp):
                        step_g_irr[l].append(True)
                    else:
                        step_g_irr[l].append(False)


        a=np.array(df_ae['DATE TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        df_ae['DATE TIME']=a
        column_headers = ["DATE TIME", "BATCH ID", "Idxs", "Recipe", "Recipe Idxs", "V Irregulars", 
                    "Bias Arc Irregulars", "I1 Irregulars", "I2 Irregulars", "I3 Irregulars", 
                    "Ar Gas Irregulars", "V total", "I1 total", "I2 total", "I3 total", 
                    "Arc total", "Ar Gas total"]
        # List of columns to repeat for each step
        step_columns = ["V Irregulars", "Bias Arc Irregulars", "I1 Irregulars", "I2 Irregulars", 
                        "I3 Irregulars", "Ar Gas Irregulars", "V total", "I1 total", "I2 total", 
                        "I3 total", "Arc total", "Ar Gas total"]

        # Create columns for steps 6 through 10
        steps = range(6, 11)  # Step 6 to Step 10

        # New column headers list that will store the expanded column names
        expanded_column_headers = column_headers[:4]  # Keep first four columns unchanged

        # Add step-specific columns for Recipe Idxs
        for step in steps:
            expanded_column_headers.append(f"Step {step} Idxs")

        # Add step-specific columns for other step columns
        for step in steps:
            for col in step_columns:
                expanded_column_headers.append(f"Step {step} {col}")
        step_keys = ["6", "7", "8", "9", "10"]
        batch_data_ae=pd.DataFrame(columns=column_headers)
        print(len(idxs_ae),len(step_dict['6']))
        for i in range(len(idxs_ae)):
            batch_data_ae.loc[i, 'DATE TIME'] = df_ae['DATE TIME'][idxs_ae[i][0]+1]
            batch_data_ae.loc[i, 'BATCH ID'] = df_ae['BATCH ID'][idxs_ae[i][0]+3]
            batch_data_ae.at[i, 'Idxs'] = idxs_ae[i]
            batch_data_ae.loc[i, 'Recipe'] = recipe[i]
            batch_data_ae.at[i, 'Recipe Idxs'] = rec_idxs[i]
            batch_data_ae.loc[i, 'V Irregulars'] = v_irr[i]
            batch_data_ae.loc[i, 'Bias Arc Irregulars'] = arc_irr[i]
            batch_data_ae.loc[i, 'I1 Irregulars'] = c1_irr[i]
            batch_data_ae.loc[i, 'I2 Irregulars'] = c2_irr[i]
            batch_data_ae.loc[i, 'I3 Irregulars'] = c3_irr[i]
            batch_data_ae.loc[i, 'Ar Gas Irregulars'] = g_irr[i]
            batch_data_ae.loc[i, 'V total'] = v_total[i]
            batch_data_ae.loc[i, 'I1 total'] = c1_total[i]
            batch_data_ae.loc[i, 'I2 total'] = c2_total[i]
            batch_data_ae.loc[i, 'I3 total'] = c3_total[i]
            batch_data_ae.loc[i, 'Ar Gas total'] = g_total[i]
            batch_data_ae.loc[i, 'Arc total'] = arc_count[i]
            for step in step_keys:
                # For each step, populate the irregulars and totals
                batch_data_ae.loc[i, f'Step {step} Idxs'] = str(step_dict[step][i])
                batch_data_ae.loc[i, f'Step {step} V total'] = step_v_total[step][i]
                batch_data_ae.loc[i, f'Step {step} Ar Gas total'] = step_g_total[step][i]
                batch_data_ae.loc[i, f'Step {step} Arc total'] = step_arc_count[step][i]  # Assuming you have a dictionary for Arc total
                
                # Populate the current totals (I1, I2, I3) from step_c_total
                batch_data_ae.loc[i, f'Step {step} I1 total'] = step_c_total["1"][step][i]
                batch_data_ae.loc[i, f'Step {step} I2 total'] = step_c_total["2"][step][i]
                batch_data_ae.loc[i, f'Step {step} I3 total'] = step_c_total["3"][step][i]

                # Populate the current irregulars (I1, I2, I3) from step_c_irr
                batch_data_ae.loc[i, f'Step {step} I1 Irregulars'] = step_c_irr["1"][step][i]
                batch_data_ae.loc[i, f'Step {step} I2 Irregulars'] = step_c_irr["2"][step][i]
                batch_data_ae.loc[i, f'Step {step} I3 Irregulars'] = step_c_irr["3"][step][i]

                # Populate other irregulars (V, Bias Arc, Ar Gas) - similar to the totals
                batch_data_ae.loc[i, f'Step {step} V Irregulars'] = step_v_irr[step][i]  # Assuming you have a step_v_irr dictionary
                batch_data_ae.loc[i, f'Step {step} Bias Arc Irregulars'] = step_arc_irr[step][i]  # Assuming a dictionary for Bias Arc Irregulars
                batch_data_ae.loc[i, f'Step {step} Ar Gas Irregulars'] = step_g_irr[step][i]
        batch_data_ae=batch_data_ae.drop_duplicates(subset=['BATCH ID'])
        batch_data_ae.reset_index(drop=True, inplace=True)
        batch_data_ae['DATE TIME']=pd.to_datetime(batch_data_ae['DATE TIME'], format='%d/%m/%Y %H:%M:%S')
        batch_data_ae = batch_data_ae.sort_values(by='DATE TIME')
        batch_data_ae = batch_data_ae.reset_index(drop=True)
        import ast
        batch_data_ae['Step 6 Idxs'] = batch_data_ae['Step 6 Idxs'].apply(ast.literal_eval)
        batch_data_ae['Step 7 Idxs'] = batch_data_ae['Step 7 Idxs'].apply(ast.literal_eval)
        batch_data_ae['Step 8 Idxs'] = batch_data_ae['Step 8 Idxs'].apply(ast.literal_eval)
        batch_data_ae['Step 9 Idxs'] = batch_data_ae['Step 9 Idxs'].apply(ast.literal_eval)
        batch_data_ae['Step 10 Idxs'] = batch_data_ae['Step 10 Idxs'].apply(ast.literal_eval)
        batch_data_ae['Idxs']=[[item] for item in idxs_ae]
        batch_data_ae['DATE TIME']=batch_data_ae['DATE TIME'].astype(str)
        idxs_ae=np.array(batch_data_ae["Idxs"])
        rec_idxs=np.array(batch_data_ae["Recipe Idxs"])
        recipe=np.array(batch_data_ae["Recipe"])
        v_irr=np.array(batch_data_ae["V Irregulars"])
        arc_irr=np.array(batch_data_ae["Bias Arc Irregulars"])
        c1_irr=np.array(batch_data_ae["I1 Irregulars"])
        c2_irr=np.array(batch_data_ae["I2 Irregulars"])
        c3_irr=np.array(batch_data_ae["I3 Irregulars"])
        g_irr=np.array(batch_data_ae["Ar Gas Irregulars"])
        v_total=np.array(batch_data_ae["V total"])
        c1_total=np.array(batch_data_ae["I1 total"])
        c2_total=np.array(batch_data_ae["I2 total"])
        c3_total=np.array(batch_data_ae["I3 total"])
        g_total=np.array(batch_data_ae["Ar Gas total"])
        arc_total=np.array(batch_data_ae["Arc total"])
        df2_ae =io_data_ae
        new_header = df2_ae.iloc[0]
        in_df = df2_ae[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        print(batch_data_ae)
        columns_to_select = ["DATE TIME","BATCH ID", "Idxs","Recipe","Recipe Idxs","V Irregulars","Bias Arc Irregulars","I1 Irregulars","I2 Irregulars","I3 Irregulars","Ar Gas Irregulars","V total","I1 total","I2 total","I3 total","Arc total","Ar Gas total"]
        merged_df_ae = pd.merge(batch_data_ae,in_df, on="BATCH ID", how="inner")
        merged_df_ae=merged_df_ae[merged_df_ae["PROCESS TYPE"]=='Coating']
        merged_df_ae.reset_index(drop=True, inplace=True)
        import json
        for i in range(len(merged_df_ae)):
            s=merged_df_ae["INTERVENSIONS"][i]
            d = json.loads(s)
            if "Yes" in d.values():
                merged_df_ae["INTERVENSIONS"][i]=d
            else:
                merged_df_ae["INTERVENSIONS"][i]=None

        for i in range(len(merged_df_ae)):
            merged_df_ae['NI PLATING DATE TIME'][i]=str(merged_df_ae['NI PLATING DATE TIME'][i])
            merged_df_ae['BATCH START TIME'][i]=str(merged_df_ae['BATCH START TIME'][i])
            merged_df_ae['BATCH END TIME'][i]=str(merged_df_ae['BATCH END TIME'][i])
        for i in range(len(merged_df_ae)):
            if "-" in merged_df_ae['NI PLATING DATE TIME'][i]:
                string=merged_df_ae['NI PLATING DATE TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ae['NI PLATING DATE TIME'][i]=string2
        for i in range(len(merged_df_ae)):
            if "-" in merged_df_ae['BATCH START TIME'][i]:
                string=merged_df_ae['BATCH START TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ae['BATCH START TIME'][i]=string2
        for i in range(len(merged_df_ae)):
            if "-" in merged_df_ae['BATCH END TIME'][i]:
                string=merged_df_ae['BATCH END TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ae['BATCH END TIME'][i]=string2
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_ae['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_ae['NI PLATING DATE TIME'][i],merged_df_ae['BATCH START TIME'][i])])
        merged_df_ae["Ni_plating_diff"]=Ni_plating_diff
        #merged_df_ae.to_excel("IO 37 batches merged.xlsx")
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_ae['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_ae['NI PLATING DATE TIME'][i],merged_df_ae['BATCH START TIME'][i])])
        
        global refined_df_ae
        refined_df_ae=merged_df_ae


        last_index_old_df_ae = df_ae_old.index[-1] if not df_ae_old.empty else -1  # Handles empty old_df case
        new_start_index = last_index_old_df_ae + 1
        columns_to_select = ["Idxs","Step 6 Idxs","Step 7 Idxs","Step 8 Idxs","Step 9 Idxs","Step 10 Idxs"]
        for col in columns_to_select:
            for i in range(len(refined_df_ae)):
                for j in range(len(refined_df_ae[col][i])):
                    #print(refined_df_ae[col][i][j])
                    refined_df_ae[col][i][j][0]=refined_df_ae[col][i][j][0]+new_start_index
                    refined_df_ae[col][i][j][1]=refined_df_ae[col][i][j][1]+new_start_index

        df_ae_old = pd.concat([df_ae_old, df_ae], ignore_index=True)
        refined_df_ae_old = pd.concat([refined_df_ae_old, refined_df_ae], ignore_index=True)
    df_ae=df_ae_old
    refined_df_ae=refined_df_ae_old
    refined_df_ae=refined_df_ae.drop_duplicates(subset=['BATCH ID'])
    refined_df_ae.reset_index(drop=True, inplace=True)
    #df_ae.to_pickle('df_ae.pkl')
    #refined_df_ae.to_pickle('refined_df_ae.pkl')
    a=refined_df_ae
    a['BATCH START TIME']=pd.to_datetime(a['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    a = a.sort_values(by='BATCH START TIME')
    a = a.reset_index(drop=True)
    start=pd.to_datetime(a['BATCH START TIME'][0], format='%d/%m/%Y %H:%M:%S')
    stop=pd.to_datetime(a['BATCH START TIME'][len(refined_df_ae)-1], format='%d/%m/%Y %H:%M:%S')
    st.session_state.start_date_ae = start
    st.session_state.end_date_ae = stop

    st.session_state.df_ae =df_ae
    #st.session_state.batch_data_ae=batch_data_ae
    st.session_state.refined_df_ae=refined_df_ae
    
    #st.session_state.idxs_ae =idxs_ae
  
    st.session_state.complete_refined_df_ae=refined_df_ae
    golden_index_ae = 32
    golden_batch_ae=refined_df_ae['BATCH ID'][golden_index_ae]
    golden_ae_details=refined_df_ae.iloc[golden_index_ae]
    golden_ae_process=df_ae[refined_df_ae['Recipe Idxs'][golden_index_ae][0]:refined_df_ae['Recipe Idxs'][golden_index_ae][1]]
    st.session_state.golden_batch_ae=golden_batch_ae
    st.session_state.golden_index_ae=golden_index_ae
    st.session_state.golden_ae_details=golden_ae_details
    st.session_state.golden_ae_process=golden_ae_process
    region_selections_ae = [True, False, False, False,False,False, False, False,"All"]
    change_date_ae(st.session_state.start_date_ae,st.session_state.end_date_ae,region_selections_ae)
def compute_ps(add_data,process_data_ps,io_data_ps):
    global df_ps
    df_ps_old=pd.read_pickle('df_ps.pkl')
    refined_df_ps_old=pd.read_pickle('refined_df_ps.pkl')
    import ast  
    if add_data==True:
        df_ps = process_data_ps
        a=np.array(df_ps['DATE TIME'] )
        for i in range(len(a)):
            a[i]=str(a[i])
        df_ps['DATE TIME'] = a
        startendtime=[]
        idxs_ps=[]
        a=np.array(df_ps['BATCH ID'])
        startendtime.append([a[0], a[0],0])
        idxs_ps.append(0)
        for i in range(1,len(df_ps)):
            if a[i]!=a[i]:
                continue
            elif i==(len(df_ps)-1):
                startendtime.append([a[i], a[i],i])
                idxs_ps.append(i)
            elif a[i]==a[i-1]:
                continue
            else:
                startendtime.append([a[i-1], a[i-1],i-1])
                startendtime.append([a[i], a[i],i])
                idxs_ps.append(i-1)
                idxs_ps.append(i)
        idxs_ps=list_to_matrix(idxs_ps,2)
        for i in idxs_ps:
            if i[0]==i[1]:
                idxs_ps.remove(i)
        drops=[]
        for i in range(len(idxs_ps)):
            if abs(int(str(df_ps['DATE TIME'][idxs_ps[i][1]])[11:13])-int(str(df_ps['DATE TIME'][idxs_ps[i][0]])[11:13]))>2:
                drops.append(i)
        idxs_ps = [item for idx, item in enumerate(idxs_ps) if idx not in drops]
        for i in range(len(df_ps)):
            if df_ps['MFP1 POWER ACTUAL'][i]>100:
                df_ps['MFP1 POWER ACTUAL'][i]=df_ps['MFP1 POWER ACTUAL'][i]/100
            if df_ps['MFP2 POWER ACTUAL'][i]>100:
                df_ps['MFP2 POWER ACTUAL'][i]=df_ps['MFP2 POWER ACTUAL'][i]/100
        v_total=[]
        for i in idxs_ps:
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ps['BIAS VOLTAGE ACTUAL'][j]
                check.append(i)
            v_total.append(tot) 
        v_irr=[]
        for i in range(len(v_total)):
            if v_total[i]>=26000 or v_total[i]<=24000:
                v_irr.append(True)
            else:
                v_irr.append(False)
        arc_count=[]
        for i in range(len(idxs_ps)):
            count=[]
            for j in range(idxs_ps[i][0],idxs_ps[i][1]):
                if df_ps["BIAS ARC COUNT"][j]==1:
                    count.append(1)
            arc_count.append(len(count))
        arc_irr=[]
        for i in range(len(arc_count)):
            if arc_count[i]==0:
                arc_irr.append(False)
            else:
                arc_irr.append(True)
        mfp1_total=[]
        for j,i in enumerate(idxs_ps):    
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ps['MFP1 POWER ACTUAL'][j]
                check.append(i)
            mfp1_total.append(tot)
        mfp2_total=[]
        for j,i in enumerate(idxs_ps):    
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ps['MFP2 POWER ACTUAL'][j]
                check.append(i)
            mfp2_total.append(tot)
        mfp1_irr=[]
        for i in range(len(mfp1_total)):
            if mfp1_total[i]<250 or mfp1_total[i]>350 :
                mfp1_irr.append(True)
            else:
                mfp1_irr.append(False)
        mfp2_irr=[]
        for i in range(len(mfp2_total)):
            if mfp2_total[i]<250 or mfp2_total[i]>350 :
                mfp2_irr.append(True)
            else:
                mfp2_irr.append(False)
        g_total=[]
        for i in idxs_ps:
            tot=0
            check=[]
            for j in range(i[0]+3,i[1]):
                tot+=df_ps['AR GAS ACTUAL'][j]
                check.append(i)
            g_total.append(tot) 
        g_irr=[]
        for i in range(len(g_total)):
            if g_total[i]>22000 or g_total[i]<20000:
                g_irr.append(True)
            else:
                g_irr.append(False)
        step_dict={"11":[],"12":[],"13":[]}
        for key in step_dict.keys():
            id_list=[]
            for i in range(len(idxs_ps)):
                temp=[]
                for j in range(idxs_ps[i][0],idxs_ps[i][1]+1):
                    if df_ps["ACTUAL STEP NO"][j]==int(key):
                        temp.append(j)
                temp=remove_solo_values(temp)

                state=0
                for i in range(1,len(temp)):
                    if temp[i]-temp[i-1]>1:
                        state=i
                        break
                    else:
                        pass
                if state==0:
                    if temp==[]:
                        id_list.append([[idxs_ps[i][0],idxs_ps[i][0]+2]])
                    else:
                        id_list.append([[temp[0],temp[len(temp)-1]]])
                elif state==i:
                    if temp[len(temp)-1]==temp[i]:
                        id_list.append([[temp[0],temp[len(temp)-1]]])
                    else:
                        id_list.append([[temp[0],temp[i-1]],[temp[i],temp[len(temp)-1]]])
            step_dict[key]=id_list
        step_v_total={"11":[],"12":[],"13":[]}
        for l in step_v_total.keys():
            for k in step_dict[l]:   
                tot=0
                for j,i in enumerate(k):
                    for j in range(i[0],i[1]):
                        tot+=df_ps['BIAS VOLTAGE ACTUAL'][j]
                step_v_total[l].append(tot)  
        step_v_irr={"11":[],"12":[],"13":[]}
        from scipy import stats as stat
        for l in step_v_total.keys():
            for i in range(len(step_v_total[l])):
                temp = [step_v_total[l][m] for m in range(len(step_v_total[l]))]
                if step_v_total[l][i]<np.median(temp)-2*np.std(temp) or step_v_total[l][i]>np.median(temp)+2*np.std(temp):
                    step_v_irr[l].append(True)
                else:
                    step_v_irr[l].append(False)
        step_mfp_total={"1":{},"2":{}}
        for m in step_mfp_total.keys():
            step_mfp_total[m]={"11":[],"12":[],"13":[]}
            for l in step_mfp_total[m].keys():
                str1='MFP'+str(m)+" POWER ACTUAL"
                for k in step_dict[l]:   
                    tot=0
                    for j,i in enumerate(k):
                        for j in range(i[0],i[1]):
                            tot+=df_ps[str1][j]
                    step_mfp_total[m][l].append(tot)  
        step_mfp_irr={"1":{},"2":{}}
        for m in step_mfp_irr.keys():
            step_mfp_irr[m]={"11":[],"12":[],"13":[]}
            for l in step_mfp_irr[m].keys():
                for i in range(len(step_mfp_total[m][l])):
                    temp = [step_mfp_total[m][l][n] for n in range(len(step_mfp_total[m][l]))]
                    if step_mfp_total[m][l][i]<np.median(temp)-2*np.std(temp) or step_mfp_total[m][l][i]>np.median(temp)+2*np.std(temp):
                        step_mfp_irr[m][l].append(True)
                    else:
                        step_mfp_irr[m][l].append(False)
        step_arc_count={"11":[],"12":[],"13":[]}
        for l in step_arc_count.keys():
            for k in step_dict[l]:   
                count=[]
                for j,i in enumerate(k):
                    for j in range(i[0],i[1]):
                        if df_ps["BIAS ARC COUNT"][j]==1:
                            count.append(1)
                step_arc_count[l].append(len(count))
        step_arc_irr={"11":[],"12":[],"13":[]}
        for l in step_arc_irr.keys():
            for i in range(len(step_arc_count[l])):
                if step_arc_count[l][i]==0:
                    step_arc_irr[l].append(False)
                else:
                    step_arc_irr[l].append(True)
        step_g_total={"11":[],"12":[],"13":[]}
        for l in step_g_total.keys():
            for k in step_dict[l]:   
                tot=0
                for j,i in enumerate(k):  
                    for j in range(i[0],i[1]):
                        tot+=df_ps['AR GAS ACTUAL'][j]
                step_g_total[l].append(tot)  
        step_g_irr={"11":[],"12":[],"13":[]}
        for l in step_g_total.keys():
            for i in range(len(step_g_total[l])):
                temp = [step_g_total[l][m] for m in range(len(step_g_total[l]))]
                if step_g_total[l][i]<np.median(temp)-2*np.std(temp) or step_g_total[l][i]>np.median(temp)+2*np.std(temp):
                    step_g_irr[l].append(True)
                else:
                    step_g_irr[l].append(False)
        a=np.array(df_ps['DATE TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        a=np.array(df_ps['DATE TIME'])
        column_headers = ["DATE TIME", "BATCH ID", "Idxs", "V Irregulars", 
                    "Bias Arc Irregulars", "MFP1 Irregulars", "MFP2 Irregulars", 
                    "Ar Gas Irregulars", "V total", "MFP1 total", "MFP2 total",
                    "Arc total", "Ar Gas total"]
        # List of columns to repeat for each step
        step_columns = ["V Irregulars", "Bias Arc Irregulars", "MFP1 Irregulars", "MFP2 Irregulars", 
                        "Ar Gas Irregulars", "V total", "MFP1 total", "MFP2 total", 
                        "Arc total", "Ar Gas total"]

        steps = range(11, 14)  

        # New column headers list that will store the expanded column names
        expanded_column_headers = column_headers[:2]  # Keep first four columns unchanged

        # Add step-specific columns for Recipe Idxs
        for step in steps:
            expanded_column_headers.append(f"Step {step} Idxs")

        # Add step-specific columns for other step columns
        for step in steps:
            for col in step_columns:
                expanded_column_headers.append(f"Step {step} {col}")
        step_keys = ["11", "12", "13"]
        batch_data_ps=pd.DataFrame(columns=column_headers)
        for i in range(len(idxs_ps)):
            batch_data_ps.loc[i, 'DATE TIME'] = df_ps['DATE TIME'][idxs_ps[i][0]+1]
            batch_data_ps.loc[i, 'BATCH ID'] = df_ps['BATCH ID'][idxs_ps[i][0]+3]
            batch_data_ps.at[i, 'Idxs'] = idxs_ps[i]
            batch_data_ps.loc[i, 'V Irregulars'] = v_irr[i]
            batch_data_ps.loc[i, 'Bias Arc Irregulars'] = arc_irr[i]
            batch_data_ps.loc[i, 'MFP1 Irregulars'] = mfp1_irr[i]
            batch_data_ps.loc[i, 'MFP2 Irregulars'] = mfp2_irr[i]
            batch_data_ps.loc[i, 'Ar Gas Irregulars'] = g_irr[i]
            batch_data_ps.loc[i, 'V total'] = v_total[i]
            batch_data_ps.loc[i, 'MFP1 total'] = mfp1_total[i]
            batch_data_ps.loc[i, 'MFP2 total'] = mfp2_total[i]
            batch_data_ps.loc[i, 'Ar Gas total'] = g_total[i]
            batch_data_ps.loc[i, 'Arc total'] = arc_count[i]
            for step in step_keys:
                # For each step, populate the irregulars and totals
                batch_data_ps.loc[i, f'Step {step} Idxs'] = str(step_dict[step][i])
                batch_data_ps.loc[i, f'Step {step} V total'] = step_v_total[step][i]
                batch_data_ps.loc[i, f'Step {step} Ar Gas total'] = step_g_total[step][i]
                batch_data_ps.loc[i, f'Step {step} Arc total'] = step_arc_count[step][i]  # Assuming you have a dictionary for Arc total

                # Populate the current totals (I1, I2, I3) from step_c_total
                batch_data_ps.loc[i, f'Step {step} MFP1 total'] = step_mfp_total["1"][step][i]
                batch_data_ps.loc[i, f'Step {step} MFP2 total'] = step_mfp_total["2"][step][i]

                # Populate the current irregulars (I1, I2, I3) from step_c_irr
                batch_data_ps.loc[i, f'Step {step} MFP1 Irregulars'] = step_mfp_irr["1"][step][i]
                batch_data_ps.loc[i, f'Step {step} MFP2 Irregulars'] = step_mfp_irr["2"][step][i]

                # Populate other irregulars (V, Bias Arc, Ar Gas) - similar to the totals
                batch_data_ps.loc[i, f'Step {step} V Irregulars'] = step_v_irr[step][i]  # Assuming you have a step_v_irr dictionary
                batch_data_ps.loc[i, f'Step {step} Bias Arc Irregulars'] = step_arc_irr[step][i]  # Assuming a dictionary for Bias Arc Irregulars
                batch_data_ps.loc[i, f'Step {step} Ar Gas Irregulars'] = step_g_irr[step][i]
        batch_data_ps=batch_data_ps.drop_duplicates(subset=['BATCH ID'])
        batch_data_ps.reset_index(drop=True, inplace=True)
        batch_data_ps['DATE TIME']=pd.to_datetime(batch_data_ps['DATE TIME'], format='%d/%m/%Y %H:%M:%S')
        batch_data_ps = batch_data_ps.sort_values(by='DATE TIME')
        batch_data_ps = batch_data_ps.reset_index(drop=True)
        import ast
        batch_data_ps['Step 11 Idxs'] = batch_data_ps['Step 11 Idxs'].apply(ast.literal_eval)
        batch_data_ps['Step 12 Idxs'] = batch_data_ps['Step 12 Idxs'].apply(ast.literal_eval)
        batch_data_ps['Step 13 Idxs'] = batch_data_ps['Step 13 Idxs'].apply(ast.literal_eval)
        batch_data_ps['Idxs']=[[item] for item in idxs_ps]
        batch_data_ps['DATE TIME']=batch_data_ps['DATE TIME'].astype(str)
        idxs_ps=np.array(batch_data_ps["Idxs"])
        v_irr=np.array(batch_data_ps["V Irregulars"])
        arc_irr=np.array(batch_data_ps["Bias Arc Irregulars"])
        mfp1_irr=np.array(batch_data_ps["MFP1 Irregulars"])
        mfp2_irr=np.array(batch_data_ps["MFP2 Irregulars"])
        g_irr=np.array(batch_data_ps["Ar Gas Irregulars"])
        v_total=np.array(batch_data_ps["V total"])
        mfp1_total=np.array(batch_data_ps["MFP1 total"])
        mfp2_total=np.array(batch_data_ps["MFP2 total"])
        g_total=np.array(batch_data_ps["Ar Gas total"])
        arc_total=np.array(batch_data_ps["Arc total"])
        df2_ps =io_data_ps
        new_header = df2_ps.iloc[0]
        in_df = df2_ps[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        merged_df_ps = pd.merge(batch_data_ps,in_df, on="BATCH ID", how="inner")
        merged_df_ps=merged_df_ps[merged_df_ps["PROCESS TYPE"]=='Coating']
        merged_df_ps.reset_index(drop=True, inplace=True)
        import json
        for i in range(len(merged_df_ps)):
            s=merged_df_ps["INTERVENSIONS"][i]
            d = json.loads(s)
            if "Yes" in d.values():
                merged_df_ps["INTERVENSIONS"][i]=d
            else:
                merged_df_ps["INTERVENSIONS"][i]=None

        for i in range(len(merged_df_ps)):
            merged_df_ps['NI PLATING DATE TIME'][i]=str(merged_df_ps['NI PLATING DATE TIME'][i])
            merged_df_ps['BATCH START TIME'][i]=str(merged_df_ps['BATCH START TIME'][i])
            merged_df_ps['BATCH END TIME'][i]=str(merged_df_ps['BATCH END TIME'][i])
        for i in range(len(merged_df_ps)):
            if "-" in merged_df_ps['NI PLATING DATE TIME'][i]:
                string=merged_df_ps['NI PLATING DATE TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ps['NI PLATING DATE TIME'][i]=string2
        for i in range(len(merged_df_ps)):
            if "-" in merged_df_ps['BATCH START TIME'][i]:
                string=merged_df_ps['BATCH START TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ps['BATCH START TIME'][i]=string2
        for i in range(len(merged_df_ps)):
            if "-" in merged_df_ps['BATCH END TIME'][i]:
                string=merged_df_ps['BATCH END TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ps['BATCH END TIME'][i]=string2
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_ps['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_ps['NI PLATING DATE TIME'][i],merged_df_ps['BATCH START TIME'][i])])
        merged_df_ps["Ni_plating_diff"]=Ni_plating_diff
        #merged_df_ps.to_excel("IO 37 batches merged.xlsx")
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_ps['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_ps['NI PLATING DATE TIME'][i],merged_df_ps['BATCH START TIME'][i])])

        global refined_df_ps
        refined_df_ps=merged_df_ps
        last_index_old_df_ps = df_ps_old.index[-1] if not df_ps_old.empty else -1  # Handles empty old_df case
        new_start_index = last_index_old_df_ps + 1
        columns_to_select = ["Idxs","Step 11 Idxs","Step 12 Idxs","Step 13 Idxs"]
        for col in columns_to_select:
            for i in range(len(refined_df_ps)):
                for j in range(len(refined_df_ps[col][i])):
                    #print(refined_df_ps[col][i][j])
                    refined_df_ps[col][i][j][0]=refined_df_ps[col][i][j][0]+new_start_index
                    refined_df_ps[col][i][j][1]=refined_df_ps[col][i][j][1]+new_start_index

        df_ps_old = pd.concat([df_ps_old, df_ps], ignore_index=True)
        refined_df_ps_old = pd.concat([refined_df_ps_old, refined_df_ps], ignore_index=True)
    df_ps=df_ps_old
    refined_df_ps=refined_df_ps_old
    refined_df_ps=refined_df_ps.drop_duplicates(subset=['BATCH ID'])
    refined_df_ps.reset_index(drop=True, inplace=True)
    #df_ps.to_pickle('df_ps.pkl')
    #refined_df_ps.to_pickle('refined_df_ps.pkl')
    a=refined_df_ps
    a['BATCH START TIME']=pd.to_datetime(a['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    a = a.sort_values(by='BATCH START TIME')
    a = a.reset_index(drop=True)
    start=pd.to_datetime(a['BATCH START TIME'][0], format='%d/%m/%Y %H:%M:%S')
    stop=pd.to_datetime(a['BATCH START TIME'][len(refined_df_ps)-1], format='%d/%m/%Y %H:%M:%S')
    st.session_state.start_date_ps = start
    st.session_state.end_date_ps = stop
    print("Start date:", start)
    print("Stop date:", stop)

    st.session_state.df_ps =df_ps
    #st.session_state.batch_data_ps=batch_data_ps
    st.session_state.refined_df_ps=refined_df_ps
    
    #st.session_state.idxs_ps =idxs_ps
  
    st.session_state.complete_refined_df_ps=refined_df_ps
    golden_index_ps = 3
    golden_batch_ps=refined_df_ps['BATCH ID'][golden_index_ps]
    golden_ps_details=refined_df_ps.iloc[golden_index_ps]
    golden_ps_process=df_ps[refined_df_ps['Idxs'][golden_index_ps][0][0]:refined_df_ps['Idxs'][golden_index_ps][0][1]]
    st.session_state.golden_batch_ps=golden_batch_ps
    st.session_state.golden_index_ps=golden_index_ps
    st.session_state.golden_ps_details=golden_ps_details
    st.session_state.golden_ps_process=golden_ps_process
    region_selections_ps = ["All Batches", False,False,False, False, False,"All"]
    change_date_ps(st.session_state.start_date_ps,st.session_state.end_date_ps,region_selections_ps)
def compute_ti(add_data,process_data_ti,io_data_ti):
    global df_ti
    df_ti_old=pd.read_pickle('df_ti.pkl')
    refined_df_ti_old=pd.read_pickle('refined_df_ti.pkl')
    import ast  
    if add_data==True:
        df_ti = process_data_ti
        a=np.array(df_ti['DATE TIME'] )
        for i in range(len(a)):
            a[i]=str(a[i])
        df_ti['DATE TIME'] = a
        startendtime=[]
        idxs_ti=[]
        a=np.array(df_ti['BATCH ID'])
        startendtime.append([a[0], a[0],0])
        idxs_ti.append(0)
        for i in range(1,len(df_ti)):
            if a[i]!=a[i]:
                continue
            elif i==(len(df_ti)-1):
                startendtime.append([a[i], a[i],i])
                idxs_ti.append(i)
            elif a[i]==a[i-1]:
                continue
            else:
                startendtime.append([a[i-1], a[i-1],i-1])
                startendtime.append([a[i], a[i],i])
                idxs_ti.append(i-1)
                idxs_ti.append(i)
        idxs_ti=list_to_matrix(idxs_ti,2)
        for i in idxs_ti:
            if i[0]==i[1]:
                idxs_ti.remove(i)
        drops=[]
        for i in range(len(idxs_ti)):
            if abs(int(str(df_ti['DATE TIME'][idxs_ti[i][1]])[11:13])-int(str(df_ti['DATE TIME'][idxs_ti[i][0]])[11:13]))>2:
                drops.append(i)
        idxs_ti = [item for idx, item in enumerate(idxs_ti) if idx not in drops]
        for i in range(len(df_ti)):
            if df_ti['MFP1 POWER ACTUAL'][i]>100:
                df_ti['MFP1 POWER ACTUAL'][i]=df_ti['MFP1 POWER ACTUAL'][i]/100
            if df_ti['MFP2 POWER ACTUAL'][i]>100:
                df_ti['MFP2 POWER ACTUAL'][i]=df_ti['MFP2 POWER ACTUAL'][i]/100
        v_total=[]
        for i in idxs_ti:
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ti['BIAS VOLTAGE ACTUAL'][j]
                check.append(i)
            v_total.append(tot) 
        v_irr=[]
        for i in range(len(v_total)):
            if v_total[i]>=9000 or v_total[i]<=7000:
                v_irr.append(True)
            else:
                v_irr.append(False)
        arc_count=[]
        for i in range(len(idxs_ti)):
            count=[]
            for j in range(idxs_ti[i][0],idxs_ti[i][1]):
                if df_ti["BIAS ARC COUNT"][j]==1:
                    count.append(1)
            arc_count.append(len(count))
        arc_irr=[]
        for i in range(len(arc_count)):
            if arc_count[i]==0:
                arc_irr.append(False)
            else:
                arc_irr.append(True)
        mfp1_total=[]
        for j,i in enumerate(idxs_ti):    
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ti['MFP1 POWER ACTUAL'][j]
                check.append(i)
            mfp1_total.append(tot)
        mfp2_total=[]
        for j,i in enumerate(idxs_ti):    
            tot=0
            check=[]
            for j in range(i[0],i[1]):
                tot+=df_ti['MFP2 POWER ACTUAL'][j]
                check.append(i)
            mfp2_total.append(tot)
        mfp1_irr=[]
        for i in range(len(mfp1_total)):
            if mfp1_total[i]<500 or mfp1_total[i]>700 :
                mfp1_irr.append(True)
            else:
                mfp1_irr.append(False)
        mfp2_irr=[]
        for i in range(len(mfp2_total)):
            if mfp2_total[i]<600 or mfp2_total[i]>800 :
                mfp2_irr.append(True)
            else:
                mfp2_irr.append(False)
        g_total=[]
        for i in idxs_ti:
            tot=0
            check=[]
            for j in range(i[0]+3,i[1]):
                tot+=df_ti['AR GAS ACTUAL'][j]
                check.append(i)
            g_total.append(tot) 
        g_irr=[]
        for i in range(len(g_total)):
            if g_total[i]>22000 or g_total[i]<19000:
                g_irr.append(True)
            else:
                g_irr.append(False)
        a=np.array(df_ti['DATE TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        a=np.array(df_ti['DATE TIME'])
        column_headers = ["DATE TIME", "BATCH ID", "Idxs", "V Irregulars", 
                    "Bias Arc Irregulars", "MFP1 Irregulars", "MFP2 Irregulars", 
                    "Ar Gas Irregulars", "V total", "MFP1 total", "MFP2 total",
                    "Arc total", "Ar Gas total"]
        batch_data_ti=pd.DataFrame(columns=column_headers)

        for i in range(len(idxs_ti)):
            batch_data_ti.loc[i, 'DATE TIME'] = df_ti['DATE TIME'][idxs_ti[i][0]+1]
            batch_data_ti.loc[i, 'BATCH ID'] = df_ti['BATCH ID'][idxs_ti[i][0]+3]
            batch_data_ti.at[i, 'Idxs'] = idxs_ti[i]
            batch_data_ti.loc[i, 'V Irregulars'] = v_irr[i]
            batch_data_ti.loc[i, 'Bias Arc Irregulars'] = arc_irr[i]
            batch_data_ti.loc[i, 'MFP1 Irregulars'] = mfp1_irr[i]
            batch_data_ti.loc[i, 'MFP2 Irregulars'] = mfp2_irr[i]
            batch_data_ti.loc[i, 'Ar Gas Irregulars'] = g_irr[i]
            batch_data_ti.loc[i, 'V total'] = v_total[i]
            batch_data_ti.loc[i, 'MFP1 total'] = mfp1_total[i]
            batch_data_ti.loc[i, 'MFP2 total'] = mfp2_total[i]
            batch_data_ti.loc[i, 'Ar Gas total'] = g_total[i]
            batch_data_ti.loc[i, 'Arc total'] = arc_count[i]
        batch_data_ti=batch_data_ti.drop_duplicates(subset=['BATCH ID'])
        batch_data_ti.reset_index(drop=True, inplace=True)
        batch_data_ti['DATE TIME']=pd.to_datetime(batch_data_ti['DATE TIME'], format='%d/%m/%Y %H:%M:%S')
        batch_data_ti = batch_data_ti.sort_values(by='DATE TIME')
        batch_data_ti = batch_data_ti.reset_index(drop=True)
        batch_data_ti['Idxs']=[[item] for item in idxs_ti]
        batch_data_ti['DATE TIME']=batch_data_ti['DATE TIME'].astype(str)
        idxs_ti=np.array(batch_data_ti["Idxs"])
        v_irr=np.array(batch_data_ti["V Irregulars"])
        arc_irr=np.array(batch_data_ti["Bias Arc Irregulars"])
        mfp1_irr=np.array(batch_data_ti["MFP1 Irregulars"])
        mfp2_irr=np.array(batch_data_ti["MFP2 Irregulars"])
        g_irr=np.array(batch_data_ti["Ar Gas Irregulars"])
        v_total=np.array(batch_data_ti["V total"])
        mfp1_total=np.array(batch_data_ti["MFP1 total"])
        mfp2_total=np.array(batch_data_ti["MFP2 total"])
        g_total=np.array(batch_data_ti["Ar Gas total"])
        arc_total=np.array(batch_data_ti["Arc total"])
        df2_ti =io_data_ti
        new_header = df2_ti.iloc[0]
        in_df = df2_ti[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        merged_df_ti = pd.merge(batch_data_ti,in_df, on="BATCH ID", how="inner")
        merged_df_ti=merged_df_ti[merged_df_ti["PROCESS TYPE"]=='Coating']
        merged_df_ti.reset_index(drop=True, inplace=True)
        import json
        for i in range(len(merged_df_ti)):
            s=merged_df_ti["INTERVENSIONS"][i]
            d = json.loads(s)
            if "Yes" in d.values():
                merged_df_ti["INTERVENSIONS"][i]=d
            else:
                merged_df_ti["INTERVENSIONS"][i]=None

        for i in range(len(merged_df_ti)):
            merged_df_ti['NI PLATING DATE TIME'][i]=str(merged_df_ti['NI PLATING DATE TIME'][i])
            merged_df_ti['BATCH START TIME'][i]=str(merged_df_ti['BATCH START TIME'][i])
            merged_df_ti['BATCH END TIME'][i]=str(merged_df_ti['BATCH END TIME'][i])
        for i in range(len(merged_df_ti)):
            if "-" in merged_df_ti['NI PLATING DATE TIME'][i]:
                string=merged_df_ti['NI PLATING DATE TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ti['NI PLATING DATE TIME'][i]=string2
        for i in range(len(merged_df_ti)):
            if "-" in merged_df_ti['BATCH START TIME'][i]:
                string=merged_df_ti['BATCH START TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ti['BATCH START TIME'][i]=string2
        for i in range(len(merged_df_ti)):
            if "-" in merged_df_ti['BATCH END TIME'][i]:
                string=merged_df_ti['BATCH END TIME'][i].replace("-","/")
                string2=string.split(" ")
                string2[0]=string2[0].split("/")
                string2[0][0],string2[0][1],string2[0][2]=string2[0][1],string2[0][2],string2[0][0]
                string2 = f"{string2[0][2]}/{string2[0][0]}/{string2[0][1]} {string2[1]}"+":00"
                merged_df_ti['BATCH END TIME'][i]=string2
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_ti['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_ti['NI PLATING DATE TIME'][i],merged_df_ti['BATCH START TIME'][i])])
        merged_df_ti["Ni_plating_diff"]=Ni_plating_diff
        #merged_df_ti.to_excel("IO 37 batches merged.xlsx")
        Ni_plating_diff=[]
        for i in range(0,len(merged_df_ti['NI PLATING DATE TIME'])):
            Ni_plating_diff.append([calculate_time_difference(merged_df_ti['NI PLATING DATE TIME'][i],merged_df_ti['BATCH START TIME'][i])])

        global refined_df_ti
        refined_df_ti=merged_df_ti
        last_index_old_df_ti = df_ti_old.index[-1] if not df_ti_old.empty else -1  # Handles empty old_df case
        new_start_index = last_index_old_df_ti + 1
        columns_to_select = ["Idxs"]
        for col in columns_to_select:
            for i in range(len(refined_df_ti)):
                for j in range(len(refined_df_ti[col][i])):
                    #print(refined_df_ti[col][i][j])
                    refined_df_ti[col][i][j][0]=refined_df_ti[col][i][j][0]+new_start_index
                    refined_df_ti[col][i][j][1]=refined_df_ti[col][i][j][1]+new_start_index

        df_ti_old = pd.concat([df_ti_old, df_ti], ignore_index=True)
        refined_df_ti_old = pd.concat([refined_df_ti_old, refined_df_ti], ignore_index=True)

    df_ti=df_ti_old
    refined_df_ti=refined_df_ti_old
    refined_df_ti=refined_df_ti.drop_duplicates(subset=['BATCH ID'])
    refined_df_ti.reset_index(drop=True, inplace=True)
    #df_ti.to_pickle('df_ti.pkl')
    #refined_df_ti.to_pickle('refined_df_ti.pkl')
    a=refined_df_ti
    a['BATCH START TIME']=pd.to_datetime(a['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    a = a.sort_values(by='BATCH START TIME')
    a = a.reset_index(drop=True)
    start=pd.to_datetime(a['BATCH START TIME'][0], format='%d/%m/%Y %H:%M:%S')
    stop=pd.to_datetime(a['BATCH START TIME'][len(refined_df_ti)-1], format='%d/%m/%Y %H:%M:%S')
    st.session_state.start_date_ti = start
    st.session_state.end_date_ti = stop
    print("Start date:", start)
    print("Stop date:", stop)

    st.session_state.df_ti =df_ti
    #st.session_state.batch_data_ti=batch_data_ti
    st.session_state.refined_df_ti=refined_df_ti
    
    #st.session_state.idxs_ti =idxs_ti
  
    st.session_state.complete_refined_df_ti=refined_df_ti
    golden_index_ti = 30
    golden_batch_ti=refined_df_ti['BATCH ID'][golden_index_ti]
    golden_ti_details=refined_df_ti.iloc[golden_index_ti]
    golden_ti_process=df_ti[refined_df_ti['Idxs'][golden_index_ti][0][0]:refined_df_ti['Idxs'][golden_index_ti][0][1]]
    st.session_state.golden_batch_ti=golden_batch_ti
    st.session_state.golden_index_ti=golden_index_ti
    st.session_state.golden_ti_details=golden_ti_details
    st.session_state.golden_ti_process=golden_ti_process
    region_selections_ti = ["All Batches", False,False,False, False, False]
    change_date_ti(st.session_state.start_date_ti,st.session_state.end_date_ti,region_selections_ti)
def change_date_ti(start_date_ti,end_date_ti,region_selections_ti):
    refined_df_ti=st.session_state.complete_refined_df_ti
    st.session_state.start_date_ti=start_date_ti
    st.session_state.end_date_ti=end_date_ti
    st.session_state.region_selections_ti=region_selections_ti
    complete_refined_df_ti=st.session_state.complete_refined_df_ti
    if type(refined_df_ti['BATCH START TIME'][0])!=str:
        refined_df_ti['BATCH START TIME']=refined_df_ti['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
        refined_df_ti['BATCH START TIME']=refined_df_ti['BATCH START TIME'].astype(str)
        a=np.array(refined_df_ti['BATCH START TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        refined_df_ti['BATCH START TIME']=a
    Ni_plating_diff=[]
    for i in range(0,len(refined_df_ti['NI PLATING DATE TIME'])):
        Ni_plating_diff.append([calculate_time_difference(refined_df_ti['NI PLATING DATE TIME'][i],refined_df_ti['BATCH START TIME'][i])])
    ni_hrs=[]
    for i in range(len(refined_df_ti)):
        ni_hrs.append(Ni_plating_diff[i][0][0]*24+Ni_plating_diff[i][0][1]+Ni_plating_diff[i][0][2]/60+Ni_plating_diff[i][0][3]/3600)
    shift_type_ti=[]
    for i in range(len(refined_df_ti)):
        if int(refined_df_ti['BATCH START TIME'][i][11:13])<6 or int(refined_df_ti['BATCH START TIME'][i][11:13])>=23:
            shift_type_ti.append("Shift 3")
        elif int(refined_df_ti['BATCH START TIME'][i][11:13])<15 and int(refined_df_ti['BATCH START TIME'][i][11:13])>=6:
            if refined_df_ti['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_ti['BATCH START TIME'][i][14:16])<=30:
                    shift_type_ti.append("Shift 1")
                else:
                    pass
            else:
                shift_type_ti.append("Shift 1")
        elif int(refined_df_ti['BATCH START TIME'][i][11:13])<23 and int(refined_df_ti['BATCH START TIME'][i][11:13])>=14 :
            if refined_df_ti['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_ti['BATCH START TIME'][i][14:16])>30:
                    shift_type_ti.append("Shift 2")
                else:
                    pass
            else:
                shift_type_ti.append("Shift 2")
    refined_df_ti['SHIFT TYPE']=shift_type_ti 
    refined_df_ti['Ni hours']=ni_hrs

    refined_df_ti['BATCH START TIME']=pd.to_datetime(refined_df_ti['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    refined_df_ti = refined_df_ti.sort_values(by='BATCH START TIME')
    refined_df_ti = refined_df_ti.reset_index(drop=True)
    filtered_df = refined_df_ti[(refined_df_ti["BATCH START TIME"] >= start_date_ti) & (refined_df_ti["BATCH START TIME"] <= end_date_ti)]
    filtered_df=filtered_df.reset_index(drop=True)
    comb_df=pd.DataFrame()

    if region_selections_ti[0]=='All Batches':
        pass
    elif region_selections_ti[0]=='Irregular Batches':
        if region_selections_ti[1]==True:
            filtered_df=filtered_df[filtered_df["V Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ti[2]==True:
            filtered_df=filtered_df[filtered_df["Bias Arc Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ti[3]==True:
            filtered_df=filtered_df[filtered_df["MFP1 Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ti[4]==True:
            filtered_df=filtered_df[filtered_df["MFP2 Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ti[5]==True:
            filtered_df=filtered_df[filtered_df["Ar Gas Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)

    elif region_selections_ti[0]=='Good Batches':
        if region_selections_ti[1]==True:
            filtered_df=filtered_df[filtered_df["V Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ti[2]==True:
            filtered_df=filtered_df[filtered_df["Bias Arc Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ti[3]==True:
            filtered_df=filtered_df[filtered_df["MFP1 Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ti[4]==True:
            filtered_df=filtered_df[filtered_df["MFP2 Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ti[5]==True:
            filtered_df=filtered_df[filtered_df["Ar Gas Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)

    refined_df_ti = filtered_df.sort_values(by='BATCH START TIME')
    refined_df_ti['BATCH START TIME']=refined_df_ti['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
    refined_df_ti['BATCH START TIME']=refined_df_ti['BATCH START TIME'].astype(str)
    a=np.array(refined_df_ti['BATCH START TIME'])
    for i in range(len(a)):
        if "-" in a[i]:
            a[i]=str(a[i].replace("-","/"))
        if ":" in a[i]:
            tot=0
            for j in a[i]:
                if j==":":
                    tot+=1
            if tot==1:
                a[i]=str(a[i]+":00")
    refined_df_ti['BATCH START TIME']=a
    product_dict=[]
    import json
    for i in range(len(refined_df_ti)):
        product_dict.append(json.loads(refined_df_ti["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt
    pt={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(refined_df_ti.iloc[i][:])
        pt[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(refined_df_ti.iloc[i][:])
    pt["mix"]=pd.DataFrame(mix_series)
    global mt
    mt={}
    ss_series=[]
    brass_series=[]
    for i in range(len(refined_df_ti)):
        if refined_df_ti['MATERIAL TYPE'][i]=="SS":
            ss_series.append(refined_df_ti.iloc[i][:])
        elif refined_df_ti['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(refined_df_ti.iloc[i][:])
    mt["ss"]=pd.DataFrame(ss_series)
    mt["brass"]=pd.DataFrame(brass_series)
    product_dict=[]
    import json
    for i in range(len(complete_refined_df_ti)):
        product_dict.append(json.loads(complete_refined_df_ti["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt_full
    pt_full={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(complete_refined_df_ti.iloc[i][:])
        pt_full[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(complete_refined_df_ti.iloc[i][:])
    pt_full["mix"]=pd.DataFrame(mix_series)
    global mt_full
    mt_full={}
    ss_series=[]
    brass_series=[]
    for i in range(len(complete_refined_df_ti)):
        if complete_refined_df_ti['MATERIAL TYPE'][i]=="SS":
            ss_series.append(complete_refined_df_ti.iloc[i][:])
        elif complete_refined_df_ti['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(complete_refined_df_ti.iloc[i][:])
    mt_full["ss"]=pd.DataFrame(ss_series)
    mt_full["brass"]=pd.DataFrame(brass_series)
    global nt
    nt={}
    I_series=[]
    II_series=[]
    III_series=[]
    for i in range(len(refined_df_ti)):
        if refined_df_ti['Ni hours'][i]<=2:
            I_series.append(refined_df_ti.iloc[i][:])
        elif refined_df_ti['Ni hours'][i]>2 and refined_df_ti['Ni hours'][i]<=8:
            II_series.append(refined_df_ti.iloc[i][:])
        else:
            III_series.append(refined_df_ti.iloc[i][:])
    nt["I_series"]=pd.DataFrame(I_series)
    nt["II_series"]=pd.DataFrame(II_series)
    nt["III_series"]=pd.DataFrame(III_series)
    #if 'refined_df' in st.session_state:    
        #columns_to_select = ["BATCH ID","RH mins"]    
        #I_ti_df = pd.merge(st.session_state.refined_df[columns_to_select],refined_df_ti, on="BATCH ID", how="inner")
        #st.session_state.I_ti_df=I_ti_df

    st.session_state.pt=pt
    st.session_state.mt=mt
    st.session_state.pt_full=pt_full
    st.session_state.mt_full=mt_full
    st.session_state.nt=nt
    st.session_state.refined_df_ti=refined_df_ti
    if st.session_state.current_page=='dashboard':
        pass
    else:
        st.rerun()
def change_date_ps(start_date_ps,end_date_ps,region_selections_ps):
    refined_df_ps=st.session_state.complete_refined_df_ps
    st.session_state.start_date_ps=start_date_ps
    st.session_state.end_date_ps=end_date_ps
    st.session_state.region_selections_ps=region_selections_ps
    complete_refined_df_ps=st.session_state.complete_refined_df_ps
    if type(refined_df_ps['BATCH START TIME'][0])!=str:
        refined_df_ps['BATCH START TIME']=refined_df_ps['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
        refined_df_ps['BATCH START TIME']=refined_df_ps['BATCH START TIME'].astype(str)
        a=np.array(refined_df_ps['BATCH START TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        refined_df_ps['BATCH START TIME']=a
    Ni_plating_diff=[]
    for i in range(0,len(refined_df_ps['NI PLATING DATE TIME'])):
        Ni_plating_diff.append([calculate_time_difference(refined_df_ps['NI PLATING DATE TIME'][i],refined_df_ps['BATCH START TIME'][i])])
    ni_hrs=[]
    for i in range(len(refined_df_ps)):
        ni_hrs.append(Ni_plating_diff[i][0][0]*24+Ni_plating_diff[i][0][1]+Ni_plating_diff[i][0][2]/60+Ni_plating_diff[i][0][3]/3600)
    shift_type_ps=[]
    for i in range(len(refined_df_ps)):
        if int(refined_df_ps['BATCH START TIME'][i][11:13])<6 or int(refined_df_ps['BATCH START TIME'][i][11:13])>=23:
            shift_type_ps.append("Shift 3")
        elif int(refined_df_ps['BATCH START TIME'][i][11:13])<15 and int(refined_df_ps['BATCH START TIME'][i][11:13])>=6:
            if refined_df_ps['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_ps['BATCH START TIME'][i][14:16])<=30:
                    shift_type_ps.append("Shift 1")
                else:
                    pass
            else:
                shift_type_ps.append("Shift 1")
        elif int(refined_df_ps['BATCH START TIME'][i][11:13])<23 and int(refined_df_ps['BATCH START TIME'][i][11:13])>=14 :
            if refined_df_ps['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_ps['BATCH START TIME'][i][14:16])>30:
                    shift_type_ps.append("Shift 2")
                else:
                    pass
            else:
                shift_type_ps.append("Shift 2")
    refined_df_ps['SHIFT TYPE']=shift_type_ps 
    refined_df_ps['Ni hours']=ni_hrs

    refined_df_ps['BATCH START TIME']=pd.to_datetime(refined_df_ps['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    refined_df_ps = refined_df_ps.sort_values(by='BATCH START TIME')
    refined_df_ps = refined_df_ps.reset_index(drop=True)
    step_columns = ["Idxs", "V Irregulars", "Bias Arc Irregulars", "MFP1 Irregulars", "MFP2 Irregulars", 
                    "Ar Gas Irregulars", "V total", "MFP1 total", "MFP2 total", 
                    "Arc total", "Ar Gas total"]
    if region_selections_ps[6]=="All":
        pass
    else:
        for col in step_columns:
            refined_df_ps[col]=refined_df_ps[f"Step {region_selections_ps[6]} {col}"]
    filtered_df = refined_df_ps[(refined_df_ps["BATCH START TIME"] >= start_date_ps) & (refined_df_ps["BATCH START TIME"] <= end_date_ps)]
    filtered_df=filtered_df.reset_index(drop=True)
    comb_df=pd.DataFrame()

    if region_selections_ps[0]=='All Batches':
        pass
    elif region_selections_ps[0]=='Irregular Batches':
        if region_selections_ps[1]==True:
            filtered_df=filtered_df[filtered_df["V Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ps[2]==True:
            filtered_df=filtered_df[filtered_df["Bias Arc Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ps[3]==True:
            filtered_df=filtered_df[filtered_df["MFP1 Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ps[4]==True:
            filtered_df=filtered_df[filtered_df["MFP2 Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ps[5]==True:
            filtered_df=filtered_df[filtered_df["Ar Gas Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)

    elif region_selections_ps[0]=='Good Batches':
        if region_selections_ps[1]==True:
            filtered_df=filtered_df[filtered_df["V Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ps[2]==True:
            filtered_df=filtered_df[filtered_df["Bias Arc Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ps[3]==True:
            filtered_df=filtered_df[filtered_df["MFP1 Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ps[4]==True:
            filtered_df=filtered_df[filtered_df["MFP2 Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ps[5]==True:
            filtered_df=filtered_df[filtered_df["Ar Gas Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)

    refined_df_ps = filtered_df.sort_values(by='BATCH START TIME')
    refined_df_ps['BATCH START TIME']=refined_df_ps['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
    refined_df_ps['BATCH START TIME']=refined_df_ps['BATCH START TIME'].astype(str)
    a=np.array(refined_df_ps['BATCH START TIME'])
    for i in range(len(a)):
        if "-" in a[i]:
            a[i]=str(a[i].replace("-","/"))
        if ":" in a[i]:
            tot=0
            for j in a[i]:
                if j==":":
                    tot+=1
            if tot==1:
                a[i]=str(a[i]+":00")
    refined_df_ps['BATCH START TIME']=a
    product_dict=[]
    import json
    for i in range(len(refined_df_ps)):
        product_dict.append(json.loads(refined_df_ps["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt
    pt={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(refined_df_ps.iloc[i][:])
        pt[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(refined_df_ps.iloc[i][:])
    pt["mix"]=pd.DataFrame(mix_series)
    global mt
    mt={}
    ss_series=[]
    brass_series=[]
    for i in range(len(refined_df_ps)):
        if refined_df_ps['MATERIAL TYPE'][i]=="SS":
            ss_series.append(refined_df_ps.iloc[i][:])
        elif refined_df_ps['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(refined_df_ps.iloc[i][:])
    mt["ss"]=pd.DataFrame(ss_series)
    mt["brass"]=pd.DataFrame(brass_series)
    product_dict=[]
    import json
    for i in range(len(complete_refined_df_ps)):
        product_dict.append(json.loads(complete_refined_df_ps["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt_full
    pt_full={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(complete_refined_df_ps.iloc[i][:])
        pt_full[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(complete_refined_df_ps.iloc[i][:])
    pt_full["mix"]=pd.DataFrame(mix_series)
    global mt_full
    mt_full={}
    ss_series=[]
    brass_series=[]
    for i in range(len(complete_refined_df_ps)):
        if complete_refined_df_ps['MATERIAL TYPE'][i]=="SS":
            ss_series.append(complete_refined_df_ps.iloc[i][:])
        elif complete_refined_df_ps['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(complete_refined_df_ps.iloc[i][:])
    mt_full["ss"]=pd.DataFrame(ss_series)
    mt_full["brass"]=pd.DataFrame(brass_series)
    global nt
    nt={}
    I_series=[]
    II_series=[]
    III_series=[]
    for i in range(len(refined_df_ps)):
        if refined_df_ps['Ni hours'][i]<=2:
            I_series.append(refined_df_ps.iloc[i][:])
        elif refined_df_ps['Ni hours'][i]>2 and refined_df_ps['Ni hours'][i]<=8:
            II_series.append(refined_df_ps.iloc[i][:])
        else:
            III_series.append(refined_df_ps.iloc[i][:])
    nt["I_series"]=pd.DataFrame(I_series)
    nt["II_series"]=pd.DataFrame(II_series)
    nt["III_series"]=pd.DataFrame(III_series)
    #if 'refined_df' in st.session_state:    
        #columns_to_select = ["BATCH ID","RH mins"]    
        #I_ps_df = pd.merge(st.session_state.refined_df[columns_to_select],refined_df_ps, on="BATCH ID", how="inner")
        #st.session_state.I_ps_df=I_ps_df

    st.session_state.pt=pt
    st.session_state.mt=mt
    st.session_state.pt_full=pt_full
    st.session_state.mt_full=mt_full
    st.session_state.nt=nt
    st.session_state.refined_df_ps=refined_df_ps
    if st.session_state.current_page=='dashboard':
        pass
    else:
        st.rerun()
def change_date_ac(start_date_ac,end_date_ac,region_selections_ac):
    refined_df_ac=st.session_state.complete_refined_df_ac
    st.session_state.start_date_ac=start_date_ac
    st.session_state.end_date_ac=end_date_ac
    st.session_state.region_selections_ac=region_selections_ac
    complete_refined_df_ac=st.session_state.complete_refined_df_ac
    if type(refined_df_ac['BATCH START TIME'][0])!=str:
        refined_df_ac['BATCH START TIME']=refined_df_ac['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
        refined_df_ac['BATCH START TIME']=refined_df_ac['BATCH START TIME'].astype(str)
        a=np.array(refined_df_ac['BATCH START TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        refined_df_ac['BATCH START TIME']=a
    Ni_plating_diff=[]
    for i in range(0,len(refined_df_ac['NI PLATING DATE TIME'])):
        Ni_plating_diff.append([calculate_time_difference(refined_df_ac['NI PLATING DATE TIME'][i],refined_df_ac['BATCH START TIME'][i])])
    ni_hrs=[]
    for i in range(len(refined_df_ac)):
        ni_hrs.append(Ni_plating_diff[i][0][0]*24+Ni_plating_diff[i][0][1]+Ni_plating_diff[i][0][2]/60+Ni_plating_diff[i][0][3]/3600)
    shift_type_ac=[]
    for i in range(len(refined_df_ac)):
        if int(refined_df_ac['BATCH START TIME'][i][11:13])<6 or int(refined_df_ac['BATCH START TIME'][i][11:13])>=23:
            shift_type_ac.append("Shift 3")
        elif int(refined_df_ac['BATCH START TIME'][i][11:13])<15 and int(refined_df_ac['BATCH START TIME'][i][11:13])>=6:
            if refined_df_ac['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_ac['BATCH START TIME'][i][14:16])<=30:
                    shift_type_ac.append("Shift 1")
                else:
                    pass
            else:
                shift_type_ac.append("Shift 1")
        elif int(refined_df_ac['BATCH START TIME'][i][11:13])<23 and int(refined_df_ac['BATCH START TIME'][i][11:13])>=14 :
            if refined_df_ac['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_ac['BATCH START TIME'][i][14:16])>30:
                    shift_type_ac.append("Shift 2")
                else:
                    pass
            else:
                shift_type_ac.append("Shift 2")
    refined_df_ac['SHIFT TYPE']=shift_type_ac 
    refined_df_ac['Ni hours']=ni_hrs

    refined_df_ac['BATCH START TIME']=pd.to_datetime(refined_df_ac['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    refined_df_ac = refined_df_ac.sort_values(by='BATCH START TIME')
    refined_df_ac = refined_df_ac.reset_index(drop=True)

    filtered_df = refined_df_ac[(refined_df_ac["BATCH START TIME"] >= start_date_ac) & (refined_df_ac["BATCH START TIME"] <= end_date_ac)]
    filtered_df=filtered_df.reset_index(drop=True)
    comb_df=pd.DataFrame()
    if region_selections_ac[0]==True:
        pass
    else:
        if region_selections_ac[1]==True:
            filtered_df=filtered_df[filtered_df["V Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ac[2]==True:
            filtered_df=filtered_df[filtered_df["Bias Arc Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ac[3]==True:
            filtered_df=filtered_df[filtered_df["I1 Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ac[4]==True:
            filtered_df=filtered_df[filtered_df["I2 Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ac[5]==True:
            filtered_df=filtered_df[filtered_df["I3 Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ac[6]==True:
            filtered_df=filtered_df[filtered_df["Ar Gas Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)

    refined_df_ac = filtered_df.sort_values(by='BATCH START TIME')
    refined_df_ac['BATCH START TIME']=refined_df_ac['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
    refined_df_ac['BATCH START TIME']=refined_df_ac['BATCH START TIME'].astype(str)
    a=np.array(refined_df_ac['BATCH START TIME'])
    for i in range(len(a)):
        if "-" in a[i]:
            a[i]=str(a[i].replace("-","/"))
        if ":" in a[i]:
            tot=0
            for j in a[i]:
                if j==":":
                    tot+=1
            if tot==1:
                a[i]=str(a[i]+":00")
    refined_df_ac['BATCH START TIME']=a
    product_dict=[]
    import json
    for i in range(len(refined_df_ac)):
        product_dict.append(json.loads(refined_df_ac["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt
    pt={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(refined_df_ac.iloc[i][:])
        pt[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(refined_df_ac.iloc[i][:])
    pt["mix"]=pd.DataFrame(mix_series)
    global mt
    mt={}
    ss_series=[]
    brass_series=[]
    for i in range(len(refined_df_ac)):
        if refined_df_ac['MATERIAL TYPE'][i]=="SS":
            ss_series.append(refined_df_ac.iloc[i][:])
        elif refined_df_ac['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(refined_df_ac.iloc[i][:])
    mt["ss"]=pd.DataFrame(ss_series)
    mt["brass"]=pd.DataFrame(brass_series)
    product_dict=[]
    import json
    for i in range(len(complete_refined_df_ac)):
        product_dict.append(json.loads(complete_refined_df_ac["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt_full
    pt_full={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(complete_refined_df_ac.iloc[i][:])
        pt_full[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(complete_refined_df_ac.iloc[i][:])
    pt_full["mix"]=pd.DataFrame(mix_series)
    global mt_full
    mt_full={}
    ss_series=[]
    brass_series=[]
    for i in range(len(complete_refined_df_ac)):
        if complete_refined_df_ac['MATERIAL TYPE'][i]=="SS":
            ss_series.append(complete_refined_df_ac.iloc[i][:])
        elif complete_refined_df_ac['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(complete_refined_df_ac.iloc[i][:])
    mt_full["ss"]=pd.DataFrame(ss_series)
    mt_full["brass"]=pd.DataFrame(brass_series)
    global nt
    nt={}
    I_series=[]
    II_series=[]
    III_series=[]
    for i in range(len(refined_df_ac)):
        if refined_df_ac['Ni hours'][i]<=2:
            I_series.append(refined_df_ac.iloc[i][:])
        elif refined_df_ac['Ni hours'][i]>2 and refined_df_ac['Ni hours'][i]<=8:
            II_series.append(refined_df_ac.iloc[i][:])
        else:
            III_series.append(refined_df_ac.iloc[i][:])
    nt["I_series"]=pd.DataFrame(I_series)
    nt["II_series"]=pd.DataFrame(II_series)
    nt["III_series"]=pd.DataFrame(III_series)
    #if 'refined_df' in st.session_state:    
        #columns_to_select = ["BATCH ID","RH mins"]    
        #I_ac_df = pd.merge(st.session_state.refined_df[columns_to_select],refined_df_ac, on="BATCH ID", how="inner")
        #st.session_state.I_ac_df=I_ac_df

    st.session_state.pt=pt
    st.session_state.mt=mt
    st.session_state.pt_full=pt_full
    st.session_state.mt_full=mt_full
    st.session_state.nt=nt
    st.session_state.refined_df_ac=refined_df_ac
    if st.session_state.current_page=='dashboard':
        pass
    else:
        st.rerun()
def change_date_ae(start_date_ae,end_date_ae,region_selections_ae):
    refined_df_ae=st.session_state.complete_refined_df_ae
    st.session_state.start_date_ae=start_date_ae
    st.session_state.end_date_ae=end_date_ae
    st.session_state.region_selections_ae=region_selections_ae
    complete_refined_df_ae=st.session_state.complete_refined_df_ae
    if type(refined_df_ae['BATCH START TIME'][0])!=str:
        refined_df_ae['BATCH START TIME']=refined_df_ae['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
        refined_df_ae['BATCH START TIME']=refined_df_ae['BATCH START TIME'].astype(str)
        a=np.array(refined_df_ae['BATCH START TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        refined_df_ae['BATCH START TIME']=a
    Ni_plating_diff=[]
    for i in range(0,len(refined_df_ae['NI PLATING DATE TIME'])):
        Ni_plating_diff.append([calculate_time_difference(refined_df_ae['NI PLATING DATE TIME'][i],refined_df_ae['BATCH START TIME'][i])])
    ni_hrs=[]
    for i in range(len(refined_df_ae)):
        ni_hrs.append(Ni_plating_diff[i][0][0]*24+Ni_plating_diff[i][0][1]+Ni_plating_diff[i][0][2]/60+Ni_plating_diff[i][0][3]/3600)
    shift_type_ae=[]
    for i in range(len(refined_df_ae)):
        if int(refined_df_ae['BATCH START TIME'][i][11:13])<6 or int(refined_df_ae['BATCH START TIME'][i][11:13])>=23:
            shift_type_ae.append("Shift 3")
        elif int(refined_df_ae['BATCH START TIME'][i][11:13])<15 and int(refined_df_ae['BATCH START TIME'][i][11:13])>=6:
            if refined_df_ae['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_ae['BATCH START TIME'][i][14:16])<=30:
                    shift_type_ae.append("Shift 1")
                else:
                    pass
            else:
                shift_type_ae.append("Shift 1")
        elif int(refined_df_ae['BATCH START TIME'][i][11:13])<23 and int(refined_df_ae['BATCH START TIME'][i][11:13])>=14 :
            if refined_df_ae['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_ae['BATCH START TIME'][i][14:16])>30:
                    shift_type_ae.append("Shift 2")
                else:
                    pass
            else:
                shift_type_ae.append("Shift 2")
    refined_df_ae['SHIFT TYPE']=shift_type_ae 
    refined_df_ae['Ni hours']=ni_hrs

    refined_df_ae['BATCH START TIME']=pd.to_datetime(refined_df_ae['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    refined_df_ae = refined_df_ae.sort_values(by='BATCH START TIME')
    refined_df_ae = refined_df_ae.reset_index(drop=True)
    step_columns = ["Idxs", "V Irregulars", "Bias Arc Irregulars", "I1 Irregulars", "I2 Irregulars", 
                    "I3 Irregulars", "Ar Gas Irregulars", "V total", "I1 total", "I2 total", 
                    "I3 total", "Arc total", "Ar Gas total"]
    if region_selections_ae[8]=="All":
        pass
    else:
        for col in step_columns:
            refined_df_ae[col]=refined_df_ae[f"Step {region_selections_ae[8]} {col}"]
    filtered_df = refined_df_ae[(refined_df_ae["BATCH START TIME"] >= start_date_ae) & (refined_df_ae["BATCH START TIME"] <= end_date_ae)]
    filtered_df=filtered_df.reset_index(drop=True)
    comb_df=pd.DataFrame()
    if region_selections_ae[0]=='All Batches':
        pass
    elif region_selections_ae[0]=='Old Recipe':
        filtered_df=filtered_df[filtered_df['Recipe']=='Old']
        filtered_df=filtered_df.reset_index(drop=True)

    elif region_selections_ae[0]=='New Recipe':
        filtered_df=filtered_df[filtered_df['Recipe']=='New']
        filtered_df=filtered_df.reset_index(drop=True)
    if region_selections_ae[1]=='All Batches':
        pass
    elif region_selections_ae[1]=='Irregular Batches':
        if region_selections_ae[2]==True:
            filtered_df=filtered_df[filtered_df["V Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ae[3]==True:
            filtered_df=filtered_df[filtered_df["Bias Arc Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ae[4]==True:
            filtered_df=filtered_df[filtered_df["I1 Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ae[5]==True:
            filtered_df=filtered_df[filtered_df["I2 Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ae[6]==True:
            filtered_df=filtered_df[filtered_df["I3 Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ae[7]==True:
            filtered_df=filtered_df[filtered_df["Ar Gas Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)

    elif region_selections_ae[1]=='Good Batches':
        if region_selections_ae[2]==True:
            filtered_df=filtered_df[filtered_df["V Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ae[3]==True:
            filtered_df=filtered_df[filtered_df["Bias Arc Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ae[4]==True:
            filtered_df=filtered_df[filtered_df["I1 Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ae[5]==True:
            filtered_df=filtered_df[filtered_df["I2 Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ae[6]==True:
            filtered_df=filtered_df[filtered_df["I3 Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_ae[7]==True:
            filtered_df=filtered_df[filtered_df["Ar Gas Irregulars"]==False]
            filtered_df=filtered_df.reset_index(drop=True)

    refined_df_ae = filtered_df.sort_values(by='BATCH START TIME')
    refined_df_ae['BATCH START TIME']=refined_df_ae['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
    refined_df_ae['BATCH START TIME']=refined_df_ae['BATCH START TIME'].astype(str)
    a=np.array(refined_df_ae['BATCH START TIME'])
    for i in range(len(a)):
        if "-" in a[i]:
            a[i]=str(a[i].replace("-","/"))
        if ":" in a[i]:
            tot=0
            for j in a[i]:
                if j==":":
                    tot+=1
            if tot==1:
                a[i]=str(a[i]+":00")
    refined_df_ae['BATCH START TIME']=a
    product_dict=[]
    import json
    for i in range(len(refined_df_ae)):
        product_dict.append(json.loads(refined_df_ae["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt
    pt={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(refined_df_ae.iloc[i][:])
        pt[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(refined_df_ae.iloc[i][:])
    pt["mix"]=pd.DataFrame(mix_series)
    global mt
    mt={}
    ss_series=[]
    brass_series=[]
    for i in range(len(refined_df_ae)):
        if refined_df_ae['MATERIAL TYPE'][i]=="SS":
            ss_series.append(refined_df_ae.iloc[i][:])
        elif refined_df_ae['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(refined_df_ae.iloc[i][:])
    mt["ss"]=pd.DataFrame(ss_series)
    mt["brass"]=pd.DataFrame(brass_series)
    product_dict=[]
    import json
    for i in range(len(complete_refined_df_ae)):
        product_dict.append(json.loads(complete_refined_df_ae["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt_full
    pt_full={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(complete_refined_df_ae.iloc[i][:])
        pt_full[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(complete_refined_df_ae.iloc[i][:])
    pt_full["mix"]=pd.DataFrame(mix_series)
    global mt_full
    mt_full={}
    ss_series=[]
    brass_series=[]
    for i in range(len(complete_refined_df_ae)):
        if complete_refined_df_ae['MATERIAL TYPE'][i]=="SS":
            ss_series.append(complete_refined_df_ae.iloc[i][:])
        elif complete_refined_df_ae['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(complete_refined_df_ae.iloc[i][:])
    mt_full["ss"]=pd.DataFrame(ss_series)
    mt_full["brass"]=pd.DataFrame(brass_series)
    global nt
    nt={}
    I_series=[]
    II_series=[]
    III_series=[]
    for i in range(len(refined_df_ae)):
        if refined_df_ae['Ni hours'][i]<=2:
            I_series.append(refined_df_ae.iloc[i][:])
        elif refined_df_ae['Ni hours'][i]>2 and refined_df_ae['Ni hours'][i]<=8:
            II_series.append(refined_df_ae.iloc[i][:])
        else:
            III_series.append(refined_df_ae.iloc[i][:])
    nt["I_series"]=pd.DataFrame(I_series)
    nt["II_series"]=pd.DataFrame(II_series)
    nt["III_series"]=pd.DataFrame(III_series)
    #if 'refined_df' in st.session_state:    
        #columns_to_select = ["BATCH ID","RH mins"]    
        #I_ae_df = pd.merge(st.session_state.refined_df[columns_to_select],refined_df_ae, on="BATCH ID", how="inner")
        #st.session_state.I_ae_df=I_ae_df

    st.session_state.pt=pt
    st.session_state.mt=mt
    st.session_state.pt_full=pt_full
    st.session_state.mt_full=mt_full
    st.session_state.nt=nt
    st.session_state.refined_df_ae=refined_df_ae
    if st.session_state.current_page=='dashboard':
        pass
    else:
        st.rerun()
def change_date_glow(start_date_glow,end_date_glow,region_selections_glow):
    refined_df_glow=st.session_state.complete_refined_df_glow
    st.session_state.start_date_glow=start_date_glow
    st.session_state.end_date_glow=end_date_glow
    st.session_state.region_selections_glow=region_selections_glow
    complete_refined_df_glow=st.session_state.complete_refined_df_glow
    if type(refined_df_glow['BATCH START TIME'][0])!=str:
        refined_df_glow['BATCH START TIME']=refined_df_glow['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
        refined_df_glow['BATCH START TIME']=refined_df_glow['BATCH START TIME'].astype(str)
        a=np.array(refined_df_glow['BATCH START TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        refined_df_glow['BATCH START TIME']=a
    Ni_plating_diff=[]
    for i in range(0,len(refined_df_glow['NI PLATING DATE TIME'])):
        Ni_plating_diff.append([calculate_time_difference(refined_df_glow['NI PLATING DATE TIME'][i],refined_df_glow['BATCH START TIME'][i])])
    ni_hrs=[]
    for i in range(len(refined_df_glow)):
        ni_hrs.append(Ni_plating_diff[i][0][0]*24+Ni_plating_diff[i][0][1]+Ni_plating_diff[i][0][2]/60+Ni_plating_diff[i][0][3]/3600)
    shift_type_glow=[]
    for i in range(len(refined_df_glow)):
        if int(refined_df_glow['BATCH START TIME'][i][11:13])<6 or int(refined_df_glow['BATCH START TIME'][i][11:13])>=23:
            shift_type_glow.append("Shift 3")
        elif int(refined_df_glow['BATCH START TIME'][i][11:13])<15 and int(refined_df_glow['BATCH START TIME'][i][11:13])>=6:
            if refined_df_glow['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_glow['BATCH START TIME'][i][14:16])<=30:
                    shift_type_glow.append("Shift 1")
                else:
                    pass
            else:
                shift_type_glow.append("Shift 1")
        elif int(refined_df_glow['BATCH START TIME'][i][11:13])<23 and int(refined_df_glow['BATCH START TIME'][i][11:13])>=14 :
            if refined_df_glow['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_glow['BATCH START TIME'][i][14:16])>30:
                    shift_type_glow.append("Shift 2")
                else:
                    pass
            else:
                shift_type_glow.append("Shift 2")
    refined_df_glow['SHIFT TYPE']=shift_type_glow 
    refined_df_glow['Ni hours']=ni_hrs

    refined_df_glow['BATCH START TIME']=pd.to_datetime(refined_df_glow['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    refined_df_glow = refined_df_glow.sort_values(by='BATCH START TIME')
    refined_df_glow = refined_df_glow.reset_index(drop=True)

    filtered_df = refined_df_glow[(refined_df_glow["BATCH START TIME"] >= start_date_glow) & (refined_df_glow["BATCH START TIME"] <= end_date_glow)]
    filtered_df=filtered_df.reset_index(drop=True)
    comb_df=pd.DataFrame()
    if region_selections_glow[0]==True:
        pass
    else:
        if region_selections_glow[1]==True:
            filtered_df=filtered_df[filtered_df["V Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_glow[2]==True:
            filtered_df=filtered_df[filtered_df["Bias Arc Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_glow[3]==True:
            filtered_df=filtered_df[filtered_df["I Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)
        if region_selections_glow[4]==True:
            filtered_df=filtered_df[filtered_df["Ar Gas Irregulars"]==True]
            filtered_df=filtered_df.reset_index(drop=True)

    refined_df_glow = filtered_df.sort_values(by='BATCH START TIME')
    refined_df_glow['BATCH START TIME']=refined_df_glow['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
    refined_df_glow['BATCH START TIME']=refined_df_glow['BATCH START TIME'].astype(str)
    a=np.array(refined_df_glow['BATCH START TIME'])
    for i in range(len(a)):
        if "-" in a[i]:
            a[i]=str(a[i].replace("-","/"))
        if ":" in a[i]:
            tot=0
            for j in a[i]:
                if j==":":
                    tot+=1
            if tot==1:
                a[i]=str(a[i]+":00")
    refined_df_glow['BATCH START TIME']=a
    product_dict=[]
    import json
    for i in range(len(refined_df_glow)):
        product_dict.append(json.loads(refined_df_glow["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt
    pt={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(refined_df_glow.iloc[i][:])
        pt[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(refined_df_glow.iloc[i][:])
    pt["mix"]=pd.DataFrame(mix_series)
    product_dict=[]
    import json
    for i in range(len(complete_refined_df_glow)):
        product_dict.append(json.loads(complete_refined_df_glow["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    pt_full={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(complete_refined_df_glow.iloc[i][:])
        pt_full[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(complete_refined_df_glow.iloc[i][:])
    pt_full["mix"]=pd.DataFrame(mix_series)
    global mt
    mt={}
    ss_series=[]
    brass_series=[]
    for i in range(len(refined_df_glow)):
        if refined_df_glow['MATERIAL TYPE'][i]=="SS":
            ss_series.append(refined_df_glow.iloc[i][:])
        elif refined_df_glow['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(refined_df_glow.iloc[i][:])
    mt["ss"]=pd.DataFrame(ss_series)
    mt["brass"]=pd.DataFrame(brass_series)
    mt_full={}
    ss_series=[]
    brass_series=[]
    for i in range(len(complete_refined_df_glow)):
        if complete_refined_df_glow['MATERIAL TYPE'][i]=="SS":
            ss_series.append(complete_refined_df_glow.iloc[i][:])
        elif complete_refined_df_glow['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(complete_refined_df_glow.iloc[i][:])
    mt_full["ss"]=pd.DataFrame(ss_series)
    mt_full["brass"]=pd.DataFrame(brass_series)
    global nt
    nt={}
    I_series=[]
    II_series=[]
    III_series=[]
    for i in range(len(refined_df_glow)):
        if refined_df_glow['Ni hours'][i]<=2:
            I_series.append(refined_df_glow.iloc[i][:])
        elif refined_df_glow['Ni hours'][i]>2 and refined_df_glow['Ni hours'][i]<=8:
            II_series.append(refined_df_glow.iloc[i][:])
        else:
            III_series.append(refined_df_glow.iloc[i][:])
    nt["I_series"]=pd.DataFrame(I_series)
    nt["II_series"]=pd.DataFrame(II_series)
    nt["III_series"]=pd.DataFrame(III_series)
    #if 'refined_df' in st.session_state:    
        #columns_to_select = ["BATCH ID","RH mins"]    
        #I_glow_df = pd.merge(st.session_state.refined_df[columns_to_select],refined_df_glow, on="BATCH ID", how="inner")
        #st.session_state.I_glow_df=I_glow_df

    st.session_state.pt=pt
    st.session_state.mt=mt
    st.session_state.mt_full=mt_full
    st.session_state.pt_full=pt_full

    st.session_state.nt=nt
    st.session_state.refined_df_glow=refined_df_glow
    print(refined_df_glow['Bias Arc Irregulars'].sum())
    if st.session_state.current_page=='dashboard':
        pass
    else:
        st.rerun()
def change_date_II(start_date_II,end_date_II,region_selections_II):
    refined_df_II=st.session_state.complete_refined_df_II
    st.session_state.start_date_II=start_date_II
    st.session_state.end_date_II=end_date_II
    st.session_state.region_selections_II=region_selections_II
    complete_refined_df_II=st.session_state.complete_refined_df_II
    print("Beginning of change: ",len(complete_refined_df_II))
    if type(refined_df_II['BATCH START TIME'][0])!=str:
        refined_df_II['BATCH START TIME']=refined_df_II['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
        refined_df_II['BATCH START TIME']=refined_df_II['BATCH START TIME'].astype(str)
        a=np.array(refined_df_II['BATCH START TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        refined_df_II['BATCH START TIME']=a
    Ni_plating_diff=[]
    for i in range(0,len(refined_df_II['NI PLATING DATE TIME'])):
        Ni_plating_diff.append([calculate_time_difference(refined_df_II['NI PLATING DATE TIME'][i],refined_df_II['BATCH START TIME'][i])])
    ni_hrs=[]
    for i in range(len(refined_df_II)):
        ni_hrs.append(Ni_plating_diff[i][0][0]*24+Ni_plating_diff[i][0][1]+Ni_plating_diff[i][0][2]/60+Ni_plating_diff[i][0][3]/3600)
    h_II_mins=[]
    for i in range(len(refined_df_II)):
        h_II_mins.append(refined_df_II["H_II Time"][i][0][1]*60+refined_df_II["H_II Time"][i][0][2]+refined_df_II["H_II Time"][i][0][3]/60)
    t_II_mins=[]
    for i in range(len(refined_df_II)):
        t_II_mins.append(refined_df_II["Temp_II Time"][i][0][1]*60+refined_df_II["Temp_II Time"][i][0][2]+refined_df_II["Temp_II Time"][i][0][3]/60)
    shift_type_II=[]
    for i in range(len(refined_df_II)):
        if int(refined_df_II['BATCH START TIME'][i][11:13])<6 or int(refined_df_II['BATCH START TIME'][i][11:13])>=23:
            shift_type_II.append("Shift 3")
        elif int(refined_df_II['BATCH START TIME'][i][11:13])<15 and int(refined_df_II['BATCH START TIME'][i][11:13])>=6:
            if refined_df_II['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_II['BATCH START TIME'][i][14:16])<=30:
                    shift_type_II.append("Shift 1")
                else:
                    pass
            else:
                shift_type_II.append("Shift 1")
        elif int(refined_df_II['BATCH START TIME'][i][11:13])<23 and int(refined_df_II['BATCH START TIME'][i][11:13])>=14 :
            if refined_df_II['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_II['BATCH START TIME'][i][14:16])>30:
                    shift_type_II.append("Shift 2")
                else:
                    pass
            else:
                shift_type_II.append("Shift 2")
    refined_df_II["H_II mins"]=h_II_mins
    refined_df_II["Ni hours"]=ni_hrs
    refined_df_II["T_II mins"]=t_II_mins
    refined_df_II['SHIFT TYPE II']=shift_type_II
    idxs_II=refined_df_II["Idxs_II"]
    h_II_time_id=refined_df_II["H_II Idxs"]
    temp_II_time_id=refined_df_II["Temp_II Idxs"]
    
    refined_df_II['BATCH START TIME']=pd.to_datetime(refined_df_II['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    refined_df_II = refined_df_II.sort_values(by='BATCH START TIME')
    refined_df_II = refined_df_II.reset_index(drop=True)

    filtered_df = refined_df_II[(refined_df_II["BATCH START TIME"] >= start_date_II) & (refined_df_II["BATCH START TIME"] <= end_date_II)]
    filtered_df=filtered_df.reset_index(drop=True)
    if region_selections_II[0]==True and region_selections_II[1]==True and region_selections_II[2]==True:
        pass
    elif region_selections_II[0]==False and region_selections_II[1]==False and region_selections_II[2]==True:
        filtered_df=filtered_df[filtered_df['H_II mins']>st.session_state.yellow_limit_global_II]
    elif region_selections_II[0]==False and region_selections_II[1]==True and region_selections_II[2]==False:
        filtered_df=filtered_df[(filtered_df['H_II mins']<=st.session_state.yellow_limit_global_II) & (filtered_df['H_II mins']>=st.session_state.green_limit_global_II)] 
    elif region_selections_II[0]==True and region_selections_II[1]==False and region_selections_II[2]==False:
        filtered_df=filtered_df[filtered_df['H_II mins']<st.session_state.green_limit_global_II]  
    elif region_selections_II[0]==True and region_selections_II[1]==True and region_selections_II[2]==False:
        filtered_df=filtered_df[(filtered_df['H_II mins']<=st.session_state.yellow_limit_global_II)] 
    elif region_selections_II[0]==False and region_selections_II[1]==True and region_selections_II[2]==True:
        filtered_df=filtered_df[(filtered_df['H_II mins']>=st.session_state.green_limit_global_II)] 
    elif region_selections_II[0]==True and region_selections_II[1]==False and region_selections_II[2]==True:
        filtered_df=filtered_df[(filtered_df['H_II mins']>st.session_state.yellow_limit_global_II) | (filtered_df['H_II mins']<st.session_state.green_limit_global_II)] 

    filtered_df=filtered_df.reset_index(drop=True)
    refined_df_II=filtered_df
    refined_df_II['BATCH START TIME']=refined_df_II['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
    refined_df_II['BATCH START TIME']=refined_df_II['BATCH START TIME'].astype(str)
    a=np.array(refined_df_II['BATCH START TIME'])
    for i in range(len(a)):
        if "-" in a[i]:
            a[i]=str(a[i].replace("-","/"))
        if ":" in a[i]:
            tot=0
            for j in a[i]:
                if j==":":
                    tot+=1
            if tot==1:
                a[i]=str(a[i]+":00")
    refined_df_II['BATCH START TIME']=a
    product_dict=[]
    import json
    for i in range(len(refined_df_II)):
        product_dict.append(json.loads(refined_df_II["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt
    pt={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(refined_df_II.iloc[i][:])
        pt[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(refined_df_II.iloc[i][:])
    pt["mix"]=pd.DataFrame(mix_series)
    global mt
    mt={}
    ss_series=[]
    brass_series=[]
    for i in range(len(refined_df_II)):
        if refined_df_II['MATERIAL TYPE'][i]=="SS":
            ss_series.append(refined_df_II.iloc[i][:])
        elif refined_df_II['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(refined_df_II.iloc[i][:])
    mt["ss"]=pd.DataFrame(ss_series)
    mt["brass"]=pd.DataFrame(brass_series)
    global nt
    nt={}
    I_series=[]
    II_series=[]
    III_series=[]
    for i in range(len(refined_df_II)):
        if refined_df_II['Ni hours'][i]<=2:
            I_series.append(refined_df_II.iloc[i][:])
        elif refined_df_II['Ni hours'][i]>2 and refined_df_II['Ni hours'][i]<=8:
            II_series.append(refined_df_II.iloc[i][:])
        else:
            III_series.append(refined_df_II.iloc[i][:])
    nt["I_series"]=pd.DataFrame(I_series)
    nt["II_series"]=pd.DataFrame(II_series)
    nt["III_series"]=pd.DataFrame(III_series)
    if 'refined_df' in st.session_state:    
        columns_to_select = ["BATCH ID","RH mins"]    
        I_II_df = pd.merge(st.session_state.refined_df[columns_to_select],refined_df_II, on="BATCH ID", how="inner")
        st.session_state.I_II_df=I_II_df
    golden_index_II = refined_df_II['H_II mins'].idxmin()
    golden_batch_II=refined_df_II['BATCH ID'][golden_index_II]
    st.session_state.golden_batch_II=golden_batch_II
    st.session_state.golden_index_II=golden_index_II
    
    st.session_state.idxs_II =idxs_II
    st.session_state.h_II_time_id=h_II_time_id
    st.session_state.temp_II_time_id=temp_II_time_id
    
    st.session_state.h_II_mins=np.array(refined_df_II["H_II mins"])
    st.session_state.t_II_mins=t_II_mins   
    st.session_state.pt=pt
    st.session_state.mt=mt
    st.session_state.nt=nt
    st.session_state.refined_df_II=refined_df_II
    if st.session_state.current_page=='dashboard':
        pass
    else:
        st.rerun()
def change_date(start_date,end_date,region_selections):
    refined_df=st.session_state.complete_refined_df
    st.session_state.start_date=start_date
    st.session_state.end_date=end_date
    st.session_state.region_selections=region_selections
    complete_refined_df=st.session_state.complete_refined_df
    if type(refined_df['BATCH START TIME'][0])!=str:
        refined_df['BATCH START TIME']=refined_df['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
        refined_df['BATCH START TIME']=refined_df['BATCH START TIME'].astype(str)
        a=np.array(refined_df['BATCH START TIME'])
        for i in range(len(a)):
            if "-" in a[i]:
                a[i]=str(a[i].replace("-","/"))
            if ":" in a[i]:
                tot=0
                for j in a[i]:
                    if j==":":
                        tot+=1
                if tot==1:
                    a[i]=str(a[i]+":00")
        refined_df['BATCH START TIME']=a
    Ni_plating_diff=[]
    for i in range(0,len(refined_df['NI PLATING DATE TIME'])):
        Ni_plating_diff.append([calculate_time_difference(refined_df['NI PLATING DATE TIME'][i],refined_df['BATCH START TIME'][i])])
    ni_hrs=[]
    for i in range(len(refined_df)):
        ni_hrs.append(Ni_plating_diff[i][0][0]*24+Ni_plating_diff[i][0][1]+Ni_plating_diff[i][0][2]/60+Ni_plating_diff[i][0][3]/3600)
    rh_mins=[]
    for i in range(len(refined_df)):
        rh_mins.append(refined_df["RH Time"][i][0][1]*60+refined_df["RH Time"][i][0][2]+refined_df["RH Time"][i][0][3]/60)
    r_mins=[]
    for i in range(len(refined_df)):
        r_mins.append(refined_df["R Time"][i][0][1]*60+refined_df["R Time"][i][0][2]+refined_df["R Time"][i][0][3]/60)
    t_mins=[]
    for i in range(len(refined_df)):
        t_mins.append(refined_df["Temp Time"][i][0][1]*60+refined_df["Temp Time"][i][0][2]+refined_df["Temp Time"][i][0][3]/60)
    shift_type=[]
    for i in range(len(refined_df)):
        if int(refined_df['BATCH START TIME'][i][11:13])<6 or int(refined_df['BATCH START TIME'][i][11:13])>=23:
            shift_type.append("Shift 3")
        elif int(refined_df['BATCH START TIME'][i][11:13])<15 and int(refined_df['BATCH START TIME'][i][11:13])>=6:
            if refined_df['BATCH START TIME'][i][11:13]==14:
                if int(refined_df['BATCH START TIME'][i][14:16])<=30:
                    shift_type.append("Shift 1")
                else:
                    pass
            else:
                shift_type.append("Shift 1")
        elif int(refined_df['BATCH START TIME'][i][11:13])<23 and int(refined_df['BATCH START TIME'][i][11:13])>=14 :
            if refined_df['BATCH START TIME'][i][11:13]==14:
                if int(refined_df['BATCH START TIME'][i][14:16])>30:
                    shift_type.append("Shift 2")
                else:
                    pass
            else:
                shift_type.append("Shift 2")
    refined_df["RH mins"]=rh_mins
    refined_df["R mins"]=r_mins
    refined_df["Ni hours"]=ni_hrs
    refined_df["T mins"]=t_mins
    refined_df['SHIFT TYPE']=shift_type
    idxs=refined_df["Idxs"]
    r_time_id=refined_df["R Idxs"]
    rh_time_id=refined_df["RH Idxs"]
    temp_time_id=refined_df["Temp Idxs"]
    
    refined_df['BATCH START TIME']=pd.to_datetime(refined_df['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    refined_df = refined_df.sort_values(by='BATCH START TIME')
    refined_df = refined_df.reset_index(drop=True)

    filtered_df = refined_df[(refined_df["BATCH START TIME"] >= start_date) & (refined_df["BATCH START TIME"] <= end_date)]
    filtered_df=filtered_df.reset_index(drop=True)
    if region_selections[0]==True and region_selections[1]==True and region_selections[2]==True:
        pass
    elif region_selections[0]==False and region_selections[1]==False and region_selections[2]==True:
        filtered_df=filtered_df[filtered_df['RH mins']>st.session_state.yellow_limit_global]
    elif region_selections[0]==False and region_selections[1]==True and region_selections[2]==False:
        filtered_df=filtered_df[(filtered_df['RH mins']<=st.session_state.yellow_limit_global) & (filtered_df['RH mins']>=st.session_state.green_limit_global)] 
    elif region_selections[0]==True and region_selections[1]==False and region_selections[2]==False:
        filtered_df=filtered_df[filtered_df['RH mins']<st.session_state.green_limit_global]  
    elif region_selections[0]==True and region_selections[1]==True and region_selections[2]==False:
        filtered_df=filtered_df[(filtered_df['RH mins']<=st.session_state.yellow_limit_global)] 
    elif region_selections[0]==False and region_selections[1]==True and region_selections[2]==True:
        filtered_df=filtered_df[(filtered_df['RH mins']>=st.session_state.green_limit_global)] 
    elif region_selections[0]==True and region_selections[1]==False and region_selections[2]==True:
        filtered_df=filtered_df[(filtered_df['RH mins']>st.session_state.yellow_limit_global) | (filtered_df['RH mins']<st.session_state.green_limit_global)] 

    filtered_df=filtered_df.reset_index(drop=True)
    refined_df=filtered_df
    refined_df['BATCH START TIME']=refined_df['BATCH START TIME'].dt.strftime('%d-%m-%Y %H:%M:%S')
    refined_df['BATCH START TIME']=refined_df['BATCH START TIME'].astype(str)
    a=np.array(refined_df['BATCH START TIME'])
    for i in range(len(a)):
        if "-" in a[i]:
            a[i]=str(a[i].replace("-","/"))
        if ":" in a[i]:
            tot=0
            for j in a[i]:
                if j==":":
                    tot+=1
            if tot==1:
                a[i]=str(a[i]+":00")
    refined_df['BATCH START TIME']=a
    product_dict=[]
    import json
    for i in range(len(refined_df)):
        product_dict.append(json.loads(refined_df["PRODUCT TYPE"][i]))
    product_types=['cases', 'clasp', 'endpiece', 'crown', 'buckles', 'flap', 'bracelet', 'pin', 'straps']
    global pt
    pt={}
    for p in product_types:
        series=[]
        for i in range(len(product_dict)):
            if p in product_dict[i] and len(product_dict[i])==1 and product_dict[i][p]!=0:
                series.append(refined_df.iloc[i][:])
        pt[p]=pd.DataFrame(series)
    mix_series=[]
    for i in range(len(product_dict)):
        if len(product_dict[i])>1:
            mix_series.append(refined_df.iloc[i][:])
    pt["mix"]=pd.DataFrame(mix_series)
    global mt
    mt={}
    ss_series=[]
    brass_series=[]
    for i in range(len(refined_df)):
        if refined_df['MATERIAL TYPE'][i]=="SS":
            ss_series.append(refined_df.iloc[i][:])
        elif refined_df['MATERIAL TYPE'][i]=="Brass":
            brass_series.append(refined_df.iloc[i][:])
    mt["ss"]=pd.DataFrame(ss_series)
    mt["brass"]=pd.DataFrame(brass_series)
    global nt
    nt={}
    I_series=[]
    II_series=[]
    III_series=[]
    for i in range(len(refined_df)):
        if refined_df['Ni hours'][i]<=2:
            I_series.append(refined_df.iloc[i][:])
        elif refined_df['Ni hours'][i]>2 and refined_df['Ni hours'][i]<=8:
            II_series.append(refined_df.iloc[i][:])
        else:
            III_series.append(refined_df.iloc[i][:])
    nt["I_series"]=pd.DataFrame(I_series)
    nt["II_series"]=pd.DataFrame(II_series)
    nt["III_series"]=pd.DataFrame(III_series)
    golden_index = refined_df['RH mins'].idxmin()
    golden_batch=refined_df['BATCH ID'][golden_index]
    st.session_state.golden_batch=golden_batch
    st.session_state.golden_index=golden_index
    
    st.session_state.idxs =idxs
    st.session_state.r_time_id=r_time_id
    st.session_state.rh_time_id=rh_time_id
    st.session_state.temp_time_id=temp_time_id
    
    st.session_state.rh_mins=np.array(refined_df["RH mins"])
    st.session_state.r_mins=r_mins
    st.session_state.t_mins=t_mins   
    st.session_state.pt=pt
    st.session_state.mt=mt
    st.session_state.nt=nt
    st.session_state.refined_df=refined_df
    if st.session_state.current_page=='dashboard':
        pass
    else:
        st.rerun()
# Initialize session state to store uploaded files
if 'pre_post_data' not in st.session_state:
    st.session_state.pre_post_data = []
if 'process_data' not in st.session_state:
    st.session_state.process_data = []
if 'pre_post_data_II' not in st.session_state:
    st.session_state.pre_post_data_II = []
if 'process_data_II' not in st.session_state:
    st.session_state.process_data_II = []
if 'pre_post_data_glow' not in st.session_state:
    st.session_state.pre_post_data_glow = []
if 'process_data_glow' not in st.session_state:
    st.session_state.process_data_glow = []
if 'pre_post_data_ac' not in st.session_state:
    st.session_state.pre_post_data_ac = []
if 'process_data_ac' not in st.session_state:
    st.session_state.process_data_ac = []
if 'pre_post_data_ae' not in st.session_state:
    st.session_state.pre_post_data_ae = []
if 'process_data_ae' not in st.session_state:
    st.session_state.process_data_ae = []
if 'pre_post_data_ps' not in st.session_state:
    st.session_state.pre_post_data_ps = []
if 'process_data_ps' not in st.session_state:
    st.session_state.process_data_ps = []
if 'pre_post_data_ti' not in st.session_state:
    st.session_state.pre_post_data_ti = []
if 'process_data_ti' not in st.session_state:
    st.session_state.process_data_ti = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'computing'
if 'input_state' not in st.session_state:
    st.session_state.input_state = {
        "material_type": {"Brass": False, "SS": False},
        "product_type": {
            "Cases": False, "Clasp": False, "Endpiece": False,
            "Crown": False, "Buckles": False, "Flap": False,
            "Bracelet": False, "Pin": False, "Straps": False, "Mix": False
        },
        "ni_plating_time": {"I_series": False, "II_series": False, "III_series": False},
    }
if 'open_sections' not in st.session_state:
    st.session_state.open_sections = []

# Custom CSS for the heading and button styling
st.markdown(
    """
    <style>
    input[type="checkbox"]:checked + div[data-testid="stMarkdownContainer"] div[style="overflow: hidden;"] {
        color: #008081; /* Change this color to your desired color */
    }
    </style>
    """, unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .main-heading {
        font-size: 50px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        margin-top: 20px;
        animation: move 1s ;
    }
    @keyframes move {
        0% {transform: translateY(0);}
        50% {transform: translateY(-10px);}
        100% {transform: translateY(0);}
    }
    .stButton>button {
        background-color: #008081;
        color: white;
        border: none;
        padding: 5px 20px;
        margin: 5px 0px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Define a function to handle file uploads
def handle_file_upload(uploaded_file, file_list_name):
    if uploaded_file:
        file_contents = StringIO(uploaded_file.getvalue().decode("utf-8"))
        df = pd.read_csv(file_contents)
        df=df.dropna(how='all')
        st.session_state[file_list_name]=df
        if file_list_name=='process_data':
            st.write("Number of batches in Process dataset : "+str(len(df['BATCH ID'].unique()))+"[",df['DATE TIME'][1][:10]," to ",df['DATE TIME'][len(df)-1][:10],"]")
            #st.write("From ",df['DATE TIME'][0],"\nTill ",df['DATE TIME'][len(df)-1])
        elif file_list_name=='pre_post_data':
            st.write("Number of batches in Pre Post dataset :"+str(len(df['BATCH ID'].unique()))+"\t[",str(df['BATCH START TIME'][1])[:10]," to ",str(df['BATCH START TIME'][len(df)-1])[:10],"]")
            #st.write("From ",df['BATCH START TIME'][1],"\nTill ",df['BATCH START TIME'][len(df)-2])
        if file_list_name=='process_data_II':
            st.write("Number of batches in Process dataset : "+str(len(df['BATCH ID'].unique()))+"[",df['DATE TIME'][1][:10]," to ",df['DATE TIME'][len(df)-1][:10],"]")
            #st.write("From ",df['DATE TIME'][0],"\nTill ",df['DATE TIME'][len(df)-1])
        elif file_list_name=='pre_post_data_II':
            st.write("Number of batches in Pre Post dataset :"+str(len(df['BATCH ID'].unique()))+"\t[",str(df['BATCH START TIME'][1])[:10]," to ",str(df['BATCH START TIME'][len(df)-1])[:10],"]")
            #st.write("From ",df['BATCH START TIME'][1],"\nTill ",df['BATCH START TIME'][len(df)-2])
        if file_list_name=='process_data_glow':
            st.write("Number of batches in Process dataset : "+str(len(df['BATCH ID'].unique()))+"[",df['DATE TIME'][1][:10]," to ",df['DATE TIME'][len(df)-1][:10],"]")
            #st.write("From ",df['DATE TIME'][0],"\nTill ",df['DATE TIME'][len(df)-1])
        elif file_list_name=='pre_post_data_glow':
            st.write("Number of batches in Pre Post dataset :"+str(len(df['BATCH ID'].unique()))+"\t[",str(df['BATCH START TIME'][1])[:10]," to ",str(df['BATCH START TIME'][len(df)-1])[:10],"]")
            #st.write("From ",df['BATCH START TIME'][1],"\nTill ",df['BATCH START TIME'][len(df)-2])
        if file_list_name=='process_data_ac':
            st.write("Number of batches in Process dataset : "+str(len(df['BATCH ID'].unique()))+"[",df['DATE TIME'][1][:10]," to ",df['DATE TIME'][len(df)-1][:10],"]")
            #st.write("From ",df['DATE TIME'][0],"\nTill ",df['DATE TIME'][len(df)-1])
        elif file_list_name=='pre_post_data_ac':
            st.write("Number of batches in Pre Post dataset :"+str(len(df['BATCH ID'].unique()))+"\t[",str(df['BATCH START TIME'][1])[:10]," to ",str(df['BATCH START TIME'][len(df)-1])[:10],"]")
            #st.write("From ",df['BATCH START TIME'][1],"\nTill ",df['BATCH START TIME'][len(df)-2])
        if file_list_name=='process_data_ae':
            st.write("Number of batches in Process dataset : "+str(len(df['BATCH ID'].unique()))+"[",df['DATE TIME'][1][:10]," to ",df['DATE TIME'][len(df)-1][:10],"]")
            #st.write("From ",df['DATE TIME'][0],"\nTill ",df['DATE TIME'][len(df)-1])
        elif file_list_name=='pre_post_data_ae':
            st.write("Number of batches in Pre Post dataset :"+str(len(df['BATCH ID'].unique()))+"\t[",str(df['BATCH START TIME'][1])[:10]," to ",str(df['BATCH START TIME'][len(df)-1])[:10],"]")
            #st.write("From ",df['BATCH START TIME'][1],"\nTill ",df['BATCH START TIME'][len(df)-2])

            

# Main page
if st.session_state.current_page == 'computing':
    st.session_state.current_page = 'dashboard'
    compute(False,None,None)
    compute_II(False,None,None)
    compute_glow(False,None,None)
    compute_ac(False,None,None)
    compute_ae(False,None,None)
    compute_ps(False,None,None)
    compute_ti(False,None,None)

    st.rerun()
elif st.session_state.current_page == 'main':
    
    
    st.header("Upload your data files:")
    
    pre_post_file = st.file_uploader("Upload Pre/Post Process Data", type=["csv"])
    handle_file_upload(pre_post_file, 'pre_post_data')
    
    process_file = st.file_uploader("Upload Process Data", type=["csv"])
    handle_file_upload(process_file, 'process_data')
    if st.button("Check common batches"):
        df1 = pd.DataFrame()
        df1 = pd.concat([df1,st.session_state.process_data], ignore_index=True)
        df1.dropna()
        df2 = pd.DataFrame()
        df2 = pd.concat([df2,st.session_state.pre_post_data], ignore_index=True)  
        new_header = df2.iloc[0]
        in_df = df2[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        tot=0
        io_array=np.array(in_df['BATCH ID'])
        p_array=np.array(df1['BATCH ID'])
        for i in range(len(io_array)):
            if io_array[i] in np.array(p_array):
                tot+=1
            else:
                pass
        st.write("Total number of common batches are: ",str(tot))
    
    if st.button("Submit"):
    
        st.session_state.current_page = 'pumpdown1_overview'
        compute(st.session_state.process_data,st.session_state.pre_post_data)
        st.rerun()
    if st.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()     
elif st.session_state.current_page=='HV II main':
    st.header("Upload your data files (HV II):")
    
    pre_post_file_II = st.file_uploader("Upload Pre/Post Process Data", type=["csv"])
    handle_file_upload(pre_post_file_II, 'pre_post_data_II')
    
    process_file_II = st.file_uploader("Upload Process Data", type=["csv"])
    handle_file_upload(process_file_II, 'process_data_II')
    if st.button("Check common batches"):
        df1 = pd.DataFrame()
        df1 = pd.concat([df1,st.session_state.process_data_II], ignore_index=True)
        df1.dropna()
        df2 = pd.DataFrame()
        df2 = pd.concat([df2,st.session_state.pre_post_data_II], ignore_index=True)  
        new_header = df2.iloc[0]
        in_df = df2[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        tot=0
        io_array=np.array(in_df['BATCH ID'])
        p_array=np.array(df1['BATCH ID'])
        for i in range(len(io_array)):
            if io_array[i] in np.array(p_array):
                tot+=1
            else:
                pass
        st.write("Total number of common batches are: ",str(tot))
    
    if st.button("Submit"):
        st.session_state.current_page = 'pumpdown2_overview'
        compute_II(st.session_state.process_data_II,st.session_state.pre_post_data_II)
        st.rerun()
    if st.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
elif st.session_state.current_page=='glow main':
    st.header("Upload your data files (Glow Discharge):")
    
    pre_post_file_glow = st.file_uploader("Upload Pre/Post Process Data", type=["csv"])
    handle_file_upload(pre_post_file_glow, 'pre_post_data_glow')
    
    process_file_glow = st.file_uploader("Upload Process Data", type=["csv"])
    handle_file_upload(process_file_glow, 'process_data_glow')
    if st.button("Check common batches"):
        df1 = pd.DataFrame()
        df1 = pd.concat([df1,st.session_state.process_data_glow], ignore_index=True)
        df1.dropna()
        df2 = pd.DataFrame()
        df2 = pd.concat([df2,st.session_state.pre_post_data_glow], ignore_index=True)  
        new_header = df2.iloc[0]
        in_df = df2[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        tot=0
        io_array=np.array(in_df['BATCH ID'])
        p_array=np.array(df1['BATCH ID'])
        for i in range(len(io_array)):
            if io_array[i] in np.array(p_array):
                tot+=1
            else:
                pass
        st.write("Total number of common batches are: ",str(tot))
    
    if st.button("Submit"):
        st.session_state.current_page = 'glow_overview'
        compute_glow(st.session_state.process_data_glow,st.session_state.pre_post_data_glow)
        st.rerun()
    if st.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
elif st.session_state.current_page=='ac main':
    st.header("Upload your data files (Arc Cleaning):")
    
    pre_post_file_ac = st.file_uploader("Upload Pre/Post Process Data", type=["csv"])
    handle_file_upload(pre_post_file_ac, 'pre_post_data_ac')
    
    process_file_ac = st.file_uploader("Upload Process Data", type=["csv"])
    handle_file_upload(process_file_ac, 'process_data_ac')
    if st.button("Check common batches"):
        df1 =st.session_state.process_data_ac
        df1.dropna()
        df2 = st.session_state.pre_post_data_ac
        in_df = df2[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        tot=0
        io_array=np.array(in_df['BATCH ID'])
        p_array=np.array(df1['BATCH ID'])
        for i in range(len(io_array)):
            if io_array[i] in np.array(p_array):
                tot+=1
            else:
                pass
        st.write("Total number of common batches are: ",str(tot))
    
    if st.button("Submit"):
        st.session_state.current_page = 'ac_overview'
        compute_ac(st.session_state.process_data_ac,st.session_state.pre_post_data_ac)
        st.rerun()
    if st.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
elif st.session_state.current_page=='ae main':
    st.header("Upload your data files (Arc Etching):")
    
    pre_post_file_ae = st.file_uploader("Upload Pre/Post Process Data", type=["csv"])
    handle_file_upload(pre_post_file_ae, 'pre_post_data_ae')
    
    process_file_ae = st.file_uploader("Upload Process Data", type=["csv"])
    handle_file_upload(process_file_ae, 'process_data_ae')
    if st.button("Check common batches"):
        df1 =st.session_state.process_data_ae
        df1.dropna()
        df2 = st.session_state.pre_post_data_ae
        in_df = df2[:]
        in_df.dropna()
        in_df=in_df.drop_duplicates(subset=['BATCH ID'])
        in_df.reset_index(drop=True, inplace=True)
        tot=0
        io_array=np.array(in_df['BATCH ID'])
        p_array=np.array(df1['BATCH ID'])
        for i in range(len(io_array)):
            if io_array[i] in np.array(p_array):
                tot+=1
            else:
                pass
        st.write("Total number of common batches are: ",str(tot))
    
    if st.button("Submit"):
        st.session_state.current_page = 'ae_overview'
        compute_ae(st.session_state.process_data_ae,st.session_state.pre_post_data_ae)
        st.rerun()
    if st.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
elif st.session_state.current_page == 'dashboard':
    st.markdown('<div class="main-heading">PVD Dashboard V4.0 - 03Oct24 -</div>', unsafe_allow_html=True)
    st.header("Select the Process")
    st.markdown(
        """
        <style>
        .stButton>button {
            width:130px;
            height:100px;
            background-color: #008081;
            color: white;
            border: none;
            padding: 5px 20px;
            margin: 0px;
            border-radius: 3px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Custom CSS for button grid and styling
    # Create interactive buttons in a grid layout
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        if st.button("PUMPDOWN HV I"):
            change_date(st.session_state.start_date,st.session_state.end_date,[True, True, True])
            st.session_state.current_page='pumpdown1_overview'
            st.rerun()
    with col2:
        if st.button("GLOW DISCHARGE"):
            region_selections_glow = [True, False, False, False, False]

            change_date_glow(st.session_state.start_date_glow,st.session_state.end_date_glow,region_selections_glow)
            st.session_state.current_page='glow_overview'
            st.rerun()
    with col3:
        if st.button("PUMPDOWN HV II"):
            change_date_II(st.session_state.start_date_II,st.session_state.end_date_II,[True, True, True])
            st.session_state.current_page='pumpdown2_overview'
            st.rerun()    
    with col4:
        if st.button("ARC CLEANING"):
            region_selections_ac = [True, False, False, False,False,False, False]
            change_date_ac(st.session_state.start_date_ac,st.session_state.end_date_ac,region_selections_ac)
            st.session_state.current_page='ac_overview'
            st.rerun()  
    with col5:
        if st.button("ARC ETCHING"):
            region_selections_ae = [True, False, False, False,False,False, False, False,"All"]
            change_date_ae(st.session_state.start_date_ae,st.session_state.end_date_ae,region_selections_ae)
            st.session_state.current_page='ae_overview'
            st.rerun()  
    col6, col7, col8, col9, col10 = st.columns(5)

    with col6:
        if st.button("PRE SPUTTERING"):
            region_selections_ps = ["All Batches", False,False,False, False, False,"All"]
            change_date_ps(st.session_state.start_date_ps,st.session_state.end_date_ps,region_selections_ps)
            st.session_state.current_page='ps_overview'
            st.rerun()  
        if st.button(""):
            pass
    with col7:
        if st.button("Ti COATING"):
            region_selections_ti = ["All Batches", False,False,False, False, False]
            change_date_ti(st.session_state.start_date_ti,st.session_state.end_date_ti,region_selections_ti)
            st.session_state.current_page='ti_overview'
            st.rerun()         
        if st.button("TiCN COATING (Only IPB)"):
            st.write("Under Construction")
    with col8:
        if st.button("TiN COATING (Only IPRG)"):
            st.write("Under Construction")
        if st.button("TiCN COATING (Only IPRG)"):
            st.write("Under Construction")
    with col9:
        if st.button("GLUE LAYER (Only IPRG)"):
            st.write("Under Construction")
        if st.button("RG COATING (Only IPRG)"):
            st.write("Under Construction")
    with col10:
        if st.button("VENTING"):
            st.write("Under Construction")
        if st.button(" "):
            pass

    st.session_state.logged_in = False
    PASSWORD='admin'
    password = st.text_input("Enter Password to Update files", type="password")

    if password == PASSWORD:
        st.session_state.logged_in = True
        st.success("Login successful!")
    else:
        st.error("Invalid username or password")
    if st.session_state.logged_in==True:
        uploaded_zip = st.file_uploader("Upload Additional Data (zipped folder)", type=["zip"])
        if st.button("Submit"):
            if uploaded_zip is not None:
                # Define paths for extraction
                import os
                extract_path = "extracted_folder"
                import shutil
                if os.path.exists(extract_path):
                    shutil.rmtree(extract_path)
                os.makedirs(extract_path, exist_ok=True)

                # Extract the zip file
                with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                    st.success("Folder extracted successfully!")

                # Identify the root folder inside the extracted path
                root_folder = os.listdir(extract_path)[0]  # Assumes there's only one root folder inside
                root_path = os.path.join(extract_path, root_folder)

                # Define subfolder names and their corresponding DataFrame variable names
                folder_mapping = {
                    "Arc Cleaning": "arc_cleaning_df",
                    "Arc Etching": "arc_etching_df",
                    "Glow Discharge": "glow_discharge_df",
                    "HV1": "hv1_df",
                    "HV2": "hv2_df",
                    "Pre Sputtering": "pre_sputtering_df",
                    "Ti Coating": "ti_coating_df"

                }

                # Initialize a dictionary to hold the combined DataFrames
                dataframes = {}

                # Iterate over each folder and combine CSV files within each subfolder
                for folder_name, df_name in folder_mapping.items():
                    folder_path = os.path.join(root_path, folder_name)
                    combined_df = pd.DataFrame()

                    if os.path.exists(folder_path):
                        # Combine all CSV files in the specified folder
                        for csv_file in os.listdir(folder_path):
                            if csv_file.endswith(".csv"):
                                file_path = os.path.join(folder_path, csv_file)
                                df = pd.read_csv(file_path)
                                combined_df = pd.concat([combined_df, df], ignore_index=True)

                        # Store the combined DataFrame in the dictionary
                        dataframes[df_name] = combined_df
                        st.write(f"Combined CSV files from {folder_name} into DataFrame: {df_name}")
                    else:
                        st.warning(f"Folder '{folder_name}' not found inside '{root_folder}'.")

                # Find and load the Excel file as a DataFrame named 'io_data_df'
                for file in os.listdir(root_path):
                    if file.endswith(".csv"):
                        csv_path = os.path.join(root_path, file)
                        io_data_df = pd.read_csv(csv_path)
                        dataframes['io_data_df'] = io_data_df
                        st.write("CSV file loaded as DataFrame: io_data_df")

                # Display the loaded DataFrames
                for key, df in dataframes.items():
                    st.write(f"DataFrame '{key}':", df)
                compute(True, dataframes['hv1_df'], dataframes['io_data_df'])
                compute_II(True, dataframes['hv2_df'], dataframes['io_data_df'])
                compute_glow(True, dataframes['glow_discharge_df'], dataframes['io_data_df'])
                compute_ps(True, dataframes['pre_sputtering_df'], dataframes['io_data_df'])
                compute_ti(True, dataframes['ti_coating_df'], dataframes['io_data_df'])
                compute_ac(True, dataframes['arc_cleaning_df'], dataframes['io_data_df'])
                compute_ae(True, dataframes['arc_etching_df'], dataframes['io_data_df'])

                # Delete the extracted folder


elif st.session_state.current_page == 'pumpdown1_overview':
    # Custom CSS for the pop-up bar at the bottom
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    green_region = st.sidebar.checkbox("Green region",value=st.session_state.region_selections[0])
    yellow_region = st.sidebar.checkbox("Yellow region",value=st.session_state.region_selections[1])
    red_region = st.sidebar.checkbox("Red region",value=st.session_state.region_selections[2])
    region_selections = [green_region, yellow_region, red_region]
    #st.session_state.green_selection=green_region
    #st.session_state.yellow_selection=yellow_region
    #st.session_state.red_selection=red_region
    st.session_state.region_selections=region_selections
    print(st.session_state.refined_df.iloc[0])
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        
        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Pumpdown Trend Analysis"):
        st.session_state.current_page = 'pta'
        st.rerun()
    if st.sidebar.button("Individual Batch Analysis"):
        st.session_state.current_page = 'iba'
        st.rerun()
    if st.sidebar.button("Input Specific Analysis"):
        st.session_state.current_page = 'isa'
        st.rerun()
    if st.sidebar.button("ML Model Inferences"):
        st.session_state.current_page = 'mmi'
        st.rerun()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    st.header("Pumpdown 1 Overview")
    
    plot_corr()
    #plot_trend()
    plot_bellcurve()

elif st.session_state.current_page == 'pumpdown2_overview':
    # Custom CSS for the pop-up bar at the bottom
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_II,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_II,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    green_region = st.sidebar.checkbox("Green region",value=st.session_state.region_selections_II[0])
    yellow_region = st.sidebar.checkbox("Yellow region",value=st.session_state.region_selections_II[1])
    red_region = st.sidebar.checkbox("Red region",value=st.session_state.region_selections_II[2])
    region_selections = [green_region, yellow_region, red_region]
    #st.session_state.green_selection=green_region
    #st.session_state.yellow_selection=yellow_region
    #st.session_state.red_selection=red_region
    st.session_state.region_selections_II=region_selections
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        
        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_II(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("HV II Trend Analysis"):
        st.session_state.current_page = 'pta_II'
        st.rerun()
    if st.sidebar.button("Individual Batch Analysis"):
        st.session_state.current_page = 'iba_II'
        st.rerun()
    if st.sidebar.button("Input Specific Analysis"):
        st.session_state.current_page = 'isa_II'
        st.rerun()
    if st.sidebar.button("ML Model Inferences"):
        st.session_state.current_page = 'mmi_II'
        st.rerun()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    st.header("High Vacuum II Overview")
    
    plot_corr_II()
    #plot_trend()
    plot_bellcurve_II()
elif st.session_state.current_page == 'glow_overview':
    # Custom CSS for the pop-up bar at the bottom
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_glow,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_glow,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches"))
    region_selections = [False,False,False,False,False,]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage Irregularities", value=True)
        arc_irreg = st.sidebar.checkbox("Arc Irregularities", value=True)
        current_irreg = st.sidebar.checkbox("Current Irregularities", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas Irregularities", value=True)
        region_selections = [False, voltage_irreg, arc_irreg, current_irreg, ar_gas_irreg]
    else:
        region_selections[0] = True  # All batches selected
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_glow(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Glow Discharge Trend Analysis"):
        st.session_state.current_page = 'gd_ta'
        st.rerun()
    if st.sidebar.button("Individual Batch Analysis"):
        st.session_state.current_page = 'gd_iba'
        st.rerun()
    if st.sidebar.button("Input Specific Analysis"):
        st.session_state.current_page = 'gd_isa'
        st.rerun()
    if st.sidebar.button("ML Model Inferences"):
        st.session_state.current_page = 'mmi_glow_discharge'
        st.rerun()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    st.header("Glow Discharge Overview")
    plot_glow_irr()
    plot_corr_glow()
    #plot_bellcurve_II()
elif st.session_state.current_page == 'ac_overview':
    # Custom CSS for the pop-up bar at the bottom
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ac,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ac,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches"))
    region_selections = [False,False,False,False,False,False,False]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage Irregularities", value=True)
        arc_irreg = st.sidebar.checkbox("Arc Irregularities", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current Irregularities", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current Irregularities", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current Irregularities", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas Irregularities", value=True)
        region_selections = [False, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg]
    else:
        region_selections[0] = True  # All batches selected
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_ac(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Arc Cleaning Trend Analysis"):
        st.session_state.current_page = 'ac_ta'
        st.rerun()
    if st.sidebar.button("Individual Batch Analysis"):
        st.session_state.current_page = 'ac_iba'
        st.rerun()
    if st.sidebar.button("Input Specific Analysis"):
        st.session_state.current_page = 'ac_isa'
        st.rerun()
    if st.sidebar.button("ML Model Inferences"):
        st.sidebar.write('Under construction')
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    st.header("Arc Cleaning Overview")
    plot_ac_irr()
    plot_corr_ac()
    #plot_bellcurve_II()
elif st.session_state.current_page == 'ae_overview':
    # Custom CSS for the pop-up bar at the bottom
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ae,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ae,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    step_options=['All','6', '7', '8', '9', '10']
    default_value = 'All'
    step_type = st.sidebar.selectbox("Select Step:",step_options)
    recipe_type = st.sidebar.radio("Select Recipe Type:", ("All Batches", "Old Recipe", "New Recipe"))

    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False,False,False,step_type]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities

    region_selections[0]=recipe_type
    region_selections[1]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [recipe_type, batch_type, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg,step_type]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [recipe_type, batch_type, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg,step_type]
    elif batch_type == "All Batches":
        region_selections[1] = batch_type 
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_ae(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Arc Etching Trend Analysis"):
        st.session_state.current_page = 'ae_ta'
        st.rerun()
    if st.sidebar.button("Individual Batch Analysis"):
        st.session_state.current_page = 'ae_iba'
        st.rerun()
    if st.sidebar.button("Input Specific Analysis"):
        st.session_state.current_page = 'ae_isa'
        st.rerun()
    if st.sidebar.button("ML Model Inferences"):
        st.sidebar.write('Under construction')

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    st.header("Arc Etching Overview")
    plot_ae_irr(region_selections)
    plot_corr_ae()
    #plot_bellcurve_II()
elif st.session_state.current_page == 'ps_overview':
    # Custom CSS for the pop-up bar at the bottom
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ps,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ps,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    step_options=['All','11', '12', '13']
    default_value = 'All'
    step_type = st.sidebar.selectbox("Select Step:",step_options)
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False,step_type]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    region_selections[0]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg,step_type]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg,step_type]
    elif batch_type == "All Batches":
        region_selections[0] = batch_type 
    if st.sidebar.button("Submit Filter"):
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        change_date_ps(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Pre Sputtering Trend Analysis"):
        st.session_state.current_page = 'ps_ta'
        st.rerun()
    if st.sidebar.button("Individual Batch Analysis"):
        st.session_state.current_page = 'ps_iba'
        st.rerun()
    if st.sidebar.button("Input Specific Analysis"):
        st.session_state.current_page = 'ps_isa'
        st.rerun()
    if st.sidebar.button("ML Model Inferences"):
        st.sidebar.write('Under construction')

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    st.header("Pre Sputtering Overview")
    plot_ps_irr(region_selections)
    plot_corr_ps()
    #plot_bellcurve_II()
elif st.session_state.current_page == 'ti_overview':
    # Custom CSS for the pop-up bar at the bottom
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ti,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ti,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    region_selections[0]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg]
    elif batch_type == "All Batches":
        region_selections[0] = batch_type 
    if st.sidebar.button("Submit Filter"):
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        change_date_ti(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Ti Coating Trend Analysis"):
        st.session_state.current_page = 'ti_ta'
        st.rerun()
    if st.sidebar.button("Individual Batch Analysis"):
        st.session_state.current_page = 'ti_iba'
        st.rerun()
    if st.sidebar.button("Input Specific Analysis"):
        st.session_state.current_page = 'ti_isa'
        st.rerun()
    if st.sidebar.button("ML Model Inferences"):
        st.sidebar.write('Under construction')

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'dashboard'
        st.rerun()
    st.header("Ti Coating Overview")
    plot_ti_irr(region_selections)
    plot_corr_ti()
    #plot_bellcurve_II()
elif st.session_state.current_page == 'mmi':
    st.header("ML Model Inferences")
    st.sidebar.title("Customize Parameters")
    from datetime import date
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    green_region = st.sidebar.checkbox("Green region",value=st.session_state.region_selections[0])
    yellow_region = st.sidebar.checkbox("Yellow region",value=st.session_state.region_selections[1])
    red_region = st.sidebar.checkbox("Red region",value=st.session_state.region_selections[2])
    region_selections = [green_region, yellow_region, red_region]
    #st.session_state.green_selection=green_region
    #st.session_state.yellow_selection=yellow_region
    #st.session_state.red_selection=red_region
    st.session_state.region_selections=region_selections
    print(st.session_state.refined_df.iloc[0])
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        
        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date(start_date,end_date,region_selections)
        st.rerun()
    r_state = st.sidebar.number_input("Change Random State", min_value=1, max_value=100, step=1, value=39) 
    test_state = st.sidebar.number_input("Change Test Size", min_value=0.1, max_value=0.5, step=0.05, value=0.25) 
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'pumpdown1_overview'
        st.rerun()   
    refined_df=st.session_state.refined_df
    df=refined_df.copy()
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    df['BATCH DATE'] = pd.to_datetime(df['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S').dt.date
    df['DAY OF YEAR'] = pd.to_datetime(df['BATCH DATE']).dt.dayofyear
    product_dict=[]
    import json
    for i in range(len(df)):
        product_dict.append(json.loads(df["PRODUCT TYPE"][i]))
    product_dict = merge_dicts_with_zero_values(product_dict)
    df["PRODUCT TYPE"]=product_dict
    product_types = ['bracelet', 'clasp', 'pin', 'pushbutton', 'buckles', 'straps', 'endpiece', 'cases', 'crown', 'link', 'flap']
    for product in product_types:
        df[product] = df['PRODUCT TYPE'].apply(lambda x: x.get(product, 0))
    X = df[['T mins', 'SHIFT TYPE', 'MATERIAL TYPE', 'COATING TYPE', 'DAY OF YEAR'] + product_types]
    y = df['RH mins']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_state, random_state=r_state)
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['T mins', 'DAY OF YEAR']),
            ('cat', OneHotEncoder(), ['SHIFT TYPE', 'MATERIAL TYPE', 'COATING TYPE'])
        ],
        remainder='passthrough'  # Keep the product type columns as they are
    )
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=r_state))
    ])
    model.fit(X_train, y_train)

    # Step 8: Make predictions and evaluate the model
    y_pred = model.predict(X_test)
    st.write("Model : Random Forest Regressor")
    st.write("Mean Absolute Error (MAE):", str(np.round(mean_absolute_error(y_test, y_pred),2)))
    st.write("Mean Squared Error (MSE):", str(np.round(mean_squared_error(y_test, y_pred),2)))
    st.write("Root Mean Squared Error (RMSE):", str(np.round(mean_squared_error(y_test, y_pred, squared=False),2)))
    st.write("----")
    st.write("R-squared:", str(np.round(r2_score(y_test, y_pred),2)))
    st.write("----")
    feature_importances = model.named_steps['regressor'].feature_importances_

    # Extract feature names
    encoder = preprocessor.named_transformers_['cat']
    feature_names = encoder.get_feature_names_out(['SHIFT TYPE', 'MATERIAL TYPE', 'COATING TYPE'])

    # Combine feature names with other features
    feature_names_combined = ['T mins', 'DAY OF YEAR'] + list(feature_names) + product_types

    # Create a DataFrame for feature importances
    importance_df = pd.DataFrame({
        'Feature': feature_names_combined,
        'Importance': feature_importances
    }).sort_values(by='Importance', ascending=False)
    c_df = pd.DataFrame({
        'Index': np.arange(len(y_test)),
        'y_pred': y_pred,
        'y_test': y_test
    })

    # Create an Altair chart
    chart = alt.Chart(c_df).mark_line().encode(
        x='Index:O',  # Use 'O' for ordinal type to ensure the x-axis is discrete
        y='value:Q',
        color='variable:N'
    ).transform_fold(
        ['y_pred', 'y_test'],
        as_=['variable', 'value']
    ).properties(
        title='Predictions vs. Actual Values',
        width=700,
        height=300
    )
    st.altair_chart(chart)
    st.table(importance_df)
    import shap
    # Transform the data
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    # Get feature names after transformation
    feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(['SHIFT TYPE', 'MATERIAL TYPE', 'COATING TYPE'])
    feature_names = ['T mins', 'DAY OF YEAR']+list(feature_names)  + product_types

    # Fit the SHAP explainer
    explainer = shap.TreeExplainer(model.named_steps['regressor'])
    shap_values = explainer.shap_values(X_test_transformed)

    # Visualize SHAP values
    shap.summary_plot(shap_values, X_test_transformed, feature_names=feature_names)

    # Convert SHAP values to DataFrame
    shap_df = pd.DataFrame(shap_values, columns=feature_names)

    # Calculate the mean absolute SHAP values for each feature
    mean_abs_shap_values = shap_df.abs().mean().reset_index()
    mean_abs_shap_values.columns = ['Feature', 'Mean Absolute SHAP Value']

    # Create an Altair bar chart for feature importance
    shap_plot = alt.Chart(mean_abs_shap_values).mark_bar().encode(
        y=alt.Y('Feature', sort='-x', title='Features'),  # Sorting by importance
        x=alt.X('Mean Absolute SHAP Value', title='Mean Absolute SHAP Value'),
        color=alt.Color('Feature', legend=None)  # Optional: Add color for distinction
    ).properties(
        title='Feature Importance based on SHAP Values',
        width=600,
        height=400
    )

    # Display the Altair chart in Streamlit
    st.altair_chart(shap_plot)

    plt.figure()  # Create a new figure
    shap.summary_plot(shap_values, X_test_transformed, feature_names=feature_names, show=False)

# Display the plot in Streamlit
    st.pyplot(plt.gcf())
elif st.session_state.current_page == 'mmi_II':
    st.header("ML Model Inferences")
    from datetime import date

    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_II,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_II,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    green_region = st.sidebar.checkbox("Green region",value=st.session_state.region_selections_II[0])
    yellow_region = st.sidebar.checkbox("Yellow region",value=st.session_state.region_selections_II[1])
    red_region = st.sidebar.checkbox("Red region",value=st.session_state.region_selections_II[2])
    region_selections = [green_region, yellow_region, red_region]
    #st.session_state.green_selection=green_region
    #st.session_state.yellow_selection=yellow_region
    #st.session_state.red_selection=red_region
    st.session_state.region_selections_II=region_selections
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        
        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_II(start_date,end_date,region_selections)
        st.rerun()
    r_state = st.sidebar.number_input("Change Random State", min_value=1, max_value=100, step=1, value=40) 
    test_state = st.sidebar.number_input("Change Test Size", min_value=0.1, max_value=0.5, step=0.05, value=0.2) 
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'pumpdown2_overview'
        st.rerun()   
    refined_df_II=st.session_state.refined_df_II
    df=refined_df_II.copy()
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    df['BATCH DATE'] = pd.to_datetime(df['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S').dt.date
    df['DAY OF YEAR'] = pd.to_datetime(df['BATCH DATE']).dt.dayofyear
    if 'refined_df' in st.session_state:
        df['RH mins']=st.session_state.I_II_df['RH mins']
    product_dict=[]
    import json
    for i in range(len(df)):
        product_dict.append(json.loads(df["PRODUCT TYPE"][i]))
    product_dict = merge_dicts_with_zero_values(product_dict)
    df["PRODUCT TYPE"]=product_dict
    product_types = ['bracelet', 'clasp', 'pin', 'pushbutton', 'buckles', 'straps', 'endpiece', 'cases', 'crown', 'link', 'flap']
    for product in product_types:
        df[product] = df['PRODUCT TYPE'].apply(lambda x: x.get(product, 0))
    X = df[['SHIFT TYPE II', 'MATERIAL TYPE', 'COATING TYPE', 'DAY OF YEAR'] + product_types]
    y = df['H_II mins']
    if 'refined_df' in st.session_state:
        X = df[['SHIFT TYPE II', 'MATERIAL TYPE', 'COATING TYPE', 'RH mins', 'DAY OF YEAR'] + product_types]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_state, random_state=r_state)
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['DAY OF YEAR']),
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['SHIFT TYPE II', 'MATERIAL TYPE', 'COATING TYPE'])
        ],
        remainder='passthrough'  # Keep the product type columns as they are
    )
    if 'refined_df' in st.session_state:
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), ['RH mins','DAY OF YEAR']),
                ('cat', OneHotEncoder(handle_unknown='ignore'), ['SHIFT TYPE II', 'MATERIAL TYPE', 'COATING TYPE'])
            ],
            remainder='passthrough'  # Keep the product type columns as they are
        )
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(random_state=r_state))
    ])
    model.fit(X_train, y_train)

    # Step 8: Make predictions and evaluate the model
    y_pred = model.predict(X_test)
    st.write("Model : Random Forest Regressor")
    st.write("Mean Absolute Error (MAE):", str(np.round(mean_absolute_error(y_test, y_pred),2)))
    st.write("Mean Squared Error (MSE):", str(np.round(mean_squared_error(y_test, y_pred),2)))
    st.write("Root Mean Squared Error (RMSE):", str(np.round(mean_squared_error(y_test, y_pred, squared=False),2)))
    st.write("----")
    st.write("R-squared:", str(np.round(r2_score(y_test, y_pred),2)))
    st.write("----")
    feature_importances = model.named_steps['regressor'].feature_importances_

    # Extract feature names
    encoder = preprocessor.named_transformers_['cat']
    feature_names = encoder.get_feature_names_out(['SHIFT TYPE II', 'MATERIAL TYPE', 'COATING TYPE'])

    # Combine feature names with other features
    feature_names_combined = ['DAY OF YEAR'] + list(feature_names) + product_types
    if 'refined_df' in st.session_state:
        feature_names_combined = ['HV I time','DAY OF YEAR'] + list(feature_names) + product_types
    # Create a DataFrame for feature importances
    importance_df = pd.DataFrame({
        'Feature': feature_names_combined,
        'Importance': feature_importances
    }).sort_values(by='Importance', ascending=False)
    c_df = pd.DataFrame({
        'Index': np.arange(len(y_test)),
        'y_pred': y_pred,
        'y_test': y_test
    })

    # Create an Altair chart
    chart = alt.Chart(c_df).mark_line().encode(
        x='Index:O',  # Use 'O' for ordinal type to ensure the x-axis is discrete
        y='value:Q',
        color='variable:N'
    ).transform_fold(
        ['y_pred', 'y_test'],
        as_=['variable', 'value']
    ).properties(
        title='Predictions vs. Actual Values',
        width=700,
        height=300
    )
    st.altair_chart(chart)
    st.table(importance_df)
    import shap
    # Transform the data
    X_train_transformed = preprocessor.fit_transform(X_train)
    X_test_transformed = preprocessor.transform(X_test)

    # Get feature names after transformation
    feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(['SHIFT TYPE II', 'MATERIAL TYPE', 'COATING TYPE'])
    feature_names = ['DAY OF YEAR']+list(feature_names)  + product_types

    # Fit the SHAP explainer
    explainer = shap.TreeExplainer(model.named_steps['regressor'])
    shap_values = explainer.shap_values(X_test_transformed)

    # Visualize SHAP values
    shap.summary_plot(shap_values, X_test_transformed, feature_names=feature_names)

    # Convert SHAP values to DataFrame
    shap_df = pd.DataFrame(shap_values, columns=feature_names)

    # Calculate the mean absolute SHAP values for each feature
    mean_abs_shap_values = shap_df.abs().mean().reset_index()
    mean_abs_shap_values.columns = ['Feature', 'Mean Absolute SHAP Value']

    # Create an Altair bar chart for feature importance
    shap_plot = alt.Chart(mean_abs_shap_values).mark_bar().encode(
        y=alt.Y('Feature', sort='-x', title='Features'),  # Sorting by importance
        x=alt.X('Mean Absolute SHAP Value', title='Mean Absolute SHAP Value'),
        color=alt.Color('Feature', legend=None)  # Optional: Add color for distinction
    ).properties(
        title='Feature Importance based on SHAP Values',
        width=600,
        height=400
    )

    # Display the Altair chart in Streamlit
    st.altair_chart(shap_plot)

    plt.figure()  # Create a new figure
    shap.summary_plot(shap_values, X_test_transformed, feature_names=feature_names, show=False)
elif st.session_state.current_page == 'mmi_glow_discharge':
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.multioutput import MultiOutputClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report
    st.header("ML Model Inferences")
    refined_df_glow=st.session_state.refined_df_glow
    print(len(refined_df_glow))
    st.sidebar.title("Customize Parameters")   
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_glow,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_glow,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches"))
    region_selections = [True,False,False,False,False,]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage Irregularities", value=True)
        arc_irreg = st.sidebar.checkbox("Arc Irregularities", value=True)
        current_irreg = st.sidebar.checkbox("Current Irregularities", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas Irregularities", value=True)
        region_selections = [False, voltage_irreg, arc_irreg, current_irreg, ar_gas_irreg]
    else:
        region_selections[0] = True  # All batches selected
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_glow(start_date,end_date,region_selections)
        st.rerun()
    r_state = st.sidebar.number_input("Change Random State", min_value=1, max_value=100, step=1, value=47) 
    test_state = st.sidebar.number_input("Change Test Size", min_value=0.1, max_value=0.5, step=0.05, value=0.2) 
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'glow_overview'
        st.rerun() 
    
    df=refined_df_glow.copy()
    df['BATCH DATE'] = pd.to_datetime(df['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S').dt.date
    df['DAY OF YEAR'] = pd.to_datetime(df['BATCH DATE']).dt.dayofyear
    product_dict=[]
    import json
    for i in range(len(df)):
        product_dict.append(json.loads(df["PRODUCT TYPE"][i]))
    product_dict = merge_dicts_with_zero_values(product_dict)
    df["PRODUCT TYPE"]=product_dict
    product_types = ['bracelet', 'clasp', 'pin', 'pushbutton', 'buckles', 'straps', 'endpiece', 'cases', 'crown', 'link', 'flap']
    for product in product_types:
        df[product] = df['PRODUCT TYPE'].apply(lambda x: x.get(product, 0))
    X = df[['SHIFT TYPE', 'MATERIAL TYPE', 'COATING TYPE', 'DAY OF YEAR'] + product_types+ ['V total','I total', 'Gas total', 'Arc total']]
    y = df[['V Irregulars', 'Bias Arc Irregulars', 'I Irregulars', 'Ar Gas Irregulars']].applymap(lambda x: 1 if x else 0)
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_state, random_state=r_state)

    # Define the preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), ['DAY OF YEAR', 'V total', 'I total', 'Gas total', 'Arc total']),
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['SHIFT TYPE', 'MATERIAL TYPE', 'COATING TYPE'])
        ],
        remainder='passthrough'  # Keep the product type columns as they are
    )

    # Define the Random Forest model pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', MultiOutputClassifier(RandomForestClassifier(random_state=42)))
    ])

    # Fit the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

        # Evaluate the model
    report = classification_report(y_test, y_pred, output_dict=True, target_names=y.columns)

    # Convert report to a DataFrame
    report_df = pd.DataFrame(report).transpose()

    # Display the classification report as a table in Streamlit
    st.write("Classification Report")
    st.dataframe(report_df.iloc[:-4,:]) 
    feature_names = (
        list(preprocessor.transformers_[0][1].get_feature_names_out(['DAY OF YEAR', 'V total', 'I total', 'Gas total', 'Arc total'])) +
        list(preprocessor.transformers_[1][1].get_feature_names_out(['SHIFT TYPE', 'MATERIAL TYPE', 'COATING TYPE'])) +
        product_types
    )

    # Extract feature importances from each Random Forest model in the MultiOutputClassifier
    importances_dict = {}
    for idx, estimator in enumerate(model.named_steps['classifier'].estimators_):
        importances = estimator.feature_importances_
        importance_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False)
        importances_dict[y.columns[idx]] = importance_df

    # Display the feature importances for each output variable
    for output_name, importance_df in importances_dict.items():
        st.write(f"\nFeature Importances for {output_name}:\n", importance_df)
elif st.session_state.current_page == 'pta':
    st.header("Pumpdown Trend Analysis")
    st.sidebar.title("Customize Parameters")   
    from datetime import date

    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    green_region = st.sidebar.checkbox("Green region",value=st.session_state.region_selections[0])
    yellow_region = st.sidebar.checkbox("Yellow region",value=st.session_state.region_selections[1])
    red_region = st.sidebar.checkbox("Red region",value=st.session_state.region_selections[2])
    region_selections = [green_region, yellow_region, red_region]
    #st.session_state.green_selection=green_region
    #st.session_state.yellow_selection=yellow_region
    #st.session_state.red_selection=red_region
    st.session_state.region_selections=region_selections
    print(st.session_state.refined_df.iloc[0])
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        
        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date(start_date,end_date,region_selections)
        st.rerun()
    plot_trend()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'pumpdown1_overview'
        st.rerun()    
elif st.session_state.current_page == 'gd_ta':
    st.header("Glow Discharge Trend Analysis")
    st.sidebar.title("Customize Parameters")   
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_glow,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_glow,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches"))
    region_selections = [True,False,False,False,False,]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage Irregularities", value=True)
        arc_irreg = st.sidebar.checkbox("Arc Irregularities", value=True)
        current_irreg = st.sidebar.checkbox("Current Irregularities", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas Irregularities", value=True)
        region_selections = [False, voltage_irreg, arc_irreg, current_irreg, ar_gas_irreg]
    else:
        region_selections[0] = True  # All batches selected
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_glow(start_date,end_date,region_selections)
        st.rerun()
    plot_trend_glow()

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'glow_overview'
        st.rerun()
elif st.session_state.current_page == 'ac_ta':
    st.header("Arc Cleaning Trend Analysis")
    st.sidebar.title("Customize Parameters")   
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ac,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ac,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches"))
    region_selections = [False,False,False,False,False,False,False]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage Irregularities", value=True)
        arc_irreg = st.sidebar.checkbox("Arc Irregularities", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current Irregularities", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current Irregularities", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current Irregularities", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas Irregularities", value=True)
        region_selections = [False, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg]
    else:
        region_selections[0] = True  # All batches selected
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_ac(start_date,end_date,region_selections)
        st.rerun()
    plot_trend_ac()

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ac_overview'
        st.rerun()
elif st.session_state.current_page == 'ae_ta':
    st.header("Arc Etching Trend Analysis")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ae,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ae,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    step_options=['All','6', '7', '8', '9', '10']
    default_value = 'All'
    step_type = st.sidebar.selectbox("Select Step:",step_options)
    recipe_type = st.sidebar.radio("Select Recipe Type:", ("All Batches", "Old Recipe", "New Recipe"))

    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False,False,False,step_type]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities

    region_selections[0]=recipe_type
    region_selections[1]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [recipe_type, batch_type, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg,step_type]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [recipe_type, batch_type, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg,step_type]
    elif batch_type == "All Batches":
        region_selections[1] = batch_type 
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_ae(start_date,end_date,region_selections)
        st.rerun()
    plot_trend_ae()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ae_overview'
        st.rerun()
elif st.session_state.current_page == 'ps_ta':
    st.header("Pre Sputtering Trend Analysis")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ps,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ps,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    step_options=['All','11', '12', '13']
    default_value = 'All'
    step_type = st.sidebar.selectbox("Select Step:",step_options)
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False,step_type]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    region_selections[0]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg,step_type]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg,step_type]
    elif batch_type == "All Batches":
        region_selections[0] = batch_type 
    if st.sidebar.button("Submit Filter"):
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        change_date_ps(start_date,end_date,region_selections)
        st.rerun()
    plot_trend_ps()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ps_overview'
        st.rerun()
elif st.session_state.current_page == 'ti_ta':
    st.header("Pre Sputtering Trend Analysis")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ti,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ti,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    region_selections[0]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg]
    elif batch_type == "All Batches":
        region_selections[0] = batch_type 
    if st.sidebar.button("Submit Filter"):
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        change_date_ti(start_date,end_date,region_selections)
        st.rerun()
    plot_trend_ti()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ti_overview'
        st.rerun()
elif st.session_state.current_page == 'pta_II':
    st.header("Pumpdown HV II Trend Analysis")
    st.sidebar.title("Customize Parameters")   
    from datetime import date

    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_II,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_II,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    green_region = st.sidebar.checkbox("Green region",value=st.session_state.region_selections_II[0])
    yellow_region = st.sidebar.checkbox("Yellow region",value=st.session_state.region_selections_II[1])
    red_region = st.sidebar.checkbox("Red region",value=st.session_state.region_selections_II[2])
    region_selections = [green_region, yellow_region, red_region]
    #st.session_state.green_selection=green_region
    #st.session_state.yellow_selection=yellow_region
    #st.session_state.red_selection=red_region
    st.session_state.region_selections_II=region_selections
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        
        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_II(start_date,end_date,region_selections)
        st.rerun()
    plot_trend_II()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'pumpdown2_overview'
        st.rerun() 
elif st.session_state.current_page == 'iba':
    st.header("Pumpdown 1 Analysis of Individual Batches")
    from datetime import date

    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    green_region = st.sidebar.checkbox("Green region",value=st.session_state.region_selections[0])
    yellow_region = st.sidebar.checkbox("Yellow region",value=st.session_state.region_selections[1])
    red_region = st.sidebar.checkbox("Red region",value=st.session_state.region_selections[2])
    region_selections = [green_region, yellow_region, red_region]
    #st.session_state.green_selection=green_region
    #st.session_state.yellow_selection=yellow_region
    #st.session_state.red_selection=red_region
    st.session_state.region_selections=region_selections
    print(st.session_state.refined_df.iloc[0])
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        
        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'pumpdown1_overview'
        st.rerun()
    batch_options = [f"{st.session_state.df['BATCH ID'][i[0]]}  {st.session_state.df['DATE TIME'][i[0]]}" for i in st.session_state.refined_df['Idxs']]
    selected_batch = st.sidebar.radio("Select a Batch", options=batch_options, index=0)

    # Get the index of the selected batch
    selected_index = batch_options.index(selected_batch)

    # Call the plot function with the selected index
    individual_plot(selected_index)
elif st.session_state.current_page == 'iba_II':
    st.header("Pumpdown II Analysis of Individual Batches")
    from datetime import date

    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_II,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_II,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    green_region = st.sidebar.checkbox("Green region",value=st.session_state.region_selections_II[0])
    yellow_region = st.sidebar.checkbox("Yellow region",value=st.session_state.region_selections_II[1])
    red_region = st.sidebar.checkbox("Red region",value=st.session_state.region_selections_II[2])
    region_selections = [green_region, yellow_region, red_region]
    #st.session_state.green_selection=green_region
    #st.session_state.yellow_selection=yellow_region
    #st.session_state.red_selection=red_region
    st.session_state.region_selections_II=region_selections
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        
        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_II(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'pumpdown2_overview'
        st.rerun()
    batch_options = [f"{st.session_state.df_II['BATCH ID'][i[0]]}  {st.session_state.df_II['DATE TIME'][i[0]]}" for i in st.session_state.refined_df_II['Idxs_II']]
    selected_batch = st.sidebar.radio("Select a Batch", options=batch_options, index=0)

    # Get the index of the selected batch
    selected_index = batch_options.index(selected_batch)

    # Call the plot function with the selected index
    individual_plot_II(selected_index)
elif st.session_state.current_page == 'gd_iba':
    st.header("Glow Discharge Analysis of Individual Batches")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_glow,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_glow,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches"))
    region_selections = [False,False,False,False,False,]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage Irregularities", value=True)
        arc_irreg = st.sidebar.checkbox("Arc Irregularities", value=True)
        current_irreg = st.sidebar.checkbox("Current Irregularities", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas Irregularities", value=True)
        region_selections = [False, voltage_irreg, arc_irreg, current_irreg, ar_gas_irreg]
    else:
        region_selections[0] = True  # All batches selected
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_glow(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'glow_overview'
        st.rerun()
    batch_options = [f"{st.session_state.df_glow['BATCH ID'][i[0]]}  {st.session_state.df_glow['DATE TIME'][i[0]]}" for i in st.session_state.refined_df_glow['Idxs']]
    selected_batch = st.sidebar.radio("Select a Batch", options=batch_options, index=0)

    # Get the index of the selected batch
    selected_index = batch_options.index(selected_batch)

    # Call the plot function with the selected index
    individual_plot_glow(selected_index)
elif st.session_state.current_page == 'ac_iba':
    st.header("Arc Cleaning Analysis of Individual Batches")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ac,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ac,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches"))
    region_selections = [False,False,False,False,False,False,False]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage Irregularities", value=True)
        arc_irreg = st.sidebar.checkbox("Arc Irregularities", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current Irregularities", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current Irregularities", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current Irregularities", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas Irregularities", value=True)
        region_selections = [False, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg]
    else:
        region_selections[0] = True  # All batches selected
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_ac(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ac_overview'
        st.rerun()
    batch_options = [f"{st.session_state.df_ac['BATCH ID'][i[0]]}  {st.session_state.df_ac['DATE TIME'][i[0]]}" for i in st.session_state.refined_df_ac['Idxs']]
    selected_batch = st.sidebar.radio("Select a Batch", options=batch_options, index=0)

    # Get the index of the selected batch
    selected_index = batch_options.index(selected_batch)

    # Call the plot function with the selected index
    individual_plot_ac(selected_index)
elif st.session_state.current_page == 'ae_iba':
    st.header("Arc Etching Analysis of Individual Batches")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ae,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ae,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    step_options=['All','6', '7', '8', '9', '10']
    default_value = 'All'
    step_type = st.sidebar.selectbox("Select Step:",step_options)
    recipe_type = st.sidebar.radio("Select Recipe Type:", ("All Batches", "Old Recipe", "New Recipe"))

    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False,False,False,step_type]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities

    region_selections[0]=recipe_type
    region_selections[1]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [recipe_type, batch_type, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg,step_type]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [recipe_type, batch_type, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg,step_type]
    elif batch_type == "All Batches":
        region_selections[1] = batch_type 
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_ae(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ae_overview'
        st.rerun()
    refined_df_ae= st.session_state.refined_df_ae
    batch_options = [f"{st.session_state.df_ae['BATCH ID'][i[0][0]]}  {st.session_state.df_ae['DATE TIME'][i[0][0]]}" for i in st.session_state.refined_df_ae['Idxs']]
    selected_batch = st.sidebar.radio("Select a Batch", options=batch_options, index=0)
    # Get the index of the selected batch
    selected_index = batch_options.index(selected_batch)

    # Call the plot function with the selected index
    individual_plot_ae(selected_index)
elif st.session_state.current_page == 'ps_iba':
    st.header("Pre Sputtering Analysis of Individual Batches")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ps,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ps,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    step_options=['All','11', '12', '13']
    default_value = 'All'
    step_type = st.sidebar.selectbox("Select Step:",step_options)
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False,step_type]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    region_selections[0]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg,step_type]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg,step_type]
    elif batch_type == "All Batches":
        region_selections[0] = batch_type 
    if st.sidebar.button("Submit Filter"):
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        change_date_ps(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ps_overview'
        st.rerun()
    refined_df_ps= st.session_state.refined_df_ps
    batch_options = [f"{st.session_state.df_ps['BATCH ID'][i[0][0]]}  {st.session_state.df_ps['DATE TIME'][i[0][0]]}" for i in st.session_state.refined_df_ps['Idxs']]
    selected_batch = st.sidebar.radio("Select a Batch", options=batch_options, index=0)
    # Get the index of the selected batch
    selected_index = batch_options.index(selected_batch)

    # Call the plot function with the selected index
    individual_plot_ps(selected_index)
elif st.session_state.current_page == 'ti_iba':
    st.header("Ti Coating Analysis of Individual Batches")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ti,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ti,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    region_selections[0]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg]
    elif batch_type == "All Batches":
        region_selections[0] = batch_type 
    if st.sidebar.button("Submit Filter"):
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        change_date_ti(start_date,end_date,region_selections)
        st.rerun()
    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ti_overview'
        st.rerun()
    refined_df_ti= st.session_state.refined_df_ti
    batch_options = [f"{st.session_state.df_ti['BATCH ID'][i[0][0]]}  {st.session_state.df_ti['DATE TIME'][i[0][0]]}" for i in st.session_state.refined_df_ti['Idxs']]
    selected_batch = st.sidebar.radio("Select a Batch", options=batch_options, index=0)
    # Get the index of the selected batch
    selected_index = batch_options.index(selected_batch)

    # Call the plot function with the selected index
    individual_plot_ti(selected_index)
elif st.session_state.current_page == 'isa':
    st.header("Pumpdown 1 Input Specific Analysis")
    from datetime import date

    st.sidebar.title("Choose the input type(s):")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    green_region = st.sidebar.checkbox("Green region",value=st.session_state.region_selections[0])
    yellow_region = st.sidebar.checkbox("Yellow region",value=st.session_state.region_selections[1])
    red_region = st.sidebar.checkbox("Red region",value=st.session_state.region_selections[2])
    region_selections = [green_region, yellow_region, red_region]
    #st.session_state.green_selection=green_region
    #st.session_state.yellow_selection=yellow_region
    #st.session_state.red_selection=red_region
    st.session_state.region_selections=region_selections
    print(st.session_state.refined_df.iloc[0])
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        
        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date(start_date,end_date,region_selections)
        st.rerun()

    if st.sidebar.button("Material Type"):
        handle_section_toggle("material_type")
    handle_all_checkbox("material_type")

    # Product Type section
    if st.sidebar.button("Product Type"):
        handle_section_toggle("product_type")
    handle_all_checkbox("product_type")

    # Ni Plating Time section
    if st.sidebar.button("Ni Plating Time"):
        handle_section_toggle("ni_plating_time")
    handle_all_checkbox("ni_plating_time")
    if st.sidebar.button("Shift Type"):
        plot_shifts()
    if st.sidebar.button("Pre Storage Type"):
        plot_pre_storage()
    if st.sidebar.button("Coating Type"):
        plot_coating_type()
    if st.sidebar.button("Fluo Level"):
        st.write("Yet to be added")
    if st.sidebar.button("Contact Angle"):
        st.write("Yet to be added")
    if st.sidebar.button("% Cleanliness"):
        st.write("Yet to be added")

    # Submit button
    if st.sidebar.button("Submit"):
        
        submit_inputs()
        st.session_state.open_sections = []
        st.session_state.input_state = {
            "material_type": {"Brass": False, "SS": False},
            "product_type": {
                "Cases": False, "Clasp": False, "Endpiece": False,
                "Crown": False, "Buckles": False, "Flap": False,
                "Bracelet": False, "Pin": False, "Straps": False, "Mix": False
            },
            "ni_plating_time": {"I_series": False, "II_series": False, "III_series": False},
        }

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'pumpdown1_overview'
        st.rerun()
elif st.session_state.current_page == 'isa_II':
    st.header("Pumpdown II Input Specific Analysis")
    from datetime import date

    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_II,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_II,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    green_region = st.sidebar.checkbox("Green region",value=st.session_state.region_selections_II[0])
    yellow_region = st.sidebar.checkbox("Yellow region",value=st.session_state.region_selections_II[1])
    red_region = st.sidebar.checkbox("Red region",value=st.session_state.region_selections_II[2])
    region_selections = [green_region, yellow_region, red_region]
    #st.session_state.green_selection=green_region
    #st.session_state.yellow_selection=yellow_region
    #st.session_state.red_selection=red_region
    st.session_state.region_selections_II=region_selections
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        
        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_II(start_date,end_date,region_selections)
        st.rerun()

    if st.sidebar.button("Material Type"):
        handle_section_toggle("material_type")
    handle_all_checkbox("material_type")

    # Product Type section
    if st.sidebar.button("Product Type"):
        handle_section_toggle("product_type")
    handle_all_checkbox("product_type")

    # Ni Plating Time section
    if st.sidebar.button("Ni Plating Time"):
        handle_section_toggle("ni_plating_time")
    handle_all_checkbox("ni_plating_time")
    if st.sidebar.button("Shift Type"):
        plot_shifts_II()
    if st.sidebar.button("Pre Storage Type"):
        plot_pre_storage_II()
    if st.sidebar.button("Coating Type"):
        plot_coating_type_II()
    if st.sidebar.button("Fluo Level"):
        st.write("Yet to be added")
    if st.sidebar.button("Contact Angle"):
        st.write("Yet to be added")
    if st.sidebar.button("% Cleanliness"):
        st.write("Yet to be added")

    # Submit button
    if st.sidebar.button("Submit"):
        
        submit_inputs_II()
        st.session_state.open_sections = []
        st.session_state.input_state = {
            "material_type": {"Brass": False, "SS": False},
            "product_type": {
                "Cases": False, "Clasp": False, "Endpiece": False,
                "Crown": False, "Buckles": False, "Flap": False,
                "Bracelet": False, "Pin": False, "Straps": False, "Mix": False
            },
            "ni_plating_time": {"I_series": False, "II_series": False, "III_series": False},
        }

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'pumpdown2_overview'
        st.rerun()
elif st.session_state.current_page == 'gd_isa':
    st.header("Glow Discharge Input Specific Analysis")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_glow,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_glow,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches"))
    region_selections = [False,False,False,False,False,]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage Irregularities", value=True)
        arc_irreg = st.sidebar.checkbox("Arc Irregularities", value=True)
        current_irreg = st.sidebar.checkbox("Current Irregularities", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas Irregularities", value=True)
        region_selections = [False, voltage_irreg, arc_irreg, current_irreg, ar_gas_irreg]
    else:
        region_selections[0] = True  # All batches selected
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_glow(start_date,end_date,region_selections)
        st.rerun()

    if st.sidebar.button("Material Type"):
        handle_section_toggle("material_type")
    handle_all_checkbox("material_type")

    # Product Type section
    if st.sidebar.button("Product Type"):
        handle_section_toggle("product_type")
    handle_all_checkbox("product_type")

    # Ni Plating Time section
    if st.sidebar.button("Ni Plating Time"):
        handle_section_toggle("ni_plating_time")
    handle_all_checkbox("ni_plating_time")
    if st.sidebar.button("Shift Type"):
        plot_shifts_glow()
    if st.sidebar.button("Pre Storage Type"):
        plot_pre_storage_glow()
    if st.sidebar.button("Coating Type"):
        plot_coating_type_glow()
    if st.sidebar.button("Fluo Level"):
        st.write("Yet to be added")
    if st.sidebar.button("Contact Angle"):
        st.write("Yet to be added")
    if st.sidebar.button("% Cleanliness"):
        st.write("Yet to be added")

    # Submit button
    if st.sidebar.button("Submit"):
        
        submit_inputs_glow()
        st.session_state.open_sections = []
        st.session_state.input_state = {
            "material_type": {"Brass": False, "SS": False},
            "product_type": {
                "Cases": False, "Clasp": False, "Endpiece": False,
                "Crown": False, "Buckles": False, "Flap": False,
                "Bracelet": False, "Pin": False, "Straps": False, "Mix": False
            },
            "ni_plating_time": {"I_series": False, "II_series": False, "III_series": False},
        }

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'glow_overview'
        st.rerun()
elif st.session_state.current_page == 'ac_isa':
    st.header("Arc Cleaning Input Specific Analysis")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ac,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ac,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches"))
    region_selections = [False,False,False,False,False,False,False]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage Irregularities", value=True)
        arc_irreg = st.sidebar.checkbox("Arc Irregularities", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current Irregularities", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current Irregularities", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current Irregularities", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas Irregularities", value=True)
        region_selections = [False, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg]
    else:
        region_selections[0] = True  # All batches selected
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_ac(start_date,end_date,region_selections)
        st.rerun()

    if st.sidebar.button("Material Type"):
        handle_section_toggle("material_type")
    handle_all_checkbox("material_type")

    # Product Type section
    if st.sidebar.button("Product Type"):
        handle_section_toggle("product_type")
    handle_all_checkbox("product_type")

    # Ni Plating Time section
    if st.sidebar.button("Ni Plating Time"):
        handle_section_toggle("ni_plating_time")
    handle_all_checkbox("ni_plating_time")
    if st.sidebar.button("Shift Type"):
        plot_shifts_ac()
    if st.sidebar.button("Pre Storage Type"):
        plot_pre_storage_ac()
    if st.sidebar.button("Coating Type"):
        plot_coating_type_ac()
    if st.sidebar.button("Fluo Level"):
        st.write("Yet to be added")
    if st.sidebar.button("Contact Angle"):
        st.write("Yet to be added")
    if st.sidebar.button("% Cleanliness"):
        st.write("Yet to be added")

    # Submit button
    if st.sidebar.button("Submit"):
        
        submit_inputs_ac()
        st.session_state.open_sections = []
        st.session_state.input_state = {
            "material_type": {"Brass": False, "SS": False},
            "product_type": {
                "Cases": False, "Clasp": False, "Endpiece": False,
                "Crown": False, "Buckles": False, "Flap": False,
                "Bracelet": False, "Pin": False, "Straps": False, "Mix": False
            },
            "ni_plating_time": {"I_series": False, "II_series": False, "III_series": False},
        }

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ac_overview'
        st.rerun()
elif st.session_state.current_page == 'ae_isa':
    st.header("Arc Etching Input Specific Analysis")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ae,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ae,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    step_options=['All','6', '7', '8', '9', '10']
    default_value = 'All'
    step_type = st.sidebar.selectbox("Select Step:",step_options)
    recipe_type = st.sidebar.radio("Select Recipe Type:", ("All Batches", "Old Recipe", "New Recipe"))

    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False,False,False,step_type]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities

    region_selections[0]=recipe_type
    region_selections[1]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [recipe_type, batch_type, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg,step_type]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        current1_irreg = st.sidebar.checkbox("Arc 1 Current", value=True)
        current2_irreg = st.sidebar.checkbox("Arc 2 Current", value=True)
        current3_irreg = st.sidebar.checkbox("Arc 3 Current", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [recipe_type, batch_type, voltage_irreg, arc_irreg, current1_irreg, current2_irreg, current3_irreg, ar_gas_irreg,step_type]
    elif batch_type == "All Batches":
        region_selections[1] = batch_type 
    if st.sidebar.button("Submit Filter"):
        #st.session_state.start_date = pd.to_datetime(st.session_state.start_date)
        #st.session_state.end_date = pd.to_datetime(st.session_state.end_date)
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)

        #print(st.session_state.start_date,type(st.session_state.start_date))

        change_date_ae(start_date,end_date,region_selections)
        st.rerun()

    if st.sidebar.button("Material Type"):
        handle_section_toggle("material_type")
    handle_all_checkbox("material_type")

    # Product Type section
    if st.sidebar.button("Product Type"):
        handle_section_toggle("product_type")
    handle_all_checkbox("product_type")

    # Ni Plating Time section
    if st.sidebar.button("Ni Plating Time"):
        handle_section_toggle("ni_plating_time")
    handle_all_checkbox("ni_plating_time")
    if st.sidebar.button("Shift Type"):
        plot_shifts_ae()
    if st.sidebar.button("Pre Storage Type"):
        plot_pre_storage_ae()
    if st.sidebar.button("Coating Type"):
        plot_coating_type_ae()
    if st.sidebar.button("Fluo Level"):
        st.write("Yet to be added")
    if st.sidebar.button("Contact Angle"):
        st.write("Yet to be added")
    if st.sidebar.button("% Cleanliness"):
        st.write("Yet to be added")

    # Submit button
    if st.sidebar.button("Submit"):
        
        submit_inputs_ac()
        st.session_state.open_sections = []
        st.session_state.input_state = {
            "material_type": {"Brass": False, "SS": False},
            "product_type": {
                "Cases": False, "Clasp": False, "Endpiece": False,
                "Crown": False, "Buckles": False, "Flap": False,
                "Bracelet": False, "Pin": False, "Straps": False, "Mix": False
            },
            "ni_plating_time": {"I_series": False, "II_series": False, "III_series": False},
        }

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ae_overview'
        st.rerun()
elif st.session_state.current_page == 'ps_isa':
    st.header("Pre Sputtering Input Specific Analysis")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ps,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ps,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    # Radio button for selecting batch type
    step_options=['All','11', '12', '13']
    default_value = 'All'
    step_type = st.sidebar.selectbox("Select Step:",step_options)
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False,step_type]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    region_selections[0]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg,step_type]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg,step_type]
    elif batch_type == "All Batches":
        region_selections[0] = batch_type 
    if st.sidebar.button("Submit Filter"):
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        change_date_ps(start_date,end_date,region_selections)
        st.rerun()

    if st.sidebar.button("Material Type"):
        handle_section_toggle("material_type")
    handle_all_checkbox("material_type")

    # Product Type section
    if st.sidebar.button("Product Type"):
        handle_section_toggle("product_type")
    handle_all_checkbox("product_type")

    # Ni Plating Time section
    if st.sidebar.button("Ni Plating Time"):
        handle_section_toggle("ni_plating_time")
    handle_all_checkbox("ni_plating_time")
    if st.sidebar.button("Shift Type"):
        plot_shifts_ps()
    if st.sidebar.button("Pre Storage Type"):
        plot_pre_storage_ps()
    if st.sidebar.button("Coating Type"):
        plot_coating_type_ps()
    if st.sidebar.button("Fluo Level"):
        st.write("Yet to be added")
    if st.sidebar.button("Contact Angle"):
        st.write("Yet to be added")
    if st.sidebar.button("% Cleanliness"):
        st.write("Yet to be added")

    # Submit button
    if st.sidebar.button("Submit"):
        
        submit_inputs_ac()
        st.session_state.open_sections = []
        st.session_state.input_state = {
            "material_type": {"Brass": False, "SS": False},
            "product_type": {
                "Cases": False, "Clasp": False, "Endpiece": False,
                "Crown": False, "Buckles": False, "Flap": False,
                "Bracelet": False, "Pin": False, "Straps": False, "Mix": False
            },
            "ni_plating_time": {"I_series": False, "II_series": False, "III_series": False},
        }

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ps_overview'
        st.rerun()
elif st.session_state.current_page == 'ti_isa':
    st.header("Ti Coating Input Specific Analysis")
    from datetime import date
    st.sidebar.title("Navigation")
    start_date = st.sidebar.date_input(
        "Select the start date",
        value=st.session_state.start_date_ti,  # Default value set to today's date
        min_value=date(2000, 1, 1),  # Minimum selectable date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    end_date = st.sidebar.date_input(
        "Select the end date",
        value=st.session_state.end_date_ti,  # Default value set to start date
        min_value=date(2000, 1, 1),  # Minimum selectable date is the start date
        max_value=date(2100, 12, 31)  # Maximum selectable date
    )
    batch_type = st.sidebar.radio("Select Batch Type:", ("All Batches", "Irregular Batches","Good Batches"))
    region_selections = [False,False,False,False,False,False]
    # If 'Irregular Batches' is selected, show checkboxes for irregularities
    region_selections[0]=batch_type
    if batch_type == "Irregular Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg]
    elif batch_type == "Good Batches":
        voltage_irreg = st.sidebar.checkbox("Voltage", value=True)
        arc_irreg = st.sidebar.checkbox("Bias Arc", value=True)
        mfp1_irreg = st.sidebar.checkbox("MFP1 Power", value=True)
        mfp2_irreg = st.sidebar.checkbox("MFP2 Power", value=True)
        ar_gas_irreg = st.sidebar.checkbox("Ar Gas", value=True)
        region_selections = [batch_type, voltage_irreg, arc_irreg, mfp1_irreg, mfp2_irreg, ar_gas_irreg]
    elif batch_type == "All Batches":
        region_selections[0] = batch_type 
    if st.sidebar.button("Submit Filter"):
        import datetime
        start_date = datetime.datetime.combine(start_date,datetime.time.min)
        end_date = datetime.datetime.combine(end_date,datetime.time.min)
        change_date_ti(start_date,end_date,region_selections)
        st.rerun()

    if st.sidebar.button("Material Type"):
        handle_section_toggle("material_type")
    handle_all_checkbox("material_type")

    # Product Type section
    if st.sidebar.button("Product Type"):
        handle_section_toggle("product_type")
    handle_all_checkbox("product_type")

    # Ni Plating Time section
    if st.sidebar.button("Ni Plating Time"):
        handle_section_toggle("ni_plating_time")
    handle_all_checkbox("ni_plating_time")
    if st.sidebar.button("Shift Type"):
        plot_shifts_ti()
    if st.sidebar.button("Pre Storage Type"):
        plot_pre_storage_ti()
    if st.sidebar.button("Coating Type"):
        plot_coating_type_ti()
    if st.sidebar.button("Fluo Level"):
        st.write("Yet to be added")
    if st.sidebar.button("Contact Angle"):
        st.write("Yet to be added")
    if st.sidebar.button("% Cleanliness"):
        st.write("Yet to be added")

    # Submit button
    if st.sidebar.button("Submit"):
        
        submit_inputs_ac()
        st.session_state.open_sections = []
        st.session_state.input_state = {
            "material_type": {"Brass": False, "SS": False},
            "product_type": {
                "Cases": False, "Clasp": False, "Endpiece": False,
                "Crown": False, "Buckles": False, "Flap": False,
                "Bracelet": False, "Pin": False, "Straps": False, "Mix": False
            },
            "ni_plating_time": {"I_series": False, "II_series": False, "III_series": False},
        }

    if st.sidebar.button("Back"):
        st.session_state.current_page = 'ti_overview'
        st.rerun()