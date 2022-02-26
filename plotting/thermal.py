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

        return len(names)

def plot(num_rows=len(names), row_pos=1):

        df_thermal = trace_thermal.as_pandas_dataframe()

        try:
            df_thermal.ts = df_thermal.ts - df_thermal.ts[0]
            df_thermal.ts = df_thermal.ts / 1000000000
            df_thermal['_ts'] = df_thermal.ts
            df_thermal.set_index('ts', inplace=True)

            df_thermal.temperature = df_thermal.temperature / 1000

            for name in names:
                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df_thermal[df_thermal.name == name].temperature.plot(title=name + ' (C)', alpha=0.75, drawstyle='steps-post', style='o-', xlim=(df_thermal.index[0], df_thermal.index[-1]))
        except Exception as e:
            # Most likely the trace has no thermal info
            # TODO: Better detect this
            print("Error processing thermal.plot()", e)
            pass

        return row_pos
