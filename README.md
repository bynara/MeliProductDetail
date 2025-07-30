# 🛒 MeliProductDetail

Una aplicación completa de detalle de productos estilo MercadoLibre con backend FastAPI y frontend Streamlit.

## 🚀 Inicio Rápido

```bash
# 1. Clonar el repositorio
git clone https://github.com/bynara/MeliProductDetail.git
cd MeliProductDetail

# 2. Ejecutar la aplicación completa
python run_fullstack.py
```

**¡Eso es todo!** El script se encarga de:
- ✅ Verificar Python
- ✅ Crear entorno virtual
- ✅ Instalar dependencias
- ✅ Ejecutar backend y frontend

## 🌐 URLs de Acceso

- **🎨 Frontend**: http://localhost:8501 (Interfaz de usuario)
- **🔧 Backend**: http://localhost:8000 (API)
- **📖 API Docs**: http://localhost:8000/docs (Documentación interactiva)

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

| Método | Comando | Descripción |
|--------|---------|-------------|
| **🌟 Completo** | `python run_fullstack.py` | Backend + Frontend automático |
| **🪟 Windows** | `run_windows.bat` | Doble click en Windows |
| **🐧 Unix** | `bash run_unix.sh` | Ejecutor para Linux/Mac |
| **🔧 Backend** | `cd Backend && python setup.py run` | Solo API |
| **🎨 Frontend** | `cd Frontend && streamlit run app.py` | Solo UI |

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

- **Python 3.7+** (Recomendado: 3.9+)
- **Conexión a Internet** (para dependencias)
- **4GB RAM** (mínimo)
- **Puertos 8000 y 8501** disponibles

## 📖 Documentación Completa

- **[RUN.md](RUN.md)** - Guía completa de ejecución
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

### Error común: "Puerto ocupado"
```bash
# Verificar qué está usando los puertos
netstat -ano | findstr :8000    # Windows
lsof -i :8000                   # Linux/Mac
```

### Error común: "Python no encontrado"
```bash
# Windows
py run_fullstack.py

# Linux/Mac  
python3 run_fullstack.py
```

### Limpiar y reinstalar
```bash
# Eliminar entorno virtual
rm -rf mlvenv/          # Linux/Mac
rmdir /s mlvenv\        # Windows

# Ejecutar de nuevo (recreará todo)
python run_fullstack.py
```

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
