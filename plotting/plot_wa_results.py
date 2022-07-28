#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import trace_processor as tp
import glob
import sys
import freq
import idle
import thermal
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
        trace = tp.get_trace(file)
        freq.init(trace)
        idle.init(trace)
        thermal.init(trace)
        power.init(trace)
        trace.close()
        break

#
# Initialize plotting stuff
#
num_metrics = int((len(metrics) + 3) / 4)
num_rows = num_metrics + freq.num_rows() + idle.num_rows() + thermal.num_rows() + power.num_rows()
row_pos = 1

plt.figure(figsize=(24,3*num_rows))

#
# Plot wa results
#
col = 0
print("Plotting Merics ({}): {}".format(len(metrics), metrics))
for metric in metrics:
    df_metric = df[df.metric == metric]

    if col == 0:
        plt.subplot(num_rows, 4, row_pos * 4 - 3)
        col = 1
    elif col == 1:
        plt.subplot(num_rows, 4, row_pos * 4 - 2)
        col = 2
    elif col == 2:
        plt.subplot(num_rows, 4, row_pos * 4 - 1)
        col = 3
    else:
        plt.subplot(num_rows, 4, row_pos * 4 - 0)
        col = 0
        row_pos += 1

    plt.gca().set_title(metric)
    plt.bar(df_metric.iteration, df_metric.value, color='grey')
    plt.gca().bar_label(plt.gca().containers[0], label_type='center', color='w')
    text.plot(-0.15, 1.1, 'Mean = {:,.2f}'.format(df_metric.value.mean()))

if col:
    row_pos += 1

#
# Plot perfetto stuff
#
row_pos = freq.plot(num_rows=num_rows, row_pos=row_pos)
row_pos = idle.plot(num_rows=num_rows, row_pos=row_pos)
row_pos = thermal.plot(num_rows=num_rows, row_pos=row_pos)
row_pos = power.plot(num_rows=num_rows, row_pos=row_pos)

prefix = "{}_{}".format(target, workload)

freq.save_csv(prefix)
idle.save_csv(prefix)
thermal.save_csv(prefix)
power.save_csv(prefix)

plt.tight_layout()
plt.savefig(prefix + "_results.png")
