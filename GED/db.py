from app import db, User, create_app
from werkzeug.security import generate_password_hash

# Crie a aplicação Flask
app = create_app()

# Inicie o contexto da aplicação
with app.app_context():
    # Gere a senha hasheada
    hashed_password = generate_password_hash('minhasenha', method='pbkdf2:sha256')
    novo_usuario = User(username='meuusuario', password=hashed_password)

    # Adicione o novo usuário ao banco de dados
    db.session.add(novo_usuario)
    db.session.commit()

    print("Usuário criado com sucesso!")
