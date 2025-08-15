# Visión General del Proyecto

El proyecto es una **aplicación web de gestión de hipotecas** que combina un backend construido con Flask y SQLAlchemy, y un frontend sencillo en HTML/Bootstrap. Su objetivo principal es permitir a los usuarios registrar clientes, propiedades y hipotecas, calcular planes de amortización y registrar pagos.

- **Backend**: Exposes REST endpoints bajo `/api`. Gestiona la persistencia con una base de datos SQLite (configurable vía `DATABASE_URL`). Utiliza CORS para aceptar peticiones desde cualquier origen.
- **Frontend**: Un único archivo `index.html` que consume los endpoints del backend, mostrando un dashboard y modales para crear hipotecas y registrar pagos. No depende de frameworks JS modernos; todo está en vanilla JavaScript.
- **Pruebas**: Tests con Pytest verifican la creación de hipotecas, el cálculo de amortización y el registro de pagos.

---

# Arquitectura del Sistema

La arquitectura sigue un patrón clásico *MVC* simplificado:

| Capa | Responsabilidad |
|------|-----------------|
| **Modelo (backend/models.py)** | Define las entidades `Cliente`, `Propiedad`, `Hipoteca` y `Pago` con relaciones ORM. |
| **Controlador / Rutas (backend/routes.py)** | Implementa la lógica de negocio: CRUD de hipotecas, cálculo de amortización y actualización del estado tras pagos. |
| **Vista (frontend/index.html + JS)** | Interfaz de usuario que consume los endpoints REST y renderiza tablas y modales. |

## Diagrama Mermaid

```mermaid
graph TD
    A[Cliente] -->|1:N| B[Hipoteca]
    C[Propiedad] -->|1:N| B
    B -->|1:N| D[Pago]

    subgraph Backend
        E[Flask App] --> F[Rutas API]
        F --> G[SQLAlchemy DB]
    end

    subgraph Frontend
        H[Browser] --> I[HTML/JS]
        I --> J[Fetch API] --> F
    end
```

---

# Endpoints de la API

| Método | Ruta | Descripción | Parámetros | Respuesta |
|--------|------|-------------|------------|-----------|
| **GET** | `/api/hipotecas` | Lista todas las hipotecas. | N/A | `[{id, cliente_nombre, propiedad_direccion, monto_principal, estado}]` |
| **POST** | `/api/hipotecas` | Crea una nueva hipoteca. | JSON: `cliente_id`, `propiedad_id`, `monto_principal`, `tasa_interes_anual`, `plazo_anos`, `fecha_inicio` | `{id}` (201) |
| **GET** | `/api/hipotecas/<int:id>/amortizacion` | Devuelve el plan de amortización mensual. | N/A | `[{mes, cuota_mensual, capital, interes, saldo_restante}]` |
| **POST** | `/api/hipotecas/<int:id>/pagos` | Registra un pago y actualiza estado si está pagada. | JSON: `fecha_pago`, `monto_pagado`, `capital_amortizado`, `interes_pagado` | `{id}` (201) |

> **Nota:** Todos los endpoints están protegidos por CORS y aceptan/retornan JSON.

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone <url_del_repositorio>
   cd <directorio_del_proyecto>
   ```

2. **Crear entorno virtual (opcional pero recomendado)**  
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos (opcional)**  
   Por defecto usa SQLite (`hipotecas.db`). Para usar otra BD, exportar `DATABASE_URL`:  
   ```bash
   export DATABASE_URL=postgresql://user:pass@localhost/dbname  # Linux/macOS
   set DATABASE_URL=postgresql://user:pass@localhost/dbname     # Windows CMD
   ```

5. **Inicializar la base de datos** (solo la primera vez)  
   ```bash
   python -c "from backend import create_app, db; app=create_app(); with app.app_context(): db.create_all()"
   ```

6. **Ejecutar el servidor Flask**  
   ```bash
   flask run  # o: python -m backend
   ```
   La aplicación estará disponible en `http://127.0.0.1:5000/`.

7. **Ejecutar pruebas unitarias**  
   ```bash
   pytest tests/test_backend.py
   ```

---

# Flujo de Datos Clave

```mermaid
sequenceDiagram
    participant U as Usuario
    participant B as Browser
    participant F as Flask API
    participant D as Database

    U->>B: Accede a / (frontend)
    B->>F: GET /api/hipotecas
    F->>D: SELECT * FROM hipotecas
    D-->>F: Hipoteca list
    F-->>B: JSON hipotecas
    B->>U: Renderiza tabla

    U->>B: Click "Crear Nueva Hipoteca"
    B->>U: Modal con formulario
    U->>B: Submit POST /api/hipotecas
    B->>D: INSERT INTO hipotecas (...)
    D-->>B: Acknowledgment (id)
    B-->>U: Cierra modal, refresca tabla

    U->>B: Click fila hipoteca → detalle
    B->>F: GET /api/hipotecas/<id>/amortizacion
    F->>D: SELECT pagos y cálculo interno
    D-->>F: Plan de amortización
    F-->>B: JSON plan
    B->>U: Renderiza tabla de amortización + botón "Registrar Pago"

    U->>B: Click "Registrar Pago"
    B->>U: Modal con formulario
    U->>B: Submit POST /api/hipotecas/<id>/pagos
    B->>D: INSERT INTO pagos (...)
    B->>F: Recalcula estado (si pagada)
    D-->>B: Acknowledgment (pago id)
    F-->>B: Actualiza hipoteca.estado si necesario
    B-->>U: Cierra modal, refresca vista
```

---

# Extensiones Futuras

| Área | Posible Mejora |
|------|----------------|
| **Autenticación** | Añadir JWT o OAuth para proteger endpoints y limitar acceso a usuarios autenticados. |
| **Frontend SPA** | Migrar a React/Vue/Angular para una experiencia más dinámica y componentes reutilizables. |
| **Notificaciones** | Enviar correos electrónicos cuando se registre un pago o la hipoteca esté próxima a vencer. |
| **Exportación de Reportes** | Generar PDFs o CSVs con el plan de amortización completo. |
| **Persistencia en Cloud** | Configurar PostgreSQL/AWS RDS como base de datos por defecto, con migraciones (Alembic). |
| **CI/CD** | Integrar pipelines de GitHub Actions para pruebas automáticas y despliegue a Heroku/Render. |

---