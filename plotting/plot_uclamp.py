#!/usr/bin/env python3
import trace_processor as tp
import uclamp
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    threads = sys.argv[1].split()
except:
    threads = []

for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp.get_trace(file)
        uclamp.init(trace)
        trace.close()

        num_rows = uclamp.num_rows(threads)

        plt.figure(figsize=(16,3*num_rows))

        prefix = file.replace('.perfetto-trace', '')

        uclamp.plot(threads=threads)
        uclamp.save_csv(prefix)

        plt.tight_layout()
        plt.savefig(prefix + '_uclamp.png')
