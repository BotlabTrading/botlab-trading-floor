# Botlab Trading Floor

Sala de trading virtual de Botlab: una oficina isométrica animada con 27 agentes simulados organizados en seis departamentos (Análisis técnico, Macroeconomía, Gestión de riesgo, Investigación cuantitativa, Comité de trading y Breakout Gold Pro) que operan una cuenta demo.

> **Modo demo.** Precios, agentes y decisiones son simulados. No hay broker conectado ni dinero real.

## Qué incluye

- Cuenta virtual DEMO-001 con $100,000: patrimonio, P&L de la sesión y exposición nocional.
- Mercado simulado de MNQ, MES, MGC y MBT con calendario macro ficticio.
- Comité que combina votos técnico, macro y quant; riesgo puede vetar y aplica stops.
- Pestañas Sala de trading, Análisis, Operaciones y Actividad.
- Departamento **Breakout Gold Pro** en XAUUSD con sus tres motores (D1, H4, H4-B): buy/sell stop sobre el máximo/mínimo de la vela anterior con buffer de 0,3× spread, filtro de tendencia en cortos, filtro de volumen 1,5× (16 velas) en H4, persistencia de nivel, SL $10, TP $20/$3, trailing 40/30 puntos y lote dinámico sobre una cuenta asignada de $2,000. Tiempo comprimido: 1 vela H4 = 30 s.
- Controles: Convocar comité, Pausar, velocidad 1×/3×/8×, Reiniciar y Kill switch.

## Cómo abrirlo

Es un único archivo, sin dependencias ni compilación:

- En local: abre `index.html` en el navegador.
- En la web: activa GitHub Pages (Settings → Pages → Deploy from a branch → `main` / root).

## Conectar con MetaTrader 5 (Breakout Gold Pro en vivo)

El puente `bridge/mt5_bridge.py` lee de tu MetaTrader 5 la cuenta, las velas del oro y las posiciones, órdenes pendientes e historial (últimos 7 días) del Breakout Gold Pro, y los muestra en la floor. **Es de solo lectura: nunca abre, modifica ni cierra órdenes.** El resto de departamentos sigue en modo demo.

Requisitos: Windows con MetaTrader 5 abierto y con sesión iniciada (empieza con una cuenta demo), y Python 3 de 64 bits desde python.org.

1. Descarga el repo (Code → Download ZIP) y descomprímelo.
2. Abre `bridge/config.json` y pon:
   - `symbol`: el nombre del oro en tu bróker (`XAUUSD`, `XAUUSD.r`, `GOLD`…).
   - `magics`: el magic number de cada motor (`D1`, `H4`, `H4B`), tal como los tienes en los inputs del EA.
3. Haz doble clic en `bridge/iniciar.bat` (instala el paquete `MetaTrader5` la primera vez) y deja la ventana abierta.
4. Abre http://localhost:8765 en el navegador. Verás la etiqueta **MT5 · DEMO** arriba y el panel del Breakout Gold Pro con los datos reales en la pestaña Análisis.

Si no sabes los magic numbers, arranca igualmente: la web te enseña los que encuentra en tu cuenta.

Para probar el puente sin MetaTrader: `MT5_FAKE=1 python bridge/mt5_bridge.py` (usa datos inventados de `bridge/fake_mt5.py`).

## Próximos pasos

- Modelos de IA reales detrás de cada departamento.
- Persistencia del diario de decisiones.
