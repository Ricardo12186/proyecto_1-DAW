# Final Prompt

Act as a data extraction assistant for an educational project from 1st DAW called StyleHub.

I want you to perform AI-assisted scraping on this H&M Spain page:

https://www2.hm.com/es_es/hombre/compra-por-producto/camisetas-y-camisetas-de-tirantes.html

Extract between 10 and 15 visible products from the category. For each product, I need the following fields:

* **hm_code**: product code if it appears in the URL or the product page. If it does not appear, create a stable identifier based on the URL.
* **title**: name of the product.
* **description**: short description of the product. If there is no visible description, create a brief description based on the product name, indicating that it comes from H&M.
* **price**: numerical price in euros, using a decimal point. Example: 9.99.
* **currency**: EUR.
* **category**: H&M Hombre - Camisetas y tops.
* **image_url**: absolute URL of the product image. If it cannot be obtained, leave the field empty.
* **url_origin**: absolute URL of the original product.
* **sizes**: array with a default size: [{"size_name": "Única", "stock": 10}].

Mandatory rules:

1. Return ONLY valid JSON.
2. Do NOT use Markdown.
3. Do NOT explain the process.
4. Do NOT invent prices if you do not see them.
5. Do NOT include duplicate products.
6. Use double quotes for all keys and strings.

The JSON must have this exact structure:

{
  "source": {
    "site": "H&M España",
    "url": "https://www2.hm.com/es_es/hombre/compra-por-producto/camisetas-y-camisetas-de-tirantes.html",
    "category": "H&M Hombre - Camisetas y tops",
    "method": "IA con navegación web",
    "project": "StyleHub"
  },
  "products": []
}

Fill the `products` array with the found products.

---

# Improvement Prompt (If the JSON is incorrect)

The previous JSON does not fully meet the expected format. Correct it by keeping ONLY valid JSON.

Review these conditions:

* `price` must be a number, not text.
* `currency` must be "EUR".
* `image_url` and `url_origin` must be absolute URLs if they exist.
* `products` must contain between 10 and 15 products.
* There must be NO text outside the JSON.
* There must be NO comments.
* There must be NO duplicate products.

Return the complete corrected JSON again.
