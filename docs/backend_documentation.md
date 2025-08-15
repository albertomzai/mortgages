# Visión General del Proyecto

Este proyecto es una API RESTful desarrollada con **Flask** que gestiona la información de clientes, propiedades y hipotecas, así como los pagos asociados a cada préstamo hipotecario. La aplicación utiliza **SQLAlchemy** como ORM para interactuar con una base de datos SQLite (o cualquier otra compatible mediante la variable `DATABASE_URL`). El objetivo principal es permitir:

- Registrar clientes y propiedades.
- Crear hipotecas vinculadas a un cliente y una propiedad.
- Calcular y exponer el plan de amortización mensual de cada hipoteca.
- Registrar pagos, actualizar el estado de la hipoteca cuando se haya pagado por completo.

El frontend (no incluido en este código) sirve como interfaz de usuario para interactuar con los endpoints expuestos. La API está protegida mediante CORS para aceptar peticiones desde cualquier origen bajo `/api/*`.

---

# Arquitectura del Sistema

## Componentes Principales
| Componente | Responsabilidad |
|------------|-----------------|
| **Flask** | Servidor web que maneja las rutas y la lógica de negocio. |
| **SQLAlchemy** | ORM que modela las tablas `clientes`, `propiedades`, `hipotecas` y `pagos`. |
| **Blueprint (`api_bp`)** | Agrupa los endpoints bajo el prefijo `/api`. |
| **CORS** | Permite peticiones cross‑origin para la API. |
| **SQLite / PostgreSQL** | Base de datos relacional (configurable vía `DATABASE_URL`). |

## Diagrama de Flujo

```mermaid
flowchart TD
    A[Cliente] -->|Solicita| B[Flask]
    B --> C{Rutas}
    subgraph Rutas
        C1[/api/hipotecas GET] --> D[Consulta Hipotecas]
        C2[/api/hipotecas POST] --> E[Crea Hipoteca]
        C3[/api/hipotecas/{id}/amortizacion GET] --> F[Calcula Amortización]
        C4[/api/hipotecas/{id}/pagos POST] --> G[Registra Pago]
    end
    D --> H{SQLAlchemy}
    E --> H
    F --> H
    G --> H
    H --> I[Base de Datos]
```

---

# Endpoints de la API

| Método | Ruta | Descripción | Parámetros | Respuesta |
|--------|------|-------------|------------|-----------|
| `GET` | `/api/hipotecas` | Lista todas las hipotecas. | Ninguno | JSON array con `id`, `cliente_nombre`, `propiedad_direccion`, `monto_principal`, `estado`. |
| `POST` | `/api/hipotecas` | Crea una nueva hipoteca. | JSON body: <br>`cliente_id` (int) <br>`propiedad_id` (int) <br>`monto_principal` (float) <br>`tasa_interes_anual` (float) <br>`plazo_anos` (int) <br>`fecha_inicio` (date `YYYY-MM-DD`) | JSON: `{ "id": newId }` con código 201. |
| `GET` | `/api/hipotecas/{id}/amortizacion` | Devuelve el plan de amortización mensual. | `id` (int) en la ruta | JSON array de objetos con `mes`, `cuota_mensual`, `capital`, `interes`, `saldo_restante`. |
| `POST` | `/api/hipotecas/{id}/pagos` | Registra un pago y actualiza estado. | `id` (int) en la ruta <br>JSON body: <br>`fecha_pago` (date) <br>`monto_pagado` (float) <br>`capital_amortizado` (float, opcional) <br>`interes_pagado` (float, opcional) | JSON: `{ "id": pagoId }` con código 201. |

### Ejemplo de Cálculo de Amortización

```python
def calcular_amortizacion(hipoteca):
    # ... implementación mostrada en routes.py ...
```

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tu_usuario/proyecto-hipotecas.git
   cd proyecto-hipotecas
   ```

2. **Crear entorno virtual (opcional pero recomendado)**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno (opcional)**  
   ```bash
   export FLASK_APP=app.py          # o el nombre del archivo que contiene create_app()
   export DATABASE_URL="sqlite:///hipotecas.db"
   ```

5. **Inicializar la base de datos**  
   ```bash
   flask shell
   >>> from app import db, create_app
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   ... 
   ```

6. **Ejecutar el servidor**  
   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```

7. **Acceder a la API**  
   - `GET http://localhost:5000/api/hipotecas`
   - `POST http://localhost:5000/api/hipotecas` (con JSON body)
   - etc.

---

# Flujo de Datos Clave

1. **Creación de Hipoteca**  
   - Cliente envía POST con datos de hipoteca.  
   - Flask valida existencia de cliente y propiedad.  
   - Se crea registro en tabla `hipotecas`.  

2. **Cálculo de Amortización**  
   - Endpoint `/hipotecas/{id}/amortizacion` llama a `calcular_amortizacion`.  
   - Función genera plan mensual usando fórmula de amortización (tasa anual, plazo).  

3. **Registro de Pago**  
   - Cliente envía POST con datos del pago.  
   - Se crea registro en tabla `pagos`.  
   - Se calcula total pagado sumando pagos anteriores + nuevo.  
   - Si el total alcanza o supera el principal y la hipoteca no está marcada como 'Pagada', se actualiza su estado a 'Pagada'.  

4. **Consulta de Hipotecas**  
   - Endpoint `/hipotecas` devuelve lista con datos agregados (nombre cliente, dirección propiedad).  

---

# Extensiones Futuras

| Área | Posible Mejora |
|------|----------------|
| **Autenticación & Autorización** | Implementar JWT o OAuth para proteger endpoints sensibles. |
| **Validaciones Avanzadas** | Añadir reglas de negocio (p.ej., tasa mínima, plazo máximo). |
| **Notificaciones** | Enviar emails al cliente cuando la hipoteca se marque como 'Pagada'. |
| **Exportación de Reportes** | Generar PDFs o CSVs con el plan de amortización y estado de pagos. |
| **Migraciones de Base de Datos** | Integrar Alembic para gestionar cambios en el esquema. |
| **Testing Automatizado** | Añadir pruebas unitarias y de integración con pytest + Flask‑testing. |

---