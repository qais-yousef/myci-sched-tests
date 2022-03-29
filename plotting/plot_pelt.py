#!/usr/bin/env python3
from perfetto.trace_processor import TraceProcessor as tp
import util
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
        trace = tp(file_path=file)
        util.init(trace)
        trace.close()

        num_rows = util.num_rows(threads)

        plt.figure(figsize=(16,3*num_rows))
        util.plot(threads=threads)
        plt.tight_layout()
        plt.savefig(file.replace('.perfetto-trace', '') + '_util.png')
