import re

import psycopg2
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


DB_CONFIG = {
    "host": "10.109.99.98",
    "port": "5432",
    "dbname": "web_scraping",
    "user": "webuser",
    "password": "password123",
}

HM_SCRAPING_URL = "https://www2.hm.com/es_es/hombre/compra-por-producto/camisetas-y-camisetas-de-tirantes.html"

CATEGORY_NAME = "H&M"
DEFAULT_SIZE = "Única"


def clean_price(price_text):
    if not price_text:
        return 0.00

    price_text = price_text.replace("\xa0", " ")
    price_text = price_text.replace("€", "")
    price_text = price_text.strip()
    price_text = price_text.replace(".", "")
    price_text = price_text.replace(",", ".")

    match = re.search(r"\d+(\.\d+)?", price_text)

    if not match:
        return 0.00

    return float(match.group(0))


def build_full_url(url):
    if not url:
        return ""

    if url.startswith("//"):
        return "https:" + url

    if url.startswith("/"):
        return "https://www2.hm.com" + url

    return url


def get_hm_code(url):
    match = re.search(r"productpage\.([0-9]+)\.html", url)

    if match:
        return match.group(1)

    return url


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_or_create_category(cursor, category_name):
    cursor.execute(
        "SELECT id_category FROM categories WHERE category_name = %s;",
        (category_name,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    cursor.execute(
        """
        INSERT INTO categories (category_name)
        VALUES (%s)
        RETURNING id_category;
        """,
        (category_name,)
    )

    return cursor.fetchone()[0]


def get_or_create_size(cursor, size_name):
    cursor.execute(
        "SELECT id_size FROM sizes WHERE size_name = %s;",
        (size_name,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    cursor.execute(
        """
        INSERT INTO sizes (size_name)
        VALUES (%s)
        RETURNING id_size;
        """,
        (size_name,)
    )

    return cursor.fetchone()[0]


def accept_cookies(driver):
    possible_texts = [
        "Aceptar todo",
        "Aceptar todas",
        "Aceptar",
        "Accept all",
        "Allow all"
    ]

    driver.implicitly_wait(3)

    for text in possible_texts:
        buttons = driver.find_elements(By.XPATH, f"//button[contains(., '{text}')]")

        if buttons:
            try:
                buttons[0].click()
                print("Cookies aceptadas.")
                driver.implicitly_wait(2)
                return
            except Exception:
                pass

    print("No se encontró botón de cookies o no hizo falta.")


def scroll_page(driver):
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 900);")


def extract_image(card):
    img = card.find("img")

    if not img:
        return ""

    image_url = (
        img.get("src")
        or img.get("data-src")
        or img.get("data-original")
        or ""
    )

    if not image_url and img.get("srcset"):
        image_url = img.get("srcset").split(",")[0].strip().split(" ")[0]

    return build_full_url(image_url)


def find_product_card(link):
    parent = link

    for _ in range(8):
        parent = parent.parent

        if not parent:
            return None

        text = parent.get_text(" ", strip=True)

        if "€" in text:
            return parent

    return None


def extract_products_from_html(html):
    soup = BeautifulSoup(html, "html.parser")

    links = soup.select("a[href*='productpage']")
    products = []

    for link in links:
        url_origin = build_full_url(link.get("href"))
        hm_code = get_hm_code(url_origin)

        card = find_product_card(link)

        if not card:
            continue

        card_text = card.get_text(" ", strip=True)

        price_match = re.search(r"\d{1,4},\d{2}\s*€", card_text)

        if not price_match:
            continue

        price_text = price_match.group(0)
        price = clean_price(price_text)

        title = (
            link.get_text(" ", strip=True)
            or link.get("aria-label")
            or ""
        )

        if not title:
            img = card.find("img")

            if img:
                title = img.get("alt", "")

        if not title or len(title) < 3:
            continue

        image_url = extract_image(card)

        product = {
            "hm_code": hm_code,
            "title": title[:150],
            "description": f"Producto obtenido mediante Selenium desde H&M: {title}",
            "price": price,
            "image_url": image_url,
            "url_origin": url_origin,
        }

        repeated = False

        for existing_product in products:
            if existing_product["hm_code"] == product["hm_code"]:
                repeated = True
                break

        if not repeated:
            products.append(product)

        if len(products) >= 20:
            break

    return products


def scrape_with_selenium():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)

    try:
        print("Abriendo navegador con Selenium...")
        driver.get(HM_SCRAPING_URL)

        driver.implicitly_wait(5)

        accept_cookies(driver)
        scroll_page(driver)

        html = driver.page_source

        with open("debug_hm.html", "w", encoding="utf-8") as file:
            file.write(html)

        products = extract_products_from_html(html)

        return products

    finally:
        driver.quit()


def save_products(products):
    connection = get_connection()
    cursor = connection.cursor()

    id_category = get_or_create_category(cursor, CATEGORY_NAME)
    id_size = get_or_create_size(cursor, DEFAULT_SIZE)

    saved_products = 0

    for product in products:
        cursor.execute(
            """
            INSERT INTO products (
                title,
                description,
                price,
                id_category,
                hm_code,
                image_url,
                url_origin,
                updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            ON CONFLICT (hm_code)
            DO UPDATE SET
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                price = EXCLUDED.price,
                id_category = EXCLUDED.id_category,
                image_url = EXCLUDED.image_url,
                url_origin = EXCLUDED.url_origin,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id_product;
            """,
            (
                product["title"],
                product["description"],
                product["price"],
                id_category,
                product["hm_code"],
                product["image_url"],
                product["url_origin"],
            )
        )

        id_product = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO product_stock (id_product, id_size, stock)
            VALUES (%s, %s, %s)
            ON CONFLICT (id_product, id_size)
            DO UPDATE SET stock = EXCLUDED.stock;
            """,
            (id_product, id_size, 10)
        )

        saved_products += 1

    connection.commit()
    cursor.close()
    connection.close()

    return saved_products


def main():
    print("Iniciando scraping con Selenium...")
    print("URL:", HM_SCRAPING_URL)

    products = scrape_with_selenium()

    print("Productos encontrados:", len(products))

    if not products:
        print("No se encontraron productos.")
        print("Se ha guardado un archivo debug_hm.html para revisar qué cargó Selenium.")
        return

    saved_count = save_products(products)
    print(f"Proceso finalizado. Se han guardado/actualizado {saved_count} productos.")


if __name__ == "__main__":
    main()
