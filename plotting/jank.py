#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import table
import text

query = "select ts, dur, surface_frame_token as app_token, display_frame_token, " \
    "jank_type, on_time_finish, present_type, layer_name, process.name from actual_frame_timeline_slice left join process using(upid)"

def init(trace):

        global trace_jank
        trace_jank = trace.query(query)

        global df_jank
        df_jank = None

        global processes
        processes = None

def num_rows():

        global df_jank
        if df_jank is None:
            df_jank = trace_jank.as_pandas_dataframe()

        if df_jank.empty:
            return 0

        global processes
        if processes is None:
            processes = sorted(df_jank.name.unique())

        return len(processes) * 3

def plot(num_rows=0, row_pos=1, names=[]):

        global df_jank
        if df_jank is None:
            df_jank = trace_jank.as_pandas_dataframe()

        global processes
        if processes is None:
            processes = sorted(df_jank.name.unique())

        if not num_rows:
            func = globals()['num_rows']
            num_rows = func()

        try:
            df_jank.ts = df_jank.ts - df_jank.ts[0]
            df_jank.ts = df_jank.ts / 1000000000
            df_jank['_ts'] = df_jank.ts
            df_jank.dur = df_jank.dur / 1000000
            df_jank.set_index('ts', inplace=True)

            for name in processes:
                if len(names):
                    if name not in names:
                        continue

                df_jank_process = df_jank[df_jank.name == name].copy()
                df_janky_frames = df_jank_process[df_jank_process.jank_type != 'None'].copy()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df_jank_process.dur.plot(title=name + ' Frame Duration', alpha=0.75, style='o', color='g', xlim=(df_jank.index[0], df_jank.index[-1]))
                df_janky_frames.dur.plot(alpha=0.5, style='o', color='r', label='janks', legend=True)
                text.plot(0.01, 1.1, "Janks: {}".format(df_janky_frames.dur.count()))
                plt.grid()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                ax = df_jank_process.dur.plot.kde(title=name + ' Frame Duration Density', alpha=0.75, color='g', xlim=(0, 30))
                ax.axvspan(16, 30, alpha=0.1, color='r')
                plt.grid()

                row_pos = table.subplot(df_jank_process, num_rows=num_rows, row_pos=row_pos, columns=['dur'])
        except Exception as e:
            # Most likely the trace has no jank info
            # TODO: Better detect this
            print("Error processing jank.plot():", e)
            pass

        return row_pos
