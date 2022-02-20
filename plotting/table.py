#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

def plot(df, columns=[], height=0.3):
    if len(columns):
        df = df.loc[:,columns]

    df_desc = df.describe(percentiles=[0.9, 0.95, 0.99]).applymap('{:,.2f}'.format)
    plt.table(cellText=df_desc.values,
              rowLabels=df_desc.index, rowLoc='center',
              colLabels=df_desc.columns, cellLoc='center',
              bbox=[0, -(height+0.1), 1, height])
