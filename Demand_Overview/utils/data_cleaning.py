import pandas as pd
import numpy as np
import re

def clean_running_total(running_total_series):
    running_total_series = running_total_series.apply(
        lambda x: pd.NA if pd.isna(x) else int(x)
    )
    return running_total_series.astype("Int64")