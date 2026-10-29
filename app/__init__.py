from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd_anuncios.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar BD
    db.init_app(app)
    
    # Importar y registrar Blueprints
    from app.auth.routes import auth_bp
    from app.anuncios.routes import anuncios_bp
    from app.categorias.routes import categorias_bp
    from app.usuarios.routes import usuarios_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(anuncios_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(usuarios_bp)
    
    # Página principal por defecto
    @app.route('/')
    def inicio():
        from flask import redirect, url_for
        return redirect(url_for('anuncios.lista'))
    
    # Crear tablas (solo la primera vez)
    with app.app_context():
        db.create_all()
    
    return app