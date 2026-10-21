# Botlab Trading Floor

Sala de trading virtual de Botlab: una oficina isométrica animada con 24 agentes simulados organizados en cinco departamentos (Análisis técnico, Macroeconomía, Gestión de riesgo, Investigación cuantitativa y Comité de trading) que operan una cuenta demo.

> **Modo demo.** Precios, agentes y decisiones son simulados. No hay broker conectado ni dinero real.

## Qué incluye

- Cuenta virtual DEMO-001 con $100,000: patrimonio, P&L de la sesión y exposición nocional.
- Mercado simulado de MNQ, MES, MGC y MBT con calendario macro ficticio.
- Comité que combina votos técnico, macro y quant; riesgo puede vetar y aplica stops.
- Pestañas Sala de trading, Análisis, Operaciones y Actividad.
- Controles: Convocar comité, Pausar, velocidad 1×/3×/8×, Reiniciar y Kill switch.

## Cómo abrirlo

Es un único archivo, sin dependencias ni compilación:

- En local: abre `index.html` en el navegador.
- En la web: activa GitHub Pages (Settings → Pages → Deploy from a branch → `main` / root).

## Próximos pasos

- Datos de mercado reales (solo lectura).
- Modelos de IA reales detrás de cada departamento.
- Persistencia del diario de decisiones.
