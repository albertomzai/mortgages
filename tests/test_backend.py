import datetime

import pytest

from backend import create_app, db
from backend.models import Cliente, Propiedad, Hipoteca, Pago

@pytest.fixture(scope='module')
 def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        # Crear datos de prueba
        cliente = Cliente(nombre_completo='Juan Pérez', email='juan@example.com', ingresos_anuales=50000)
        propiedad = Propiedad(direccion_completa='Calle Falsa 123', valor_tasacion=200000)
        db.session.add_all([cliente, propiedad])
        db.session.commit()

    yield app

    # Teardown
    with app.app_context():
        db.drop_all()

@pytest.fixture
 def client(app):
    return app.test_client()

def test_get_hipotecas_empty(client, app):
    response = client.get('/api/hipotecas')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_and_list_hipoteca(client, app):
    data = {
        'cliente_id': 1,
        'propiedad_id': 1,
        'monto_principal': 150000.0,
        'tasa_interes_anual': 3.5,
        'plazo_anos': 20,
        'fecha_inicio': datetime.date.today().isoformat(),
    }

    resp = client.post('/api/hipotecas', json=data)
    assert resp.status_code == 201

    get_resp = client.get('/api/hipotecas')
    hipotecas = get_resp.get_json()
    assert len(hipotecas) == 1
    assert hipotecas[0]['cliente_nombre'] == 'Juan Pérez'

def test_amortizacion_plan(client, app):
    # Asumimos que ya existe la hipoteca con id 1
    resp = client.get('/api/hipotecas/1/amortizacion')
    plan = resp.get_json()
    assert len(plan) == 20 * 12, 'Debe haber un mes por cada pago mensual'

def test_registrar_pago(client, app):
    # Registrar un pago que cubre el monto principal
    data = {
        'fecha_pago': datetime.date.today().isoformat(),
        'monto_pagado': 150000.0,
        'capital_amortizado': 150000.0,
        'interes_pagado': 0.0
    }

    resp = client.post('/api/hipotecas/1/pagos', json=data)
    assert resp.status_code == 201

    # Verificar que la hipoteca está marcada como Pagada
    get_resp = client.get('/api/hipotecas')
    hipotecas = get_resp.get_json()
    assert hipotecas[0]['estado'] == 'Pagada'