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

## Próximos pasos

- Datos de mercado reales (solo lectura).
- Modelos de IA reales detrás de cada departamento.
- Persistencia del diario de decisiones.
