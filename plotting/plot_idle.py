#!/usr/bin/env python3
from perfetto.trace_processor import TraceProcessor as tp
import idle
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp(file_path=file)
        idle.init(trace)
        trace.close()

        plt.figure(figsize=(16,16))
        idle.plot()
        plt.tight_layout()
        plt.savefig(file.replace('.perfetto-trace', '') + '_idle.png')
