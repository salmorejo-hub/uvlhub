<p align="center">
    <img src="https://www.cnature.es/wp-content/uploads/2020/08/salmorejo-tradicional.jpg" alt="Salmorejo">
</p>

# Documento del Proyecto

## Portada

*    Grupo 2
*    Curso escolar: 2024/2025
*    Asignatura: Evolución y gestión de la configuración

| Miembro del equipo        | Implicación |
| ------------------------- | ----------- |
| Javier Aponte Pozón       | 10          |
| Javier Muñoz Romero       | 10          |
| Juan Núñez Sánchez        | 10          |
| Jose María Portela Huerta | 10          |
| Juan Luis Ruano Muriedas  | 10          |
| Álvaro Sevilla Cabrera    | 10          |

### Enlaces de interes
* [Repositorio del equipo](https://github.com/salmorejo-hub-2/uvlhub)
* [Repositorio Upstream](https://github.com/salmorejo-hub/uvlhub)
* [Despliegue en Render](https://uvlhub-salmorejo-hub.onrender.com/)

---
## Indicadores

| Miembro del equipo        | Horas | Commits | LoC | Test | Issues | Work Item |
| ------------------------- | ----- | ------- | --- | ---- | ------ | --------- |
| Javier Aponte Pozón       |       |         |     |      |        |           |
| Javier Muñoz Romero       |       |         |     |      |        |           |
| Juan Núñez Sánchez        |       |         |     |      |        |           |
| Jose María Portela Huerta |       |         |     |      |        |           |
| Juan Luis Ruano Muriedas  |       |         |     |      |        |           |
| Álvaro Sevilla Cabrera    |       |         |     |      |        |           |

## Integración 


---
## Resumen Ejecutivo

### Descripción del Sistema

Usando como proyecto base uvlhub se ha desarrollado con éxito varios cambios que aumentan las funcionalidades que es capaz de hacer este sistema. La esencia del sistema es que permite subir tus propios datasets y uvl´s asi como descargar los que hayan subido otros usuarios. 
    **Cambios Realizados**
        **1. Previsualizar Uvl**: Dentro de cada dataset podemos ver listados sus uvl`s, se ha implementado un botón "view" en cada uvl que permite previsualizar dicho uvl en formato texto.
        **2. Listar Uvl:** Una vez estas logeado y accedemos a los datos de "My Profile" se ha añadido una columna donde cada usuario podrá ver listados los uvl`s que ha subido.
        **3. Modo Oscuro** A falta de una funcionalidad de poder cambiar el aspecto de las UI, se ha conseguido desarrollar en cada pantalla unos botones "Dark Mode" y "Light Mode" que permiten intercambiar automáticamente la paleta de colores del sitio web a tonos oscuros, o blancos, según proceda.
        **4. Rating:** El equipo ha decidido que sería una buena idea añadir una funcionalidad que permita valorar datasets de los usuarios que hayan subido alguno. Ahora dataset tiene un nuevo atributo *rating* que solo podrá ser modificado por un usuario logueado. Dicho rating será una media aritmética de todos los usuarios que hayan dejado una valoración de ese dataset. Solo se podrá valorar con números enteros del 1 al 5, siendo 1 la peor valoración y 5 la mejor.
        **5. Stagging Area:** Esta funcionalidad introduce una *zona de staging* para datasets, permitiendo que los nuevos se añadan inicialmente como “unstaged” y, tras revisión o edición, pasen a “staged” antes de publicarse definitivamente. De este modo, se revisan y validan los metadatos o la descripción del dataset en un punto intermedio, evitando la publicación directa sin control. Finalmente, los datasets aprobados se promueven a “published datasets”, mientras que los “unsynchronized datasets” requieren acciones adicionales. Todo esto se puede hacer clicando en el icono de la derecha en independientemente del área en la que se encuentre. Para mayor calidad se ha añadido un botón que permita mover de área a todos los datasets que se encuentren en ella para no tener porque hacerlo uno a uno.
        **6. Search Queries:**  En el proyecto existía la opción de buscar por dataset. Ahora, se ha añadido un buscador por uvl.Además, esta funcionalidad introduce un panel de búsqueda avanzada (search queries) que permite filtrar los UVLs listados de forma más específica usando criterios como título, descripción, autores , etiquetas, rango de fechas o incluso tamaño máximo del archivo. Dichos filtros, ubicados a la derecha, facilitan localizar rápidamente modelos que cumplan parámetros concretos en lugar de revisar toda la lista. Una vez aplicados, se refinan los resultados mostrados en el panel principal.



### Visión Global del Proceso de Desarrollo

### Entorno de Desarrollo

### Ejercicio de Propuesta de Cambio

### Conclusiones y trabajo futuro
