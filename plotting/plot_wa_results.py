#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import glob
import sys

target = sys.argv[1]
workload = sys.argv[2]

df = pd.read_csv("wa_output/results.csv")

metrics = df.metric.unique()
for metric in metrics:
    df_metric = df[df.metric == metric]
    plt.plot(df_metric.iteration, df_metric.value, label=metric)
    print("--", metric)
    print(df_metric.value.describe(percentiles=[0.9, 0.95, 0.99]))

plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.savefig("{}_{}_results.png".format(target, workload), bbox_inches="tight")

for metric in metrics:
    df_metric = df[df.metric == metric]
    plt.figure()
    plt.plot(df_metric.iteration, df_metric.value, label=metric)
    plt.legend()
    plt.ylabel(df_metric.units.unique())
    plt.xlabel("Iteration")
    plt.savefig("{}_{}_{}.png".format(target, workload, metric))
