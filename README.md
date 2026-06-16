# ETI — Evaluación de Trabajos de Investigación

Aplicación web para la gestión y evaluación de trabajos de investigación del **Congreso Anual de Ecología**. Permite a los autores enviar sus trabajos, a los organizadores gestionar el proceso de asignación de evaluadores, y a los evaluadores registrar sus dictámenes.

---

## Características

- Envío de trabajos de investigación con archivo adjunto
- Consulta de estado de trabajos por parte del autor
- Asignación automática de evaluadores por área de especialidad
- Panel del organizador para consultar estados de trabajos por área
- Bandeja de entrada para evaluadores con trabajos pendientes y evaluados
- Cálculo automático del estado final (Aceptado / Rechazado)

---

## Áreas del Congreso

| Código | Área |
|--------|------|
| AE | Agroecología |
| CA | Comunicación Ambiental |
| EF | Ecofisiología |
| ES | Ecosistemas |
| RN | Recursos Naturales |

---

## Perfiles de Usuario

**Autor** — puede enviar trabajos y consultar su estado.

**Organizador** — puede ejecutar el proceso de asignación de evaluadores y consultar el estado de todos los trabajos.

**Evaluador** — puede ver sus trabajos asignados, descargar los archivos y registrar su valoración y comentarios.

---

## Tecnologías

- Python 3
- Flask
- SQLAlchemy
- SQLite
- Jinja2
- HTML / CSS

---

## Instalación

**1. Cloná el repositorio**
```bash
git clone https://github.com/Luna013/Pagina-ETI.git
cd Pagina-ETI
```

**2. Instalá las dependencias**
```bash
pip install flask flask-sqlalchemy werkzeug
```

**3. Ejecutá la aplicación**
```bash
python app.py
```

**4. Abrí el navegador en**
```
http://127.0.0.1:5000
```

---

## Estructura del Proyecto

```
Pagina-ETI/
├── app.py              # Rutas y lógica principal
├── modelo.py           # Modelos de la base de datos
├── gestorBD.py         # Gestor de operaciones sobre la BD
├── config.py           # Configuración de la aplicación
├── static/
│   └── styles/
│       └── styles.css  # Estilos globales
├── templates/
│   ├── base.html       # Plantilla base
│   ├── enviarTrabajo.html
│   └── aviso.html
└── uploads/            # Archivos subidos por los autores
```

---

## Reglas de Evaluación

- Cada trabajo debe ser evaluado por **3 evaluadores** del mismo área.
- Un evaluador no puede superar su límite máximo de trabajos asignados.
- El estado final se calcula cuando los 3 evaluadores emiten su dictamen:
  - **Aceptado** — las 3 valoraciones son ≥ 70
  - **Rechazado** — al menos una valoración es < 70
