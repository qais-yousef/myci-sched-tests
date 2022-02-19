#!/usr/bin/env python3
import pandas as pd
from tabulate import tabulate
from perfetto.trace_processor import TraceProcessor as tp
import freq
import util
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp(file_path=file)
        freq.init(trace)
        util.init(trace)
        trace.close()

        plt.figure(figsize=(16,16))
        num_rows = freq.nr_cpus() * 2 + 1
        row_pos = 1

        row_pos = util.plot(num_rows=num_rows, row_pos=row_pos, threads=['make'])
        row_pos = freq.plot(num_rows=num_rows, row_pos=row_pos)

        plt.tight_layout()
        plt.savefig('kernel_compile_time_result.png')
