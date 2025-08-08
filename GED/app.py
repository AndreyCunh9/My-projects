import os
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# Cria a instância do Flask
app = Flask(__name__)

# Define o caminho para o banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "app.db")}'
app.config['SECRET_KEY'] = '123456789'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração para a pasta de uploads
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Cria a instância do SQLAlchemy
db = SQLAlchemy(app)

# Define o modelo User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    sector = db.Column(db.String(150), nullable=True)  # Pode ser NULL para usuários com acesso total
    is_admin = db.Column(db.Boolean, default=False)  # Adiciona flag para acesso total

    def __repr__(self):
        return f'<User {self.username}>'


# Define o modelo Document (para armazenamento dos documentos)
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    filename = db.Column(db.String(150), nullable=False)
    sector = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<Document {self.title}>'

# Função para criar o banco de dados e tabelas
def create_tables():
    with app.app_context():
        print("Criando as tabelas...")
        db.create_all()
        print("Tabelas criadas!")

# Chama a função para criar as tabelas antes do primeiro request
create_tables()

@app.route('/logout')
def logout():
    # Remove o usuário da sessão
    session.pop('username', None)
    # Redireciona para a página de login
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username  # Salva o nome de usuário na sessão
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos')

    return render_template('login.html')

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        sector = request.form.get('sector')
        is_admin = request.form.get('is_admin') == 'on'

        if username and password:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, sector=sector, is_admin=is_admin)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuário adicionado com sucesso!')
            return redirect(url_for('login'))
        else:
            flash('Por favor, preencha todos os campos.')
    return render_template('add_user.html')


from flask import session

@app.route('/dashboard')
def dashboard():
    # Obtém o setor do usuário logado
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    if user and user.is_admin:
        # Administrador vê todos os setores
        sectors = ['AUDITORIA', 'CONTROLADORIA', 'FINANCEIRO', 'MARKETING', 'GENTE E CULTURA', 'DEPARTAMENTO PESSOAL',
                   'CONTABILIDADE', 'FISCAL', 'SUPRIMENTOS', 'COMERCIAL']
    elif user:
        # Usuário normal vê apenas seu setor
        sectors = [user.sector]
    else:
        # Redireciona se o usuário não estiver autenticado
        return redirect(url_for('login'))

    return render_template('dashboard.html', sectors=sectors, user=user)



@app.route('/search_documents', methods=['POST'])
def search_documents():
    title = request.form.get('search_title')
    user = User.query.filter_by(username=session.get('username')).first()

    if title and user:
        # Busca documentos pelo título sem filtrar por setor
        documents = Document.query.filter(Document.title.ilike(f'%{title}%')).all()
        return render_template('search_results.html', documents=documents)
    else:
        flash('Nenhum título fornecido para a busca ou usuário não encontrado.')
        return redirect(url_for('dashboard'))


@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'document_file' not in request.files:
        flash('Nenhum arquivo enviado.')
        return redirect(url_for('dashboard'))

    file = request.files['document_file']
    title = request.form.get('document_title')
    sector = request.form.get('sector')
    username = session.get('username')
    user = User.query.filter_by(username=username).first()

    if file.filename == '' or not title:
        flash('Nenhum arquivo ou título fornecido.')
        return redirect(url_for('dashboard'))

    if not user or (not user.is_admin and user.sector != sector):
        flash('Você não tem permissão para fazer upload neste setor.')
        return redirect(url_for('dashboard'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_document = Document(title=title, filename=filename, sector=sector)
        db.session.add(new_document)
        db.session.commit()
        flash('Documento anexado com sucesso!')
    else:
        flash('Tipo de arquivo não permitido.')

    return redirect(url_for('dashboard'))


@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
