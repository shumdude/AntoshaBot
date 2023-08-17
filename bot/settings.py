from bot.database import Product


def get_product_caption(product: Product) -> str:
    product_caption: str = f"Название: {product.name}\n\nЦена: {product.price}\n\nСайт: {product.url}"
    return product_caption


# сделать телеграм фото и хранить в БД в отдельной служебной таблице
NO_PHOTO = "https://topzero.com/wp-content/uploads/2020/06/topzero-products-Malmo-Matte-Black-TZ-PE458M-image-003.jpg"
