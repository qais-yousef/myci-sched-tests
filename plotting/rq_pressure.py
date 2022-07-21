#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import text

query_irq = "select ts, \
             EXTRACT_ARG(arg_set_id, 'cpu') as cpu, \
             EXTRACT_ARG(arg_set_id, 'util') as util \
             from raw where name = 'sched_pelt_irq'"

query_rt = "select ts, \
            EXTRACT_ARG(arg_set_id, 'cpu') as cpu, \
            EXTRACT_ARG(arg_set_id, 'util') as util \
            from raw where name = 'sched_pelt_rt'"

query_thermal = "select ts, \
                 EXTRACT_ARG(arg_set_id, 'cpu') as cpu, \
                 EXTRACT_ARG(arg_set_id, 'util') as util \
                 from raw where name = 'sched_pelt_thermal'"

df_pelt_irq = None
df_pelt_rt = None
df_pelt_thermal = None

def init(trace):

        global trace_pelt_irq
        global trace_pelt_rt
        global trace_pelt_thermal
        trace_pelt_irq = trace.query(query_irq)
        trace_pelt_rt = trace.query(query_rt)
        trace_pelt_thermal = trace.query(query_thermal)

def __init():

        global df_pelt_irq
        if df_pelt_irq is None:
            df_pelt_irq = trace_pelt_irq.as_pandas_dataframe()
            df_pelt_irq.ts = df_pelt_irq.ts - df_pelt_irq.ts[0]
            df_pelt_irq.ts = df_pelt_irq.ts / 1000000000
            df_pelt_irq.set_index('ts', inplace=True)

        global df_pelt_rt
        if df_pelt_rt is None:
            df_pelt_rt = trace_pelt_rt.as_pandas_dataframe()
            df_pelt_rt.ts = df_pelt_rt.ts - df_pelt_rt.ts[0]
            df_pelt_rt.ts = df_pelt_rt.ts / 1000000000
            df_pelt_rt.set_index('ts', inplace=True)

        global df_pelt_thermal
        if df_pelt_thermal is None:
            df_pelt_thermal = trace_pelt_thermal.as_pandas_dataframe()
            df_pelt_thermal.ts = df_pelt_thermal.ts - df_pelt_thermal.ts[0]
            df_pelt_thermal.ts = df_pelt_thermal.ts / 1000000000
            df_pelt_thermal.set_index('ts', inplace=True)

def num_rows():

        __init()

        return len(df_pelt_cfs.cpu.unique())

def save_csv(prefix):

        __init()

        df_pelt_irq.to_csv(prefix + '_pelt_irq.csv')
        df_pelt_rt.to_csv(prefix + '_pelt_rt.csv')
        df_pelt_thermal.to_csv(prefix + '_pelt_thermal.csv')

def plot(num_rows=0, row_pos=1):

        __init()

        if not num_rows:
            func = globals()['num_rows']
            num_rows = func()

        try:
            for cpu in sorted(df_pelt_irq.cpu.unique()):
                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1

                df = df_pelt_irq[df_pelt_irq.cpu == cpu]
                df.util.plot(title='CPU {} rq pressure'.format(cpu), drawstyle='steps-post', alpha=0.75, xlim=(df_pelt_irq.index[0], df_pelt_irq.index[-1]))

                df = df_pelt_rt[df_pelt_rt.cpu == cpu]
                df.util.plot(title='CPU {} rt pressure'.format(cpu), drawstyle='steps-post', alpha=0.75, xlim=(df_pelt_rt.index[0], df_pelt_rt.index[-1]))

                df = df_pelt_thermal[df_pelt_irq.cpu == cpu]
                df.util.plot(title='CPU {} thermal pressure'.format(cpu), drawstyle='steps-post', alpha=0.75, xlim=(df_pelt_thermal.index[0], df_pelt_thermal.index[-1]))

                plt.grid()
        except Exception as e:
            # Most likely the trace has no rq pressure info
            # TODO: Better detect this
            print("Error processing rq_pressure.plot():", e)
            pass

        return row_pos
