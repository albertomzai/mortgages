import datetime

from flask import Blueprint, request, jsonify, abort
from sqlalchemy.exc import IntegrityError

from . import db
from .models import Cliente, Propiedad, Hipoteca, Pago

api_bp = Blueprint('api', __name__, url_prefix='/api')

def calcular_amortizacion(hipoteca):
    """Calcula el plan de amortización mensual para una hipoteca."""
    P = hipoteca.monto_principal
    r_annual = hipoteca.tasa_interes_anual / 100.0
    n_years = hipoteca.plazo_anos
    n_months = n_years * 12

    if r_annual == 0:
        cuota_mensual = P / n_months
    else:
        r_monthly = r_annual / 12.0
        cuota_mensual = P * (r_monthly * (1 + r_monthly) ** n_months) / ((1 + r_monthly) ** n_months - 1)

    plan = []
    saldo_restante = P
    for mes in range(1, n_months + 1):
        interes_mensual = saldo_restante * (r_annual / 12.0)
        capital = cuota_mensual - interes_mensual
        saldo_restante -= capital

        plan.append({
            'mes': mes,
            'cuota_mensual': round(cuota_mensual, 2),
            'capital': round(capital, 2),
            'interes': round(interes_mensual, 2),
            'saldo_restante': round(max(saldo_restante, 0.0), 2)
        })

    return plan

@api_bp.route('/hipotecas', methods=['GET'])
def get_hipotecas():
    hipotecas = Hipoteca.query.all()
    result = []
    for h in hipotecas:
        result.append({
            'id': h.id,
            'cliente_nombre': h.cliente.nombre_completo,
            'propiedad_direccion': h.propiedad.direccion_completa,
            'monto_principal': h.monto_principal,
            'estado': h.estado
        })
    return jsonify(result)

@api_bp.route('/hipotecas', methods=['POST'])
def crear_hipoteca():
    data = request.get_json() or {}

    cliente_id = data.get('cliente_id')
    propiedad_id = data.get('propiedad_id')

    if not Cliente.query.get(cliente_id) or not Propiedad.query.get(propiedad_id):
        abort(404, description='Cliente o propiedad no encontrada')

    hipoteca = Hipoteca(**data)
    db.session.add(hipoteca)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback(); abort(400, description='Datos inválidos')

    return jsonify({'id': hipoteca.id}), 201

@api_bp.route('/hipotecas/<int:id>/amortizacion', methods=['GET'])
def obtener_amortizacion(id):
    hipoteca = Hipoteca.query.get_or_404(id)
    plan = calcular_amortizacion(hipoteca)
    return jsonify(plan)

@api_bp.route('/hipotecas/<int:id>/pagos', methods=['POST'])
def registrar_pago(id):
    hipoteca = Hipoteca.query.get_or_404(id)
    data = request.get_json() or {}

    pago = Pago(**data, hipoteca_id=id)
    db.session.add(pago)

    # Actualizar estado si la hipoteca está pagada
    total_pagado = sum(p.monto_pagado for p in hipoteca.pagos) + data.get('monto_pagado', 0.0)
    plan_total = calcular_amortizacion(hipoteca)[-1]['saldo_restante']

    if total_pagado >= hipoteca.monto_principal and not hipoteca.estado == 'Pagada':
        hipoteca.estado = 'Pagada'

    db.session.commit()

    return jsonify({'id': pago.id}), 201