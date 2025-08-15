import pytest
from backend import create_app

@pytest.fixture(scope='module')
def app():
    app = create_app()
    return app

@pytest.fixture(scope='module')
def client(app):
    with app.test_client() as client:
        yield client

def test_get_hipotecas(client):
    response = client.get('/api/hipotecas')
    assert response.status_code == 200

def test_create_and_get_hipoteca(client):
    # Crear cliente y propiedad de forma directa a la BD para el test
    from backend import _db, models
    with client.application.app_context():
        cliente = models.Cliente(nombre_completo='Juan Perez', email='juan@example.com')
        propiedad = models.Propiedad(direccion_completa='Calle Falsa 123', valor_tasacion=200000)
        _db.session.add(cliente); _db.session.add(propiedad); _db.session.commit()

    payload = {
        'cliente_id': cliente.id,
        'propiedad_id': propiedad.id,
        'monto_principal': 150000,
        'tasa_interes_anual': 5.0,
        'plazo_anos': 30
    }

    response = client.post('/api/hipotecas', json=payload)
    assert response.status_code == 201

    hipoteca_id = response.get_json()['id']

    # Obtener amortización
    response2 = client.get(f'/api/hipotecas/{hipoteca_id}/amortizacion')
    assert response2.status_code == 200
    plan = response2.get_json()
    assert isinstance(plan, list) and len(plan) > 0

def test_registrar_pago(client):
    # Asumimos que ya existe una hipoteca creada en el test anterior
    from backend import _db, models
    with client.application.app_context():
        hipoteca = models.Hipoteca.query.first()

    payload = {
        'monto_pagado': 5000,
        'capital_amortizado': 4000,
        'interes_pagado': 1000
    }

    response = client.post(f'/api/hipotecas/{hipoteca.id}/pagos', json=payload)
    assert response.status_code == 201