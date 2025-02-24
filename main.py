import uvicorn
from fastapi import FastAPI, Request, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse
import uuid
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from backend.dbase.models import ProductORM
from backend.utils.dependencies import get_current_user, AsyncSession, get_db
from backend.api import auth, product, cart, admin
from backend.conf import secret_key, templates


app = FastAPI()
app.mount("/frontend/static", StaticFiles(directory="frontend/static"), name="static")
app.add_middleware(SessionMiddleware, secret_key=secret_key)


app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(admin.router)


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request, db: AsyncSession = Depends(get_db)):
    current_user = await get_current_user(request, db)
    if not current_user:
        if "session_id" not in request.session:
            session_id = str(uuid.uuid4())
            request.session["session_id"] = session_id

    products = await db.execute(select(ProductORM))
    products = products.scalars().all()
    user_name = request.session.get("user_name")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products,
        "user": user_name,
        "role": current_user,
    })


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)
