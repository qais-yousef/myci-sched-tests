#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import glob
import sys
import table

target = sys.argv[1]
workload = sys.argv[2]

df = pd.read_csv("wa_output/results.csv")

num_args = len(sys.argv)
if num_args > 3:
    metrics = []
    for idx in range(3, num_args):
        metrics.append(sys.argv[idx])
else:
    metrics = df.metric.unique()

num_rows = len(metrics)
row_pos = 1

plt.figure(figsize=(16,32))

print("Plotting Merics: {}".format(metrics))
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
