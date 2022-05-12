#!/usr/bin/env python3
from perfetto.trace_processor import TraceProcessor as tp
import thermal
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp(file_path=file)
        thermal.init(trace)
        trace.close()

        plt.figure(figsize=(16,16))

        prefix = file.replace('.perfetto-trace', '')

        thermal.plot()
        thermal.save_csv(prefix)

        plt.tight_layout()
        plt.savefig(prefix + '_thermal.png')
