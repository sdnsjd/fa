from backend.conf import templates
from backend.dbase.models import ProductORM
from backend.utils.dependencies import AsyncSession
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select


class CartService:
    @staticmethod
    async def get_cart(request: Request, db: AsyncSession):
        cart = request.session.get("cart", {"items": []})
        if not cart["items"]:
            return templates.TemplateResponse("cart.html", {"request": request, "products": [], "total_price": 0})

        product_quantities = {item["product_id"]: item["quantity"] for item in cart["items"]}
        cart_product_ids = [item["product_id"] for item in cart["items"]]

        products = await db.execute(select(ProductORM).where(ProductORM.id.in_(cart_product_ids)))
        products = products.scalars().all()

        if not products:
            request.session.pop("cart", None)

        cart_products = []
        for product in products:
            product.quantity = product_quantities[str(product.id)]
            product.total_price = product.price * product.quantity
            cart_products.append(product)

        total_price = sum(product.total_price for product in cart_products)

        return templates.TemplateResponse("cart.html", {
            "request": request,
            "products": cart_products,
            "total_price": total_price,
        })

    @staticmethod
    async def add_to_cart(request: Request):
        try:
            data = await request.json()
            product_id = data.get('product_id')
            quantity = data.get('quantity')

            if product_id is None or quantity is None:
                return JSONResponse(status_code=400, content={"message": "Invalid data"})

            if "cart" not in request.session:
                request.session["cart"] = {"items": []}

            cart = request.session["cart"]
            found = False

            for item in cart["items"]:
                if item["product_id"] == product_id:
                    item["quantity"] += quantity
                    found = True
                    break

            if not found:
                cart["items"].append({"product_id": product_id, "quantity": quantity})

            request.session["cart"] = cart

            return {"cart": cart}
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": str(e)})

    @staticmethod
    async def increase_quantity(request: Request):
        data = await request.json()
        product_id = data.get("product_id")
        cart = request.session.get("cart", {"items": []})
        for item in cart["items"]:
            if item["product_id"] == product_id:
                item["quantity"] += 1
                break
        else:
            raise HTTPException(status_code=404, detail="Product not found in cart")

        request.session["cart"] = cart
        return JSONResponse(content={"status": "success"})

    @staticmethod
    async def decrease_quantity(request: Request):
        data = await request.json()
        product_id = data.get("product_id")
        cart = request.session.get("cart", {"items": []})
        for item in cart["items"]:
            if item["product_id"] == product_id:
                if item["quantity"] > 1:
                    item["quantity"] -= 1
                else:
                    cart["items"].remove(item)
                break
        else:
            raise HTTPException(status_code=404, detail="Product not found in cart")

        if not cart["items"]:
            request.session.pop("cart", None)
        else:
            request.session["cart"] = cart

        return JSONResponse({"status": "success"})

    @staticmethod
    async def remove_product(request: Request):
        data = await request.json()
        product_id = data.get("product_id")
        cart = request.session.get("cart", {"items": []})
        cart["items"] = [item for item in cart["items"] if item["product_id"] != product_id]

        if not cart["items"]:
            request.session.pop("cart", None)
        else:
            request.session["cart"] = cart

        return JSONResponse({"status": "success"})

