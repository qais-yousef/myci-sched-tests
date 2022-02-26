#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
from perfetto.trace_processor import TraceProcessor as tp
import glob
import sys
import freq
import idle
import power
import text
import os

#
# Init wa stuff
#
target = sys.argv[1]
workload = sys.argv[2]

df = pd.read_csv("wa_output/results.csv")

num_args = len(sys.argv)
if num_args > 3:
    metrics = []
    for idx in range(3, num_args):
        metrics.append(sys.argv[idx])
else:
    metrics = df.metric.sort_values().unique()

#
# Init perfetto traces stuff
#
for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp(file_path=file)
        freq.init(trace)
        idle.init(trace)
        power.init(trace)
        trace.close()
        break

#
# Initialize plotting stuff
#
num_rows = (len(metrics) + 1)/2 + freq.num_rows() + idle.num_rows() + power.num_rows()
num_rows = int(num_rows)
row_pos = 1

plt.figure(figsize=(20,2*num_rows))

#
# Plot wa results
#
col = 0
print("Plotting Merics: {}".format(metrics))
for metric in metrics:
    df_metric = df[df.metric == metric]

    if len(metrics) == 1:
        plt.subplot(num_rows, 1, row_pos)
        row_pos += 1
    else:
        if not col:
            plt.subplot(num_rows, 2, row_pos * 2 - 1)
            col = 1
        else:
            plt.subplot(num_rows, 2, row_pos * 2 - 0)
            col = 0
            row_pos += 1

    plt.gca().set_title(metric)
    plt.bar(df_metric.iteration, df_metric.value)
    plt.gca().bar_label(plt.gca().containers[0], label_type='center', color='w')
    text.plot(0.1, 1.2, 'Mean = {:,.2f}'.format(df_metric.value.mean()))

#
# Plot perfetto stuff
#
row_pos = freq.plot(num_rows=num_rows, row_pos=row_pos)
row_pos = idle.plot(num_rows=num_rows, row_pos=row_pos)
row_pos = power.plot(num_rows=num_rows, row_pos=row_pos)

plt.tight_layout()
plt.savefig("{}_{}_results.png".format(target, workload))
