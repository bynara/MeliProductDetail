# 🐧 MeliProductDetail - Guía Linux

Guía específica para ejecutar MeliProductDetail en sistemas Linux.

## 🚀 Inicio Rápido

### Opción 1: Script Unix (Recomendado)

```bash
# Clonar el repositorio (si no lo tienes)
git clone https://github.com/bynara/MeliProductDetail.git
cd MeliProductDetail

# Hacer ejecutable y ejecutar
chmod +x run_unix.sh
./run_unix.sh
```

### Opción 2: Makefile (Para usuarios avanzados)

```bash
# Ver opciones disponibles
make help

# Ejecutar directamente
make run

# Instalación completa desde cero
make full-install
make run
```

### Opción 3: Instalación Automática

```bash
# Instala automáticamente todas las dependencias del sistema
chmod +x install_linux.sh
./install_linux.sh
```

## 📋 Dependencias del Sistema

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential curl wget git
```

### CentOS/RHEL/Fedora

```bash
# Fedora
sudo dnf install -y python3 python3-pip python3-devel gcc gcc-c++ make curl wget git

# CentOS/RHEL
sudo yum install -y python3 python3-pip python3-devel gcc gcc-c++ make curl wget git
```

### Arch Linux

```bash
sudo pacman -S --noconfirm python python-pip base-devel curl wget git
```

## 🔧 Comandos del Makefile

| Comando | Descripción |
|---------|-------------|
| `make help` | Muestra ayuda y comandos disponibles |
| `make install` | Instala dependencias del sistema |
| `make setup` | Configura entorno virtual Python |
| `make run` | Ejecuta la aplicación completa |
| `make backend` | Ejecuta solo el backend |
| `make frontend` | Ejecuta solo el frontend |
| `make test` | Ejecuta todos los tests |
| `make clean` | Limpia entorno y archivos temporales |
| `make docs` | Muestra documentación |
| `make info` | Información del sistema |

## 🌐 URLs de Acceso

Una vez ejecutando:

- **Frontend**: http://localhost:8502
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **API Schema**: http://localhost:8000/openapi.json

## 🐛 Solución de Problemas Linux

### Python no encontrado

```bash
# Verificar Python
python3 --version
which python3

# Si no está instalado
sudo apt install python3 python3-pip  # Ubuntu/Debian
sudo dnf install python3 python3-pip  # Fedora
```

### Permisos denegados

```bash
# Hacer scripts ejecutables
chmod +x run_unix.sh
chmod +x install_linux.sh

# Verificar permisos del directorio
ls -la
```

### Puerto ocupado

```bash
# Verificar qué usa el puerto
sudo lsof -i :8000
sudo lsof -i :8502

# Matar proceso específico
sudo kill -9 <PID>

# O usar netstat
sudo netstat -tulpn | grep :8000
```

### Dependencias de compilación

```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel

# Fedora
sudo dnf groupinstall "Development Tools"
sudo dnf install python3-devel
```

### Error de SSL/Certificados

```bash
# Actualizar certificados
sudo apt update && sudo apt install ca-certificates  # Ubuntu/Debian
sudo dnf update ca-certificates                      # Fedora
```

## 🎯 Comandos Útiles

### Verificar Estado

```bash
# Ver procesos Python
ps aux | grep python

# Ver puertos en uso
sudo ss -tulpn | grep python

# Logs del sistema
journalctl -f | grep python
```

### Limpiar Sistema

```bash
# Limpiar completamente
make clean

# O manualmente
rm -rf mlvenv/
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -delete
```

### Monitoreo

```bash
# Ver logs en tiempo real
tail -f Backend/logs/*.log  # Si existen

# Monitorear recursos
htop
```

## 🚀 Automatización

### Crear Servicio Systemd (Opcional)

```bash
# Crear archivo de servicio
sudo tee /etc/systemd/system/meliproduct.service << EOF
[Unit]
Description=MeliProductDetail App
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(which python3) run_simple.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Activar servicio
sudo systemctl daemon-reload
sudo systemctl enable meliproduct.service
sudo systemctl start meliproduct.service

# Ver estado
sudo systemctl status meliproduct.service
```

### Script de Inicio Automático

```bash
# Agregar al .bashrc para inicio automático
echo "cd ~/MeliProductDetail && make run" >> ~/.bashrc
```

## 📚 Más Información

- **Documentación completa**: `cat RUN.md`
- **Información del proyecto**: `cat README.md`
- **Estado de completado**: `cat COMPLETADO.md`

## 🎉 ¡Listo!

Con estos comandos deberías tener MeliProductDetail funcionando perfectamente en Linux. El script `run_unix.sh` maneja automáticamente la mayoría de configuraciones necesarias.

Para soporte adicional, revisa los logs o usa `make help` para ver todas las opciones disponibles.
