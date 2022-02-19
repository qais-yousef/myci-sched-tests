#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

query = "select ts, EXTRACT_ARG(arg_set_id, 'comm'), EXTRACT_ARG(arg_set_id, 'util') from raw where name = 'sched_pelt_se'"

def init(trace):

        global trace_util
        trace_util = trace.query(query)

def plot(num_rows=0, row_pos=1, threads=[]):

        df_util = trace_util.as_pandas_dataframe()

        if not len(threads):
            print("Error: must specify threads in util.plot()")
            return row_pos

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
                plt.axhline(y=100, color='r', linestyle='-')
        except:
            # Most likely the trace has no util info
            # TODO: Better detect this
            print("Error processing util.plot()")
            pass

        return row_pos