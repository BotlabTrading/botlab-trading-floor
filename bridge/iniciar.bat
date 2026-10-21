@echo off
rem Puente de solo lectura entre MetaTrader 5 y la Botlab Trading Floor.
cd /d "%~dp0"
echo Instalando/actualizando el paquete MetaTrader5 de Python...
py -m pip install --quiet --upgrade MetaTrader5
if errorlevel 1 (
  echo.
  echo No se pudo instalar MetaTrader5. Comprueba que tienes Python 3 de 64 bits instalado desde python.org.
  pause
  exit /b 1
)
py mt5_bridge.py
pause
