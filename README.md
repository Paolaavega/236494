Planificador de Horarios UACJ - Proyecto Integrador
Alumna: Paola Vega Franco
Matrícula: 236494

Este proyecto implementa un algoritmo de Búsqueda en Profundidad (DFS iterativo) para resolver el problema real de la creación de horarios universitarios y la prevención de choques de materias.

Requisitos previos
Python 3.9 o superior.

Tener instalado pip.

Instalación y Ejecución
Clonar el repositorio:


git clone https://github.com/Paolaavega/236494.git
cd 236494

Instalar las dependencias:
Se recomienda crear un entorno virtual, pero no es obligatorio. Para instalar las librerías necesarias ejecuta:

pip install -r requirements.txt
Ejecutar la aplicación:

streamlit run app.py

Uso:
Se abrirá automáticamente una pestaña en tu navegador web.

Sube el archivo PDF oficial de horarios (IIT-2026-febrero-junio.pdf).

Utiliza los filtros laterales para buscar tus materias y agrégalas a tu horario.

Análisis de Complejidad (Big O)
Temporal: O(N), donde N es el número de grupos en el catálogo. El DFS iterativo recorre la lista una sola vez.

Espacial: O(N), debido al almacenamiento de los nodos en la Pila (Stack) y la lista de resultados.