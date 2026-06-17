from flask import Flask, current_app, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from modelo import db
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

from gestorBD import GestorBD
gestor = GestorBD()

@app.route('/')
def inicio():
    return render_template('aviso.html', mensaje="Pagina en construccion", tipo="error-1")


@app.route('/consultarTrabajo', methods = ['GET', 'POST'])
def consultarTrabajo():
    if request.method == 'POST':
        campos = ['id', 'correo']
        if not all([request.form.get(c) for c in campos]):
            resultado = render_template('aviso.html', mensaje="Porfavor llene todos los campos", tipo="error")
        else:
            estado = gestor.consultarEstado(int(request.form.get('id')), request.form.get('correo'))
            if estado:
                resultado = render_template('aviso.html', mensaje=f"El estado del trabajo es: {estado}", tipo="exito")
            else:
                resultado = render_template('aviso.html', mensaje=f"Trabajo no encontrado revise sus datos", tipo="error")
    else:
        resultado = render_template('consultarTrabajo.html')
    return resultado

@app.route('/enviarTrabajo', methods = ['GET', 'POST'])
def enviarTrabajo():
    if request.method =='POST':
        campos = ['titulo', 'resumen', 'area', 'nombreAutor', 'apellidoAutor', 'email']
        if not all([request.form.get(c) for c in campos]):
            resultado = render_template('aviso.html', mensaje="Llene todos los campos...", tipo="error")
        else:
            archivo = request.files.get('archivo')
            if archivo:
                nombre_seguro = secure_filename(archivo.filename)
                archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_seguro))
                idCreado = gestor.registrarTrabajo(request.form.get('titulo'),request.form.get('resumen'),request.form.get('area'),request.form.get('nombreAutor'),request.form.get('apellidoAutor'),request.form.get('email'), nombre_seguro)
                resultado = render_template('aviso.html', mensaje=f"El trabajo ha sido cargado correctamente. Su numero es: {idCreado}", tipo="exito")
            else:
                resultado = render_template('aviso.html', mensaje = "Archivo no cargado", tipo="error")          
    else:
        resultado = render_template('enviarTrabajo.html')
    return resultado

@app.route('/asignar')
def asignar():
    trabajos_pendientes = gestor.getTrabajosPendientes()
    for trabajo in trabajos_pendientes:
        if len(trabajo.asignaciones) < 3:
            faltantes = 3 - len(trabajo.asignaciones)
            areabuscada = trabajo.getArea()
            evaluadores_area = gestor.getEvaluadoresPorArea(areabuscada)
            ya_asignados = [asignado.evaluador_id for asignado in trabajo.asignaciones]
            for evaluador in evaluadores_area:
                if evaluador.id not in ya_asignados and len(evaluador.asignaciones) < evaluador.max_trabajos:
                    gestor.crearAsignacion(trabajo.id, evaluador.id)
                    faltantes -=1
                    if faltantes == 0:
                        break    
    return render_template('aviso.html', mensaje="Asignacion Completada", tipo="exito")

if __name__ == '__main__':
    with app.app_context():
        gestor.crearBD()
        app.run(debug=True)