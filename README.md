# Event-Driven Microservices Architecture (Django, Flask & React)

Este proyecto es una aplicación full-stack basada en una arquitectura de microservicios impulsada por eventos (Event-Driven). Está diseñada para demostrar la comunicación asíncrona entre servicios independientes utilizando un broker de mensajería (RabbitMQ) y la comunicación síncrona a través de APIs REST.

## 🏗 Arquitectura del Sistema

El proyecto se divide en tres componentes principales:

1. **Admin Service (Django / Django REST Framework):** - Actúa como la fuente principal de la verdad (Source of Truth) para la creación y gestión de productos.
   - Expone un CRUD completo para los productos.
   - Actúa como **Productor** de eventos: Cada vez que se crea, actualiza o elimina un producto, publica un evento en RabbitMQ (`product_created`, `product_updated`, `product_deleted`).
   - Expone un endpoint mock para simular la autenticación y obtención de usuarios aleatorios.

2. **Main Service (Flask / SQLAlchemy):**
   - Servicio orientado al usuario final.
   - Mantiene una copia de solo lectura de los productos en su propia base de datos (MySQL) consumiendo los eventos de RabbitMQ.
   - Gestiona el sistema de "Likes" de los productos.
   - Al dar "Like", realiza una petición HTTP síncrona al servicio de Django para obtener el usuario actual y asegurar la unicidad (un usuario solo puede dar un like por producto).
   - Actúa también como productor publicando el evento `product_liked`.

3. **Frontend (React):**
   - Single Page Application (SPA) que consume ambos microservicios.
   - **Main View:** Interfaz de usuario donde se listan los productos y se pueden dar "Likes" (conectado al puerto de Flask).
   - **Admin Panel:** Panel de administración con operaciones CRUD completas para gestionar el inventario (conectado al puerto de Django).

## 🚀 Tecnologías Utilizadas

- **Backend:** Python 3, Django, Django REST Framework, Flask, Flask-SQLAlchemy, Flask-Migrate.
- **Frontend:** React, React Router Dom, Bootstrap / CSS.
- **Base de Datos:** MySQL.
- **Mensajería / Eventos:** RabbitMQ (Pika).
- **Contenedores:** Docker & Docker Compose (configurado para despliegue local).

## ⚙️ Instalación y Configuración local

### Prerrequisitos
- Docker y Docker Compose instalados.
- Node.js y npm instalados.
- Python 3.x.

### 1. Levantar los Microservicios (Backend)
Ambos microservicios y la base de datos están dockerizados. Ejecuta el siguiente comando en la raíz donde se encuentre tu `docker-compose.yml`:

```bash
docker-compose up --build
