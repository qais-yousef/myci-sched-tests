#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

query = "select ts, cpu, value as freq from counter as c left join cpu_counter_track as t on c.track_id = t.id where t.name = 'cpufreq'"

df_freq = None
clusters = None

def init(trace):

        global trace_freq
        trace_freq = trace.query(query)

def find_clusters():

        global clusters

        if clusters:
            return

        nr_cpus = len(df_freq.cpu.unique())

        clusters = [0]
        df_freq_cpu = df_freq[df_freq.cpu == 0]
        for cpu in range(nr_cpus):
            df_freq_next_cpu = df_freq[df_freq.cpu == cpu]

            if np.array_equal(df_freq_cpu.freq.values, df_freq_next_cpu.freq.values):
                continue

            df_freq_cpu = df_freq[df_freq.cpu == cpu]
            clusters.append(cpu)

def num_rows():

        global df_freq
        if df_freq is None:
            df_freq = trace_freq.as_pandas_dataframe()

        find_clusters()

        return len(clusters) * 2

def plot(num_rows=0, row_pos=1, cpus=[]):

        global df_freq
        if df_freq is None:
            df_freq = trace_freq.as_pandas_dataframe()

        try:
            df_freq.ts = df_freq.ts - df_freq.ts[0]
            df_freq.ts = df_freq.ts / 1000000000
            df_freq['_ts'] = df_freq.ts
            df_freq.freq = df_freq.freq / 1000000
            df_freq.set_index('ts', inplace=True)

            find_clusters()

            for cpu in clusters:
                if len(cpus):
                    if cpu not in cpus:
                        continue

                df_freq_cpu = df_freq[df_freq.cpu == cpu].copy()
                df_freq_cpu['duration'] = -1 * df_freq_cpu._ts.diff(periods=-1)

                total_duration = df_freq_cpu.duration.sum()
                df_duration =  df_freq_cpu.groupby('freq').duration.sum() * 100 / total_duration

                if not num_rows:
                    num_rows = num_rows()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df_freq_cpu.freq.plot(title='CPU' + str(cpu) + ' Frequency', alpha=0.75, drawstyle='steps-post', style='o-', xlim=(df_freq.index[0], df_freq.index[-1]))

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                if not df_duration.empty:
                    ax = df_duration.plot.bar(title='CPU' + str(cpu) + ' Frequency residency %', alpha=0.75)
                    ax.bar_label(ax.containers[0])
        except Exception as e:
            # Most likely the trace has no freq info
            # TODO: Better detect this
            print("Error processing freq.plot():", e)
            pass

        return row_pos
