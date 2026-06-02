from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Designer, Project, Document, Room, SpecificationItem
from datetime import datetime
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'interior-designer-secret-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interior_designer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'dwg', 'dxf', 'zip', 'rar'}

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите в систему'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Designer, int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    if ext in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
        return 'image'
    elif ext == 'pdf':
        return 'pdf'
    elif ext in ['doc', 'docx']:
        return 'word'
    elif ext in ['xls', 'xlsx']:
        return 'excel'
    elif ext in ['dwg', 'dxf']:
        return 'cad'
    return 'file'

def save_file(file, project_id):
    if file and file.filename and allowed_file(file.filename):
        original_name = file.filename
        ext = original_name.rsplit('.', 1)[1].lower()
        unique_filename = uuid.uuid4().hex + '.' + ext
        project_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(project_id))
        os.makedirs(project_folder, exist_ok=True)
        filepath = os.path.join(project_folder, unique_filename)
        file.save(filepath)
        return unique_filename, original_name, get_file_type(original_name), os.path.getsize(filepath)
    return None, None, None, None

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        designer = Designer.query.filter_by(username=username).first()
        if designer and check_password_hash(designer.password_hash, password):
            login_user(designer)
            return redirect(url_for('dashboard'))
        flash('Неверный логин или пароль')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        if Designer.query.filter_by(username=username).first():
            flash('Пользователь уже существует')
            return render_template('register.html')
        designer = Designer(
            username=username, email=email, full_name=full_name,
            password_hash=generate_password_hash(password)
        )
        db.session.add(designer)
        db.session.commit()
        login_user(designer)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(designer_id=current_user.id).order_by(Project.updated_at.desc()).all()
    return render_template('dashboard.html', projects=projects)

@app.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    if request.method == 'POST':
        project = Project(
            title=request.form.get('title'),
            client_name=request.form.get('client_name'),
            client_phone=request.form.get('client_phone'),
            client_email=request.form.get('client_email'),
            address=request.form.get('address'),
            description=request.form.get('description'),
            start_date=request.form.get('start_date'),
            end_date=request.form.get('end_date'),
            designer_id=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('project_detail', project_id=project.id))
    return render_template('new_project.html')

@app.route('/project/<int:project_id>')
@login_required
def project_detail(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    docs = Document.query.filter_by(project_id=project_id, room_id=None).all()
    docs_by_category = {}
    for doc in docs:
        docs_by_category.setdefault(doc.category, []).append(doc)
    rooms = Room.query.filter_by(project_id=project_id).all()
    spec_items = SpecificationItem.query.filter_by(project_id=project_id).order_by(SpecificationItem.room_name).all()
    spec_by_room = {}
    for item in spec_items:
        spec_by_room.setdefault(item.room_name or 'Без комнаты', []).append(item)
    total_sum = sum(item.total for item in spec_items)
    return render_template('project.html', project=project, docs_by_category=docs_by_category,
                           rooms=rooms, spec_by_room=spec_by_room, total_sum=total_sum)

@app.route('/project/<int:project_id>/edit', methods=['POST'])
@login_required
def edit_project(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    project.title = request.form.get('title')
    project.client_name = request.form.get('client_name')
    project.client_phone = request.form.get('client_phone')
    project.client_email = request.form.get('client_email')
    project.address = request.form.get('address')
    project.description = request.form.get('description')
    project.start_date = request.form.get('start_date')
    project.end_date = request.form.get('end_date')
    project.updated_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('project_detail', project_id=project_id))

@app.route('/project/<int:project_id>/stage', methods=['POST'])
@login_required
def update_stage(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    data = request.get_json()
    stage = data.get('stage')
    value = data.get('value')
    stage_map = {
        'brief': 'stage_brief', 'measurements': 'stage_measurements',
        'concept': 'stage_concept', 'planning': 'stage_planning',
        'drawings': 'stage_drawings', 'visualization': 'stage_visualization',
        'procurement': 'stage_procurement', 'completion': 'stage_completion'
    }
    if stage in stage_map:
        setattr(project, stage_map[stage], value)
        project.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'progress': project.get_progress()})
    return jsonify({'success': False}), 400

@app.route('/project/<int:project_id>/upload', methods=['POST'])
@login_required
def upload_document(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return jsonify({'success': False, 'error': 'Файл не выбран'}), 400
    category = request.form.get('category', 'other')
    description = request.form.get('description', '')
    room_id = request.form.get('room_id')
    docs_created = []
    for file in files:
        filename, original_name, file_type, file_size = save_file(file, project_id)
        if filename:
            doc = Document(
                filename=filename, original_name=original_name,
                file_type=file_type, file_size=file_size,
                category=category, description=description,
                project_id=project_id,
                room_id=int(room_id) if room_id else None
            )
            db.session.add(doc)
            docs_created.append(doc)
    if docs_created:
        project.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'docs': [
            {
                'id': d.id,
                'original_name': d.original_name,
                'file_type': d.file_type,
                'file_size': d.file_size,
                'category': d.category,
                'filename': d.filename
            } for d in docs_created
        ]})
    return jsonify({'success': False, 'error': 'Ошибка загрузки'}), 400

