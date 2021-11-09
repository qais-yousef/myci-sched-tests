#!/usr/bin/env python3
import pandas as pd
from tabulate import tabulate
import os

import matplotlib
matplotlib.use('Agg')

df_all = pd.DataFrame()

for file in sorted(os.listdir()):
    if file.endswith(".csv"):
        df = pd.read_csv(file)
        df_all[file] = df['slack']

print(tabulate(df_all.describe(), headers='keys', tablefmt='psql'))

df_all.plot(figsize=(16,8), ylim=(-40000, 20000), style='o-').get_figure().savefig("result.png")
df_all.plot.hist(figsize=(16,8), bins=100, alpha=1, xlim=(-40000, 20000)).get_figure().savefig("result_hist.png")
df_all.plot.box(figsize=(16,8), ylim=(-40000, 20000)).get_figure().savefig("result_box.png")
