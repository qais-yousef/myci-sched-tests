#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import glob
import sys
import table

target = sys.argv[1]
workload = sys.argv[2]

df = pd.read_csv("wa_output/results.csv")

metrics = df.metric.unique()
num_rows = len(metrics)
row_pos = 1

plt.figure(figsize=(16,32))

for metric in metrics:
    df_metric = df[df.metric == metric]
    plt.subplot(num_rows, 1, row_pos)
    row_pos += 1
    plt.stem(df_metric.iteration, df_metric.value, label=metric)
    table.plot(df_metric, columns=['value'])
    # plt.gca().legend(loc='upper right')
    plt.gca().set_title(metric)

plt.tight_layout()
plt.savefig("{}_{}_results.png".format(target, workload))
