#!/usr/bin/env python3
import pandas as pd
from tabulate import tabulate
import table
import text
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df_all_run = pd.DataFrame()
df_all_duty = pd.DataFrame()
df_all_ratios = pd.DataFrame()

ticks=[x * 5 for x in range(0, 21)]

plt.figure(figsize=(16,24))
num_rows=4
plot_row=1

for file in sorted(os.listdir()):
    if file.endswith(".csv"):
        df = pd.read_csv(file)
        df_all_run[file] = df['run']
        df_all_duty[file] = df['run'] * 100.0 / df['period']

#
# Calculate ratios of runtime for all runs
#
for col in df_all_run:
    for row in df_all_run:
        if row == col:
            continue
        if col + '/' + row in df_all_ratios:
            continue
        df_all_ratios[row + '/' + col] = df_all_run[row] / df_all_run[col]

#
# Print ratio of min & max freqs
#
def print_ratios():
    try:
        sysfs_max_freq = '/sys/devices/system/cpu/cpufreq/policy0/cpuinfo_max_freq'
        sysfs_min_freq = '/sys/devices/system/cpu/cpufreq/policy0/cpuinfo_min_freq'
        with open(sysfs_max_freq) as max, open(sysfs_min_freq) as min:
            for x, y in zip(max, min):
                x = float(x.strip())
                y = float(y.strip())
                text.plot(0.01, 0.95, "Freq Ratio:")
                text.plot(0.01, 0.90, "max/min = {:,.2f}".format(x/y))
                text.plot(0.01, 0.85, "min/max = {:,.2f}".format(y/x))
    except:
        pass

#
# Generate all plots
#
try:
    plt.subplot(num_rows, 1, plot_row)
    df_all_run.plot(ax=plt.gca(), style='o-', title='Runtime')
    table.plot(df_all_run)
    plot_row += 1
    plt.subplot(num_rows, 1, plot_row)
    df_all_duty.plot(ax=plt.gca(), yticks=ticks, style='o-', title='Duty')
    plot_row += 1
    plt.subplot(num_rows, 1, plot_row)
    for file in sorted(os.listdir()):
        if file.endswith(".csv"):
            df_all_duty[file].plot.hist(ax=plt.gca(), legend=True, bins=32, xticks=ticks, alpha=0.5, title='Duty Hist')
    table.plot(df_all_duty)
    plot_row += 1
    plt.subplot(num_rows, 1, plot_row)
    df_all_ratios.plot(ax=plt.gca(), style='o-', title='Runtime Ratios')
    table.plot(df_all_ratios)
    print_ratios()
except:
    pass

plt.tight_layout()
plt.savefig("rampup_time_results.png")
