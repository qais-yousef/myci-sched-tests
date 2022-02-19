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
        df_all[file] = df['events_per_second']

print(tabulate(df_all.describe(), headers='keys', tablefmt='psql'))

df_all.plot(figsize=(16,8), style='o-').get_figure().savefig("result.png")
