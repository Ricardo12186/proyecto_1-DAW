import os
from html import escape

import psycopg2
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

OUTPUT_PATH = os.getenv("OUTPUT_PATH", "/var/www/stylehub/index.html")


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_products():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            p.id_product,
            p.title,
            p.description,
            p.price,
            p.image_url,
            p.url_origin,
            COALESCE(c.category_name, 'Sin categoría') AS category_name,
            COALESCE(SUM(ps.stock), 0) AS total_stock
        FROM products p
        LEFT JOIN categories c ON p.id_category = c.id_category
        LEFT JOIN product_stock ps ON p.id_product = ps.id_product
        GROUP BY
            p.id_product,
            p.title,
            p.description,
            p.price,
            p.image_url,
            p.url_origin,
            c.category_name
        ORDER BY p.id_product DESC;
        """
    )

    products = cursor.fetchall()

    cursor.close()
    connection.close()

    return products


def build_product_card(product):
    (
        id_product,
        title,
        description,
        price,
        image_url,
        url_origin,
        category_name,
        total_stock,
    ) = product

    title = escape(title or "Producto sin nombre")
    description = escape(description or "Sin descripción")
    category_name = escape(category_name or "Sin categoría")
    image_url = escape(image_url or "")
    url_origin = escape(url_origin or "#")

    if image_url:
        image_html = f'<img src="{image_url}" alt="{title}">'
    else:
        image_html = '<div class="no-image">Sin imagen</div>'

    if total_stock > 0:
        stock_html = f'<span class="stock ok">Stock: {total_stock}</span>'
    else:
        stock_html = '<span class="stock empty">Sin stock</span>'

    return f"""
    <article class="product-card">
        <div class="image-box">
            {image_html}
        </div>

        <div class="product-info">
            <p class="category">{category_name}</p>
            <h2>{title}</h2>
            <p class="description">{description}</p>

            <div class="bottom-row">
                <span class="price">{price} €</span>
                {stock_html}
            </div>

            <a class="button" href="{url_origin}" target="_blank">
                Ver producto original
            </a>
        </div>
    </article>
    """


def build_html(products):
    cards = ""

    for product in products:
        cards += build_product_card(product)

    if not cards:
        cards = """
        <div class="empty-message">
            <h2>No hay productos todavía</h2>
            <p>Ejecuta primero el script de scraping.</p>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>StyleHub - Productos H&M</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background: #f5f5f5;
            color: #222;
        }}

        header {{
            background: #111;
            color: white;
            padding: 32px 20px;
            text-align: center;
        }}

        header h1 {{
            margin: 0;
            font-size: 42px;
            letter-spacing: 1px;
        }}

        header p {{
            margin-top: 10px;
            color: #ddd;
        }}

        main {{
            max-width: 1200px;
            margin: 30px auto;
            padding: 0 20px;
        }}

        .summary {{
            background: white;
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 24px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }}

        .products-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 24px;
        }}

        .product-card {{
            background: white;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.10);
            display: flex;
            flex-direction: column;
        }}

        .image-box {{
            width: 100%;
            height: 320px;
            background: #eee;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .image-box img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}

        .no-image {{
            color: #777;
            font-size: 18px;
        }}

        .product-info {{
            padding: 18px;
            display: flex;
            flex-direction: column;
            flex: 1;
        }}

        .category {{
            margin: 0 0 8px;
            font-size: 13px;
            color: #777;
            text-transform: uppercase;
        }}

        h2 {{
            margin: 0 0 12px;
            font-size: 20px;
        }}

        .description {{
            color: #555;
            font-size: 14px;
            line-height: 1.4;
            flex: 1;
        }}

        .bottom-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 16px;
            margin-bottom: 16px;
        }}

        .price {{
            font-size: 22px;
            font-weight: bold;
        }}

        .stock {{
            font-size: 13px;
            padding: 6px 10px;
            border-radius: 20px;
        }}

        .stock.ok {{
            background: #e4f7e4;
            color: #1d7a1d;
        }}

        .stock.empty {{
            background: #fde3e3;
            color: #b00020;
        }}

        .button {{
            display: block;
            text-align: center;
            background: #111;
            color: white;
            padding: 12px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
        }}

        .button:hover {{
            background: #333;
        }}

        footer {{
            margin-top: 40px;
            padding: 24px;
            text-align: center;
            color: #777;
        }}

        .empty-message {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <header>
        <h1>StyleHub</h1>
        <p>Productos obtenidos mediante scraping desde H&M y guardados en PostgreSQL</p>
    </header>

    <main>
        <section class="summary">
            <strong>Productos cargados:</strong> {len(products)}
        </section>

        <section class="products-grid">
            {cards}
        </section>
    </main>

    <footer>
        Proyecto DAW - Scraping con Selenium, PostgreSQL y Nginx
    </footer>
</body>
</html>
"""

    return html


def save_html(html):
    output_dir = os.path.dirname(OUTPUT_PATH)

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        file.write(html)


def main():
    print("Leyendo productos desde PostgreSQL...")

    products = get_products()

    print(f"Productos encontrados en BBDD: {len(products)}")

    html = build_html(products)

    save_html(html)

    print(f"OK: HTML generado en {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
