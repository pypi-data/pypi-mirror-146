from typing import NamedTuple

import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy as np
import pandas as pd
import talib.abstract as ta


class SqueezeStatus(NamedTuple):
    df: pd.DataFrame
    strong_k: str = "strong_squeeze"
    soft: str = "soft_squeeze"
    half: str = "half_squeeze"


# source; https://www.tradingview.com/script/OE6FQU4Z-Williams-Vix-Fix-BB-RVI-LinReg-Squeeze-Keltner-BBW-B/


def squeeze(
    candles: pd.DataFrame,
    length_bb_kc: int = 20,
    mult_kc: float = 1.5,
    mult_bb: float = 2.0,
    period_sqz_detect: int = 60,
    percent_margin_err: float = 1.5,
    b_impulse_lvl: float = 0.35,
) -> SqueezeStatus:
    src = candles["close"]

    bb = qtpylib.bollinger_bands(src, length_bb_kc, mult_bb)
    upper_bb = bb["upper"]
    mid_bb = bb["mid"]
    lower_bb = bb["lower"]
    bbw = (upper_bb - lower_bb) / mid_bb
    sqz_bbw = bbw.rolling(window=period_sqz_detect).min()
    percent = 1 + (percent_margin_err / 100)

    bbr = (src - lower_bb) / (upper_bb - lower_bb)
    bbi = pd.Series(np.convolve(bbr, [1, -1], "same"))

    kc = _kc(candles, length_bb_kc, mult_kc)
    upper_kc = kc["upper"]
    lower_kc = kc["lower"]
    sqz_on = (lower_bb > lower_kc) & (upper_bb < upper_kc)
    sqz_off = (lower_bb < lower_kc) & (upper_bb > upper_kc)

    strong_sqz = sqz_on & (
        (bbw <= sqz_bbw * percent)
        | ((bbi < 1) & (bbi >= b_impulse_lvl) | (bbi <= -b_impulse_lvl))
    )
    soft_sqz = ~strong_sqz & sqz_on
    half_sqz = ~sqz_on & ~sqz_off

    return SqueezeStatus(
        df=pd.DataFrame(
            {"strong_sqz": strong_sqz, "soft_sqz": soft_sqz, "half_sqz": half_sqz}
        )
    )


def _kc(candles: pd.DataFrame, kc_len: int, mult: float) -> np.ndarray:
    """
    Keltner channels using SMA instead of EMA
    """
    ma = ta.SMA(candles["close"], kc_len)
    high = candles["high"]
    low = candles["low"]
    rangema = ta.SMA(high - low, kc_len)
    upper = ma + rangema * mult
    lower = ma - rangema * mult

    return pd.DataFrame({"upper": upper, "lower": lower})
