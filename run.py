from app import create_app, db
from app.models import Usuario

app = create_app()

with app.app_context():
    # Crear un administrador si no existe
    if not Usuario.query.filter_by(correo="admin@test.com").first():
        admin = Usuario(
            nombre="Administrador",
            correo="admin@test.com",
            es_admin=True
        )
        admin.contrasena = "admin123"
        db.session.add(admin)
        db.session.commit()
        print(" Usuario administrador creado: admin@test.com / admin123")

if __name__ == '__main__':
    app.run(debug=True)