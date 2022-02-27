#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

query = "select ts, name, value as temperature from counter as c left join counter_track t on c.track_id = t.id {}"

names = ["BIG Temperature", "MID Temperature", "LITTLE Temperature"]

def init(trace):

        global trace_thermal

        condition = None
        for name in names:
            if condition is None:
                condition = "where t.name = '{}'".format(name)
            else:
                condition += " or t.name = '{}'".format(name)

        trace_thermal = trace.query(query.format(condition))

def num_rows():

        return len(names) * 2

def plot(num_rows=0, row_pos=1):

        df_thermal = trace_thermal.as_pandas_dataframe()

        if not num_rows:
            func = globals()['num_rows']
            num_rows = func()

        try:
            df_thermal.ts = df_thermal.ts - df_thermal.ts[0]
            df_thermal.ts = df_thermal.ts / 1000000000
            df_thermal['_ts'] = df_thermal.ts
            df_thermal.set_index('ts', inplace=True)

            df_thermal.temperature = df_thermal.temperature / 1000

            color = ['r', 'y', 'b']
            i = 0
            for name in names:
                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df_thermal[df_thermal.name == name].temperature.plot(title=name + ' (C)', alpha=0.75, drawstyle='steps-post', style='-', color=color[i], xlim=(df_thermal.index[0], df_thermal.index[-1]))
                plt.grid()

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                plt.title(name + ' Histogram (C)')
                df_thermal[df_thermal.name == name].temperature.hist(bins=100, density=True, grid=True, alpha=0.75, color=color[i])

                i += 1
                if i == 3:
                    i = 0
        except Exception as e:
            # Most likely the trace has no thermal info
            # TODO: Better detect this
            print("Error processing thermal.plot()", e)
            pass

        return row_pos
