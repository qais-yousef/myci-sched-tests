#!/usr/bin/env python3
import trace_processor as tp
import freq
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp.get_trace(file)
        freq.init(trace)
        trace.close()

        plt.figure(figsize=(16,16))

        prefix = file.replace('.perfetto-trace', '')

        freq.plot()
        freq.save_csv(prefix)

        plt.tight_layout()
        plt.savefig(prefix + '_frequency.png')
