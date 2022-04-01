#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import text

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
df_pelt_cfs = None

def init(trace):

        global trace_pelt_se
        global trace_pelt_cfs
        global trace_ou
        trace_pelt_se = trace.query(query_se)
        trace_pelt_cfs = trace.query(query_cfs)
        trace_ou = trace.query(query_ou)

def num_rows(threads=[]):

        global df_pelt_cfs
        if df_pelt_cfs is None:
            df_pelt_cfs = trace_pelt_cfs.as_pandas_dataframe()

        # User must multiple this with len(threads) passed to plot()
        return 3 * len(threads) + len(df_pelt_cfs.cpu.unique()) * 2 + len(df_pelt_cfs.path.unique()) - 1

def overlay_ou():

        global df_ou
        if df_ou is None:
            df_ou = trace_ou.as_pandas_dataframe()
            df_ou.ts = df_ou.ts - df_ou.ts[0]
            df_ou.ts = df_ou.ts / 1000000000
            df_ou.set_index('ts', inplace=True)

        threshold = 0 # df_ou.index[-1] / 1000.
        start_ts = None
        total_ou = 0
        i = 0
        for ou in df_ou.overutilized:
            if ou:
                if start_ts is None:
                    start_ts = df_ou.index[i]
            else:
                if start_ts is not None:
                    stop_ts = df_ou.index[i]
                    total_ou += (stop_ts - start_ts)
                    if stop_ts - start_ts > threshold:
                        plt.gca().axvspan(start_ts, stop_ts, alpha=0.1, color='r')
                    start_ts = None
            i += 1

        text.plot(0.01, 1.10, "OU: {:,.2f}%".format(total_ou * 100. / (df_ou.index[-1] - df_ou.index[0])))

def plot(num_rows=0, row_pos=1, threads=[]):

        df_pelt_se = trace_pelt_se.as_pandas_dataframe()

        global df_pelt_cfs
        if df_pelt_cfs is None:
            df_pelt_cfs = trace_pelt_cfs.as_pandas_dataframe()

        if not num_rows:
            func = globals()['num_rows']
            num_rows = func(threads)

        try:
            df_pelt_cfs.ts = df_pelt_cfs.ts - df_pelt_cfs.ts[0]
            df_pelt_cfs.ts = df_pelt_cfs.ts / 1000000000
            df_pelt_cfs.set_index('ts', inplace=True)

            df_pelt_cfs_root = df_pelt_cfs[df_pelt_cfs.path == '/']
            df_pelt_cfs_others = df_pelt_cfs[df_pelt_cfs.path != '/']
            for cpu in sorted(df_pelt_cfs.cpu.unique()):
                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df = df_pelt_cfs_root[df_pelt_cfs_root.cpu == cpu]
                df.util.plot(title='CPU {} util'.format(cpu), drawstyle='steps-post', alpha=0.75, xlim=(df_pelt_cfs.index[0], df_pelt_cfs.index[-1]))
                plt.grid()
                overlay_ou()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df = df_pelt_cfs_others[df_pelt_cfs_others.cpu == cpu]
                df.groupby('path').util.plot(title='CPU {} taskgroup util'.format(cpu), drawstyle='steps-post', alpha=0.75, legend=True, xlim=(df_pelt_cfs.index[0], df_pelt_cfs.index[-1]))
                plt.grid()
                overlay_ou()

            for path in sorted(df_pelt_cfs_others.path.unique()):
                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df = df_pelt_cfs_others[df_pelt_cfs_others.path == path]
                plt.title(path + ' CPU Histogram')
                df.cpu.hist(bins=100, density=False, grid=True, alpha=0.5)
        except Exception as e:
            # Most likely the trace has no util info
            # TODO: Better detect this
            print("Error processing pelt.plot() for cpus:", e)
            pass

        try:
            df_pelt_se.ts = df_pelt_se.ts - df_pelt_se.ts[0]
            df_pelt_se.ts = df_pelt_se.ts / 1000000000
            df_pelt_se.set_index('ts', inplace=True)

            for thread in threads:
                df = df_pelt_se[df_pelt_se.comm.str.contains(thread)]

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df.groupby('comm').util.plot(title=thread + ' util', drawstyle='steps-post', alpha=0.75, legend=True, xlim=(df_pelt_se.index[0], df_pelt_se.index[-1]))
                plt.grid()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                plt.title(thread + ' util Histogram')
                df.groupby('comm').util.hist(bins=100, density=False, grid=True, alpha=0.5, legend=True)

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                plt.title(thread + ' CPU Histogram')
                df.groupby('comm').cpu.hist(bins=100, density=False, grid=True, alpha=0.5, legend=True)
        except Exception as e:
            # Most likely the trace has no util info
            # TODO: Better detect this
            print("Error processing pelt.plot() for threads:", e)
            pass

        return row_pos
