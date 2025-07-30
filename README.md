# 🛒 MeliProductDetail

Una aplicación completa de detalle de productos estilo MercadoLibre con backend FastAPI y frontend Streamlit.

## 🚀 Inicio Rápido

### 🪟 **Para Windows (RECOMENDADO)**
```bash
# Opción 1: Script optimizado para Windows (SIN problemas Unicode/Performance)
python run_fixed.py

# Opción 2: Batch file (doble click)
run_windows_simple.bat

# Opción 3: Script estable con auto-restart
python run_stable.py
```

### 🐧 **Para Linux/Mac**
```bash
# Clonar y ejecutar
git clone https://github.com/bynara/MeliProductDetail.git
cd MeliProductDetail
python run_fullstack.py
```

**✅ El script `run_fixed.py` resuelve:**
- ❌ Problemas de encoding Unicode en Windows
- ❌ Cuelgues del backend por puerto bloqueado (8000)
- ❌ Problemas de performance con uvicorn
- ❌ Errores de firewall de Windows

**� URLs tras ejecutar run_fixed.py:**
- **🎨 Frontend**: http://localhost:8502
- **🔧 Backend**: http://localhost:8000 
- **📖 API Docs**: http://localhost:8000/docs

## 📋 Características

### 🔧 Backend (FastAPI)
- **Autenticación JWT** con tokens seguros
- **API RESTful** con documentación automática
- **Modelos Pydantic** para validación de datos
- **Sistema de logging** estructurado
- **Tests unitarios** completos (pytest)
- **Auto-instalación** de dependencias

### 🎨 Frontend (Streamlit)
- **Interfaz intuitiva** estilo MercadoLibre
- **Visualización de productos** con imágenes
- **Información de vendedores** y reviews
- **Productos similares** y categorías
- **Carousel de imágenes** interactivo
- **Tests unitarios** con mocks avanzados

### 📊 Datos
- **Productos** con detalles completos
- **Vendedores** con reputación
- **Reviews** y calificaciones
- **Categorías** y métodos de pago
- **Imágenes** y características

## 📁 Estructura del Proyecto

```
MeliProductDetail/
├── 🚀 run_fullstack.py      # Ejecutor principal (USAR ESTE)
├── 📖 RUN.md                # Guía completa de ejecución
├── 🪟 run_windows.bat       # Ejecutor para Windows
├── 🐧 run_unix.sh           # Ejecutor para Linux/Mac
├── Backend/                 # 🔧 API FastAPI
│   ├── app/                # Aplicación principal
│   ├── tests/              # Tests unitarios
│   ├── Data/               # Archivos JSON
│   └── setup.py           # Auto-setup
├── Frontend/               # 🎨 UI Streamlit
│   ├── pages/             # Páginas UI
│   ├── services/          # Servicios API
│   ├── tests/             # Tests con mocks
│   └── assets/            # Recursos
└── mlvenv/                # 📦 Entorno virtual
```

## 🎯 Formas de Ejecutar

| Método | Comando | Descripción | Windows |
|--------|---------|-------------|---------|
| **🌟 Windows Optimizado** | `python run_fixed.py` | ✅ Sin Unicode/Performance issues | ⭐ RECOMENDADO |
| **🔄 Auto-restart** | `python run_stable.py` | Backend auto-restart + monitoring | ✅ Avanzado |
| **🪟 Batch Simple** | `run_windows_simple.bat` | Doble click en Windows | ✅ Fácil |
| **🌍 Multiplataforma** | `python run_fullstack.py` | Backend + Frontend automático | ⚠️ Puede fallar en Windows |
| **🐧 Unix** | `bash run_unix.sh` | Ejecutor para Linux/Mac | ❌ Solo Unix |
| **🔧 Backend Solo** | `cd Backend && python setup.py run` | Solo API | ⚠️ Puerto 8000 |
| **🎨 Frontend Solo** | `cd Frontend && streamlit run app.py` | Solo UI | ⚠️ Requiere backend |

### 🛡️ **Problemas Comunes en Windows y Soluciones**

| Problema | Error | Solución |
|----------|-------|----------|
| **Puerto bloqueado** | `WinError 10013` | Usar `run_fixed.py` (puerto 8000) |
| **Unicode en consola** | `UnicodeEncodeError` | Usar `run_fixed.py` (sin emojis) |
| **Backend se cuelga** | Proceso no responde | Usar `run_stable.py` (auto-restart) |
| **Firewall bloquea** | Conexión rechazada | Usar `127.0.0.1` en lugar de `0.0.0.0` |

## 🧪 Testing

### Tests del Backend
```bash
cd Backend
python setup.py test        # Con auto-setup
python -m pytest tests/ -v  # Manualmente
```

### Tests del Frontend
```bash
cd Frontend/tests
python run_all_tests.py     # 36 tests completos
```

## 🔧 Requisitos

### 🪟 **Windows (Configuración Recomendada)**
- **Python 3.7+** (Recomendado: 3.9+)
- **PowerShell** o **CMD** con permisos de administrador
- **Puertos 8000 y 8502** disponibles (no 8000/8501 que suelen estar bloqueados)
- **Windows Defender/Firewall** configurado para permitir Python
- **4GB RAM** (mínimo)

### 🐧 **Linux/Mac**  
- **Python 3.7+** (Recomendado: 3.9+)
- **Bash shell**
- **Puertos 8000 y 8501** disponibles
- **4GB RAM** (mínimo)

