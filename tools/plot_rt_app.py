#!/usr/bin/env python3
import pandas as pd
from tabulate import tabulate
from perfetto.trace_processor import TraceProcessor as tp
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

query_freq = "select ts, cpu, value as freq from counter join cpu_counter_track on counter.track_id = cpu_counter_track.id"
query_util = "select ts, EXTRACT_ARG(arg_set_id, 'comm'), EXTRACT_ARG(arg_set_id, 'util') from raw where name = 'sched_pelt_se'"
query_runtime = "select ts, EXTRACT_ARG(arg_set_id, 'comm'), EXTRACT_ARG(arg_set_id, 'runtime'), EXTRACT_ARG(arg_set_id, 'vruntime') from raw where name = 'sched_stat_runtime'"

for file in sorted(os.listdir()):
    if file.endswith(".csv"):
        file = file.replace('.csv', '')
        df_result = pd.read_csv(file + '.csv')

        print(tabulate(df_result.describe(), headers='keys', tablefmt='psql'))

        trace = tp(file_path=file + '.perfetto-trace')
        trace_freq = trace.query(query_freq)
        trace_util = trace.query(query_util)
        trace_runtime = trace.query(query_runtime)
        df_freq = trace_freq.as_pandas_dataframe()
        df_util = trace_util.as_pandas_dataframe()
        df_runtime = trace_runtime.as_pandas_dataframe()

        plt.figure(figsize=(16,8))
        plt.subplot(6, 1, 1)
        df_result.slack.plot(ylim=(0, 20000), style='o-', title='slack', xlim=(df_result.index[0], df_result.index[-1]))
        plt.subplot(6, 2, 7)
        df_result.slack.plot.hist(bins=100, alpha=1, title='slack hist')
        plt.subplot(6, 2, 8)
        df_result.slack.plot.box(title='slack box')

        try:
            df_freq.ts = df_freq.ts - df_freq.ts[0]
            df_freq.ts = df_freq.ts / 1000000000
            df_freq.freq = df_freq.freq / 1000000
            df_freq.set_index('ts', inplace=True)

            df_freq = df_freq[df_freq.cpu == 0]

            plt.subplot(6, 1, 2)
            df_freq.freq.plot(title='frequency', alpha=0.75, drawstyle='steps-post', xlim=(df_util.index[0], df_util.index[-1]))
        except:
            pass

        try:
            df_util.ts = df_util.ts - df_util.ts[0]
            df_util.ts = df_util.ts / 1000000000
            df_util.set_index('ts', inplace=True)

            df_util.columns = df_util.columns.str.replace('EXTRACT_ARG\(arg_set_id, \'', '')
            df_util.columns = df_util.columns.str.replace('\'\)', '')
            df_util = df_util[df_util.comm.str.contains('thread0')]

            plt.subplot(6, 1, 3)
            df_util.groupby('comm').util.plot(title='util', alpha=0.75, xlim=(df_util.index[0], df_util.index[-1]))
            plt.axhline(y=100, color='r', linestyle='-')
        except:
            pass

        try:
            df_runtime.ts = df_runtime.ts - df_runtime.ts[0]
            df_runtime.ts = df_runtime.ts / 1000000000
            df_runtime.set_index('ts', inplace=True)

            df_runtime.columns = df_runtime.columns.str.replace('EXTRACT_ARG\(arg_set_id, \'', '')
            df_runtime.columns = df_runtime.columns.str.replace('\'\)', '')
            df_runtime = df_runtime[df_runtime.comm.str.contains('thread0')]

            df_runtime.runtime = df_runtime.runtime / 1000000
            df_runtime.vruntime = df_runtime.vruntime / 1000000

            plt.subplot(6, 1, 5)
            df_runtime.groupby('comm').runtime.plot(title='runtime (ms)', alpha=0.75, xlim=(df_runtime.index[0], df_runtime.index[-1]))
            plt.subplot(6, 1, 6)
            df_runtime.groupby('comm').vruntime.plot(title='vruntime (ms)', alpha=0.75, xlim=(df_runtime.index[0], df_runtime.index[-1]))
        except:
            pass

        plt.tight_layout()
        plt.savefig('result.png')
