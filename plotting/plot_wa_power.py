#!/usr/bin/env python
import pandas as pd
import matplotlib.pyplot as plt
import glob
import sys

target = sys.argv[1]
workload = sys.argv[2]

files = glob.glob("wa_output/*{}*/*.csv".format(workload))

df_big = []
for file in files:
    df = pd.read_csv(file, index_col=None, header=0)
    df_big.append(df)

df = pd.concat(df_big, axis=0, ignore_index=True)

df.set_index("timestamp_time", inplace=True)
df.sort_index(inplace=True)

df.battery_current.plot(label="c", legend=True)
df.battery_percent.plot(label="%", legend=True)
df.battery_voltage.plot(label="v", legend=True)
df.battery_power.plot(label="p", legend=True)

plt.savefig("{}_{}_power_summary.png".format(target, workload))

print(df.describe())

plt.figure()
df.battery_percent.plot(label="%", legend=True)
plt.savefig("{}_{}_battery_charge.png".format(target, workload))

plt.figure()
df.battery_current.plot(label="c", legend=True)
plt.savefig("{}_{}_current.png".format(target, workload))

plt.figure()
df.battery_voltage.plot(label="v", legend=True)
plt.savefig("{}_{}_voltage.png".format(target, workload))

plt.figure()
df.battery_power.plot(label="p", legend=True)
plt.savefig("{}_{}_power.png".format(target, workload))
