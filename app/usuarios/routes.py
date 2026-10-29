from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Usuario

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Helper: verificar que el usuario ha iniciado sesión
def requiere_sesion():
    return not session.get('usuario_id')

# Helper: verificar que es administrador
def es_administrador():
    return session.get('es_admin', False)

#  CONSULTA — Listar todos los usuarios
@usuarios_bp.route('/')
def lista():
    if requiere_sesion():
        flash('⚠️ Debes iniciar sesión primero')
        return redirect(url_for('auth.login'))
    
    # Solo administrador puede ver la lista completa
    if not es_administrador():
        flash(' No tienes permiso para ver esta página')
        return redirect(url_for('anuncios.lista'))
    
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return render_template('usuarios/lista.html', usuarios=usuarios)

#  MODIFICAR — Editar usuario
@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if requiere_sesion():
        return redirect(url_for('auth.login'))
    
    usuario = Usuario.query.get_or_404(id)
    
    # Permitir editar solo a sí mismo o al admin
    if usuario.id != session.get('usuario_id') and not es_administrador():
        flash(' No puedes modificar a otros usuarios')
        return redirect(url_for('anuncios.lista'))
    
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        
        # Solo el admin puede cambiar el rol
        if es_administrador():
            usuario.es_admin = 'es_admin' in request.form
        
        db.session.commit()
        flash(f' Usuario "{usuario.nombre}" actualizado correctamente')
        return redirect(url_for('usuarios.lista'))
    
    return render_template('usuarios/editar.html', usuario=usuario)

#  ELIMINAR — Borrar usuario
@usuarios_bp.route('/eliminar/<int:id>')
def eliminar(id):
    if requiere_sesion():
        return redirect(url_for('auth.login'))
    
    if not es_administrador():
        flash(' Solo el administrador puede eliminar usuarios')
        return redirect(url_for('anuncios.lista'))
    
    usuario = Usuario.query.get_or_404(id)
    
    # Evitar que se elimine a sí mismo
    if usuario.id == session.get('usuario_id'):
        flash(' No puedes eliminarte a ti mismo')
        return redirect(url_for('usuarios.lista'))
    
    db.session.delete(usuario)
    db.session.commit()
    flash(f' Usuario "{usuario.nombre}" eliminado')
    return redirect(url_for('usuarios.lista'))