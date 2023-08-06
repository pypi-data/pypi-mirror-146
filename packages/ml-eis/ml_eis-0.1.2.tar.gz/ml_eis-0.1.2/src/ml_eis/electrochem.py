#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 14:04:07 2022

@author: yuefanji
"""

import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt


def cycling_CCCV(file_name,cycle_num):
    '''
    This function helps the user plot the battery cycling data for the visualization

    Parameters
    ----------
  
    file_name : str
        file name of the file to be read. Should be the battery cycling data.
    cycle_num : in
        battery cycle number.

    Returns
    -------
    fig : figure
        Plot of charge discharge curve.
    '''
 
    
    
    df=pd.read_csv(file_name)
    charge=cycling_data_processing(df,cycle_num,'charge');
    discharge=cycling_data_processing(df,cycle_num,'discharge');
    
    plt.plot(charge['Capacity(Ah)'],charge['Voltage(V)'],label='charge')
    plt.plot(discharge['Capacity(Ah)'],discharge['Voltage(V)'],label='discharge')
    plt.legend()
    plt.xlabel('Capacity(Ah)')
    plt.ylabel('Voltage(V)')
    fig = plt.gcf()
    return(fig)

def diff_cap(file_name,cycle_num):
    '''
    

     This function helps the user plot the differential capacity data for the visualization

     Parameters
     ----------
     file_name : str
         file name of the file to be read. Should be the battery cycling data.
     cycle_num : in
         battery cycle number.

     Returns
     -------
     fig : figure
        Plot of differential capacity curve.
     '''
     
    df=pd.read_csv(file_name)
    charge=cycling_data_processing(df,cycle_num,'charge')
    discharge=cycling_data_processing(df,cycle_num,'discharge')
    charge_V=charge['Voltage(V)'][(charge['Voltage(V)']<4.18)]
    charge_cap=charge['Capacity(Ah)'][(charge['Voltage(V)']<4.18)]
    discharge_V=discharge['Voltage(V)'][(discharge['Voltage(V)']<4.18)]
    discharge_cap=discharge['Capacity(Ah)'][(discharge['Voltage(V)']<4.18)]
    
    dqdv_charge=np.diff(charge_cap)/np.diff(charge_V)

    N_charge=len(dqdv_charge)
    dqdv_discharge=np.diff(discharge_cap)/np.diff(discharge_V)
    N_discharge=len(dqdv_discharge)
    plt.plot(charge_V[0:N_charge],dqdv_charge,label='charge')
    plt.plot(discharge_V[0:N_discharge],dqdv_discharge,label='discharge')
    plt.legend()
    plt.xlabel('Voltage(V)')
    plt.ylabel('dQ/dV')
    fig = plt.gcf()
    return (fig)

def cycling_data_processing(df,cycle_num,data_type):
    '''
    
    This function helps user to process the battery cycling data
    
    Parameters
    ----------
    df : DataFrame
        dataframe of the battery cycling data.
    cycle_num : int
        cycle number of interest.
    data_type : str
        input 'charge' for the charge data
        input 'discharge' for the discharge data .

    Returns
    -------
    A : DataFrame
        dataframe of the battery cycling data for the cycle number of interest.

    '''
    
    if data_type == 'discharge':
        A=df[(df['Cyc#']==cycle_num)&(df['Current(A)']<0)]
    if data_type == 'charge':
        A=df[(df['Cyc#']==cycle_num)&(df['Current(A)']>0)]
        
    return (A)

def Capacity_voltage_extract(df):
    '''
    

    Parameters
    ----------
    df : DataFrame
        dataframe of the pre processed battery cycling data.

    Returns
    -------
    dataframe with column 'Capacity(Ah)' and 'Voltage(V)'.

    '''
    df_1=pd.DataFrame()
    df_1['Capacity(Ah)']=df['Capacity(Ah)']
    df_1['Voltage(V)']=df['Voltage(V)']
    return(df_1)
    

def impedance_data_processing(text_file):
    '''
    

    Parameters
    ----------
    text_file : str
        file name of the impedance data.

    Returns
    -------
    the dataframe with column 'Z1', 'Z2', and 'frequency'.

    '''
    data=np.loadtxt(text_file,delimiter=",",skiprows=11)
    f=data[:,0]
    Z1=data[:,4]
    Z2=data[:,5]
    df=pd.DataFrame()
    df1=pd.DataFrame()
    df['frequency']=f
    df['Z1']=Z1
    df['Z2']=Z2
    df1=df.copy()
    df1=df1[(df1['Z2']<0)]
    df1.reset_index(inplace = True)
    return(df1)

def Nyquist_plot_UI(text_file):
    '''
    

    Parameters
    ----------
    text_file : str
        file name of the impedance data .

    Returns
    -------
    Nyquist_plot for the visualization.

    '''
    df=impedance_data_processing(text_file)
    return(Nyquist_plot(df))
    
def Nyquist_plot(df):
    '''
    

    Parameters
    ----------
    df : DataFrame
        dataframe that is processed by impedance_data_processing() .

    Returns
    -------
    fig : figure
        Nyquist_plot for the visualization.

    '''
    
    plt.plot(df['Z1'],-df['Z2'])
    plt.xlabel('Z1')
    plt.ylabel('-Z1')
    fig = plt.gcf()
    return (fig)
    
def dis_cap(df,max_cycle):
    '''
    
    Parameters
    ----------
    df : DataFrame
        dataframe of battery cycling data.
    max_cycle : in
        maximum cycle of interest.

    Returns
    -------
    capacity at the max_cycle

    '''
    N=max_cycle+1
    cap=np.zeros(N)
    for i in range(0,N):
        discharge=cycling_data_processing(df,i,'discharge')

        cap[i]=discharge['Capacity(Ah)'].iloc[-1]

    return(cap[-1])

def cap_ret(df,max_cycle):
    '''
    
    Parameters
    ----------
    df : DataFrame
        dataframe of battery cycling data.
    max_cycle : int
        maximum cycle of interest.

    Returns
    -------
    Capacity retention for all cycles up to the max_cycle

    '''
    N=max_cycle+1
    ret=np.zeros(max_cycle)
    discharge=cycling_data_processing(df,1,'discharge')
    first_cap=discharge['Capacity(Ah)'].iloc[-1]
    ret[0]=1
    for i in range(2,N):
        discharge=cycling_data_processing(df,i,'discharge')
        ret[i-1]=(discharge['Capacity(Ah)'].iloc[-1])/first_cap

    return(ret)
        
    
