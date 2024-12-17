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

## Descripción del Sistema

# **Descripción del Sistema**

## **Introducción**  

El proyecto **UVLHub** ha sido diseñado y desarrollado como una herramienta robusta y colaborativa que facilita la gestión, carga, consulta y descarga de **datasets** y **UVLs** (Uniform Value Lists). Su propósito principal es ofrecer a los usuarios una plataforma eficiente para compartir recursos de datos estructurados, mejorar el acceso a la información y optimizar la interacción entre los miembros de la comunidad.  

Con el objetivo de mejorar las capacidades del sistema base, se han implementado una serie de **funcionalidades avanzadas** que aumentan su utilidad y brindan mayor flexibilidad. Estas mejoras responden a necesidades concretas identificadas durante el desarrollo del proyecto y fueron diseñadas para optimizar la experiencia del usuario tanto desde un punto de vista **funcional** como **técnico**.

En esta sección se describirán de manera detallada las nuevas características desarrolladas, su funcionamiento, la relación con otros componentes del sistema y los beneficios que aportan a la plataforma.

---

## **Descripción Funcional y Técnica del Sistema**  

El sistema **UVLHub** se compone de los siguientes módulos principales:

1. **Módulo de Gestión de Datasets**: Permite a los usuarios subir, organizar y administrar datasets. Incluye funcionalidades de previsualización, valoración y control de publicación mediante un área de staging.
2. **Módulo de Gestión de UVLs**: Proporciona herramientas para cargar y listar UVLs, así como un buscador avanzado que facilita su localización.
3. **Módulo de Interfaz de Usuario**: Integra opciones visuales como **modo oscuro** y **modo claro**, mejorando la experiencia de navegación y adaptabilidad.
4. **Módulo de Búsqueda Avanzada**: Permite aplicar filtros específicos para localizar recursos de manera eficiente.  
5. **Módulo de Valoración de Datasets**: Facilita la interacción social entre usuarios mediante un sistema de valoración.  
6. **Módulo de Publicación Controlada**: Introduce un flujo estructurado para asegurar la calidad de los datasets compartidos.  

Cada uno de estos módulos ha sido desarrollado con el objetivo de ser **intuitivo**, **escalable** y fácilmente integrable con otros subsistemas.

---

## **Cambios Realizados**

### **1. Previsualizar UVL**  

La funcionalidad de **previsualización de UVLs** permite a los usuarios visualizar el contenido de un UVL directamente en la interfaz, sin necesidad de descargarlo. Esta mejora resuelve el problema de tener que descargar archivos innecesarios solo para verificar su contenido.

#### **Funcionamiento**:  
- En cada dataset, los UVLs ahora incluyen un botón **"View"**.  
- Al hacer clic en el botón, se abre una ventana emergente o sección de previsualización donde se muestra el contenido del UVL en **formato texto**.  
- Esta vista soporta archivos de tamaño moderado y presenta la información de manera ordenada y legible.  

#### **Beneficios**:  
- **Consulta rápida**: Permite a los usuarios verificar el contenido antes de decidir si descargarlo.  
- **Optimización del tiempo**: Evita la necesidad de descargar archivos innecesarios.  
- **Accesibilidad**: Brinda una manera eficiente de acceder a los datos.  

#### **Ejemplo de Uso**:  
Un investigador necesita consultar varios UVLs dentro de un dataset para analizar patrones en los datos. En lugar de descargar cada archivo, puede previsualizarlos uno a uno, seleccionando solo aquellos que son relevantes para su análisis.

---

### **2. Listar UVLs**  

La funcionalidad de **listar UVLs** proporciona a cada usuario un acceso centralizado a los UVLs que ha subido. Esta mejora facilita la **gestión y organización personal** de los recursos compartidos.

#### **Funcionamiento**:  
- En la sección **"My Profile"**, se ha añadido una nueva columna donde se listan todos los UVLs subidos por el usuario.  
- La tabla muestra información clave como:  
   - Nombre del UVL.  
   - Fecha de subida.  
   - Etiquetas asignadas.  
   - Tamaño del archivo.  
- Los usuarios pueden realizar acciones rápidas, como editar o eliminar un UVL directamente desde la lista.  

#### **Beneficios**:  
- **Organización eficiente**: Facilita la gestión de los UVLs personales.  
- **Acceso rápido**: Permite localizar y consultar recursos propios con facilidad.  
- **Actualización continua**: Proporciona un registro centralizado para mantener los UVLs al día.  

#### **Ejemplo de Uso**:  
Un usuario que ha subido múltiples UVLs a lo largo del tiempo puede consultar rápidamente su lista, verificar cuáles están desactualizados y proceder a editarlos o reemplazarlos.

---

### **3. Modo Oscuro (Dark Mode)**  

