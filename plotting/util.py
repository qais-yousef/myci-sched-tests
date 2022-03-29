#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

query = "select ts, EXTRACT_ARG(arg_set_id, 'comm'), EXTRACT_ARG(arg_set_id, 'util') from raw where name = 'sched_pelt_se'"

def init(trace):

        global trace_util
        trace_util = trace.query(query)

def num_rows():

        # User must multiple this with len(threads) passed to plot()
        return 1

def plot(num_rows=0, row_pos=1, threads=[]):

        df_util = trace_util.as_pandas_dataframe()

        if not len(threads):
            print("Error: must specify threads in util.plot()")
            return row_pos

        if not num_rows:
            func = globals()['num_rows']
            num_rows = func() * len(threads)

        try:
            df_util.ts = df_util.ts - df_util.ts[0]
            df_util.ts = df_util.ts / 1000000000
            df_util.set_index('ts', inplace=True)

            df_util.columns = df_util.columns.str.replace('EXTRACT_ARG\(arg_set_id, \'', '', regex=True)
            df_util.columns = df_util.columns.str.replace('\'\)', '', regex=True)

            for thread in threads:
                df_util = df_util[df_util.comm.str.contains(thread)]

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df_util.groupby('comm').util.plot(title=thread + ' util', alpha=0.75, xlim=(df_util.index[0], df_util.index[-1]))
                plt.grid()
        except Exception as e:
            # Most likely the trace has no util info
            # TODO: Better detect this
            print("Error processing util.plot():", e)
            pass

        return row_pos
