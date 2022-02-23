#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import text

query = "select ts, cpu, value as idle from counter as c left join cpu_counter_track as t on c.track_id = t.id where t.name = 'cpuidle'"

df_idle = None

def init(trace):

        global trace_idle
        trace_idle = trace.query(query)

def num_rows():

        global df_idle
        if df_idle is None:
            df_idle = trace_idle.as_pandas_dataframe()

        return len(df_idle.cpu.unique())

def plot(num_rows=0, row_pos=1, cpus=[]):

        global df_idle
        if df_idle is None:
            df_idle = trace_idle.as_pandas_dataframe()

        try:
            df_idle.ts = df_idle.ts - df_idle.ts[0]
            df_idle.ts = df_idle.ts / 1000000000
            df_idle['_ts'] = df_idle.ts
            df_idle.set_index('ts', inplace=True)

            # This magic value is exit from idle. Values 0 and above are idle
            # states
            df_idle.idle.replace(4294967295, -1, inplace=True)
            df_idle.idle = df_idle.idle + 1

            nr_cpus = len(df_idle.cpu.unique())

            df_idle_cpu = df_idle[df_idle.cpu == 0]
            for cpu in range(nr_cpus):
                if len(cpus):
                    if cpu not in cpus:
                        continue

                df_idle_cpu = df_idle[df_idle.cpu == cpu].copy()
                df_idle_cpu['duration'] = -1 * df_idle_cpu._ts.diff(periods=-1)

                total_duration = df_idle_cpu.duration.sum()
                df_duration =  df_idle_cpu.groupby('idle').duration.sum() * 100 / total_duration

                if not num_rows:
                    func = globals()['num_rows']
                    num_rows = func()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                if not df_duration.empty:
                    ax = df_duration.plot.bar(title='CPU{}'.format(cpu) + ' Idle residency %', alpha=0.75)
                    ax.bar_label(ax.containers[0])
                    text.plot(0.01, 1.20, "0 is NOT idle (IDLE_EXIT)")
        except Exception as e:
            # Most likely the trace has no idle info
            # TODO: Better detect this
            print("Error processing idle.plot():", e)
            pass

        return row_pos
