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
| Javier Aponte Pozón       |   35    |    10     |  791   |  6    |  1      |     5      |
| Javier Muñoz Romero       |    45   |  17       |   661  |   9   |   7     |   3  (2.1, 2.2, 2.4)        | 
| Juan Núñez Sánchez        |       |         |     |      |        |           |
| Jose María Portela Huerta |       |         |     |      |        |           |
| Juan Luis Ruano Muriedas  | 60    | 53      | 489 | 8    | 6      | 2.6       |
| Álvaro Sevilla Cabrera    |       |         |     |      |        |           |

## Integración 
* [Salmorejo-hub-1](https://github.com/salmorejo-hub-1/uvlhub): Hemos hecho integración con este grupo para tener un alcance más amplio para nuestro proyecto y queremos optar a la nota máxima. 
---
## Resumen Ejecutivo
En *Salmorejo-hub-2* nos hemos encargado de crear las **mejoras de UI, mejoras en el perfil y de búsqueda de "Feature models"** de UVLHub". Hemos creado nuevos módulos que los incluimos al sistema existente para hacer un desarrollo cohesivo con el UVLHub original y modificamos en pequeña medida los modulos ya implementados para añadir fuciones que constituyan mejoras a la UI. **En cuanto a la visión global del proceso**, nos hemos intentado adherir a las metodologias ágiles con un proceso de desarrollo de integración y despliegue continuos junto con nuestros compañeros del equipo de Salmorejo-hub-1. Hemos acordado entre ambos equipos **usar el mismo versionado y la misma politica de incidencias y cambios** para todos nuestros repositorios y nos comunicaremos con el repositorio upstream de donde haremos la integración y nos pondremos las incidencias hacia otro grupo. Internamente, siguiendo la misma metodologia, tenemos nuestro propio ciclo para las incidencias y así trabajar en nuestro propio equipo. El sistema que hemos utilizado para nuestros proyectos es una especie de Gitflow modificado donde tratamos cada uno de nuestros repositorios como ramas glorificadas y en estos se pueden hacer ramas dedicadas a los work items de cada equipo y trabajar internamente. Al contrario que en el gitflow clásico, se podran reusar ramas de desarrollo siempre que se trate del mismo work item y este carece de rama develop para evitar más merges de los que sean necesarios. Dicha metetodologia consiste en hacer incidencias de los cambios o incidencias que surjan y asignarlas a los miembros para que empiecen a trabajar en ramas especificas para los Work Items o incidencias en especifico. Para ello hemos usado las herramientas de github como github proyect o el uso de la wiki del grupo para establecer las reglas del equipo y poder trabajar todos en sintonia. A lo largo de este proyecto hemos ganado disciplina a base de acostumbrandonos a las medidas que hemos implementado que consideramos que son de buenas prácticas para mejorar el proceso de desarrollo de proyectos futuros. En cuanto al entorno de desarrollo de nuestro equipo especificamente hemos usado herramientas comunes como VisualStudio code, Mariadb, selenium y locust para los test y el despliegue realizado en Render. El proceso de despliegue local comprende instalar la aplicación localmente y sus dependencias junto con la base de datos y realizar las migraciones consecuentes para poder establecerla, más adelante se profundizará este aspecto. Una parte clave para nuestro proyecto ha sido en el apartado de integración continua, nuestra organización entre los dos equipos requiere una implementación continua de los cambios y por tanto requiere hacer multitud de integraciones en el repositorio upstream, para ello nos hemos apoyado en varios workflows de github actions para poder tener una implementación rápida y eficaz en cuanto a la revisión de modulos con los tests y la integración al upstream. 

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

#### Introducción

El proceso de desarrollo del sistema ha sido diseñado para implementar prácticas de integración continua mientras se mantiene un flujo de trabajo eficiente y colaborativo. Nuestro enfoque se centra en la segmentación del proyecto en elementos manejables, conocidos como Work Items (WI), y en el manejo de ramas de desarrollo para garantizar la integración y despliegue controlados.

Para asegurar un flujo organizado y consistente, se han establecido convenciones claras para el manejo de tareas, ramas, commits y Pull Requests. Las tareas se gestionan mediante issues en GitHub, donde se especifican prioridades, tipos y relaciones con los WI. Estas convenciones permiten priorizar actividades, identificar problemas de manera temprana y asegurar que cada etapa del desarrollo esté alineada con los objetivos del proyecto.

El despliegue sigue un flujo riguroso que involucra tres repositorios: dos repositorios de grupo y un repositorio principal. El sistema solo se despliega cuando los cambios están validados en la rama `main` del repositorio principal, garantizando que solo el código completamente integrado y probado llegue a producción.

---

#### Metodología Adoptada

- **Enfoque general**: Se sigue un flujo de trabajo iterativo, basado en una división clara de tareas y una estructura organizada para la gestión del desarrollo.
- **Organización del trabajo**: 
  1. El proyecto se divide en Work Items (WI), cada uno asignado a un equipo o grupo de trabajo.
  2. Cada WI se desglosa en un issue que se gestionan y rastrean en GitHub.
  3. Las tareas se organizan por prioridad y tipo, lo que permite un manejo estructurado del trabajo.
  4. Se establecen convenciones de nombres para ramas y commits, asegurando cohesión y trazabilidad.
- **Estructura de repositorios**:
  - Cada grupo tiene su propio repositorio con una rama `main` para consolidar el trabajo del equipo y ramas específicas para cada WI.
  - Existe un repositorio principal con las ramas `develop` y `main`, donde se realiza la integración final, ademas de ramas `fix` para resolver errores y una rama para `fakenodo`.
- **Flujo general**:
  - Desarrollo en ramas específicas por WI en los repositorios de grupo.
  - Integración en la rama `main` del repositorio de grupo.
  - Fusión en la rama `develop` del repositorio principal para validación.
  - Promoción a la rama `main` del repositorio principal para el despliegue final.

---

#### Herramientas Utilizadas

- **Gestión de tareas**: GitHub Projects, con etiquetas y prioridades definidas para cada issue.
- **Control de versiones**: Git y GitHub.
- **Integración y despliegue continuos**: GitHub Actions y Render, con workflows automatizados.
- **Pruebas**: Pytest para pruebas unitarias, Selenium para pruebas de interfaz, y Locust para pruebas de carga.
- **Documentación**: Markdown.

---

#### Workflows Automatizados

Para garantizar la calidad y consistencia del código en cada etapa del desarrollo, se utilizan varios workflows automatizados configurados en GitHub Actions. Estos incluyen:

- **Verificación de Commits**:
  - Asegura que los mensajes de commit sigan las convenciones establecidas, como el uso de formatos específicos (`fix`, `feat`, `docs`, etc.).
  - Garantiza trazabilidad y claridad en los cambios realizados.

- **Codacy**:
  - Realiza análisis estático del código para detectar errores, mejorar la calidad y garantizar que el código cumpla con los estándares de estilo definidos.

- **Lint**:
  - Verifica automáticamente que el código siga las reglas de formato especificadas, evitando inconsistencias.

- **Pruebas Automatizadas**:
  - Ejecuta pruebas unitarias con **Pytest** para validar la funcionalidad básica.
  
- **Render**:
  - Despliegue automatizado del sistema basado en el contenido de la rama `main` del repositorio principal, asegurando que solo el código completamente validado llegue a los entornos de producción.

- **CI2.yml**:
  - Si los cambios en la rama `main` de un repositorio de grupo pasan todas las validaciones, se genera automáticamente una Pull Request hacia la rama `develop` del repositorio principal.

Estos workflows se ejecutan en momentos específicos del desarrollo, proporcionando una capa adicional de confianza en la calidad y estabilidad del sistema:

- **Verificación de Commits**: 
  - Se ejecuta al realizar un commit para garantizar que los mensajes cumplan con las convenciones establecidas y la trazabilidad sea clara.

- **Test, Codacy y Lint**:
  - Estos workflows se ejecutan automáticamente en las Pull Requests (PR) para validar que el código propuesto cumple con los estándares de calidad, funcionalidad y estilo.

- **Render**:
  - Este workflow se activa automáticamente cuando se fusionan cambios en la rama `main` del repositorio principal, desplegando el sistema en el entorno de producción.

- **CI2.yml**:
  - Se ejecuta automáticamente cuando los cambios en la rama `main` de un repositorio de grupo pasan todas las validaciones. Genera una Pull Request hacia la rama `develop` del repositorio principal para integrar los cambios del grupo al repositorio padre.

---

#### Ciclo de Vida del Desarrollo

1. **Identificación de Requisitos**
   - Cada Work Item (WI) se gestiona como una única issue en GitHub, representando una funcionalidad o tarea principal del proyecto.
   - Los equipos trabajan directamente en los WI sin necesidad de dividirlos en sub-issues.

2. **Planificación**
   - Las issues se crean en GitHub con un formato estructurado (e.g., `2.X Nombre del WI`).
   - Se asignan etiquetas para definir la prioridad (#priority: critical, medium, low) y el tipo (#type: bug, documentation, enhancement, etc.).

3. **Desarrollo**
   - Cada issue se trabaja en una rama específica del WI (e.g., `feat/WI-2.X-nombre`) dentro del repositorio del grupo.
   - Los commits siguen convenciones establecidas para indicar el tipo de cambio (`fix`, `feat`, `docs`) y su relación con issues (#Ref o #Closes).

4. **Pruebas**
   - **Unitarias**: Pytest se utiliza para validar la lógica de funciones y módulos.
   - **De interfaz**: Selenium asegura que las interacciones gráficas operan correctamente.
   - **De carga**: Locust simula múltiples usuarios para evaluar el rendimiento bajo diferentes condiciones.
   - Los workflows automatizados en GitHub verifican que las pruebas se ejecuten correctamente antes de cualquier integración.

5. **Revisión e Integración**
   - Las PRs son revisadas por otros miembros del equipo para garantizar la calidad.
   - Los cambios de las ramas de grupo se integran en la rama `develop` del repositorio principal, donde se ejecutan pruebas adicionales y validaciones.
   - Solo los cambios aprobados se fusionan en la rama `main` del repositorio principal.

6. **Despliegue**
   - El despliegue está automatizado mediante Render y solo ocurre desde la rama `main` del repositorio principal.
   - Esto garantiza que solo el código completamente validado e integrado llegue a producción.

7. **Monitorización y Feedback**
   - Render proporciona herramientas básicas de monitoreo para supervisar el sistema en producción.
   - Los problemas detectados generan nuevas incidencias, que se gestionan dentro del flujo habitual.

---

### Entorno de Desarrollo

Ahora pasaremos a una explicación exhausta del entorno de desarrollo. Aquí, entre otras cosas, podemos comprobar cómo se ha de instalar la herramienta, además de cómo ha trabajado el equipo de desarrollo en el trabajo a nivel de entorno de desarrollo.

Para empezar, comentaremos que se ha usado un mismo entorno de desarrollo por parte de todos los miembros del equipo. Esta decisión se tomo, si se puede llegar a decir así, por la recomendación de los profesores de la asignatura, siendo el sistema operativo `Linux Ubuntu 22.04 LTS`. No elegimos en ningún momento máquinas virtuales ni hacerlo en `Windows` porque sabíamos de antemano los fallos que podía llegar a dar, caso de `Windows`; y lo lento que iría según avanzara el proyecto y las prácticas, caso de las máquinas virtuales.

Para continuar, comentaremos las versiones usadas, recalcando la de `Python3.12`. Esto es de vital importancia, pues usando `Python3.10` no se puede ejecutar el proyecto, ni usarlo. De ahí la importancia de usar este versionado. Además, como es lógico, hemos usado muchas más herramientas. Todas ellas se encuentran almacenadas en el `requirements.txt`.

Luego, para simplificación de la instalación de la herramienta, se deben seguir los siguientes pasos:

1. Descargar el repositorio del proyecto en su dispositivo. Para ello, ejecutamos:
```
git clone https://github.com/salmorejo-hub-2/uvlhub.git
cd uvlhub
```

2. Una vez tengamos la herramienta instalada, necesitamos instalar la base de datos. Nosotros usamos MariaDB. Con MariaDB instalado, hay que configurarlo. Todo esto lo podemos realizar con:
``` 
sudo apt install mariadb-server -y
sudo systemctl start mariadb
sudo mysql_secure_installation
```

3. Ahora, podemos visualizar cómo entramos en la configuración de MySQL. Necesitamos configurar nuestra base de datos. Esto se hace contestando de la siguiente forma:
``` 
- Enter current password for root (enter for none): (enter)
- Switch to unix_socket authentication [Y/n]: `y`
- Change the root password? [Y/n]: `y`
    - New password: `uvlhubdb_root_password`
    - Re-enter new password: `uvlhubdb_root_password`
- Remove anonymous users? [Y/n]: `y`
- Disallow root login remotely? [Y/n]: `y` 
- Remove test database and access to it? [Y/n]: `y`
- Reload privilege tables now? [Y/n] : `y`
```

4. Crearemos en este punto la base de datos. Accedemos a ella con:
```
sudo mysql -u root -p
```
- Pero, si estás repitiendo estos pasos, primero bórrala con esto (este paso es **opcional**, recuerda):
``` 
DROP DATABASE uvlhubdb;
DROP DATABASE uvlhubdb_test;
```
- Ahora seguimos con la creación
``` 
CREATE DATABASE uvlhubdb;
CREATE DATABASE uvlhubdb_test;
CREATE USER 'uvlhubdb_user'@'localhost' IDENTIFIED BY 'uvlhubdb_password';
GRANT ALL PRIVILEGES ON uvlhubdb.* TO 'uvlhubdb_user'@'localhost';
GRANT ALL PRIVILEGES ON uvlhubdb_test.* TO 'uvlhubdb_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

5. Es importante para el proyecto que te lleves los cambios de ejemplo de env para tener el tuyo propio, y así poder usar el proyecto. Esto se hace con:
```
cp .env.local.example .env
```

6. Y, una vez instalemos las dependencias con los siguiente comandos, podremos poner a funcionar la aplicación:
- Para instalar las dependencias:
```
sudo apt install python3.12-venv
python3.12 -m venv venv
source venv/bin/activate
```
```
sudo apt install python3.12-venv
python3.12 -m venv venv
source venv/bin/activate
```
```
pip install --upgrade pip
pip install -r requirements.txt
pip install -e ./
```

7. Aplicando las migraciones y llenando las bases de datos son necesarios. Lo conseguimos con:
```
flask db upgrade
rosemary db:seed
```

8. Y tu aplicación ya debe estar instalada. Solo tienes que usar el siguiente comando para poder usarla.
```
flask run --host=0.0.0.0 --reload --debug
```

Si se quiere repetir para vaciar la base de datos, los pasos a seguir son pocos por suerte. Usamos el paso 4 entero, luego el paso 7 y con ello estaría todo.



### Ejercicio de Propuesta de Cambio

1. Se identifica una mejora o problema a resolver.
   - Puede tratarse de un bug, una mejora, o una nueva funcionalidad detectada.

2. Se crea una nueva issue en GitHub, categorizada por prioridad y tipo.
   - Se asignan etiquetas de prioridad (`critical`, `medium`, `low`) y tipo (`bug`, `enhancement`, etc.) para clasificar el trabajo de forma clara.

3. El trabajo se asigna a un WI si el problema está relacionado con un cambio realizado previamente en ese WI.
   - Por ejemplo, si un bug ocurre debido a algo desarrollado en el WI-2, el fix se asigna al mismo WI.
   - Si no está relacionado con ningún WI, se gestiona como una tarea independiente.

4. Si el fix está relacionado con un WI en desarrollo:
   - El trabajo se realiza dentro de la rama de ese WI correspondiente, manteniendo la relación entre el problema y su solución.
   - Esto asegura que las correcciones relacionadas con un WI en curso se integren directamente en su rama.

5. Si el fix corresponde a algo ya integrado en el repositorio principal:
   - Se crea una nueva rama de tipo `fix` desde la rama relevante del repositorio principal (`develop` o `main`).
   - Esto es necesario para corregir problemas en código ya integrado y validado previamente.

6. Cuando los cambios en la rama `main` de un repositorio de grupo pasan las pruebas automáticas de los workflows:
   - Se genera automáticamente una Pull Request (PR) desde la rama `main` del grupo hacia la rama `develop` del repositorio principal.
   - Esto permite integrar el trabajo del grupo en el repositorio padre de forma controlada.

7. La PR es revisada y fusionada en la rama `develop` del repositorio principal.
   - Otro miembro del equipo revisa el código para garantizar su calidad.
   - Los workflows automáticos verifican la validez del código mediante pruebas adicionales.

8. Una vez validada en la rama `develop`, se promueve a la rama `main` del repositorio principal.
   - Esto marca el paso final antes del despliegue.
   - El despliegue es automático y se realiza directamente desde la rama `main` del repositorio principal.
   
### Conclusiones y trabajo futuro
