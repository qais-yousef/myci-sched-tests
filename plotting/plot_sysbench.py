#!/usr/bin/env python3
import pandas as pd
import os
import table

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df_all = pd.DataFrame()

for file in sorted(os.listdir()):
    if file.endswith(".csv"):
        df = pd.read_csv(file)
        df_all[file] = df['events_per_second']

plt.figure(figsize=(16,16))
df_all.plot(ax=plt.gca(), style='o-')

color = ['b', 'orange', 'g']
i = 0
for column in df_all.columns:
    mean = df_all[column].mean()
    plt.axhline(y=mean, color=color[i], linestyle='-')
    i += 1

table.plot(df_all)
plt.tight_layout()
plt.savefig("sysbench_result.png")
