from typing import NamedTuple

import numpy as np
import pandas as pd
import talib.abstract as ta

TSVAction = {
    "PAL": "PA Long",
    "PAL_FAIL": "PA Long Fail",
    "PAS": "PA Short",
    "PAS_FAIL": "PA Short Fail",
    "PA_N": "PA Neutral",
}


class TSV(NamedTuple):
    df: pd.DataFrame
    t_key: str = "tsv_t"
    m_key: str = "tsv_m"
    action_key: str = "tsv_action"


def tsv(
    candles: pd.DataFrame,
    tsv_length: int = 13,
    ma_length: int = 7,
    source_type: str = "close",
) -> TSV:
    """
    Enhanced Time Segmented Volume
    """
    src = candles[source_type]
    volume = candles["volume"]
    t = (
        src.transform(lambda c: np.convolve(c, [1, -1], "same") * volume)
        .rolling(window=tsv_length)
        .sum()
        .fillna(0)
    )
    m = pd.Series(ta.SMA(t, timeperiod=ma_length)).fillna(0)
    action = t.combine(m, _compute_tsv_action)

    return TSV(df=pd.DataFrame({"tsv_t": t, "tsv_m": m, "tsv_action": action}))


def _compute_tsv_action(t: float, m: float) -> str:
    if t > m and t > 0:
        return TSVAction["PAL"]
    elif t < m and t > 0:
        return TSVAction["PAL_FAIL"]
    elif t < m and t < 0:
        return TSVAction["PAS"]
    elif t > m and t < 0:
        return TSVAction["PAS_FAIL"]
    else:
        return TSVAction["PA_N"]
