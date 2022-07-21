#!/usr/bin/env python3
import trace_processor as tp
import rq_pressure
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

for file in sorted(os.listdir()):
    if file.endswith(".perfetto-trace"):
        trace = tp.get_trace(file)
        rq_pressure.init(trace)
        trace.close()

        num_rows = rq_pressure.num_rows()

        plt.figure(figsize=(16,3*num_rows))

        prefix = file.replace('.perfetto-trace', '')

        rq_pressure.plot()
        rq_pressure.save_csv(prefix)

        plt.tight_layout()
        plt.savefig(prefix + '_rq_pressure.png')