### 🌐 **General**
- **Conexión a Internet** (para descargar dependencias)
- **pip** actualizado (`python -m pip install --upgrade pip`)

## 📖 Documentación Completa

- **[WINDOWS.md](WINDOWS.md)** - 🪟 **Guía específica y optimizada para Windows**
- **[RUN.md](RUN.md)** - Guía completa de ejecución
- **[LINUX.md](LINUX.md)** - Guía específica para sistemas Linux/Unix
- **[Backend/README.md](Backend/README.md)** - Documentación del backend
- **[Frontend/tests/README.md](Frontend/tests/README.md)** - Documentación de tests frontend

## 🎮 Credenciales de Prueba

```
Usuario: testuser
Contraseña: testpass
```

## 🚀 Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validación de datos
- **Python-JOSE** - JWT tokens
- **Passlib** - Hashing de passwords
- **Pytest** - Framework de testing

### Frontend  
- **Streamlit** - Framework UI
- **Requests** - Cliente HTTP
- **Pillow** - Procesamiento de imágenes
- **Streamlit-Carousel** - Componente carousel

## 🎯 Funcionalidades Principales

### Para Usuarios
- ✅ **Login automático** con credenciales de prueba
- ✅ **Visualización de productos** con detalles completos
- ✅ **Galería de imágenes** con carousel interactivo
- ✅ **Información de vendedores** con reputación
- ✅ **Reviews y calificaciones** de otros compradores
- ✅ **Productos similares** y recomendaciones
- ✅ **Categorías** y métodos de pago
- ✅ **Simulación de compra** con stock

### Para Desarrolladores
- ✅ **API RESTful** con documentación automática
- ✅ **Autenticación JWT** segura
- ✅ **Tests unitarios** completos (Backend + Frontend)
- ✅ **Auto-instalación** de dependencias
- ✅ **Logging estructurado** para debugging
- ✅ **Arquitectura modular** fácil de extender
- ✅ **Mocks avanzados** para testing sin dependencias

## 🐛 Solución de Problemas

### 🪟 **Problemas Específicos de Windows**

#### ❌ Error: "WinError 10013 - Access socket forbidden"
```bash
# SOLUCIÓN: Usar puerto alternativo
python run_fixed.py    # Usa puerto 8000 en lugar de 8000
```

#### ❌ Error: "UnicodeEncodeError - charmap codec"
```bash
# SOLUCIÓN: Script sin emojis Unicode
python run_fixed.py    # Sin emojis problemáticos
# O configurar codepage UTF-8
chcp 65001
```

#### ❌ Backend se cuelga o no responde
```bash
# SOLUCIÓN: Script con auto-restart
python run_stable.py   # Monitorea y reinicia automáticamente
```

#### ❌ Firewall bloquea conexiones
```bash
# SOLUCIÓN: Usar localhost en lugar de 0.0.0.0
# El script run_fixed.py ya usa 127.0.0.1 por defecto
```

### 🌍 **Problemas Generales**

#### Error: "Puerto ocupado"
```bash
# Verificar qué está usando los puertos
netstat -ano | findstr :8000    # Windows (puerto actualizado)
lsof -i :8000                   # Linux/Mac

# Liberar puerto (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

#### Error: "Python no encontrado"
```bash
# Windows - probar diferentes comandos
python run_fixed.py
py run_fixed.py
python3 run_fixed.py

# Verificar instalación
python --version
```

#### Limpiar y reinstalar
```bash
# Eliminar entorno virtual
rm -rf mlvenv/          # Linux/Mac
rmdir /s mlvenv\        # Windows

# Ejecutar script optimizado (recreará todo)
python run_fixed.py
```

### 🚀 **Scripts de Diagnóstico**
```bash
# Para diagnosticar problemas de puertos
python -c "import socket; s=socket.socket(); s.bind(('127.0.0.1', 8000)); print('Puerto 8000 disponible'); s.close()"

# Para verificar dependencias
python -c "import fastapi, streamlit, requests; print('Dependencias OK')"
```

## 📚 Documentación Técnica

### 🚀 Guías de Usuario
- **[RUN.md](RUN.md)** - Guía completa de ejecución paso a paso
- **[LINUX.md](LINUX.md)** - Guía específica para sistemas Linux/Unix
- **[COMPLETADO.md](COMPLETADO.md)** - Resumen completo de logros del proyecto

### 🏗️ Documentación Técnica Avanzada
- **[STACK_DOCUMENTATION.md](STACK_DOCUMENTATION.md)** - Análisis profundo del stack tecnológico, ventajas y arquitectura
- **[TECHNICAL_CHALLENGES.md](TECHNICAL_CHALLENGES.md)** - Desafíos técnicos encontrados y soluciones implementadas

### 🎯 Highlights Técnicos
- **Backend**: FastAPI con autenticación JWT, validación Pydantic y documentación automática
- **Frontend**: Streamlit con gestión de estado avanzada y componentes interactivos
- **Testing**: 36+ tests unitarios con sistema de mock models para independencia total
- **Deployment**: Scripts multiplataforma con auto-instalación de dependencias
- **Cross-Platform**: Soporte completo para Windows, Linux y macOS

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Bryan Ara** - [@bynara](https://github.com/bynara)

## 🎉 Agradecimientos

- Inspirado en MercadoLibre
- FastAPI por su excelente documentación
- Streamlit por hacer el frontend simple
- La comunidad Python por las librerías

---

**¿Problemas?** Revisa [RUN.md](RUN.md) para guía detallada o abre un issue.
