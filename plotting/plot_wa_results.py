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
    metrics = df.metric.unique()

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
num_rows = len(metrics) + freq.num_rows() + idle.num_rows() + power.num_rows()
row_pos = 1

plt.figure(figsize=(1*num_rows,2*num_rows))

#
# Plot wa results
#
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

#
# Plot perfetto stuff
#
row_pos = freq.plot(num_rows=num_rows, row_pos=row_pos)
row_pos = idle.plot(num_rows=num_rows, row_pos=row_pos)
row_pos = power.plot(num_rows=num_rows, row_pos=row_pos)

plt.tight_layout()
plt.savefig("{}_{}_results.png".format(target, workload))
