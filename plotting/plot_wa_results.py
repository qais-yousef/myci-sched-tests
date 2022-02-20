#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import glob
import sys
import table
import text

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

    plt.gca().set_title(metric)
    plt.bar(df_metric.iteration, df_metric.value)
    plt.gca().bar_label(plt.gca().containers[0])

    mean = df_metric.value.mean()
    b, t = plt.gca().get_ylim()
    plt.axhline(y=mean, color='r', linestyle='-')
    text.plot(0.1, mean/t, 'Mean = {:,.2f}'.format(mean))

    table.plot(df_metric, columns=['value'])

plt.tight_layout()
plt.savefig("{}_{}_results.png".format(target, workload))
