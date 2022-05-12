#!/usr/bin/env python3
from perfetto.trace_processor import TraceProcessor as tp
import pelt
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
        pelt.init(trace)
        trace.close()

        num_rows = pelt.num_rows(threads)

        plt.figure(figsize=(16,3*num_rows))

        prefix = file.replace('.perfetto-trace', '')

        pelt.plot(threads=threads)
        pelt.save_csv(prefix)

        plt.tight_layout()
        plt.savefig(prefix + '_pelt.png')
