from datetime import timedelta
import os
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

try:
    # Importaciones relativas para cuando se ejecuta como módulo
    from .core.security import authenticate_user, create_access_token
    from .controllers import seller_controller, category_controller, payment_method_controller, product_controller, review_controller
except ImportError:
    # Importaciones absolutas para cuando se ejecuta directamente
    from core.security import authenticate_user, create_access_token
    from controllers import seller_controller, category_controller, payment_method_controller, product_controller, review_controller

app = FastAPI(
    title="MeLi Marketplace API",
    description="A robust API for managing products, categories, and sellers in the MeLi marketplace ecosystem.",
    version="1.0.0",
    contact={
        "name": "MeLi Dev Team",
        "url": "https://meli.example.com",
        "email": "support@meli.example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(seller_controller.router)
app.include_router(product_controller.router)
app.include_router(category_controller.router)
app.include_router(payment_method_controller.router)
app.include_router(review_controller.router)

@app.get("/", tags=["Info"])
def root():
    return {
        "title": app.title,
        "description": app.description,
        "version": app.version,
    }


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
