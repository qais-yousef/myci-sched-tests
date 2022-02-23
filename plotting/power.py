#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import text

query = "select ts, value as current_ua from counter as c left join counter_track t on c.track_id = t.id where t.name = 'batt.current_ua'"

def init(trace):

        global trace_power
        trace_power = trace.query(query)

def num_rows():

        return 2

def plot(num_rows=2, row_pos=1):

        df_power = trace_power.as_pandas_dataframe()

        try:
            df_power.ts = df_power.ts - df_power.ts[0]
            df_power.ts = df_power.ts / 1000000000
            df_power['_ts'] = df_power.ts
            df_power.set_index('ts', inplace=True)

            df_power['current_ma'] = df_power.current_ua / 1000
            df_power['power'] = df_power.current_ma * df_power.current_ma * 1000 / (1000 * 1000)

            plt.subplot(num_rows, 1, row_pos)
            row_pos += 1
            df_power.current_ma.plot(title='Current (mA)', alpha=0.75, drawstyle='steps-post', style='o-', xlim=(df_power.index[0], df_power.index[-1]))
            text.plot(0.01, 1.05, "Sum: {:,.2f}A".format(df_power.current_ma.sum()/1000))
            text.plot(0.11, 1.05, "Mean: {:,.2f}mA".format(df_power.current_ma.mean()))

            plt.subplot(num_rows, 1, row_pos)
            row_pos += 1
            df_power.power.plot(title='Power (mW)', alpha=0.75, drawstyle='steps-post', style='o-', xlim=(df_power.index[0], df_power.index[-1]))
            text.plot(0.01, 1.05, "Sum: {:,.2f}W".format(df_power.power.sum()/1000))
            text.plot(0.11, 1.05, "Mean: {:,.2f}mW".format(df_power.power.mean()))
        except Exception as e:
            # Most likely the trace has no power info
            # TODO: Better detect this
            print("Error processing power.plot():", e)
            pass

        return row_pos
