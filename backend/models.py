from . import db

class Cliente(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    telefono = db.Column(db.String)
    ingresos_anuales = db.Column(db.Float)

    hipotecas = db.relationship('Hipoteca', backref='cliente', lazy=True)

class Propiedad(db.Model):
    __tablename__ = 'propiedades'

    id = db.Column(db.Integer, primary_key=True)
    direccion_completa = db.Column(db.String, nullable=False)
    valor_tasacion = db.Column(db.Float, nullable=False)

    hipotecas = db.relationship('Hipoteca', backref='propiedad', lazy=True)

class Hipoteca(db.Model):
    __tablename__ = 'hipotecas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    propiedad_id = db.Column(db.Integer, db.ForeignKey('propiedades.id'), nullable=False)
    monto_principal = db.Column(db.Float, nullable=False)
    tasa_interes_anual = db.Column(db.Float, nullable=False)
    plazo_anos = db.Column(db.Integer, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String, default='Activa')

    pagos = db.relationship('Pago', backref='hipoteca', lazy=True)

class Pago(db.Model):
    __tablename__ = 'pagos'

    id = db.Column(db.Integer, primary_key=True)
    hipoteca_id = db.Column(db.Integer, db.ForeignKey('hipotecas.id'), nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False)
    monto_pagado = db.Column(db.Float, nullable=False)
    capital_amortizado = db.Column(db.Float)
    interes_pagado = db.Column(db.Float)