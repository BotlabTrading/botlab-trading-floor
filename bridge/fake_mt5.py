"""MetaTrader 5 de mentira para probar el puente sin terminal (MT5_FAKE=1)."""
import random
import time
from types import SimpleNamespace as NS

TIMEFRAME_H4, TIMEFRAME_D1 = 16388, 16408
_p = 2650.0
_t0 = int(time.time())


def initialize(*a, **k): return True
def terminal_info(): return NS(connected=True)
def last_error(): return (0, "ok")
def symbol_select(s, e): return True


def account_info():
    return NS(login=5012345, server="Broker-Demo", name="Botlab", currency="USD", balance=2000.0, equity=2012.4, profit=12.4, trade_mode=0)


def symbol_info_tick(s):
    global _p
    _p += random.gauss(0, 0.4)
    return NS(time=int(time.time()), bid=round(_p, 2), ask=round(_p + 0.25, 2))


def copy_rates_from_pos(s, tf, start, n):
    step = 14400 if tf == TIMEFRAME_H4 else 86400
    out, p = [], _p - n * 0.5
    for i in range(n):
        o = p; c = o + random.gauss(0.5, 6); h = max(o, c) + abs(random.gauss(0, 3)); l = min(o, c) - abs(random.gauss(0, 3))
        out.append({"time": _t0 - (n - i) * step, "open": o, "high": h, "low": l, "close": c, "tick_volume": random.randint(4000, 16000)})
        p = c
    return out


def positions_get(symbol=None):
    return (NS(ticket=900001, magic=2002, type=0, volume=0.08, price_open=round(_p - 1.2, 2), sl=round(_p - 11.2, 2), tp=round(_p + 18.8, 2), profit=9.6, time=_t0 - 600),)


def orders_get(symbol=None):
    return (NS(ticket=900010, magic=1001, type=4, price_open=round(_p + 6.4, 2), volume_current=0.06),
            NS(ticket=900011, magic=1001, type=5, price_open=round(_p - 8.1, 2), volume_current=0.06))


def history_deals_get(a, b):
    d = []
    for k, (mg, side, pin, pout, pr, rs) in enumerate([(3003, 0, 2641.2, 2644.2, 39.0, 5), (2002, 1, 2648.0, 2647.1, 7.2, 4), (1001, 0, 2630.5, 2620.5, -60.0, 4)]):
        pid = 800000 + k
        d.append(NS(ticket=pid * 10, position_id=pid, entry=0, magic=mg, type=side, volume=0.1, price=pin, profit=0.0, swap=0.0, commission=-0.7, time=_t0 - 9000 + k * 1000, reason=3, symbol="XAUUSD"))
        d.append(NS(ticket=pid * 10 + 1, position_id=pid, entry=1, magic=mg, type=1 - side, volume=0.1, price=pout, profit=pr, swap=0.0, commission=-0.7, time=_t0 - 8000 + k * 1000, reason=rs, symbol="XAUUSD"))
    return tuple(d)
