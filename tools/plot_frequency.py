#!/usr/bin/env python3
import pandas as pd
import numpy as np
from perfetto.trace_processor import TraceProcessor as tp
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

query = "select ts, cpu, value as freq from counter join cpu_counter_track on counter.track_id = cpu_counter_track.id where t.name = 'cpufreq'"
query = "select ts, cpu, value as freq from counter as c left join cpu_counter_track as t on c.track_id = t.id where t.name = 'cpufreq'"

def plot(trace, start_row=1, num_cols=1):
        trace_freq = trace.query(query)
        df_freq = trace_freq.as_pandas_dataframe()

        try:
            df_freq.ts = df_freq.ts - df_freq.ts[0]
            df_freq.ts = df_freq.ts / 1000000000
            df_freq['_ts'] = df_freq.ts
            df_freq.freq = df_freq.freq / 1000000
            df_freq.set_index('ts', inplace=True)

            nr_cpus = len(df_freq.cpu.unique())

            clusters = [0]
            df_freq_cpu = df_freq[df_freq.cpu == 0]
            for cpu in range(nr_cpus):
                df_freq_next_cpu = df_freq[df_freq.cpu == cpu]

                if np.array_equal(df_freq_cpu.freq.values, df_freq_next_cpu.freq.values):
                    continue

                df_freq_cpu = df_freq[df_freq.cpu == cpu]
                clusters.append(cpu)

            nr_cpus = len(clusters)
            for cpu in clusters:
                df_freq_cpu = df_freq[df_freq.cpu == cpu].copy()
                df_freq_cpu['duration'] = -1 * df_freq_cpu._ts.diff(periods=-1)

                total_duration = df_freq_cpu.duration.sum()
                df_duration =  df_freq_cpu.groupby('freq').duration.sum() * 100 / total_duration

                plt.subplot(nr_cpus * 2, num_cols, start_row)
                df_freq_cpu.freq.plot(title='CPU' + str(cpu) + ' frequency', alpha=0.75, drawstyle='steps-post', style='o-', xlim=(df_freq.index[0], df_freq.index[-1]))

                plt.subplot(nr_cpus * 2, num_cols, start_row + 1)
                df_duration.plot.bar(title='Frequency residency %', alpha=0.75)

                start_row += 2
        except:
            pass

for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp(file_path=file)
        plt.figure(figsize=(16,16))
        plot(trace)
        trace.close()

        plt.tight_layout()
        plt.savefig(file.replace('.perfetto-trace', '') + '_frequency.png')
