# Web-Store Project - 1º DAW

# Virtual Machines Infrastructure (Linux Mint)

We have configured two virtual machines using **Linux Mint** to separate the web services from the data storage, ensuring a professional environment for our store.

### 1. Web Server VM
*   **Operating System:** Linux Mint 21 (Vanessa)
*   **Role:** Hosting the Python-based web server and Scraping scripts.
*   **Resources:** 2048 MB RAM / 20 GB Disk.
*   **Network:** NAT Network.
*   **IP Address:** 10.0.2.15
*   **User:** Admin

### 2. Database VM
*   **Operating System:** Linux Mint 21 (Vanessa)
*   **Role:** Hosting the PostgreSQL database.
*   **Resources:** 2048 MB RAM / 20 GB Disk.
*   **Network:** NAT Network.
*   **IP Address:** 10.0.2.16
*   **User:** Admin

---

###  Project Architecture
To understand how the data flows between the host, the web server, and the database, you can check the following diagram:

![Diagrama de la arquitectura](./img/diagrama-proyecto.png)
