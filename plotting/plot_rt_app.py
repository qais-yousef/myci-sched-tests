#!/usr/bin/env python3
import pandas as pd
from tabulate import tabulate
from perfetto.trace_processor import TraceProcessor as tp
import freq
import util
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

query_runtime = "select ts, EXTRACT_ARG(arg_set_id, 'comm'), EXTRACT_ARG(arg_set_id, 'runtime'), EXTRACT_ARG(arg_set_id, 'vruntime') from raw where name = 'sched_stat_runtime'"

num_rows=7

for file in sorted(os.listdir()):
    if file.endswith(".csv"):
        file = file.replace('.csv', '')
        df_result = pd.read_csv(file + '.csv')

        # print(tabulate(df_result.describe(), headers='keys', tablefmt='psql'))

        trace = tp(file_path=file + '.perfetto-trace')
        freq.init(trace)
        util.init(trace)
        trace_runtime = trace.query(query_runtime)
        trace.close()

        df_runtime = trace_runtime.as_pandas_dataframe()

        plt.figure(figsize=(16,16))
        row_pos = 1

        plt.subplot(num_rows, 1, row_pos)
        row_pos += 1
        df_result.slack.plot(ylim=(0, 20000), style='o-', title='slack', xlim=(df_result.index[0], df_result.index[-1]))

        row_pos = freq.plot(num_rows=num_rows, row_pos=row_pos, cpus=[0])
        row_pos = util.plot(num_rows=num_rows, row_pos=row_pos, threads=['thread0'])

        plt.subplot(num_rows, 2, row_pos * 2 - 1)
        df_result.slack.plot.hist(bins=100, alpha=1, title='slack hist')
        plt.subplot(num_rows, 2, row_pos * 2 - 0)
        df_result.slack.plot.box(title='slack box')
        row_pos += 1

        try:
            df_runtime.ts = df_runtime.ts - df_runtime.ts[0]
            df_runtime.ts = df_runtime.ts / 1000000000
            df_runtime.set_index('ts', inplace=True)

            df_runtime.columns = df_runtime.columns.str.replace('EXTRACT_ARG\(arg_set_id, \'', '', regex=True)
            df_runtime.columns = df_runtime.columns.str.replace('\'\)', '', regex=True)
            df_runtime = df_runtime[df_runtime.comm.str.contains('thread0')]

            df_runtime.runtime = df_runtime.runtime / 1000000
            df_runtime.vruntime = df_runtime.vruntime / 1000000

            plt.subplot(num_rows, 1, row_pos)
            row_pos += 1
            df_runtime.groupby('comm').runtime.plot(title='runtime (ms)', alpha=0.75, xlim=(df_runtime.index[0], df_runtime.index[-1]))
            plt.subplot(num_rows, 1, row_pos)
            row_pos += 1
            df_runtime.groupby('comm').vruntime.plot(title='vruntime (ms)', alpha=0.75, xlim=(df_runtime.index[0], df_runtime.index[-1]))
        except:
            print("Error plotting runtime")
            pass

        plt.tight_layout()
        plt.savefig(file + '.png')
