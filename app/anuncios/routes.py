from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Anuncio, Categoria

anuncios_bp = Blueprint('anuncios', __name__)

@anuncios_bp.route('/')
def lista():
    anuncios = Anuncio.query.order_by(Anuncio.fecha_creacion.desc()).all()
    return render_template('anuncios/lista.html', anuncios=anuncios)

@anuncios_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if not session.get('usuario_id'):
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        anuncio = Anuncio(
            titulo=request.form['titulo'],
            contenido=request.form['contenido'],
            usuario_id=session['usuario_id'],
            categoria_id=request.form['categoria_id']
        )
        db.session.add(anuncio)
        db.session.commit()
        flash(' Anuncio publicado')
        return redirect(url_for('anuncios.lista'))
    
    categorias = Categoria.query.all()
    return render_template('anuncios/crear.html', categorias=categorias)

@anuncios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    anuncio = Anuncio.query.get_or_404(id)
    # Solo autor o admin pueden editar
    if anuncio.usuario_id != session.get('usuario_id') and not session.get('es_admin'):
        flash(' No tienes permiso')
        return redirect(url_for('anuncios.lista'))
    
    if request.method == 'POST':
        anuncio.titulo = request.form['titulo']
        anuncio.contenido = request.form['contenido']
        anuncio.categoria_id = request.form['categoria_id']
        db.session.commit()
        flash(' Anuncio actualizado')
        return redirect(url_for('anuncios.lista'))
    
    categorias = Categoria.query.all()
    return render_template('anuncios/editar.html', anuncio=anuncio, categorias=categorias)

@anuncios_bp.route('/eliminar/<int:id>')
def eliminar(id):
    anuncio = Anuncio.query.get_or_404(id)
    if anuncio.usuario_id != session.get('usuario_id') and not session.get('es_admin'):
        flash(' No tienes permiso')
        return redirect(url_for('anuncios.lista'))
    
    db.session.delete(anuncio)
    db.session.commit()
    flash(' Anuncio eliminado')
    return redirect(url_for('anuncios.lista'))