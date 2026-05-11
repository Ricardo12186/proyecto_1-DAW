#  Product Research Documentation - Web-Store

This section documents the process of searching, analyzing, and selecting the data source for our virtual store's catalog.

###  Reference Websites
1. **ASOS (Selected):** [https://asos.com](https://asos.com)
   - *Observation:* A global fashion leader with an extensive and visually appealing catalog.

###  Evaluated APIs
The following interfaces were analyzed to obtain products dynamically:
- **Asos API (via RapidAPI):** Provides direct access to ASOS's real catalog, including prices, sizes, and high-resolution images.
- **Fake Store API:** A simple option with static test data.
- **Platzi Fake Store API:** Useful for development testing, but with generic products.

##  Final Selection: ASOS
For the development of this **web-store**, the **ASOS API** has been chosen as the primary product source.

### Justification of the Choice:
- **Visual Quality:** ASOS images provide a professional aesthetic to the user interface.
- **Realism:** It allows working with actual stock data, real brands, and detailed descriptions that enhance the browsing experience.
- **Scalability:** The use of a JSON-structured API facilitates the implementation of category filters and real-time searches within the application.
