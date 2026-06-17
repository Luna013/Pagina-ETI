from werkzeug.security import generate_password_hash
from modelo import db, Organizador, Evaluador, Trabajo, Asignacion

class GestorBD:
    def crearBD(self):
        db.create_all()

    def registrarTrabajo(self,tit, res, ar, nombre, apellido, email, arch_nombre):
        nuevoTrabajo = Trabajo(titulo = tit, resumen = res, area = ar, autor_nombre = nombre, autor_apellido = apellido, autor_email = email, archivo_nombre = arch_nombre)
        if not nuevoTrabajo.id:
            db.session.add(nuevoTrabajo)
            db.session.commit()
            idCreada = nuevoTrabajo.getID()
            return idCreada

    def getTrabajosPendientes(self):
        return Trabajo.query.filter_by(estado="Pendiente").all()

    def getEvaluadoresPorArea(self, area):
        return Evaluador.query.filter_by(area=area).all()

    def crearAsignacion(self, trabajoId, evaluadorId):
        nuevoAsignacion = Asignacion(trabajo_id = trabajoId, evaluador_id = evaluadorId)
        if not nuevoAsignacion.id:
            db.session.add(nuevoAsignacion)
            db.session.commit()

    def consultarEstado(self, codigoID, correo):
        trabajo = Trabajo.query.filter_by(id = codigoID, autor_email=correo).first()
        if trabajo:
            return trabajo.getEstado()
        return None