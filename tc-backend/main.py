from app import create_app
from app.core.config import settings

app = create_app()

# Execução com Uvicorn (apenas se rodar como script)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.port, reload=True)
