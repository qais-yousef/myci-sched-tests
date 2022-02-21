#!/usr/bin/env python3
import pandas as pd
import os
import table
import text

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df_all = pd.DataFrame()

for file in sorted(os.listdir()):
    if file.endswith(".csv"):
        df = pd.read_csv(file)
        df_all[file] = df['events_per_second']

plt.figure(figsize=(16,16))
df_all.plot.bar(ax=plt.gca())
b, t = plt.gca().get_ylim()
i = 0
color = ['b', 'orange', 'g']
for column in df_all.columns:
    mean = df_all[column].mean()
    plt.axhline(y=mean, color=color[i], linestyle='-')
    text.plot(0.1, mean/t, 'Mean = {:,.2f}'.format(mean))
    i += 1
table.plot(df_all)
plt.tight_layout()
plt.savefig("sysbench_result.png")
