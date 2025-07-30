# 🚀 MeliProductDetail - Guía de Ejecución

Esta guía explica cómo ejecutar el proyecto MeliProductDetail de manera completa, incluyendo tanto el backend como el frontend.

## 📋 Índice

1. [Requisitos Previos](#-requisitos-previos)
2. [Ejecución Rápida](#-ejecución-rápida)
3. [Ejecución Manual](#-ejecución-manual)
4. [Ejecución de Tests](#-ejecución-de-tests)
5. [URLs de Acceso](#-urls-de-acceso)
6. [Solución de Problemas](#-solución-de-problemas)
7. [Estructura del Proyecto](#-estructura-del-proyecto)

## 🔧 Requisitos Previos

### Requisitos Mínimos
- **Python 3.7+** (Recomendado: Python 3.9 o superior)
- **Git** (para clonar el repositorio)
- **Conexión a Internet** (para instalación de dependencias)

### Verificar Instalación
```bash
python --version          # Debe mostrar 3.7+
pip --version             # Verificar que pip esté disponible
```

## 🚀 Ejecución Rápida

### Opción 1: Script Simple (🌟 **RECOMENDADO PARA WINDOWS**)

El script `run_simple.py` ejecuta sin caracteres Unicode (compatible con Windows):

```bash
# 1. Navegar al directorio del proyecto
cd MeliProductDetail

# 2. Ejecutar el script simple
python run_simple.py
```

### Opción 2: Script Full Stack Completo

El script `run_fullstack.py` ejecuta automáticamente tanto backend como frontend:

```bash
# 1. Navegar al directorio del proyecto
cd MeliProductDetail

# 2. Ejecutar el script completo
python run_fullstack.py
```

**¿Qué hacen estos scripts?**
- ✅ Verifica la versión de Python
- ✅ Crea automáticamente un entorno virtual (`mlvenv/`)
- ✅ Instala todas las dependencias necesarias
- ✅ Inicia el backend (FastAPI) en puerto 8000
- ✅ Inicia el frontend (Streamlit) en puerto 8501
- ✅ Monitorea ambos procesos
- ✅ Permite detener ambos con Ctrl+C

### Opción 3: Lanzadores por Plataforma

**🐧 Linux (Múltiples opciones):**

```bash
# Opción A: Script Unix universal (recomendado)
chmod +x run_unix.sh
./run_unix.sh

# Opción B: Makefile (para usuarios avanzados)
make run                    # Ejecutar directamente
make full-install          # Instalación completa desde cero

# Opción C: Instalador automático
chmod +x install_linux.sh
./install_linux.sh         # Instala dependencias del sistema automáticamente

# Opción D: Script específico Linux
chmod +x run_linux.sh
./run_linux.sh
```

**🪟 Windows:**

```cmd
# Opción A: Simple (sin Unicode - recomendado)
run_windows_simple.bat

# Opción B: Completo (con emojis)
run_windows.bat
```

**🍎 macOS:**

```bash
# Mismo que Linux
chmod +x run_unix.sh
./run_unix.sh
```

### Salida Esperada
```
======================================================================
🚀 MELIPRODUCTDETAIL - FULL STACK RUNNER
======================================================================
📦 Backend: FastAPI + JWT Authentication
🎨 Frontend: Streamlit + Product Detail UI
🔧 Auto-instalación de dependencias incluida
======================================================================
🐍 Verificando versión de Python...
✅ Python 3.11.0 detectado
✅ Entorno virtual encontrado
🔍 Verificando dependencias...
📋 Instalando 11 dependencias...
📦 Instalando fastapi (framework web)...
✅ fastapi instalado exitosamente
[... más instalaciones ...]
🔧 Iniciando Backend (FastAPI)...
   📍 URL: http://localhost:8000
   📖 Docs: http://localhost:8000/docs
✅ Backend iniciado exitosamente
🎨 Iniciando Frontend (Streamlit)...
   📍 URL: http://localhost:8501
✅ Frontend iniciado exitosamente

======================================================================
🎉 APLICACIÓN FUNCIONANDO
======================================================================
🔧 Backend:  http://localhost:8000
🎨 Frontend: http://localhost:8501
📖 API Docs: http://localhost:8000/docs
======================================================================
💡 Presiona Ctrl+C para detener ambos servidores
======================================================================
```

## 🔧 Ejecución Manual

Si prefieres ejecutar cada componente por separado:

### Backend (FastAPI)

```bash
# 1. Navegar al directorio backend
cd Backend

# 2. Opción A: Usar script de auto-setup (Recomendado)
python setup.py run

# 2. Opción B: Usar script de ejecución mejorado
python run.py

# 2. Opción C: Instalación manual
pip install -r requirements.txt
python -m app.main

# 2. Opción D: Uvicorn directo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Streamlit)

```bash
# 1. Navegar al directorio frontend (en otra terminal)
cd Frontend

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar Streamlit
streamlit run app.py --server.port 8501
```

## 🧪 Ejecución de Tests

### Tests del Backend
```bash
cd Backend

# Tests completos
python -m pytest tests/ -v

# Tests específicos
python -m unittest tests.test_product_service -v
python setup.py test  # Con auto-setup
```

### Tests del Frontend
```bash
cd Frontend/tests

# Setup del entorno de testing
python setup_tests.py

# Todos los tests (36 tests)
python run_all_tests.py

# Tests individuales
python -m unittest test_login_service.py -v
python -m unittest test_product_service.py -v
```

### Verificación del Sistema
```bash
# Backend
cd Backend
python verify.py

# Frontend  
cd Frontend/tests
python setup_tests.py
```

## 🌐 URLs de Acceso

Una vez que la aplicación esté ejecutándose:

### 🎨 Frontend (Streamlit)
- **URL Principal**: http://localhost:8502
- **Descripción**: Interfaz de usuario para ver detalles de productos
- **Funcionalidades**:
  - Login automático con credenciales de prueba
  - Visualización de productos con imágenes
  - Información de vendedores y reviews
  - Productos similares y categorías

### 🔧 Backend (FastAPI)
- **API Base**: http://localhost:8000
- **Documentación Interactiva**: http://localhost:8000/docs
- **Esquemas OpenAPI**: http://localhost:8000/openapi.json
- **Endpoints principales**:
  - `POST /token` - Autenticación JWT
  - `GET /products/{id}` - Detalle de producto
  - `GET /products/{id}/similar` - Productos similares
  - `GET /sellers/{id}` - Información de vendedor
  - `GET /reviews/product/{id}` - Reviews de producto

### 📊 Credenciales de Prueba
```
Usuario: testuser
Contraseña: testpass
```

## 🐛 Solución de Problemas

### Error: "Python no encontrado"
```bash
# Windows
py --version
py run_fullstack.py

# Linux/Mac
python3 --version
python3 run_fullstack.py
```

### Error: "Puerto ocupado"
```bash
# Verificar qué está usando el puerto
netstat -ano | findstr :8000    # Windows
lsof -i :8000                   # Linux/Mac

# Cambiar puertos manualmente
# Backend: editar run_fullstack.py línea del uvicorn
# Frontend: usar --server.port 8502
```

### Error: "Módulo no encontrado"
```bash
# Reinstalar dependencias
python run_fullstack.py  # Se encarga automáticamente

# O manualmente:
cd Backend
pip install -r requirements.txt
cd ../Frontend  
pip install -r requirements.txt
```

### Error: "Streamlit no inicia"
```bash
# Verificar instalación
pip install streamlit --upgrade

# Ejecutar con debug
streamlit run app.py --logger.level debug
```

### Error: "FastAPI no responde"
```bash
# Verificar logs del backend
cd Backend
python run.py  # Ver logs detallados

# Verificar puerto
curl http://localhost:8000/docs
```

### Limpiar Entorno
```bash
# Eliminar entorno virtual y recrear
rm -rf mlvenv/          # Linux/Mac
rmdir /s mlvenv\        # Windows
python run_fullstack.py  # Recreará automáticamente
```

## 📁 Estructura del Proyecto

```
MeliProductDetail/
├── run_fullstack.py          # 🌟 Script principal full-stack
├── RUN.md                    # 📖 Esta guía
├── Backend/                  # 🔧 API Backend (FastAPI)
│   ├── app/
│   │   ├── main.py          # Punto de entrada FastAPI
│   │   ├── controllers/     # Controladores API
│   │   ├── services/        # Lógica de negocio
│   │   ├── models/          # Modelos de datos
│   │   └── schemas/         # Esquemas Pydantic
│   ├── tests/               # Tests del backend
│   ├── Data/                # Archivos JSON de datos
│   ├── requirements.txt     # Dependencias backend
│   ├── setup.py            # Auto-setup backend
│   ├── run.py              # Ejecutor mejorado
│   └── verify.py           # Verificador sistema
├── Frontend/                # 🎨 UI Frontend (Streamlit)
│   ├── app.py              # Aplicación principal
│   ├── pages/              # Páginas de la UI
│   ├── services/           # Servicios de API
│   ├── models/             # Modelos frontend
│   ├── tests/              # Tests del frontend
│   │   ├── run_all_tests.py # Ejecutor tests completo
│   │   ├── mock_models.py   # Modelos mock
│   │   └── *.py            # Tests individuales
│   ├── assets/             # Recursos estáticos
│   └── requirements.txt    # Dependencias frontend
└── mlvenv/                 # 📦 Entorno virtual (auto-creado)
```

## 🎯 Opciones de Ejecución Resumidas

| Método | Comando | Descripción | Recomendado |
|--------|---------|-------------|-------------|
| **Full Stack** | `python run_fullstack.py` | Ejecuta todo automáticamente | ✅ **SÍ** |
| Backend Auto | `cd Backend && python setup.py run` | Backend con auto-setup | ✅ |
| Backend Manual | `cd Backend && python run.py` | Backend estándar | ⚠️ |
| Frontend | `cd Frontend && streamlit run app.py` | Solo frontend | ⚠️ |
| Tests Backend | `cd Backend && python setup.py test` | Tests backend | ✅ |
| Tests Frontend | `cd Frontend/tests && python run_all_tests.py` | Tests frontend | ✅ |

## 🎉 ¡Listo!

Con esta guía deberías poder ejecutar MeliProductDetail sin problemas. El script `run_fullstack.py` es la opción más fácil y maneja todo automáticamente.

Si encuentras algún problema, revisa la sección de solución de problemas o verifica que todos los requisitos estén instalados correctamente.
