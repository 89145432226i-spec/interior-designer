from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Designer, Project, Document, Room, SpecificationItem
from datetime import datetime
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'interior-designer-secret-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///interior_designer.db')
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
    if file and allowed_file(file.filename):
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
            login_user(designer, remember=True)
            return redirect(url_for('dashboard'))
        flash('Неверный логин или пароль', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        if Designer.query.filter_by(username=username).first():
            flash('Такой логин уже существует', 'error')
            return render_template('login.html', show_register=True)
        designer = Designer(
            username=username, email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name
        )
        db.session.add(designer)
        db.session.commit()
        login_user(designer)
        flash('Аккаунт успешно создан!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html', show_register=True)

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
            client_email=request.form.get('client_email'),
            client_phone=request.form.get('client_phone'),
            address=request.form.get('address'),
            description=request.form.get('description'),
            designer_id=current_user.id
        )
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        if start_date:
            project.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            project.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        db.session.add(project)
        db.session.commit()
        flash('Проект создан!', 'success')
        return redirect(url_for('project_view', project_id=project.id))
    return render_template('new_project.html')

@app.route('/project/<int:project_id>')
@login_required
def project_view(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    rooms = Room.query.filter_by(project_id=project_id).order_by(Room.order).all()
    docs_by_category = {}
    for doc in project.documents:
        if doc.room_id is None:
            if doc.category not in docs_by_category:
                docs_by_category[doc.category] = []
            docs_by_category[doc.category].append(doc)
    spec_items = SpecificationItem.query.filter_by(project_id=project_id).all()
    spec_by_room = {}
    total_sum = 0
    for item in spec_items:
        rn = item.room_name or 'Без комнаты'
        if rn not in spec_by_room:
            spec_by_room[rn] = []
        spec_by_room[rn].append(item)
        total_sum += item.total
    spec_count = len(spec_items)
    progress = project.get_progress()
    return render_template('project.html', project=project, rooms=rooms,
                           docs_by_category=docs_by_category,
                           spec_by_room=spec_by_room, total_sum=total_sum,
                           spec_count=spec_count, progress=progress)

@app.route('/project/<int:project_id>/edit', methods=['POST'])
@login_required
def edit_project(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    project.title = request.form.get('title', project.title)
    project.client_name = request.form.get('client_name', project.client_name)
    project.client_email = request.form.get('client_email', project.client_email)
    project.client_phone = request.form.get('client_phone', project.client_phone)
    project.address = request.form.get('address', project.address)
    project.description = request.form.get('description', project.description)
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    if start_date:
        project.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if end_date:
        project.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    project.updated_at = datetime.utcnow()
    db.session.commit()
    flash('Проект обновлён!', 'success')
    return redirect(url_for('project_view', project_id=project_id))

@app.route('/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    db.session.delete(project)
    db.session.commit()
    flash('Проект удалён', 'info')
    return redirect(url_for('dashboard'))

@app.route('/project/<int:project_id>/stage', methods=['POST'])
@login_required
def update_stage(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    data = request.get_json()
    stage_map = {
        'contract': 'stage_contract', 'planning': 'stage_planning',
        'collages': 'stage_collages', 'visualization': 'stage_visualization',
        'drawings': 'stage_drawings', 'specification': 'stage_specification'
    }
    stage = data.get('stage')
    if stage in stage_map:
        setattr(project, stage_map[stage], data.get('val'))
        project.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'success': True, 'progress': project.get_progress()})
    return jsonify({'success': False}), 400

@app.route('/project/<int:project_id>/upload', methods=['POST'])
@login_required
def upload_document(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Файл не выбран'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Файл не выбран'}), 400
    category = request.form.get('category', 'other')
    description = request.form.get('description', '')
    room_id = request.form.get('room_id')
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
        project.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'success': True,
            'doc': {
                'id': doc.id, 'original_name': doc.original_name,
                'file_type': doc.file_type, 'file_size': doc.file_size,
                'category': doc.category,
                'url': url_for('get_file', project_id=project_id, filename=filename)
            }
        })
    return jsonify({'success': False, 'error': 'Ошибка загрузки'}), 400

@app.route('/project/<int:project_id>/document/<int:doc_id>/delete', methods=['POST'])
@login_required
def delete_document(project_id, doc_id):
    Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    doc = Document.query.filter_by(id=doc_id, project_id=project_id).first_or_404()
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], str(project_id), doc.filename)
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
    Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    data = request.get_json()
    max_order = db.session.query(db.func.max(Room.order)).filter_by(project_id=project_id).scalar() or 0
    room = Room(name=data.get('name'), description=data.get('description', ''),
                project_id=project_id, order=max_order + 1)
    db.session.add(room)
    db.session.commit()
    return jsonify({'success': True, 'room': {'id': room.id, 'name': room.name}})

@app.route('/project/<int:project_id>/room/<int:room_id>/delete', methods=['POST'])
@login_required
def delete_room(project_id, room_id):
    Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    room = Room.query.filter_by(id=room_id, project_id=project_id).first_or_404()
    db.session.delete(room)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/project/<int:project_id>/spec/add', methods=['POST'])
@login_required
def add_spec_item(project_id):
    Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    data = request.get_json()
    item = SpecificationItem(
        project_id=project_id,
        room_name=data.get('room_name', ''),
        category=data.get('category', ''),
        item_name=data.get('item_name', ''),
        article=data.get('article', ''),
        supplier=data.get('supplier', ''),
        quantity=float(data.get('quantity', 1)),
        unit=data.get('unit', 'шт'),
        price=float(data.get('price', 0)),
        comment=data.get('comment', ''),
        status=data.get('status', 'не заказано')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'success': True, 'item': {'id': item.id, 'item_name': item.item_name, 'total': item.total}})

