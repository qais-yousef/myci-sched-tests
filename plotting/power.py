#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import text

query_current = "select ts, value as current_ua from counter as c left join counter_track t on c.track_id = t.id where t.name = 'batt.current_ua'"
query_power = "select ts, t.name as rail, value as energy from counter as c left join counter_track t on c.track_id = t.id where t.name like 'power.rails.cpu.%'"

df_power = None

def init(trace):

        global trace_current
        global trace_power
        trace_current = trace.query(query_current)
        trace_power = trace.query(query_power)

def num_rows():

        global df_power
        if df_power is None:
            df_power = trace_power.as_pandas_dataframe()

        if df_power.empty:
            return 1
        else:
            return len(df_power.rail.unique()) + 1

def plot(num_rows=0, row_pos=1):

        df_current = trace_current.as_pandas_dataframe()

        global df_power
        if df_power is None:
            df_power = trace_power.as_pandas_dataframe()

        if not num_rows:
            func = globals()['num_rows']
            num_rows = func()

        try:
            df_current.ts = df_current.ts - df_current.ts[0]
            df_current.ts = df_current.ts / 1000000000
            df_current['_ts'] = df_current.ts
            df_current.set_index('ts', inplace=True)

            df_current['current_ma'] = df_current.current_ua / 1000

            plt.subplot(num_rows, 1, row_pos)
            row_pos += 1
            df_current.current_ma.plot(title='Battery Current (mA)', alpha=0.75, drawstyle='steps-post', style='o-', xlim=(df_current.index[0], df_current.index[-1]))
            text.plot(0.01, 1.20, "Sum: {:,.2f}A".format(df_current.current_ma.sum()/1000))
            text.plot(0.11, 1.20, "Mean: {:,.2f}mA".format(df_current.current_ma.mean()))
        except Exception as e:
            # Most likely the trace has no power info
            # TODO: Better detect this
            print("Error processing power.plot()::current_ua", e)
            pass

        try:
            df_power.ts = df_power.ts - df_power.ts[0]
            df_power.ts = df_power.ts / 1000000000
            df_power['_ts'] = df_power.ts
            df_power.set_index('ts', inplace=True)

            df_power['duration'] = pd.Series()
            df_power['energy_diff'] = pd.Series()
            df_power['power'] = pd.Series()

            for source in df_power.rail.unique():
                df = df_power[df_power.rail == source].copy()
                df.duration = -1 * df._ts.diff(periods=-1)
                df = df[df.duration != 0]
                df.energy_diff = -1 * df.energy.diff(periods=-1)
                df.power = df.energy_diff / (1000 * df.duration)

                plt.subplot(num_rows, 1, row_pos)
                row_pos += 1
                df.power.plot(title=source + ' Power (mW)', alpha=0.75, drawstyle='steps-post', style='o-', xlim=(df.index[0], df.index[-1]))
                text.plot(0.01, 1.20, "Sum: {:,.2f}W".format(df.power.sum()/1000))
                text.plot(0.11, 1.20, "Mean: {:,.2f}mW".format(df.power.mean()))
        except Exception as e:
            # Most likely the trace has no power info
            # TODO: Better detect this
            print("Error processing power.plot()::energy", e)
            pass

        return row_pos
