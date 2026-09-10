@echo off
echo Limpando git locks...
del /f /q ".git\HEAD.lock" 2>nul && echo HEAD.lock removido || echo HEAD.lock nao encontrado
del /f /q ".git\index.lock" 2>nul && echo index.lock removido || echo index.lock nao encontrado
echo Pronto.
pause
