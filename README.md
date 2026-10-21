# Botlab Trading Floor

Sala de trading virtual de Botlab para el **Breakout Gold Pro**, el EA de rupturas en XAUUSD. Es una oficina isométrica animada: carlus en su despacho, tres traders (uno por motor: D1, H4 y H4-B) en la sala de estrategias y cinco equipos en la planta abierta, uno por cada filtro de la estrategia.

> **Modo demo.** Sin el puente MT5, precios y operaciones son simulados sobre una cuenta virtual de $2,000. No hay dinero real.

## Qué incluye

- Solo se opera XAUUSD. Tiempo comprimido en simulación: 1 vela H4 = 30 s, 1 día = 6 velas H4.
- Cada vela cerrada pasa por la cadena de filtros, y cada filtro es un equipo de la sala:
  1. **Niveles de ruptura:** buy/sell stop en el máximo/mínimo de la vela anterior ± 0,3× spread.
  2. **Filtro de vela:** solo vende tras una vela bajista; en H4 guarda el mínimo (persistencia de nivel) y descarta niveles ya rotos.
  3. **Filtro de volumen:** en H4 y H4-B la vela debe tener 1,5× el volumen medio de las 16 anteriores.
  4. **Riesgo y lotaje:** 0,01 lotes por $300 (D1), $200 (H4) o $150 (H4-B), límite diario −2% y borrado de pendientes al cierre del día.
  5. **Gestión de la operación:** SL $10, TP $20 (H4-B $3) y trailing desde +40 puntos a 30 puntos.
- Reuniones periódicas en la sala de reuniones: carlus, los tres traders y un representante de cada filtro.
- Pestañas Sala de trading, Análisis (velas H4 y tabla de la cadena de filtros por motor), Operaciones y Actividad.
- Controles: Convocar reunión, Pausar, velocidad 1×/3×/8×, Reiniciar y Kill switch.

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
