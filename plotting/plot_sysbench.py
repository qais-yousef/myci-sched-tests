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

plt.figure(figsize=(16,8))
df_all.plot(style='o-')
table.plot(df_all)
plt.tight_layout()
plt.savefig("sysbench_result.png")
