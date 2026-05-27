# Configuración del Servidor Web Nginx - StyleHub Project

Este documento detalla los pasos técnicos seguidos en el entorno de producción (Máquina Virtual Ubuntu) para la instalación, despliegue y optimización de **Nginx** como proxy inverso para la aplicación web StyleHub.

---

## 1. Instalación de Nginx

En primer lugar, actualizamos los repositorios del sistema e instalamos el paquete oficial de Nginx de forma local:

```bash
sudo apt update
sudo apt install nginx -y
```

## 2. Configuración del Proxy Inverso

Para redirigir de forma segura las peticiones entrantes del puerto estándar HTTP (`80`) hacia el puerto interno donde corre el backend de nuestra aplicación, creamos un archivo de configuración dedicado.

1. Eliminamos el enlace del sitio por defecto para evitar conflictos de enrutamiento:
   ```bash
   sudo rm /etc/nginx/sites-enabled/default
   ```

2. Creamos y editamos el archivo de configuración para StyleHub:
   ```bash
   sudo nano /etc/nginx/sites-available/stylehub
   ```

3. Añadimos el siguiente bloque de configuración estructurado:
   ```server {
    listen 80;
    server_name 10.109.99.2;

    root /var/www/stylehub;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}   ```

## 3. Activación del Sitio y Verificación

Una vez redactado el archivo de configuración, habilitamos el entorno mediante un enlace simbólico hacia los sitios activos:

```bash
sudo ln -s /etc/nginx/sites-available/stylehub /etc/nginx/sites-enabled/
```

Antes de reiniciar el servidor, realizamos un test de sintaxis estricto para asegurar que no existan fallos o bloqueos en el código de Nginx:

```bash
sudo nginx -t
```
*Si la respuesta de la terminal devuelve un estado de éxito (`syntax is ok` / `test is successful`), procedemos al reinicio.*

## 4. Control de Servicios y Arranque Diario

Para aplicar los cambios estructurales, reiniciamos el demonio de Nginx y lo configuramos para que se inicie de forma automática con el encendido del sistema operativo Linux:

```bash
sudo systemctl restart nginx
sudo systemctl enable nginx
```

Para monitorizar que el proxy inverso se mantiene activo en segundo plano (`active (running)`), podemos emplear la directiva:

```bash
sudo systemctl status nginx
```

---
 *Despliegue finalizado con éxito. El servidor web Nginx procesa ahora de forma nativa todo el tráfico de StyleHub.*
