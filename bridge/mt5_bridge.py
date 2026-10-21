"""Puente de SOLO LECTURA entre MetaTrader 5 y la Botlab Trading Floor.

Lee del terminal MT5 abierto en este PC la cuenta, las velas del oro y las
posiciones, órdenes pendientes e historial del Breakout Gold Pro, y los sirve
en http://localhost:8765/api/state. También sirve la propia web, así que basta
con abrir http://localhost:8765 en el navegador.

Este script nunca envía, modifica ni cierra órdenes.
"""
import datetime as dt
import json
import os
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

if os.environ.get("MT5_FAKE"):
    import fake_mt5 as mt5  # solo para pruebas sin MetaTrader
else:
    try:
        import MetaTrader5 as mt5
    except ImportError:
        sys.exit("Falta el paquete MetaTrader5. Ejecuta: py -m pip install MetaTrader5")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DEFAULTS = {"symbol": "XAUUSD", "magics": {"D1": 0, "H4": 0, "H4B": 0}, "history_days": 7, "port": 8765, "terminal_path": ""}
REASONS = {0: "Manual", 1: "Móvil", 2: "Web", 3: "Experto", 4: "Stop loss", 5: "Take profit", 6: "Stop out"}
# MetaTrader5 se usa siempre desde un único hilo; la web solo lee la última foto.
CACHE = {"connected": False, "error": "Conectando con MetaTrader 5..."}
CACHE_LOCK = threading.Lock()


def load_config():
    cfg = dict(DEFAULTS)
    try:
        with open(os.path.join(HERE, "config.json"), encoding="utf-8") as f:
            cfg.update(json.load(f))
    except FileNotFoundError:
        pass
    return cfg


CFG = load_config()
MAGICS = {k: int(v) for k, v in CFG["magics"].items() if int(v or 0)}
ENGINE_BY_MAGIC = {v: k for k, v in MAGICS.items()}


def ensure_connected():
    if mt5.terminal_info() is not None:
        return None
    ok = mt5.initialize(path=CFG["terminal_path"]) if CFG["terminal_path"] else mt5.initialize()
    if not ok:
        return f"No se pudo conectar con MetaTrader 5: {mt5.last_error()}. ¿Está el terminal abierto y con sesión iniciada?"
    return None


def ts(t):
    return dt.datetime.fromtimestamp(int(t), dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def rates(symbol, tf, count):
    r = mt5.copy_rates_from_pos(symbol, tf, 0, count)
    if r is None:
        return []
    return [{"t": int(x["time"]), "o": float(x["open"]), "h": float(x["high"]), "l": float(x["low"]),
             "c": float(x["close"]), "v": float(x["tick_volume"])} for x in r]


def closed_trades(deals):
    entries = {}
    for d in deals:
        if d.entry == 0:  # DEAL_ENTRY_IN
            entries[d.position_id] = d
    out = []
    for d in deals:
        if d.entry not in (1, 3):  # DEAL_ENTRY_OUT / OUT_BY
            continue
        opened = entries.get(d.position_id)
        magic = opened.magic if opened else d.magic
        out.append({
            "ticket": int(d.ticket), "position_id": int(d.position_id), "magic": int(magic),
            "engine": ENGINE_BY_MAGIC.get(int(magic)),
            "side": "Largo" if d.type == 1 else "Corto",  # cerrar un largo es un deal de venta
            "volume": float(d.volume), "entry": float(opened.price) if opened else None, "exit": float(d.price),
            "profit": float(d.profit + d.swap + d.commission), "time": ts(d.time),
            "reason": REASONS.get(int(d.reason), "Otro"),
        })
    return out


def state():
    err = ensure_connected()
    if err:
        return {"connected": False, "error": err}
    sym = CFG["symbol"]
    if not mt5.symbol_select(sym, True):
        return {"connected": False, "error": f"El símbolo {sym} no existe en este bróker. Cámbialo en bridge/config.json."}
    acc, tick = mt5.account_info(), mt5.symbol_info_tick(sym)
    if acc is None or tick is None:
        return {"connected": False, "error": f"MetaTrader 5 no devuelve datos: {mt5.last_error()}"}
    positions = [p for p in (mt5.positions_get(symbol=sym) or ())]
    orders = [o for o in (mt5.orders_get(symbol=sym) or ())]
    now = dt.datetime.now()
    deals = [d for d in (mt5.history_deals_get(now - dt.timedelta(days=int(CFG["history_days"])), now + dt.timedelta(days=2)) or ()) if d.symbol == sym]
    seen = sorted({int(x.magic) for x in positions + orders + deals if int(x.magic)})
    return {
        "connected": True,
        "server_time": ts(tick.time),
        "account": {"login": int(acc.login), "server": acc.server, "name": acc.name, "currency": acc.currency,
                    "balance": float(acc.balance), "equity": float(acc.equity), "profit": float(acc.profit),
                    "mode": {0: "DEMO", 1: "CONCURSO", 2: "REAL"}.get(int(acc.trade_mode), "?")},
        "symbol": sym, "bid": float(tick.bid), "ask": float(tick.ask),
        "h4": rates(sym, mt5.TIMEFRAME_H4, 40), "d1": rates(sym, mt5.TIMEFRAME_D1, 10),
        "magics": MAGICS, "seen_magics": seen,
        "positions": [{"ticket": int(p.ticket), "magic": int(p.magic), "engine": ENGINE_BY_MAGIC.get(int(p.magic)),
                       "dir": 1 if p.type == 0 else -1, "volume": float(p.volume), "entry": float(p.price_open),
                       "sl": float(p.sl), "tp": float(p.tp), "profit": float(p.profit), "time": ts(p.time)} for p in positions],
        "orders": [{"ticket": int(o.ticket), "magic": int(o.magic), "engine": ENGINE_BY_MAGIC.get(int(o.magic)),
                    "type": {4: "buy_stop", 5: "sell_stop", 2: "buy_limit", 3: "sell_limit"}.get(int(o.type), "otra"),
                    "price": float(o.price_open), "volume": float(o.volume_current)} for o in orders],
        "trades": closed_trades(deals),
    }


def worker():
    global CACHE
    reported = None
    while True:
        try:
            snap = state()
        except Exception as e:  # nunca tumbar el puente por un fallo de lectura
            snap = {"connected": False, "error": f"Error leyendo MT5: {e}"}
        with CACHE_LOCK:
            CACHE = snap
        msg = "Conectado a MetaTrader 5 (solo lectura)." if snap["connected"] else snap["error"]
        if msg != reported:
            print(msg, flush=True)
            reported = msg
        time.sleep(1)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/state":
            with CACHE_LOCK:
                data = json.dumps(CACHE).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if self.path.startswith("/bridge/"):
            self.send_error(404)
            return
        super().do_GET()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    port = int(CFG["port"])
    threading.Thread(target=worker, daemon=True).start()
    if not MAGICS:
        print("Aviso: no hay magic numbers en bridge/config.json; la web mostrará los que encuentre para que los configures.")
    print(f"Abre http://localhost:{port} en el navegador. Ctrl+C para salir.")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
