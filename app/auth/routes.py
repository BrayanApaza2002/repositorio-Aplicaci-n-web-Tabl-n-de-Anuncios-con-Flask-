from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    # Si ya está logueado, no necesita registrarse
    if session.get('usuario_id'):
        return redirect(url_for('anuncios.lista'))
    
    if request.method == 'POST':
        # Verificar si el correo ya existe
        if Usuario.query.filter_by(correo=request.form['correo']).first():
            flash(' Este correo ya está registrado')
            return redirect(url_for('auth.registro'))
        
        # Crear nuevo usuario
        usuario = Usuario(
            nombre=request.form['nombre'],
            correo=request.form['correo']
        )
        usuario.contrasena = request.form['contrasena']
        
        # El primer usuario será administrador
        if Usuario.query.count() == 0:
            usuario.es_admin = True
        
        db.session.add(usuario)
        db.session.commit()
        
        flash(' Registro exitoso. ¡Ya puedes iniciar sesión!')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('usuario_id'):
        return redirect(url_for('anuncios.lista'))
    
    if request.method == 'POST':
        usuario = Usuario.query.filter_by(correo=request.form['correo']).first()
        
        if usuario and usuario.verificar_contrasena(request.form['contrasena']):
            # Guardar datos en sesión
            session['usuario_id'] = usuario.id
            session['nombre'] = usuario.nombre
            session['es_admin'] = usuario.es_admin
            
            flash(f' Bienvenido, {usuario.nombre}')
            return redirect(url_for('anuncios.lista'))
        else:
            flash(' Correo o contraseña incorrectos')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash(' Sesión cerrada correctamente')
    return redirect(url_for('anuncios.lista'))