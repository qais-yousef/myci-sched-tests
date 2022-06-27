#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

query = "select ts, cpu, value as idle from counter as c left join cpu_counter_track as t on c.track_id = t.id where t.name = 'cpuidle'"

df_idle = None

def init(trace):

        global trace_idle
        trace_idle = trace.query(query)

def __init():

        global df_idle
        if df_idle is None:
            df_idle = trace_idle.as_pandas_dataframe()
            df_idle.ts = df_idle.ts - df_idle.ts[0]
            df_idle.ts = df_idle.ts / 1000000000
            df_idle['_ts'] = df_idle.ts
            df_idle.set_index('ts', inplace=True)

            # This magic value is exit from idle. Values 0 and above are idle
            # states
            df_idle.idle.replace(4294967295, -1, inplace=True)

def num_rows():

        __init()

        return int((len(df_idle.cpu.unique()) + 3) / 4)

def save_csv(prefix):

        __init()

        df_idle.to_csv(prefix + '_idle.csv')

def plot(num_rows=0, row_pos=1, cpus=[]):

        __init()

        if not num_rows:
            func = globals()['num_rows']
            num_rows = func()

        try:
            nr_cpus = len(df_idle.cpu.unique())

            col = 0
            df_idle_cpu = df_idle[df_idle.cpu == 0]
            for cpu in range(nr_cpus):
                if len(cpus):
                    if cpu not in cpus:
                        continue

                df_idle_cpu = df_idle[df_idle.cpu == cpu].copy()
                df_idle_cpu['duration'] = -1 * df_idle_cpu._ts.diff(periods=-1)

                total_duration = df_idle_cpu.duration.sum()
                df_duration =  df_idle_cpu.groupby('idle').duration.sum() * 100 / total_duration

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

                if not df_duration.empty:
                    ax = df_duration.plot.bar(title='CPU{}'.format(cpu) + ' Idle residency %', alpha=0.75, color='grey')
                    ax.bar_label(ax.containers[0])
                    ax.set_xlabel('Idle State')
                    plt.grid()

            if col:
                row_pos += 1
        except Exception as e:
            # Most likely the trace has no idle info
            # TODO: Better detect this
            print("Error processing idle.plot():", e)
            pass

        return row_pos
