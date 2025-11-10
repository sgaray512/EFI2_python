from app import app, db
from models import User, UserCredential, Category, Post, Comment
from passlib.hash import bcrypt

def seed_data():
    with app.app_context():
        if User.query.first():
            print("La base de datos ya tiene datos cargados.")
            return

        # USUARIOS
        admin = User(name="Admin User", email="admin@example.com")
        moderator = User(name="Moderator User", email="moderator@example.com")
        user = User(name="Regular User", email="user@example.com")

        db.session.add_all([admin, moderator, user])
        db.session.flush()

        admin_cred = UserCredential(
            user_id=admin.id,
            password_hash=bcrypt.hash("admin123"),
            role="admin",
        )
        mod_cred = UserCredential(
            user_id=moderator.id,
            password_hash=bcrypt.hash("mod123"),
            role="moderator",
        )
        user_cred = UserCredential(
            user_id=user.id,
            password_hash=bcrypt.hash("user123"),
            role="user",
        )

        db.session.add_all([admin_cred, mod_cred, user_cred])

        # CATEGORÍAS
        tech = Category(name="Tecnología")
        travel = Category(name="Viajes")
        food = Category(name="Comida")
        db.session.add_all([tech, travel, food])
        db.session.flush()

        # POSTS
        post1 = Post(
            title="Bienvenidos al MiniBlog",
            content="Primer post de prueba del administrador.",
            user_id=admin.id,
            category_id=tech.id,
        )
        post2 = Post(
            title="Mis viajes favoritos",
            content="Compartiendo experiencias de mis viajes por el mundo.",
            user_id=user.id,
            category_id=travel.id,
        )
        post3 = Post(
            title="Receta de empanadas criollas",
            content="Receta tradicional paso a paso.",
            user_id=moderator.id,
            category_id=food.id,
        )

        db.session.add_all([post1, post2, post3])
        db.session.flush()

        # COMENTARIOS
        com1 = Comment(content="Excelente post!", user_id=user.id, post_id=post1.id)
        com2 = Comment(content="Me encantaron las fotos!", user_id=moderator.id, post_id=post2.id)
        com3 = Comment(content="Muy buena receta", user_id=admin.id, post_id=post3.id)

        db.session.add_all([com1, com2, com3])

        # GUARDAR
        db.session.commit()
        print("Datos de prueba insertados correctamente.")

if __name__ == "__main__":
    seed_data()