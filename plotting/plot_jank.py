#!/usr/bin/env python3
import trace_processor as tp
import jank
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp.get_trace(file)
        jank.init(trace)
        trace.close()

        plt.figure(figsize=(16,3*jank.num_rows()))

        prefix = file.replace('.perfetto-trace', '')

        jank.plot()
        jank.save_csv(prefix)

        plt.tight_layout()
        plt.savefig(prefix + '_jank.png')
