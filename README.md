# Proyecto de cátedra: Metodologías ágiles 2024

## Resumen del proyecto
Este proyecto presenta todas las funcionalidades esenciales de un gestor de inventarios. Es un sitio web completo, programado en Python utilizando el framework Flask.

## Funcionalidades
Las funciones con las que cuenta el sistema son:
- Creación, eliminación, edición y consulta de productos
- Gestión de usuarios autorizados y administradores
- Creación de alertas para productos con bajo nivel de inventario (stock)
- Generación de reportes con información general de cada producto
- Historial de transacciones de entrada/salida del inventario para los productos
- Sistema de categorías para clasificar cada producto
- Filtrado de búsqueda de productos

## Planificación y estructura
El sistema contará con las siguientes vistas para el usuario:

- Si el usuario identificado es un administrador:
    - *Dashboard* general de la aplicación
    - Vista para administración de productos
    - Creación de nuevas categorías 
    - Administración de usuarios con acceso al sistema
    - Creación de nuevas transacciones
    - Vista para la generación de reportes de inventario

### Sistema de alertas
Luego de cada transacción, el sistema verificará si el stock de algún producto 
es menor al mínimo establecido (un umbral ingresado por el usuario). En caso de 
que así sea, se enviará una alerta al correo electrónico del usuario que ha colocado la alerta.
