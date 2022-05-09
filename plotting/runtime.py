#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

query = "select ts, EXTRACT_ARG(arg_set_id, 'comm') as comm, EXTRACT_ARG(arg_set_id, 'runtime') as runtime, EXTRACT_ARG(arg_set_id, 'vruntime') as vruntime from raw where name = 'sched_stat_runtime'"

df_runtime = None

def init(trace):

        global trace_runtime
        trace_runtime = trace.query(query)

def __init():

        global df_runtime
        if df_runtime is None:
            df_runtime = trace_runtime.as_pandas_dataframe()
            df_runtime.ts = df_runtime.ts - df_runtime.ts[0]
            df_runtime.ts = df_runtime.ts / 1000000000
            df_runtime.set_index('ts', inplace=True)

def num_rows():

        # User must multiple this with len(threads) passed to plot()
        return 2

def save_csv(prefix):

        __init()

        df_runtime.to_csv(prefix + '_runtime.csv')

def plot(num_rows=0, row_pos=1, threads=[]):

        __init()

        if not len(threads):
            print("Error: must specify threads in runtime.plot()")
            return row_pos

        try:
            for thread in threads:
                df_runtime = df_runtime[df_runtime.comm.str.contains(thread)]

                df_runtime.runtime = df_runtime.runtime / 1000000
                df_runtime.vruntime = df_runtime.vruntime / 1000000

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df_runtime.groupby('comm').runtime.plot(title='runtime (ms)', alpha=0.75, xlim=(df_runtime.index[0], df_runtime.index[-1]))
                plt.grid()
                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df_runtime.groupby('comm').vruntime.plot(title='vruntime (ms)', alpha=0.75, xlim=(df_runtime.index[0], df_runtime.index[-1]))
                plt.grid()
        except Exception as e:
            # Most likely the trace has no runtime info
            # TODO: Better detect this
            print("Error processing runtime.plot():", e)
            pass

        return row_pos
