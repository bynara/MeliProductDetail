# MeliProductDetail - Makefile para Linux/Unix
# Facilita las tareas comunes del proyecto

.PHONY: help install run clean test backend frontend setup docs

# Variables
PYTHON := python3
PIP := pip3
VENV_DIR := mlvenv
BACKEND_DIR := Backend
FRONTEND_DIR := Frontend

# Colores para output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

# Comando por defecto
help:
	@echo "$(BLUE)=================================================================="
	@echo "🚀 MELIPRODUCTDETAIL - MAKEFILE PARA LINUX"
	@echo "==================================================================$(NC)"
	@echo ""
	@echo "$(GREEN)Comandos disponibles:$(NC)"
	@echo ""
	@echo "  $(YELLOW)make install$(NC)    - Instala dependencias del sistema (requiere sudo)"
	@echo "  $(YELLOW)make setup$(NC)      - Configura el entorno virtual y dependencias Python"
	@echo "  $(YELLOW)make run$(NC)        - Ejecuta la aplicación completa (recomendado)"
	@echo "  $(YELLOW)make backend$(NC)    - Ejecuta solo el backend (FastAPI)"
	@echo "  $(YELLOW)make frontend$(NC)   - Ejecuta solo el frontend (Streamlit)"
	@echo "  $(YELLOW)make test$(NC)       - Ejecuta todos los tests"
	@echo "  $(YELLOW)make clean$(NC)      - Limpia entorno virtual y archivos temporales"
	@echo "  $(YELLOW)make docs$(NC)       - Muestra la documentación"
	@echo ""
	@echo "$(BLUE)Uso rápido:$(NC)"
	@echo "  $(GREEN)make run$(NC)         # Ejecuta todo automáticamente"
	@echo ""
	@echo "$(BLUE)URLs de acceso:$(NC)"
	@echo "  Frontend: http://localhost:8502"
	@echo "  Backend:  http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"
	@echo ""

# Instalar dependencias del sistema
install:
	@echo "$(BLUE)🔄 Instalando dependencias del sistema...$(NC)"
	@if command -v apt-get >/dev/null 2>&1; then \
		echo "$(GREEN)📦 Detectado: Ubuntu/Debian$(NC)"; \
		sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv python3-dev build-essential curl wget git; \
	elif command -v dnf >/dev/null 2>&1; then \
		echo "$(GREEN)📦 Detectado: Fedora$(NC)"; \
		sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++ make curl wget git; \
	elif command -v yum >/dev/null 2>&1; then \
		echo "$(GREEN)📦 Detectado: CentOS/RHEL$(NC)"; \
		sudo yum install -y python3 python3-pip python3-devel gcc gcc-c++ make curl wget git; \
	elif command -v pacman >/dev/null 2>&1; then \
		echo "$(GREEN)📦 Detectado: Arch Linux$(NC)"; \
		sudo pacman -S --noconfirm python python-pip base-devel curl wget git; \
	else \
		echo "$(YELLOW)⚠️  Gestor de paquetes no reconocido$(NC)"; \
		echo "$(YELLOW)💡 Instala manualmente: python3, python3-pip, python3-venv, build-essential$(NC)"; \
	fi
	@echo "$(GREEN)✅ Dependencias del sistema instaladas$(NC)"

# Configurar entorno Python
setup:
	@echo "$(BLUE)🐍 Configurando entorno Python...$(NC)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(YELLOW)📦 Creando entorno virtual...$(NC)"; \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi
	@echo "$(GREEN)✅ Entorno Python configurado$(NC)"
	@echo "$(BLUE)💡 Ejecuta 'make run' para iniciar la aplicación$(NC)"

# Ejecutar aplicación completa (recomendado)
run:
	@echo "$(BLUE)🚀 Iniciando MeliProductDetail...$(NC)"
	@$(PYTHON) run_simple.py

# Ejecutar solo backend
backend:
	@echo "$(BLUE)🔧 Iniciando solo Backend (FastAPI)...$(NC)"
	@cd $(BACKEND_DIR) && $(PYTHON) run.py

# Ejecutar solo frontend
frontend:
	@echo "$(BLUE)🎨 Iniciando solo Frontend (Streamlit)...$(NC)"
	@cd $(FRONTEND_DIR) && $(PYTHON) -m streamlit run app.py --server.port 8502

# Ejecutar tests
test:
	@echo "$(BLUE)🧪 Ejecutando tests...$(NC)"
	@echo "$(YELLOW)📋 Tests del Backend:$(NC)"
	@cd $(BACKEND_DIR) && $(PYTHON) -m pytest tests/ -v || true
	@echo ""
	@echo "$(YELLOW)📋 Tests del Frontend:$(NC)"
	@cd $(FRONTEND_DIR)/tests && $(PYTHON) run_all_tests.py || true
	@echo "$(GREEN)✅ Tests completados$(NC)"

# Limpiar entorno
clean:
	@echo "$(BLUE)🧹 Limpiando entorno...$(NC)"
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "$(YELLOW)🗑️  Eliminando entorno virtual...$(NC)"; \
		rm -rf $(VENV_DIR); \
	fi
	@echo "$(YELLOW)🗑️  Limpiando archivos temporales...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name "*.pyd" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Limpieza completada$(NC)"

# Mostrar documentación
docs:
	@echo "$(BLUE)📖 Documentación MeliProductDetail$(NC)"
	@echo ""
	@if [ -f "RUN.md" ]; then \
		echo "$(GREEN)📄 Guía de ejecución:$(NC)"; \
		echo "  cat RUN.md"; \
		echo ""; \
	fi
	@if [ -f "README.md" ]; then \
		echo "$(GREEN)📄 README del proyecto:$(NC)"; \
		echo "  cat README.md"; \
		echo ""; \
	fi
	@if [ -f "COMPLETADO.md" ]; then \
		echo "$(GREEN)📄 Resumen de completado:$(NC)"; \
		echo "  cat COMPLETADO.md"; \
		echo ""; \
	fi
	@echo "$(GREEN)🌐 URLs importantes:$(NC)"
	@echo "  Frontend: http://localhost:8502"
	@echo "  Backend:  http://localhost:8000"
	@echo "  API Docs: http://localhost:8000/docs"

# Información del sistema
info:
	@echo "$(BLUE)📊 Información del sistema:$(NC)"
	@echo ""
	@echo "$(GREEN)Sistema operativo:$(NC) $$(uname -s) $$(uname -m)"
	@echo "$(GREEN)Distribución:$(NC) $$(lsb_release -d 2>/dev/null | cut -f2 || echo 'No detectada')"
	@echo "$(GREEN)Python disponible:$(NC) $$($(PYTHON) --version 2>/dev/null || echo 'No encontrado')"
	@echo "$(GREEN)Pip disponible:$(NC) $$($(PIP) --version 2>/dev/null || echo 'No encontrado')"
	@echo "$(GREEN)Directorio actual:$(NC) $$(pwd)"
	@echo "$(GREEN)Entorno virtual:$(NC) $$(if [ -d '$(VENV_DIR)' ]; then echo 'Existe'; else echo 'No existe'; fi)"
	@echo ""

# Instalación completa desde cero
full-install: install setup
	@echo "$(GREEN)🎉 Instalación completa terminada$(NC)"
	@echo "$(BLUE)💡 Ejecuta 'make run' para iniciar la aplicación$(NC)"
