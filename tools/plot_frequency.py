#!/usr/bin/env python3
import pandas as pd
from perfetto.trace_processor import TraceProcessor as tp
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

query_freq = "select ts, cpu, value as freq from counter join cpu_counter_track on counter.track_id = cpu_counter_track.id"

for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp(file_path=file)
        trace_freq = trace.query(query_freq)
        trace.close()

        df_freq = trace_freq.as_pandas_dataframe()

        plt.figure(figsize=(16,16))

        try:
            df_freq.ts = df_freq.ts - df_freq.ts[0]
            df_freq.ts = df_freq.ts / 1000000000
            df_freq.freq = df_freq.freq / 1000000
            df_freq.set_index('ts', inplace=True)

            nr_cpus = len(df_freq.cpu.unique())
            nr_freqs = len(df_freq.freq.unique())

            for cpu in range(nr_cpus):
                plt.subplot(nr_cpus * 2 + 1, 1, cpu * 2 + 1)
                df_freq[df_freq.cpu == cpu].freq.plot(title='CPU' + str(cpu) + ' frequency', alpha=0.75, drawstyle='steps-post', xlim=(df_freq.index[0], df_freq.index[-1]))
                plt.subplot(nr_cpus * 2 + 1, 1, cpu * 2 + 2)
                df_freq[df_freq.cpu == cpu].freq.hist(bins=nr_freqs, alpha=0.75)
        except:
            pass

        plt.tight_layout()
        plt.savefig(file.replace('.perfetto-trace', '') + '_frequency.png')
