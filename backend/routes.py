from flask import Blueprint, request, jsonify, abort
from datetime import date

from . import _db
from .models import Cliente, Propiedad, Hipoteca, Pago

api_bp = Blueprint('api', __name__, url_prefix='/api')

# ------------------- Helpers -------------------

def calcular_amortizacion(hipoteca):
    """Calcula el plan de amortización mensual.

    Devuelve una lista de dicts con cuota, capital y interés por mes."""
    P = hipoteca.monto_principal
    r = hipoteca.tasa_interes_anual / 100 / 12
    n = hipoteca.plazo_anos * 12

    if r == 0:
        cuota = P / n
    else:
        cuota = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    amortizacion = []
    saldo = P
    for mes in range(1, n + 1):
        interes = saldo * r
        capital = cuota - interes
        saldo -= capital
        if saldo < 0:
            saldo = 0
        amortizacion.append({
            'mes': mes,
            'cuota_mensual': round(cuota, 2),
            'capital_amortizado': round(capital, 2),
            'interes_pagado': round(interes, 2),
            'saldo_restante': round(saldo, 2)
        })

    return amortizacion

# ------------------- Endpoints -------------------

@api_bp.route('/hipotecas', methods=['GET'])
def get_hipotecas():
    hipotecas = Hipoteca.query.all()
    result = []
    for h in hipotecas:
        result.append({
            'id': h.id,
            'cliente_nombre': h.cliente.nombre_completo if h.cliente else None,
            'propiedad_direccion': h.propiedad.direccion_completa if h.propiedad else None,
            'monto_principal': h.monto_principal,
            'estado': h.estado        })
    return jsonify(result)

@api_bp.route('/hipotecas', methods=['POST'])
def crear_hipoteca():
    data = request.get_json() or {}
    cliente_id = data.get('cliente_id')
    propiedad_id = data.get('propiedad_id')

    cliente = Cliente.query.get(cliente_id)
    propiedad = Propiedad.query.get(propiedad_id)

    if not cliente or not propiedad:
        abort(400, description='Cliente o propiedad no encontrados.')

    hipoteca = Hipoteca(
        cliente_id=cliente.id,
        propiedad_id=propiedad.id,
        monto_principal=data.get('monto_principal', 0),
        tasa_interes_anual=data.get('tasa_interes_anual', 0),
        plazo_anos=data.get('plazo_anos', 0),
        fecha_inicio=date.today(),
        estado='Activa'    )

    _db.session.add(hipoteca)
    _db.session.commit()

    return jsonify({'id': hipoteca.id}), 201

@api_bp.route('/hipotecas/<int:id>/amortizacion', methods=['GET'])
def get_amortizacion(id):
    hipoteca = Hipoteca.query.get_or_404(id)
    plan = calcular_amortizacion(hipoteca)
    return jsonify(plan)

@api_bp.route('/hipotecas/<int:id>/pagos', methods=['POST'])
def registrar_pago(id):
    hipoteca = Hipoteca.query.get_or_404(id)
    data = request.get_json() or {}

    pago = Pago(
        hipoteca_id=hipoteca.id,
        fecha_pago=date.today(),
        monto_pagado=data.get('monto_pagado', 0),
        capital_amortizado=data.get('capital_amortizado'),
        interes_pagado=data.get('interes_pagado')
    )

    _db.session.add(pago)

    # Actualizar estado si el saldo es cero
    plan = calcular_amortizacion(hipoteca)
    if all(item['saldo_restante'] == 0 for item in plan):
        hipoteca.estado = 'Pagada'

    _db.session.commit()

    return jsonify({'id': pago.id}), 201