@app.route('/project/<int:project_id>/spec/<int:item_id>/edit', methods=['POST'])
@login_required
def edit_spec_item(project_id, item_id):
    Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    item = SpecificationItem.query.filter_by(id=item_id, project_id=project_id).first_or_404()
    data = request.get_json()
    item.room_name = data.get('room_name', item.room_name)
    item.category = data.get('category', item.category)
    item.item_name = data.get('item_name', item.item_name)
    item.article = data.get('article', item.article)
    item.supplier = data.get('supplier', item.supplier)
    item.quantity = float(data.get('quantity', item.quantity))
    item.unit = data.get('unit', item.unit)
    item.price = float(data.get('price', item.price))
    item.comment = data.get('comment', item.comment)
    item.status = data.get('status', item.status)
    db.session.commit()
    return jsonify({'success': True, 'total': item.total})

@app.route('/project/<int:project_id>/spec/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_spec_item(project_id, item_id):
    Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    item = SpecificationItem.query.filter_by(id=item_id, project_id=project_id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/project/<int:project_id>/client-link')
@login_required
def get_client_link(project_id):
    project = Project.query.filter_by(id=project_id, designer_id=current_user.id).first_or_404()
    client_url = url_for('client_view', token=project.client_token, _external=True)
    return jsonify({'url': client_url})

@app.route('/client/<token>')
def client_view(token):
    project = Project.query.filter_by(client_token=token).first_or_404()
    rooms = Room.query.filter_by(project_id=project.id).order_by(Room.order).all()
    viz_docs_by_room = {}
    for room in rooms:
        room_docs = Document.query.filter_by(room_id=room.id).all()
        if room_docs:
            viz_docs_by_room[room.id] = room_docs
    client_docs = Document.query.filter_by(project_id=project.id, room_id=None).filter(
        Document.category.in_(['contract', 'collages', 'planning'])).all()
    spec_items = SpecificationItem.query.filter_by(project_id=project.id).all()
    spec_by_room = {}
    total_sum = 0
    for item in spec_items:
        rn = item.room_name or 'Без комнаты'
        if rn not in spec_by_room:
            spec_by_room[rn] = []
        spec_by_room[rn].append(item)
        total_sum += item.total
    designer = db.session.get(Designer, project.designer_id)
    return render_template('client_view.html', project=project, rooms=rooms,
                           viz_docs_by_room=viz_docs_by_room, client_docs=client_docs,
                           spec_by_room=spec_by_room, total_sum=total_sum, designer=designer)

@app.route('/room/<int:room_id>/upload', methods=['POST'])
@login_required
def room_upload(room_id):
    room = Room.query.get_or_404(room_id)
    project = Project.query.filter_by(id=room.project_id, designer_id=current_user.id).first_or_404()
    upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(project.id))
    os.makedirs(upload_dir, exist_ok=True)
    images = []
    for f in request.files.getlist('files'):
        ext = f.filename.rsplit('.', 1)[-1].lower() if '.' in f.filename else 'jpg'
        filename = f"{uuid.uuid4().hex}.{ext}"
        f.save(os.path.join(upload_dir, filename))
        doc = Document(
            project_id=project.id,
            room_id=room.id,
            filename=filename,
            original_name=f.filename,
            file_type='image',
            file_size=os.path.getsize(os.path.join(upload_dir, filename)),
            category='visualization'
        )
        db.session.add(doc)
        images.append({'filename': filename})
    db.session.commit()
    return jsonify({'success': True, 'images': images})

@app.route('/doc/<int:doc_id>/delete', methods=['POST'])
@login_required
def delete_doc_short(doc_id):
    doc = Document.query.get_or_404(doc_id)
    project = Project.query.filter_by(id=doc.project_id, designer_id=current_user.id).first_or_404()
    try:
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], str(project.id))
        os.remove(os.path.join(upload_dir, doc.filename))
    except:
        pass
    db.session.delete(doc)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/room/<int:room_id>/delete', methods=['POST'])
@login_required
def delete_room_short(room_id):
    room = Room.query.get_or_404(room_id)
    project = Project.query.filter_by(id=room.project_id, designer_id=current_user.id).first_or_404()
    db.session.delete(room)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/spec/<int:item_id>/edit', methods=['POST'])
@login_required
def edit_spec_short(item_id):
    item = SpecificationItem.query.get_or_404(item_id)
    Project.query.filter_by(id=item.project_id, designer_id=current_user.id).first_or_404()
    data = request.get_json()
    item.room_name = data.get('room_name', item.room_name)
    item.category = data.get('category', item.category)
    item.item_name = data.get('item_name', item.item_name)
    item.article = data.get('article', item.article)
    item.supplier = data.get('supplier', item.supplier)
    item.quantity = data.get('quantity', item.quantity)
    item.unit = data.get('unit', item.unit)
    item.price = data.get('price', item.price)
    item.total = item.quantity * item.price
    item.comment = data.get('comment', item.comment)
    item.status = data.get('status', item.status)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/spec/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_spec_short(item_id):
    item = SpecificationItem.query.get_or_404(item_id)
    Project.query.filter_by(id=item.project_id, designer_id=current_user.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('База данных инициализирована')
    app.run(debug=True, port=5000)
