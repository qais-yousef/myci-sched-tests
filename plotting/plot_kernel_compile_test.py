#!/usr/bin/env python3
import pandas as pd
from perfetto.trace_processor import TraceProcessor as tp
import freq
import pelt
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp(file_path=file)
        freq.init(trace)
        pelt.init(trace)
        trace.close()

        plt.figure(figsize=(16,16))

        num_rows = freq.num_rows() + pelt.num_rows()
        row_pos = 1

        row_pos = pelt.plot(num_rows=num_rows, row_pos=row_pos, threads=['make'])
        row_pos = freq.plot(num_rows=num_rows, row_pos=row_pos)

        prefix = file.replace('.perfetto-trace', '')
        pelt.save_csv(prefix)
        freq.save_csv(prefix)

        plt.tight_layout()
        plt.savefig('kernel_compile_time_result.png')
