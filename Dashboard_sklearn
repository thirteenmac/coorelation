


import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import math
import altair as alt
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
from fpdf import FPDF
from PIL import Image
import tempfile
import altair_saver
from selenium import webdriver

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

    elif len(brass_data) == 0 and len(ss_data) != 0:

        d_ss = pd.DataFrame({
            "Ni Plating Time": [x[1] for x in ss_data],
            "H_II Time": [x[2] for x in ss_data],
            "Average H_II Time": [x[2] for x in ss_data],
            "Max H_II Time": [x[3] for x in ss_data],
            "Min H_II Time": [x[4] for x in ss_data],
            "Number of Batches": [x[5] for x in ss_data]
        })

        chart = alt.Chart(d_ss).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title='Ni Plating Time'),
            y='sum(H_II Time):Q',
            color=alt.value('#888888'),  # Set color for SS bars
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
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
            "H_II Time": [x[2] for x in brass_data],
            "Average H_II Time": [x[2] for x in brass_data],
            "Max H_II Time": [x[3] for x in brass_data],
            "Min H_II Time": [x[4] for x in brass_data],
            "Number of Batches": [x[5] for x in brass_data]
        })

        chart = alt.Chart(d_brass).mark_bar().encode(
            x=alt.X('Ni Plating Time:N', title='Ni Plating Time'),
            y='sum(H_II Time):Q',
            color=alt.value('#a07000'),  # Set color for Brass bars
            tooltip=[
                alt.Tooltip('Ni Plating Time:N', title='Ni Plating Time'),
                alt.Tooltip('Average H_II Time:Q', title='Average H_II Time'),
                alt.Tooltip('Max H_II Time:Q', title='Max H_II Time'),
                alt.Tooltip('Min H_II Time:Q', title='Min H_II Time'),
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
        x='Abs Correlation:Q',
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
        if refined_df_II['PVD MACHINE LOADING TIME'][i]!=None and type(refined_df_II['PVD MACHINE LOADING TIME'][i])!=float and ":" not in refined_df_II['PVD MACHINE LOADING TIME'][i] and "#" not in refined_df_II['PVD MACHINE LOADING TIME'][i] and refined_df_II['PVD MACHINE LOADING TIME'][i]!='0':
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
        x='Abs Correlation:Q',
        y=alt.Y('Variable:N', sort='-x'),
        color=alt.Color('Correlation Type:N', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#f02060', '#008081'])),
        tooltip=['Variable', 'Correlation']
    ).properties(
        title='Correlation with H_II mins (Total Pumpdown Time)',
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
        x=alt.X('Count:Q', title='Number of Batches'),
        y=alt.Y('Irregularities:N', sort='-x', title='Irregularities'),
    ).properties(
        title='Count of True Values for Different Irregularities',
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
            print(i)
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
            print(i)
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
def compute(process_data,io_data):
    global df 
    df = pd.DataFrame()
    df=df.dropna(how='all')
    for i in range(len(process_data)):
        df = pd.concat([df,process_data[i]], ignore_index=True)
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
    df2 = pd.DataFrame()
    for i in range(len(io_data)):
        df2 = pd.concat([df2,io_data[i]], ignore_index=True)  
    new_header = df2.iloc[0]
    in_df = df2[:]
    in_df.drop(0)
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
        if r_mins[i]<5 or r_mins[i]>30 or rh_mins[i]<11 or rh_mins[i]>33:
            drop_labels.append(i)
    
    global refined_df
    refined_df=merged_df.drop(labels=drop_labels, axis=0)
    refined_df=refined_df.reset_index(drop=True)

    #st.session_state.start_date=refined_df['BATCH START TIME'][0][:10]
    #st.session_state.end_date=refined_df['BATCH START TIME'][0][:10]
    a=refined_df
    a['BATCH START TIME']=pd.to_datetime(a['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    a = a.sort_values(by='BATCH START TIME')
    a = a.reset_index(drop=True)
    start=pd.to_datetime(a['BATCH START TIME'][0], format='%d/%m/%Y %H:%M:%S')
    stop=pd.to_datetime(a['BATCH START TIME'][len(refined_df)-1], format='%d/%m/%Y %H:%M:%S')
    st.session_state.start_date = start
    st.session_state.end_date = stop

    st.session_state.df =df
    st.session_state.batch_data=batch_data
    st.session_state.refined_df=refined_df
    
    st.session_state.idxs =idxs
    st.session_state.r_time_id=r_time_id
    st.session_state.rh_time_id=rh_time_id
    st.session_state.temp_time_id=temp_time_id
    
    st.session_state.rh_mins=rh_mins
    st.session_state.r_mins=r_mins
    st.session_state.t_mins=t_mins   
    st.session_state.complete_refined_df=refined_df
    region_selections = [True, True, True]
    st.session_state.green_limit_global=19
    st.session_state.yellow_limit_global=23
    change_date(st.session_state.start_date,st.session_state.end_date,region_selections)

def compute_II(process_data_II,io_data_II):
    global df_II 
    df_II = pd.DataFrame()
    df_II=df_II.dropna(how='all')
    for i in range(len(process_data_II)):
        df_II = pd.concat([df_II,process_data_II[i]], ignore_index=True)
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
    df2_II = pd.DataFrame()
    for i in range(len(io_data_II)):
        df2_II = pd.concat([df2_II,io_data_II[i]], ignore_index=True)  
    new_header = df2_II.iloc[0]
    in_df = df2_II[:]
    in_df.drop(0)
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

    #st.session_state.start_date=refined_df_II['BATCH START TIME'][0][:10]
    #st.session_state.end_date=refined_df_II['BATCH START TIME'][0][:10]
    a=refined_df_II
    a['BATCH START TIME']=pd.to_datetime(a['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    a = a.sort_values(by='BATCH START TIME')
    a = a.reset_index(drop=True)
    start=pd.to_datetime(a['BATCH START TIME'][0], format='%d/%m/%Y %H:%M:%S')
    stop=pd.to_datetime(a['BATCH START TIME'][len(refined_df_II)-1], format='%d/%m/%Y %H:%M:%S')
    st.session_state.start_date_II = start
    st.session_state.end_date_II = stop

    st.session_state.df_II =df_II
    st.session_state.batch_data_II=batch_data_II
    st.session_state.refined_df_II=refined_df_II
    
    st.session_state.idxs_II =idxs_II
    st.session_state.h_II_time_id=h_II_time_id
    st.session_state.temp_II_time_id=temp_II_time_id
    
    st.session_state.h_II_mins=h_II_mins
    st.session_state.t_II_mins=t_II_mins   
    st.session_state.complete_refined_df_II=refined_df_II
    region_selections_II = [True, True, True]
    st.session_state.green_limit_global_II=2
    st.session_state.yellow_limit_global_II=6
    change_date_II(st.session_state.start_date_II,st.session_state.end_date_II,region_selections_II)
def compute_glow(process_data_glow,io_data_glow):
    global df_glow
    df_glow = pd.DataFrame()
    df_glow=df_glow.dropna(how='all')
    for i in range(len(process_data_glow)):
        df_glow = pd.concat([df_glow,process_data_glow[i]], ignore_index=True)
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
    for i in range(len(idxs_glow)):
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
    for i in v_time_id_in:
        v_time_in.append((i[1]-i[0]-1)*5)
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
            print(df_glow['BATCH ID'][v_time_id[i][0]])
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
    for i in range(len(idxs_glow)):
        count=[]
        for j in range(idxs_glow[i][0],idxs_glow[i][1]):
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
    c_irr=g_irr




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
    for i in range(len(idxs_glow)):
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
    df2_glow = pd.DataFrame()
    for i in range(len(io_data_glow)):
        df2_glow = pd.concat([df2_glow,io_data_glow[i]], ignore_index=True)  
    new_header = df2_glow.iloc[0]
    in_df = df2_glow[:]
    in_df.drop(0)
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

    #st.session_state.start_date=refined_df_glow['BATCH START TIME'][0][:10]
    #st.session_state.end_date=refined_df_glow['BATCH START TIME'][0][:10]
    a=refined_df_glow
    a['BATCH START TIME']=pd.to_datetime(a['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    a = a.sort_values(by='BATCH START TIME')
    a = a.reset_index(drop=True)
    start=pd.to_datetime(a['BATCH START TIME'][0], format='%d/%m/%Y %H:%M:%S')
    stop=pd.to_datetime(a['BATCH START TIME'][len(refined_df_glow)-1], format='%d/%m/%Y %H:%M:%S')
    st.session_state.start_date_glow = start
    st.session_state.end_date_glow = stop

    st.session_state.df_glow =df_glow
    st.session_state.batch_data_glow=batch_data_glow
    st.session_state.refined_df_glow=refined_df_glow
    
    st.session_state.idxs_glow =idxs_glow
  
    st.session_state.complete_refined_df_glow=refined_df_glow
    region_selections_glow = [True, False, False, False, False]

    change_date_glow(st.session_state.start_date_glow,st.session_state.end_date_glow,region_selections_glow)
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
            shift_type_glow.append("Shift 1")
        elif int(refined_df_glow['BATCH START TIME'][i][11:13])<15 and int(refined_df_glow['BATCH START TIME'][i][11:13])>=6:
            if refined_df_glow['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_glow['BATCH START TIME'][i][14:16])<=30:
                    shift_type_glow.append("Shift 2")
                else:
                    pass
            else:
                shift_type_glow.append("Shift 2")
        elif int(refined_df_glow['BATCH START TIME'][i][11:13])<23 and int(refined_df_glow['BATCH START TIME'][i][11:13])>=14 :
            if refined_df_glow['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_glow['BATCH START TIME'][i][14:16])>30:
                    shift_type_glow.append("Shift 3")
                else:
                    pass
            else:
                shift_type_glow.append("Shift 3")
    refined_df_glow['SHIFT TYPE']=shift_type_glow 
    refined_df_glow['Ni hours']=ni_hrs

    refined_df_glow['BATCH START TIME']=pd.to_datetime(refined_df_glow['BATCH START TIME'], format='%d/%m/%Y %H:%M:%S')
    refined_df_glow = refined_df_glow.sort_values(by='BATCH START TIME')
    refined_df_glow = refined_df_glow.reset_index(drop=True)

    filtered_df = refined_df_glow[(refined_df_glow["BATCH START TIME"] > start_date_glow) & (refined_df_glow["BATCH START TIME"] <= end_date_glow)]
    filtered_df=filtered_df.reset_index(drop=True)
    comb_df=pd.DataFrame()
    if region_selections_glow[0]==True:
        pass
    else:
        if region_selections_glow[1]==True:
            comb_df=pd.concat([comb_df,filtered_df[filtered_df["V Irregulars"]==True]], ignore_index=True)
        if region_selections_glow[2]==True:
            comb_df=pd.concat([comb_df,filtered_df[filtered_df['Bias Arc Irregulars']==True]], ignore_index=True)
        if region_selections_glow[3]==True:
            comb_df=pd.concat([comb_df,filtered_df[filtered_df["I Irregulars"]==True]], ignore_index=True)
        if region_selections_glow[4]==True:
            comb_df=pd.concat([comb_df,filtered_df[filtered_df["Ar Gas Irregulars"]==True]], ignore_index=True)      
        filtered_df=comb_df.reset_index(drop=True)

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
    golden_index_glow = 2
    golden_batch_glow=refined_df_glow['BATCH ID'][golden_index_glow]
    st.session_state.golden_batch_glow=golden_batch_glow
    st.session_state.golden_index_glow=golden_index_glow
    st.session_state.pt=pt
    st.session_state.mt=mt
    st.session_state.nt=nt
    st.session_state.refined_df_glow=refined_df_glow
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
            shift_type_II.append("Shift 1")
        elif int(refined_df_II['BATCH START TIME'][i][11:13])<15 and int(refined_df_II['BATCH START TIME'][i][11:13])>=6:
            if refined_df_II['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_II['BATCH START TIME'][i][14:16])<=30:
                    shift_type_II.append("Shift 2")
                else:
                    pass
            else:
                shift_type_II.append("Shift 2")
        elif int(refined_df_II['BATCH START TIME'][i][11:13])<23 and int(refined_df_II['BATCH START TIME'][i][11:13])>=14 :
            if refined_df_II['BATCH START TIME'][i][11:13]==14:
                if int(refined_df_II['BATCH START TIME'][i][14:16])>30:
                    shift_type_II.append("Shift 3")
                else:
                    pass
            else:
                shift_type_II.append("Shift 3")
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

    filtered_df = refined_df_II[(refined_df_II["BATCH START TIME"] > start_date_II) & (refined_df_II["BATCH START TIME"] <= end_date_II)]
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
    st.rerun()
def change_date(start_date,end_date,region_selections):
    refined_df=st.session_state.complete_refined_df
    st.session_state.start_date=start_date
    st.session_state.end_date=end_date
    st.session_state.region_selections=region_selections
    complete_refined_df=st.session_state.complete_refined_df
    print("Beginning of change: ",len(complete_refined_df))
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
            shift_type.append("Shift 1")
        elif int(refined_df['BATCH START TIME'][i][11:13])<15 and int(refined_df['BATCH START TIME'][i][11:13])>=6:
            if refined_df['BATCH START TIME'][i][11:13]==14:
                if int(refined_df['BATCH START TIME'][i][14:16])<=30:
                    shift_type.append("Shift 2")
                else:
                    pass
            else:
                shift_type.append("Shift 2")
        elif int(refined_df['BATCH START TIME'][i][11:13])<23 and int(refined_df['BATCH START TIME'][i][11:13])>=14 :
            if refined_df['BATCH START TIME'][i][11:13]==14:
                if int(refined_df['BATCH START TIME'][i][14:16])>30:
                    shift_type.append("Shift 3")
                else:
                    pass
            else:
                shift_type.append("Shift 3")
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

    filtered_df = refined_df[(refined_df["BATCH START TIME"] > start_date) & (refined_df["BATCH START TIME"] <= end_date)]
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
    st.rerun()
    print("End of change:"+str(st.session_state.refined_df['BATCH START TIME'][1])+str(type(st.session_state.refined_df['BATCH START TIME'][1])))
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
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'
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
        margin: 10px;
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
        st.session_state[file_list_name].append(df)
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

            

# Main page
if st.session_state.current_page == 'main':
    
    
    st.header("Upload your data files:")
    
    pre_post_file = st.file_uploader("Upload Pre/Post Process Data", type=["csv"])
    handle_file_upload(pre_post_file, 'pre_post_data')
    
    process_file = st.file_uploader("Upload Process Data", type=["csv"])
    handle_file_upload(process_file, 'process_data')
    if st.button("Check common batches"):
        df1 = pd.DataFrame()
        for i in range(len(st.session_state.process_data)):
            df1 = pd.concat([df1,st.session_state.process_data[i]], ignore_index=True)
        df1.dropna()
        df2 = pd.DataFrame()
        for i in range(len(st.session_state.pre_post_data)):
            df2 = pd.concat([df2,st.session_state.pre_post_data[i]], ignore_index=True)  
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
        for i in range(len(st.session_state.process_data_II)):
            df1 = pd.concat([df1,st.session_state.process_data_II[i]], ignore_index=True)
        df1.dropna()
        df2 = pd.DataFrame()
        for i in range(len(st.session_state.pre_post_data_II)):
            df2 = pd.concat([df2,st.session_state.pre_post_data_II[i]], ignore_index=True)  
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
        for i in range(len(st.session_state.process_data_glow)):
            df1 = pd.concat([df1,st.session_state.process_data_glow[i]], ignore_index=True)
        df1.dropna()
        df2 = pd.DataFrame()
        for i in range(len(st.session_state.pre_post_data_glow)):
            df2 = pd.concat([df2,st.session_state.pre_post_data_glow[i]], ignore_index=True)  
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
elif st.session_state.current_page == 'dashboard':
    st.markdown('<div class="main-heading">PVD Dashboard</div>', unsafe_allow_html=True)
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
            st.session_state.current_page='main'
            st.rerun()
    with col2:
        if st.button("GLOW DISCHARGE"):
            st.session_state.current_page='glow main'
            st.rerun()
    with col3:
        if st.button("PUMPDOWN HV II"):
            st.session_state.current_page='HV II main'
            st.rerun()    
    with col4:
        if st.button("ARC CLEANING"):
            st.write("Button 4 clicked!")
    with col5:
        if st.button("ARC ETCHING"):
            st.write("Button 5 clicked!")

    col6, col7, col8, col9, col10 = st.columns(5)

    with col6:
        if st.button("Button 6"):
            st.write("Button 6 clicked!")
    with col7:
        if st.button("Button 7"):
            st.write("Button 7 clicked!")
    with col8:
        if st.button("Button 8"):
            st.write("Button 8 clicked!")
    with col9:
        if st.button("Button 9"):
            st.write("Button 9 clicked!")
    with col10:
        if st.button("Button 10"):
            st.write("Button 10 clicked!")



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
        st.session_state.current_page = 'main'
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
        st.session_state.current_page = 'main'
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
        st.session_state.current_page = 'main'
        st.rerun()
    st.header("Glow Discharge Overview")
    
    #plot_corr_II()
    plot_glow_irr()
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
    r_state = st.sidebar.number_input("Change Random State", min_value=1, max_value=100, step=1, value=42) 
    test_state = st.sidebar.number_input("Change Test Size", min_value=0.1, max_value=0.5, step=0.05, value=0.2) 
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
    r_state = st.sidebar.number_input("Change Random State", min_value=1, max_value=100, step=1, value=47) 
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
