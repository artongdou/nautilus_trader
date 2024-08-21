from datetime import datetime, timezone
from lightweight_charts import Chart
import pandas as pd

OB_COLOR_MAP = {"BUY": "#3179f5", "SELL": "#f77c80"}

if __name__ == "__main__":
    chart = Chart()

    # Columns: time | open | high | low | close | volume
    df_bars = pd.read_csv("playground/bars.csv").drop(["ts_init", "bar_type", "type"], axis=1)

    # ts_event,type,bar_type,open,high,low,close,volume,ts_init
    df_bars.rename(columns={"ts_event": "time"}, inplace=True)
    df_bars["time"] = pd.to_datetime(df_bars["time"])

    # Columns: | low | high | ts_event | OrderBlockType

    chart.set(df_bars)

    df_ob = pd.read_csv("playground/ob.csv")
    df_ob.rename(columns={"ts_event": "time"}, inplace=True)
    df_ob["time"] = pd.to_datetime(df_ob["time"])

    for index, ob in df_ob.iterrows():
        chart.box(
            start_time=ob["time"],
            end_time=df_bars["time"].iloc[-1],
            start_value=ob["low"],
            end_value=ob["high"],
            color=OB_COLOR_MAP[ob["OrderBlockType"]],
        )

    chart.show(block=True)
