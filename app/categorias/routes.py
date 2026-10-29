from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Categoria

categorias_bp = Blueprint('categorias', __name__, url_prefix='/categorias')

@categorias_bp.route('/')
def lista():
    if not session.get('usuario_id'):
        return redirect(url_for('auth.login'))
    categorias = Categoria.query.all()
    return render_template('categorias/lista.html', categorias=categorias)

@categorias_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if not session.get('usuario_id'):
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        categoria = Categoria(
            nombre=request.form['nombre'],
            descripcion=request.form['descripcion']
        )
        db.session.add(categoria)
        db.session.commit()
        flash(' Categoría creada')
        return redirect(url_for('categorias.lista'))
    return render_template('categorias/crear.html')

#  AQUÍ FALTABA LA RUTA DE EDITAR
@categorias_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if not session.get('usuario_id'):
        return redirect(url_for('auth.login'))
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        categoria.nombre = request.form['nombre']
        categoria.descripcion = request.form['descripcion']
        db.session.commit()
        flash(' Categoría actualizada')
        return redirect(url_for('categorias.lista'))
    return render_template('categorias/editar.html', categoria=categoria)

#  Ruta de eliminar
@categorias_bp.route('/eliminar/<int:id>')
def eliminar(id):
    if not session.get('usuario_id'):
        return redirect(url_for('auth.login'))
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash(' Categoría eliminada')
    return redirect(url_for('categorias.lista'))