La introducción de un botón de **"Dark Mode"** y **"Light Mode"** resuelve la necesidad de ofrecer una experiencia de usuario más personalizable y adaptable a diferentes condiciones de uso.

#### **Funcionamiento**:  
- El sistema ahora incluye dos botones visibles en la interfaz para cambiar entre **modo oscuro** (fondo negro con texto claro) y **modo claro** (fondo blanco con texto oscuro).  
- Este cambio se aplica automáticamente a toda la interfaz, ajustando la paleta de colores del sistema.  

#### **Beneficios**:  
- **Reducción de fatiga visual**: Ideal para entornos con poca luz o largas sesiones de trabajo.  
- **Personalización**: Cada usuario puede elegir la apariencia que prefiera.  
- **Ahorro energético**: En pantallas OLED, el modo oscuro consume menos batería.  

#### **Ejemplo de Uso**:  
Un usuario que trabaja de noche puede activar el **modo oscuro** para reducir la fatiga ocular y hacer más cómoda la lectura de datos.

---

### **4. Rating (Valoración de Datasets)**  

Se ha implementado un sistema de **valoración de datasets** que permite a los usuarios calificar los recursos compartidos por otros.

#### **Funcionamiento**:  
- Cada dataset incluye un atributo **rating** visible para todos los usuarios.  
- Los usuarios autenticados pueden calificar el dataset con un número entero entre **1 y 5**.  
- El rating general del dataset se calcula como la **media aritmética** de todas las valoraciones recibidas.  

#### **Beneficios**:  
- **Identificación de calidad**: Facilita encontrar datasets de mayor relevancia.  
- **Retroalimentación comunitaria**: Promueve la interacción entre usuarios.  
- **Confianza en los recursos**: Ayuda a los usuarios a confiar en los datasets mejor valorados.  

#### **Ejemplo de Uso**:  
Un usuario sube un dataset con información detallada sobre un modelo estadístico. Otros usuarios lo valoran con una puntuación alta, lo que permite destacar ese dataset dentro de la plataforma.

---

### **5. Staging Area (Zona de Staging)**  

La funcionalidad de **Staging Area** introduce un flujo controlado para la publicación de datasets, asegurando su revisión y validación antes de ser publicados.

#### **Funcionamiento**:  
- Los datasets subidos inicialmente se marcan como **“unstaged”**.  
- Los usuarios pueden revisarlos, editar metadatos y corregir descripciones antes de pasarlos a la categoría **“staged”**.  
- Una vez validados, los datasets se promueven a **“published datasets”**.  
- Se incluye un botón adicional para mover **todos los datasets** entre áreas de manera masiva.  

#### **Beneficios**:  
- **Control de calidad**: Garantiza que solo los datasets revisados se publiquen.  
- **Gestión eficiente**: Facilita la organización y revisión de los recursos.  
- **Reducción de errores**: Evita la publicación de información incorrecta o incompleta.  

---

### **6. Search Queries (Búsqueda Avanzada)**  

Se ha mejorado la funcionalidad de búsqueda mediante la implementación de **filtros avanzados** para localizar UVLs de manera más eficiente.

#### **Funcionamiento**:  
El panel de búsqueda avanzada permite filtrar UVLs utilizando criterios como:  
- **Título**.  
- **Descripción**.  
- **Autores** (nombre, ORCID, afiliación).  
- **Etiquetas**.  
- **Rango de fechas** de publicación.  
- **Tamaño máximo del archivo**.  

#### **Beneficios**:  
- **Búsqueda precisa**: Localiza recursos de manera específica.  
- **Eficiencia**: Ahorra tiempo al evitar la revisión manual de grandes volúmenes de datos.  
- **Experiencia optimizada**: Mejora la accesibilidad y organización de la información.  

#### **Ejemplo de Uso**:  
Un usuario necesita encontrar un UVL subido por un autor específico en una fecha determinada. Utiliza los filtros avanzados para localizarlo rápidamente.

---

#### **Conclusión de los cambios realizados**  

Las mejoras implementadas en **UVLHub** han elevado su funcionalidad, eficiencia y accesibilidad. Funcionalidades como la **previsualización de UVLs**, el **modo oscuro**, el sistema de **rating**, la **zona de staging** y la **búsqueda avanzada** optimizan la experiencia del usuario y garantizan un flujo de trabajo más organizado y colaborativo. Estas mejoras posicionan a **UVLHub** como una herramienta robusta y adaptable para la gestión e intercambio de datos, beneficiando a usuarios que dependen de recursos de calidad y fáciles de localizar.






### Visión Global del Proceso de Desarrollo

### Entorno de Desarrollo

### Ejercicio de Propuesta de Cambio

### Conclusiones y trabajo futuro
