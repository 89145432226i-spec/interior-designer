from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import uuid

db = SQLAlchemy()

class Designer(db.Model, UserMixin):
    __tablename__ = 'designers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project', backref='designer', lazy=True)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    client_name = db.Column(db.String(200), nullable=False)
    client_phone = db.Column(db.String(50))
    client_email = db.Column(db.String(120))
    address = db.Column(db.String(300))
    description = db.Column(db.Text)
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    designer_id = db.Column(db.Integer, db.ForeignKey('designers.id'), nullable=False)
    client_token = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    stage_brief = db.Column(db.Boolean, default=False)
    stage_measurements = db.Column(db.Boolean, default=False)
    stage_concept = db.Column(db.Boolean, default=False)
    stage_planning = db.Column(db.Boolean, default=False)
    stage_drawings = db.Column(db.Boolean, default=False)
    stage_visualization = db.Column(db.Boolean, default=False)
    stage_procurement = db.Column(db.Boolean, default=False)
    stage_completion = db.Column(db.Boolean, default=False)
    documents = db.relationship('Document', backref='project', lazy=True, cascade='all, delete-orphan')
    rooms = db.relationship('Room', backref='project', lazy=True, cascade='all, delete-orphan')
    spec_items = db.relationship('SpecificationItem', backref='project', lazy=True, cascade='all, delete-orphan')

    def get_progress(self):
        stages = [self.stage_brief, self.stage_measurements, self.stage_concept,
                  self.stage_planning, self.stage_drawings, self.stage_visualization,
                  self.stage_procurement, self.stage_completion]
        done = sum(1 for s in stages if s)
        return int(done / len(stages) * 100)

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(300), nullable=False)
    original_name = db.Column(db.String(300), nullable=False)
    file_type = db.Column(db.String(20))
    file_size = db.Column(db.Integer)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    images = db.relationship('Document', backref='room', lazy=True,
                             foreign_keys='Document.room_id')

class SpecificationItem(db.Model):
    __tablename__ = 'specification_items'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    room_name = db.Column(db.String(200))
    category = db.Column(db.String(200))
    item_name = db.Column(db.String(300), nullable=False)
    article = db.Column(db.String(200))
    supplier = db.Column(db.String(200))
    quantity = db.Column(db.Float, default=1)
    unit = db.Column(db.String(20), default='шт')
    price = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    status = db.Column(db.String(50), default='не заказано')
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
