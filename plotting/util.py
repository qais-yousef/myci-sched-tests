#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

query_se = "select ts, \
            EXTRACT_ARG(arg_set_id, 'cpu') as cpu, \
            EXTRACT_ARG(arg_set_id, 'path') as path, \
            EXTRACT_ARG(arg_set_id, 'comm') as comm, \
            EXTRACT_ARG(arg_set_id, 'pid') as pid, \
            EXTRACT_ARG(arg_set_id, 'util') as util \
            from raw where name = 'sched_pelt_se'"

query_cfs = "select ts, \
            EXTRACT_ARG(arg_set_id, 'cpu') as cpu, \
            EXTRACT_ARG(arg_set_id, 'path') as path, \
            EXTRACT_ARG(arg_set_id, 'util') as util \
            from raw where name = 'sched_pelt_cfs'"

query_ou = "select ts, \
            EXTRACT_ARG(arg_set_id, 'overutilized') as overutilized, \
            EXTRACT_ARG(arg_set_id, 'span') as span \
            from raw where name = 'sched_overutilized'"

df_ou = None
df_util_cfs = None

def init(trace):

        global trace_util_se
        global trace_util_cfs
        global trace_ou
        trace_util_se = trace.query(query_se)
        trace_util_cfs = trace.query(query_cfs)
        trace_ou = trace.query(query_ou)

def num_rows(threads=[]):

        global df_util_cfs
        if df_util_cfs is None:
            df_util_cfs = trace_util_cfs.as_pandas_dataframe()

        # User must multiple this with len(threads) passed to plot()
        return 4 * len(threads) + len(df_util_cfs.cpu.unique()) * 2

def overlay_ou():

        global df_ou
        if df_ou is None:
            df_ou = trace_ou.as_pandas_dataframe()
            df_ou.ts = df_ou.ts - df_ou.ts[0]
            df_ou.ts = df_ou.ts / 1000000000
            df_ou.set_index('ts', inplace=True)

        start_ts = None
        i = 0
        for ou in df_ou.overutilized:
            if ou:
                if start_ts is None:
                    start_ts = df_ou.index[i]
            else:
                if start_ts is not None:
                    plt.gca().axvspan(start_ts, df_ou.index[i], alpha=0.1, color='r')
                    start_ts = None
            i += 1

def plot(num_rows=0, row_pos=1, threads=[]):

        df_util_se = trace_util_se.as_pandas_dataframe()

        global df_util_cfs
        if df_util_cfs is None:
            df_util_cfs = trace_util_cfs.as_pandas_dataframe()

        if not num_rows:
            func = globals()['num_rows']
            num_rows = func(threads)

        try:
            df_util_cfs.ts = df_util_cfs.ts - df_util_cfs.ts[0]
            df_util_cfs.ts = df_util_cfs.ts / 1000000000
            df_util_cfs.set_index('ts', inplace=True)

            df_util_cfs_root = df_util_cfs[df_util_cfs.path == '/']
            df_util_cfs_others = df_util_cfs[df_util_cfs.path != '/']
            for cpu in sorted(df_util_cfs.cpu.unique()):
                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df = df_util_cfs_root[df_util_cfs_root.cpu == cpu]
                df.util.plot(title='CPU {} util'.format(cpu), drawstyle='steps-post', alpha=0.75, legend=True, xlim=(df_util_cfs.index[0], df_util_cfs.index[-1]))
                overlay_ou()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df = df_util_cfs_others[df_util_cfs_others.cpu == cpu]
                df.groupby('path').util.plot(title='CPU {} taskgroup util'.format(cpu), drawstyle='steps-post', alpha=0.75, legend=True, xlim=(df_util_cfs.index[0], df_util_cfs.index[-1]))
                overlay_ou()
        except Exception as e:
            # Most likely the trace has no util info
            # TODO: Better detect this
            print("Error processing util.plot() for cpus:", e)
            pass

        try:
            df_util_se.ts = df_util_se.ts - df_util_se.ts[0]
            df_util_se.ts = df_util_se.ts / 1000000000
            df_util_se.set_index('ts', inplace=True)

            for thread in threads:
                df = df_util_se[df_util_se.comm.str.contains(thread)]

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df.groupby('comm').util.plot(title=thread + ' util', drawstyle='steps-post', alpha=0.75, legend=True, xlim=(df_util_se.index[0], df_util_se.index[-1]))
                plt.grid()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                plt.title(thread + ' util per pid Histogram')
                df.groupby('comm').util.hist(bins=100, density=False, grid=True, alpha=0.5, legend=True)

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                plt.title(thread + ' cpu per pid Histogram')
                df.groupby('comm').cpu.hist(bins=100, density=False, grid=True, alpha=0.5, legend=True)

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                plt.title(thread + ' taskgroup per pid Histogram')
                df.groupby('comm').path.hist(bins=100, density=False, grid=True, alpha=0.5, legend=True)
        except Exception as e:
            # Most likely the trace has no util info
            # TODO: Better detect this
            print("Error processing util.plot() for threads:", e)
            pass

        return row_pos