@app.route('/doc/<int:doc_id>/delete', methods=['POST'])
@login_required
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    project = Project.query.filter_by(id=doc.project_id, designer_id=current_user.id).first_or_404()
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], str(project.id), doc.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(doc)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/uploads/<int:project_id>/<filename>')
def get_file(project_id, filename):
    folder = os.path.join(app.config['UPLOAD_FOLDER'], str(project_id))
    return send_from_directory(folder, filename)

@app.route('/project/<int:project_id>/room/add', methods=['POST'])
@login_required
def add_room(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'success': False, 'error': 'Название обязательно'}), 400
    room = Room(name=name, project_id=project_id)
    db.session.add(room)
    db.session.commit()
    return jsonify({'success': True, 'room': {'id': room.id, 'name': room.name}})

@app.route('/room/<int:room_id>/delete', methods=['POST'])
@login_required
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    Project.query.filter_by(id=room.project_id, designer_id=current_user.id).first_or_404()
    db.session.delete(room)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/room/<int:room_id>/upload', methods=['POST'])
@login_required
def room_upload(room_id):
    room = Room.query.get_or_404(room_id)
    project = Project.query.filter_by(id=room.project_id, designer_id=current_user.id).first_or_404()
    files = request.files.getlist('file')
    if not files or files[0].filename == '':
        return jsonify({'success': False, 'error': 'Файл не выбран'}), 400
    imgs_created = []
    for file in files:
        filename, original_name, file_type, file_size = save_file(file, project.id)
        if filename:
            doc = Document(
                filename=filename, original_name=original_name,
                file_type='image', file_size=file_size,
                category='visualization', description='',
                project_id=project.id, room_id=room_id
            )
            db.session.add(doc)
            imgs_created.append(doc)
    if imgs_created:
        project.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'images': [
            {'id': d.id, 'filename': d.filename} for d in imgs_created
        ]})
    return jsonify({'success': False, 'error': 'Ошибка загрузки'}), 400

@app.route('/project/<int:project_id>/client-link')
@login_required
def client_link(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    link = url_for('client_view', token=project.client_token, _external=True)
    return jsonify({'link': link})

@app.route('/client/<token>')
def client_view(token):
    project = Project.query.filter_by(client_token=token).first_or_404()
    rooms = Room.query.filter_by(project_id=project.id).all()
    docs = Document.query.filter_by(project_id=project.id, room_id=None).all()
    docs_by_category = {}
    for doc in docs:
        docs_by_category.setdefault(doc.category, []).append(doc)
    spec_items = SpecificationItem.query.filter_by(project_id=project.id).order_by(SpecificationItem.room_name).all()
    spec_by_room = {}
    for item in spec_items:
        spec_by_room.setdefault(item.room_name or 'Без комнаты', []).append(item)
    total_sum = sum(item.total for item in spec_items)
    return render_template('client_view.html', project=project, rooms=rooms,
                           docs_by_category=docs_by_category,
                           spec_by_room=spec_by_room, total_sum=total_sum)

@app.route('/project/<int:project_id>/spec/add', methods=['POST'])
@login_required
def add_spec(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    data = request.get_json()
    qty = float(data.get('quantity', 1))
    price = float(data.get('price', 0))
    item = SpecificationItem(
        project_id=project_id,
        room_name=data.get('room_name', ''),
        category=data.get('category', ''),
        item_name=data.get('item_name', ''),
        article=data.get('article', ''),
        supplier=data.get('supplier', ''),
        quantity=qty, unit=data.get('unit', 'шт'),
        price=price, total=qty * price,
        status=data.get('status', 'не заказано'),
        comment=data.get('comment', '')
    )
    db.session.add(item)
    project.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True, 'item': {
        'id': item.id, 'room_name': item.room_name, 'category': item.category,
        'item_name': item.item_name, 'article': item.article, 'supplier': item.supplier,
        'quantity': item.quantity, 'unit': item.unit, 'price': item.price,
        'total': item.total, 'status': item.status, 'comment': item.comment
    }})

@app.route('/spec/<int:item_id>/edit', methods=['POST'])
@login_required
def edit_spec(item_id):
    item = SpecificationItem.query.get_or_404(item_id)
    Project.query.filter_by(id=item.project_id, designer_id=current_user.id).first_or_404()
    data = request.get_json()
    qty = float(data.get('quantity', 1))
    price = float(data.get('price', 0))
    item.room_name = data.get('room_name', '')
    item.category = data.get('category', '')
    item.item_name = data.get('item_name', '')
    item.article = data.get('article', '')
    item.supplier = data.get('supplier', '')
    item.quantity = qty
    item.unit = data.get('unit', 'шт')
    item.price = price
    item.total = qty * price
    item.status = data.get('status', 'не заказано')
    item.comment = data.get('comment', '')
    db.session.commit()
    return jsonify({'success': True, 'item': {
        'id': item.id, 'room_name': item.room_name, 'category': item.category,
        'item_name': item.item_name, 'article': item.article, 'supplier': item.supplier,
        'quantity': item.quantity, 'unit': item.unit, 'price': item.price,
        'total': item.total, 'status': item.status, 'comment': item.comment
    }})

@app.route('/spec/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_spec(item_id):
    item = SpecificationItem.query.get_or_404(item_id)
    Project.query.filter_by(id=item.project_id, designer_id=current_user.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('База данных инициализирована')
    app.run(debug=True)
