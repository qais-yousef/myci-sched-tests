#!/usr/bin/env python3
import pandas as pd
import trace_processor as tp
import freq
import pelt
import runtime
import table
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        file = file.replace('.perfetto-trace', '')
        df_result = pd.read_csv(file + '.csv')

        trace = tp.get_trace(file + '.perfetto-trace')
        freq.init(trace)
        pelt.init(trace)
        runtime.init(trace)
        trace.close()

        threads = ['thread0']
        num_rows = freq.num_rows() + pelt.num_rows(threads=threads)

        plt.figure(figsize=(16,3*num_rows))
        row_pos = 1

        plt.subplot(num_rows, 1, row_pos)
        row_pos += 1
        df_result.run.plot(ylim=(0, 20000), style='-', title='runtime (rt-app)', xlim=(df_result.index[0], df_result.index[-1]))
        plt.grid()
        plt.subplot(num_rows, 1, row_pos)
        row_pos += 1
        df_result.slack.plot(ylim=(0, 20000), style='-', title='slack', xlim=(df_result.index[0], df_result.index[-1]))
        plt.grid()

        row_pos = freq.plot(num_rows=num_rows, row_pos=row_pos, cpus=[0])
        row_pos = pelt.plot(num_rows=num_rows, row_pos=row_pos, threads=threads)

        plt.subplot(num_rows, 2, row_pos * 2 - 1)
        df_result.slack.plot.hist(bins=100, alpha=1, title='slack hist')
        plt.grid()
        plt.subplot(num_rows, 2, row_pos * 2 - 0)
        df_result.slack.plot.box(title='slack box')
        plt.grid()
        row_pos += 1

        row_pos = runtime.plot(num_rows=num_rows, row_pos=row_pos, threads=threads)

        row_pos = table.subplot(df_result, num_rows=num_rows, row_pos=row_pos)

        freq.save_csv(file)
        pelt.save_csv(file)
        runtime.save_csv(file)

        plt.tight_layout()
        plt.savefig(file + '.png')
