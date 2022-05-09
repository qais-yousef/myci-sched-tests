#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

query_se = "select ts, \
            EXTRACT_ARG(arg_set_id, 'cpu') as cpu, \
            EXTRACT_ARG(arg_set_id, 'comm') as comm, \
            EXTRACT_ARG(arg_set_id, 'pid') as pid, \
            EXTRACT_ARG(arg_set_id, 'util_avg') as util, \
            EXTRACT_ARG(arg_set_id, 'uclamp_avg') as uclamp_avg, \
            EXTRACT_ARG(arg_set_id, 'uclamp_min') as uclamp_min, \
            EXTRACT_ARG(arg_set_id, 'uclamp_max') as uclamp_max \
            from raw where name = 'uclamp_util_se'"

query_cfs = "select ts, \
            EXTRACT_ARG(arg_set_id, 'cpu') as cpu, \
            EXTRACT_ARG(arg_set_id, 'util_avg') as util, \
            EXTRACT_ARG(arg_set_id, 'uclamp_avg') as uclamp_avg, \
            EXTRACT_ARG(arg_set_id, 'uclamp_min') as uclamp_min, \
            EXTRACT_ARG(arg_set_id, 'uclamp_max') as uclamp_max \
            from raw where name = 'uclamp_util_cfs'"

df_uclamp_cfs = None
df_uclamp_se = None

def init(trace):

        global trace_uclamp_se
        global trace_uclamp_cfs
        trace_uclamp_se = trace.query(query_se)
        trace_uclamp_cfs = trace.query(query_cfs)

def __init():

        global df_uclamp_cfs
        if df_uclamp_cfs is None:
            df_uclamp_cfs = trace_uclamp_cfs.as_pandas_dataframe()
            df_uclamp_cfs.ts = df_uclamp_cfs.ts - df_uclamp_cfs.ts[0]
            df_uclamp_cfs.ts = df_uclamp_cfs.ts / 1000000000
            df_uclamp_cfs.set_index('ts', inplace=True)

        global df_uclamp_se
        if df_uclamp_se is None:
            df_uclamp_se = trace_uclamp_se.as_pandas_dataframe()
            df_uclamp_se.ts = df_uclamp_se.ts - df_uclamp_se.ts[0]
            df_uclamp_se.ts = df_uclamp_se.ts / 1000000000
            df_uclamp_se.set_index('ts', inplace=True)

def num_rows(threads=[]):

        __init()

        # User must multiple this with len(threads) passed to plot()
        return 4 * len(threads) + len(df_uclamp_cfs.cpu.unique()) * 2

def save_csv(prefix):

        __init()

        df_uclamp_cfs.to_csv(prefix + '_uclamp_cfs.csv')
        df_uclamp_se.to_csv(prefix + '_uclamp_se.csv')

def plot(num_rows=0, row_pos=1, threads=[]):

        __init()

        if not num_rows:
            func = globals()['num_rows']
            num_rows = func(threads)

        try:
            for cpu in sorted(df_uclamp_cfs.cpu.unique()):
                df = df_uclamp_cfs[df_uclamp_cfs.cpu == cpu]

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df.util.plot(title='CPU {} util'.format(cpu), drawstyle='steps-post', alpha=0.75, xlim=(df_uclamp_cfs.index[0], df_uclamp_cfs.index[-1]))
                plt.grid()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df.uclamp_avg.plot(title='CPU {} uclamp'.format(cpu), label='uclamp_avg', legend=True, drawstyle='steps-post', alpha=0.75, xlim=(df_uclamp_cfs.index[0], df_uclamp_cfs.index[-1]))
                df.uclamp_min.plot(label='uclamp_min', legend=True, drawstyle='steps-post', alpha=0.75, color='g', xlim=(df_uclamp_cfs.index[0], df_uclamp_cfs.index[-1]))
                df.uclamp_max.plot(label='uclamp_max', legend=True, drawstyle='steps-post', alpha=0.75, color='r', xlim=(df_uclamp_cfs.index[0], df_uclamp_cfs.index[-1]))
                plt.grid()
        except Exception as e:
            # Most likely the trace has no util info
            # TODO: Better detect this
            print("Error processing uclamp.plot() for cpus:", e)
            pass

        try:
            for thread in threads:
                df = df_uclamp_se[df_uclamp_se.comm.str.contains(thread)]

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df.groupby('comm').util.plot(title=thread + ' util', drawstyle='steps-post', alpha=0.75, legend=True, xlim=(df_uclamp_se.index[0], df_uclamp_se.index[-1]))
                plt.grid()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df.groupby('comm').uclamp_avg.plot(title=thread + ' uclamp_avg', drawstyle='steps-post', alpha=0.75, legend=True, xlim=(df_uclamp_se.index[0], df_uclamp_se.index[-1]))

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df.groupby('comm').uclamp_min.plot(title=thread + ' uclamp_min', drawstyle='steps-post', alpha=0.75, legend=True, xlim=(df_uclamp_se.index[0], df_uclamp_se.index[-1]))

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df.groupby('comm').uclamp_max.plot(title=thread + ' uclamp_max', drawstyle='steps-post', alpha=0.75, legend=True, xlim=(df_uclamp_se.index[0], df_uclamp_se.index[-1]))
        except Exception as e:
            # Most likely the trace has no util info
            # TODO: Better detect this
            print("Error processing uclamp.plot() for threads:", e)
            pass

        return row_pos
