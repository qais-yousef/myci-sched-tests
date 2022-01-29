#!/usr/bin/env python3
import pandas as pd
from tabulate import tabulate
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df_all_run = pd.DataFrame()
df_all_duty = pd.DataFrame()
df_all_ratios = pd.DataFrame()

ticks=[x * 5 for x in range(0, 21)]

for file in sorted(os.listdir()):
    if file.endswith(".csv"):
        df = pd.read_csv(file)
        df_all_run[file] = df['run']
        df_all_duty[file] = df['run'] * 100.0 / df['period']
        df_all_duty[file].plot.hist(figsize=(16,8), bins=32, xticks=ticks, alpha=0.75, title=file + ' Duty Hist').get_figure().savefig(file.replace('.csv', '') + "_result_duty_hist.png")
        plt.close()

print("Runtime:")
print(tabulate(df_all_run.describe(), headers='keys', tablefmt='psql'))
print("Duty:")
print(tabulate(df_all_duty.describe(), headers='keys', tablefmt='psql'))

#
# Print ratio of runtime for all runs
#
for col in df_all_run:
    for row in df_all_run:
        if row == col:
            continue
        if col + '/' + row in df_all_ratios:
            continue
        df_all_ratios[row + '/' + col] = df_all_run[row] / df_all_run[col]

try:
    print("Runtime Ratios:")
    print(tabulate(df_all_ratios.describe(), headers='keys', tablefmt='psql'))
except:
    pass

#
# Print ratio of min & max freqs
#
try:
    sysfs_max_freq = '/sys/devices/system/cpu/cpufreq/policy0/cpuinfo_max_freq'
    sysfs_min_freq = '/sys/devices/system/cpu/cpufreq/policy0/cpuinfo_min_freq'
    with open(sysfs_max_freq) as max, open(sysfs_min_freq) as min:
        for x, y in zip(max, min):
            x = float(x.strip())
            y = float(y.strip())
            print("Freq Ratio:")
            print("max/min =", x/y)
            print("min/max =", y/x)
except:
    pass

#
# Generate all plots
#
try:
    df_all_run.plot(figsize=(16,8), style='o-', title='Runtime').get_figure().savefig("result_run.png")
    df_all_duty.plot(figsize=(16,8), yticks=ticks, style='o-', title='Duty').get_figure().savefig("result_duty.png")
    df_all_duty.plot.hist(figsize=(16,8), bins=32, xticks=ticks, alpha=0.5, title='Duty Hist').get_figure().savefig("result_duty_hist.png")
    df_all_ratios.plot(figsize=(16,8), style='o-', title='Runtime Ratios').get_figure().savefig("result_run_ratios.png")
except:
    pass
