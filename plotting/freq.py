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

def __find_clusters():

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

def __init():

        global df_freq
        if df_freq is None:
            df_freq = trace_freq.as_pandas_dataframe()
            df_freq.ts = df_freq.ts - df_freq.ts[0]
            df_freq.ts = df_freq.ts / 1000000000
            df_freq['_ts'] = df_freq.ts
            df_freq.freq = df_freq.freq / 1000000
            df_freq.set_index('ts', inplace=True)

        __find_clusters()

def num_rows():

        __init()

        return len(clusters) * 2

def save_csv(prefix):

        __init()

        df_freq.to_csv(prefix + '_freq.csv')

def plot(num_rows=0, row_pos=1, cpus=[]):

        __init()

        try:
            color = ['b', 'y', 'r']
            i = 0
            for cpu in clusters:
                if len(cpus):
                    if cpu not in cpus:
                        continue

                df_freq_cpu = df_freq[df_freq.cpu == cpu].copy()
                df_freq_cpu['duration'] = -1 * df_freq_cpu._ts.diff(periods=-1)

                total_duration = df_freq_cpu.duration.sum()
                df_duration =  df_freq_cpu.groupby('freq').duration.sum() * 100 / total_duration

                if not num_rows:
                    func = globals()['num_rows']
                    num_rows = func()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df_freq_cpu.freq.plot(title='CPU' + str(cpu) + ' Frequency', alpha=0.75, drawstyle='steps-post', style='-', color=color[i], xlim=(df_freq.index[0], df_freq.index[-1]))
                plt.grid()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                if not df_duration.empty:
                    ax = df_duration.plot.bar(title='CPU' + str(cpu) + ' Frequency residency %', alpha=0.75, color=color[i])
                    ax.bar_label(ax.containers[0])
                    plt.grid()

                i += 1
                if i == 3:
                    i = 0
        except Exception as e:
            # Most likely the trace has no freq info
            # TODO: Better detect this
            print("Error processing freq.plot():", e)
            pass

        return row_pos
