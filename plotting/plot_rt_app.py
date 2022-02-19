#!/usr/bin/env python3
import pandas as pd
from tabulate import tabulate
from perfetto.trace_processor import TraceProcessor as tp
import freq
import util
import runtime
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


num_rows=7

for file in sorted(os.listdir()):
    if file.endswith(".csv"):
        file = file.replace('.csv', '')
        df_result = pd.read_csv(file + '.csv')

        # print(tabulate(df_result.describe(), headers='keys', tablefmt='psql'))

        trace = tp(file_path=file + '.perfetto-trace')
        freq.init(trace)
        util.init(trace)
        runtime.init(trace)
        trace.close()


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

        row_pos = runtime.plot(num_rows=num_rows, row_pos=row_pos, threads=['thread0'])

        plt.tight_layout()
        plt.savefig(file + '.png')
