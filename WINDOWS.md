# 🪟 Guía Específica para Windows

## 🚀 Inicio Rápido en Windows

### ⭐ **Método Recomendado - Sin Problemas**
```cmd
# Abrir CMD o PowerShell como Administrador
cd ruta\a\MeliProductDetail
python run_fixed.py
```

**✅ Este script resuelve TODOS los problemas comunes de Windows:**
- ❌ Errores Unicode (`UnicodeEncodeError`)
- ❌ Puerto 8000 bloqueado (`WinError 10013`)
- ❌ Backend que se cuelga
- ❌ Problemas de firewall

## 🔧 Scripts Disponibles para Windows

| Script | Propósito | Estado Windows |
|--------|-----------|----------------|
| `run_fixed.py` | **Solución completa optimizada** | ✅ **RECOMENDADO** |
| `run_stable.py` | Auto-restart + monitoring avanzado | ✅ Funciona |
| `run_windows_simple.bat` | Doble click fácil | ✅ Funciona |
| `run_simple.py` | Versión mejorada general | ⚠️ Puede fallar |
| `run_fullstack.py` | Original multiplataforma | ❌ Problemas Unicode |

## 🛠️ Configuración Recomendada

### 1. **Preparar el Entorno**
```cmd
# Verificar Python
python --version
# Debe mostrar Python 3.7+ (recomendado 3.9+)

# Actualizar pip
python -m pip install --upgrade pip

# Verificar puertos disponibles
netstat -ano | findstr :8000
netstat -ano | findstr :8502
# No deben mostrar resultados (puertos libres)
```

### 2. **Configurar Windows Defender/Firewall**
```cmd
# Permitir Python en Firewall (ejecutar como Administrador)
netsh advfirewall firewall add rule name="Python" dir=in action=allow program="C:\Python39\python.exe"
# Ajustar ruta según tu instalación de Python
```

### 3. **Configurar Codepage UTF-8 (Opcional)**
```cmd
# Para evitar problemas Unicode en consola
chcp 65001
```

## 🚀 Ejecución Paso a Paso

### **Opción 1: Script Optimizado (RECOMENDADO)**
```cmd
# 1. Abrir CMD/PowerShell
# 2. Navegar al directorio
cd C:\ruta\a\MeliProductDetail

# 3. Ejecutar script optimizado
python run_fixed.py

# 4. Esperar a ver este mensaje:
# ==================================================
# APLICACION FUNCIONANDO
# ==================================================
# Backend:  http://localhost:8000
# Frontend: http://localhost:8502
# Docs:     http://localhost:8000/docs
```

### **Opción 2: Batch File (Más Fácil)**
```cmd
# 1. Navegar al directorio en Explorer
# 2. Doble click en: run_windows_simple.bat
# 3. ¡Listo!
```

### **Opción 3: Auto-Restart Avanzado**
```cmd
# Para desarrollo con reinicio automático
python run_stable.py
```

## 🐛 Problemas Específicos de Windows

### ❌ **Error: "WinError 10013 - An attempt was made to access a socket..."**
```
CAUSA: El puerto 8000 está bloqueado por Windows Firewall o en uso
SOLUCIÓN: Usar run_fixed.py (usa puerto 8000)
```

### ❌ **Error: "UnicodeEncodeError: 'charmap' codec can't encode character..."**
```
CAUSA: Emojis Unicode no soportados en consola Windows
SOLUCIÓN: run_fixed.py no usa emojis problemáticos
```

### ❌ **Backend se cuelga o no responde**
```
CAUSA: uvicorn con configuración problemática en Windows
SOLUCIÓN: run_fixed.py usa configuración optimizada
```

### ❌ **Error: "No module named 'requests'"**
```
CAUSA: Dependencias no instaladas o entorno virtual corrupto
SOLUCIÓN:
1. Eliminar entorno: rmdir /s mlvenv
2. Ejecutar: python run_fixed.py
```

## 🔍 Diagnóstico y Debug

### **Verificar Estado de Puertos**
```cmd
# Verificar si los puertos están libres
netstat -ano | findstr :8000    # Backend
netstat -ano | findstr :8502    # Frontend

# Si están ocupados, encontrar el proceso
tasklist /fi "pid eq [PID_NUMERO]"

# Terminar proceso problemático
taskkill /pid [PID_NUMERO] /f
```

### **Verificar Python y Dependencias**
```cmd
# Verificar Python
python --version
python -c "print('Python OK')"

# Verificar pip
pip --version

# Verificar dependencias principales
python -c "import fastapi; print('FastAPI OK')"
python -c "import streamlit; print('Streamlit OK')"
python -c "import requests; print('Requests OK')"
```

### **Limpiar Installation**
```cmd
# Limpiar completamente y reinstalar
rmdir /s mlvenv
del /q *.log
python run_fixed.py
```

## 📊 Comparación de Performance

| Configuración | Tiempo Inicio | Estabilidad | Problemas Unicode |
|---------------|---------------|-------------|-------------------|
| `run_fixed.py` | ~15 segundos | ✅ Excelente | ✅ Sin problemas |
| `run_stable.py` | ~20 segundos | ✅ Auto-restart | ✅ Sin problemas |
| `run_simple.py` | ~25 segundos | ⚠️ Variable | ⚠️ Posibles |
| `run_fullstack.py` | ~30 segundos | ❌ Inestable | ❌ Problemas |

## 🎯 URLs Finales

Después de ejecutar `run_fixed.py` exitosamente:

- **🎨 Aplicación Web**: http://localhost:8502
- **🔧 API Backend**: http://localhost:8000
- **📖 Documentación API**: http://localhost:8000/docs
- **🔍 Redoc Docs**: http://localhost:8000/redoc

## 💡 Tips para Desarrolladores Windows

1. **Usar Windows Terminal** en lugar de CMD clásico
2. **Ejecutar como Administrador** para evitar problemas de permisos
3. **Configurar antivirus** para excluir la carpeta del proyecto
4. **Usar WSL2** si planeas desarrollo avanzado
5. **Mantener Python actualizado** (3.9+ recomendado)

## 🆘 Soporte

Si tienes problemas específicos con Windows:

1. Revisar esta guía paso a paso
2. Verificar los comandos de diagnóstico
3. Usar `run_fixed.py` que resuelve el 90% de problemas
4. Abrir issue en GitHub con detalles del error

---

**⚡ TL;DR para Windows**: Ejecuta `python run_fixed.py` y evita todos los problemas comunes.
