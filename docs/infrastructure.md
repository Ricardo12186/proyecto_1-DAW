# Web-Store Project - 1º DAW

# Virtual Machines Infrastructure (Linux Mint)

We have configured two virtual machines using **Linux Mint** to separate the web services from the data storage, ensuring a professional environment for our store.

### 1. Web Server VM
*   **Operating System:** Linux Mint 21 (Vanessa)
*   **Role:** Hosting the Python-based web server and Scraping scripts.
*   **Resources:** 2048 MB RAM / 20 GB Disk.
*   **Network:** Bridge Network.
*   **IP Address:** 10.109.99.2
*   **User:** servidor-web

### 2. Database VM
*   **Operating System:** Linux Mint 21 (Vanessa)
*   **Role:** Hosting the PostgreSQL database.
*   **Resources:** 2048 MB RAM / 20 GB Disk.
*   **Network:** Bridge Network.
*   **IP Address:** 10.109.99.245
*   **User:** servidor-bbdd

---

###  Project Architecture
To understand how the data flows between the host, the web server, and the database, you can check the following diagram:

![Diagrama de la arquitectura](/proyecto_1-DAW/img/arquitectura_diagrama.png)
