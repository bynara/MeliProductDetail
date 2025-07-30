import logging
import sys

# Configuración más robusta del logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("backend.log", mode="a", encoding="utf-8")
    ]
)

logger = logging.getLogger("meli_api")

# Reducir logs de uvicorn para evitar spam
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.INFO)
