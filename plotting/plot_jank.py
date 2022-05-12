#!/usr/bin/env python3
from perfetto.trace_processor import TraceProcessor as tp
import jank
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp(file_path=file)
        jank.init(trace)
        trace.close()

        plt.figure(figsize=(16,3*jank.num_rows()))

        prefix = file.replace('.perfetto-trace', '')

        jank.plot()
        jank.save_csv(prefix)

        plt.tight_layout()
        plt.savefig(prefix + '_jank.png')
