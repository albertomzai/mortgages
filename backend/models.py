from . import _db

class Cliente(_db.Model):
    __tablename__ = 'clientes'

    id = _db.Column(_db.Integer, primary_key=True)
    nombre_completo = _db.Column(_db.String, nullable=False)
    email = _db.Column(_db.String, unique=True)
    telefono = _db.Column(_db.String)
    ingresos_anuales = _db.Column(_db.Float)

    def __repr__(self):
        return f"<Cliente {self.id} - {self.nombre_completo}>"

class Propiedad(_db.Model):
    __tablename__ = 'propiedades'

    id = _db.Column(_db.Integer, primary_key=True)
    direccion_completa = _db.Column(_db.String, nullable=False)
    valor_tasacion = _db.Column(_db.Float, nullable=False)

    def __repr__(self):
        return f"<Propiedad {self.id} - {self.direccion_completa}>"

class Hipoteca(_db.Model):
    __tablename__ = 'hipotecas'

    id = _db.Column(_db.Integer, primary_key=True)
    cliente_id = _db.Column(_db.Integer, _db.ForeignKey('clientes.id'))
    propiedad_id = _db.Column(_db.Integer, _db.ForeignKey('propiedades.id'))
    monto_principal = _db.Column(_db.Float, nullable=False)
    tasa_interes_anual = _db.Column(_db.Float, nullable=False)
    plazo_anos = _db.Column(_db.Integer, nullable=False)
    fecha_inicio = _db.Column(_db.Date, nullable=False)
    estado = _db.Column(_db.String, default='Activa')

    cliente = _db.relationship('Cliente', backref=_db.backref('hipotecas', lazy=True))
    propiedad = _db.relationship('Propiedad', backref=_db.backref('hipotecas', lazy=True))

    def __repr__(self):
        return f"<Hipoteca {self.id} - {self.estado}>"

class Pago(_db.Model):
    __tablename__ = 'pagos'

    id = _db.Column(_db.Integer, primary_key=True)
    hipoteca_id = _db.Column(_db.Integer, _db.ForeignKey('hipotecas.id'))
    fecha_pago = _db.Column(_db.Date, nullable=False)
    monto_pagado = _db.Column(_db.Float, nullable=False)
    capital_amortizado = _db.Column(_db.Float)
    interes_pagado = _db.Column(_db.Float)

    hipoteca = _db.relationship('Hipoteca', backref=_db.backref('pagos', lazy=True))

    def __repr__(self):
        return f"<Pago {self.id} - Hipoteca {self.hipoteca_id}>"