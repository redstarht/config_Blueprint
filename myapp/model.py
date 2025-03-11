
from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta
import os


class Accounts(UserMixin, db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, default='', nullable=False)
    display_name = db.Column(db.String(100), default='', nullable=False)
    role = db.Column(db.Integer, default=1, nullable=False)
    # 廃盤flag （0: 現役, 1: 廃止）
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(
        timezone(timedelta(hours=9))))
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(
            timezone(timedelta(hours=9))),
        onupdate=lambda: datetime.now(timezone(timedelta(hours=9)))
    )


class Factory(db.Model):
    __tablename__ = 'factories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sort_order = db.Column(db.Integer, default=500, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    departments = db.relationship('Department', backref='factory', lazy=True)

    # Departmentテーブルのfactory列と双方向リレーション
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'departments': [dept.to_dict() for dept in self.departments],
            'sort_order': self.sort_order,
            'is_deleted': self.is_deleted

        }


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    factory_id = db.Column(db.Integer, db.ForeignKey(
        'factories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sort_order = db.Column(db.Integer, default=500, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    sections = db.relationship('Section', backref='department', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'sections': [sec.to_dict() for sec in self.sections],
            'sort_order': self.sort_order,
            'is_deleted': self.is_deleted
        }


class Section(db.Model):
    __tablename__ = 'sections'
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'departments.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sort_order = db.Column(db.Integer, default=500, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    subsections = db.relationship('Subsection', backref='section', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subsections': [sub.to_dict() for sub in self.subsections],
            'sort_order': self.sort_order,
            'is_deleted': self.is_deleted
        }


class Subsection(db.Model):
    __tablename__ = 'subsections'
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey(
        'sections.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), default='', nullable=False)
    # 順番を管理するカラム（デフォルト値なし、NULL許容）
    sort_order = db.Column(db.Integer, default=500, nullable=True)
    # 廃盤flag （0: 現役, 1: 廃止）
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    # 作成ユーザーID（NULL許容）
    created_by = db.Column(db.Integer,db.ForeignKey('accounts.id'), nullable=True)
    # 更新ユーザーID（NULL許容）
    updated_by = db.Column(db.Integer,db.ForeignKey('accounts.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(
        timezone(timedelta(hours=9))))
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(
            timezone(timedelta(hours=9))),
        onupdate=lambda: datetime.now(timezone(timedelta(hours=9)))
    )

    creator = db.relationship('Accounts',foreign_keys=[created_by],lazy='joined',backref='created_subsection')
    updater = db.relationship('Accounts',foreign_keys=[updated_by],lazy='joined',backref='updated_subsection')
    production_lines = db.relationship('Production_line',backref='subsection',lazy=True)
    employees = db.relationship('Employee',backref='subsection',lazy=True)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'section_id': self.section_id,
            'code': self.code,
            'sort_order': self.sort_order,
            'is_deleted': self.is_deleted,
            'created_by': self.created_by,
            'created_by_username':self.creator.username if self.creator else None,
            'updated_by': self.created_by,
            'updated_by_username':self.updater.username if self.updater else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            'production_lines': [prod_line.to_dict() for prod_line in self.production_lines],
            'employees': [employee.to_dict() for employee in self.employees]
        }


class Production_line(db.Model):
    __tablename__ = 'production_lines'
    id = db.Column(db.Integer, primary_key=True)
    subsection_id = db.Column(db.Integer, db.ForeignKey(
        'subsections.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), default='', nullable=False)
    sort_order = db.Column(db.Integer, default=500, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer,db.ForeignKey('accounts.id'), nullable=True)
    # 更新ユーザーID（NULL許容）
    updated_by = db.Column(db.Integer,db.ForeignKey('accounts.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(
        timezone(timedelta(hours=9))))
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(
            timezone(timedelta(hours=9))),
        onupdate=lambda: datetime.now(timezone(timedelta(hours=9)))
    )
    creator = db.relationship('Accounts',foreign_keys=[created_by],lazy='joined',backref='created_production_lines')
    updater = db.relationship('Accounts',foreign_keys=[updated_by],lazy='joined',backref='updated_production_lines')
    # abnormal_infos = db.relationship('Abnormal_info', backref='production_line', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subsection_id': self.subsection_id,
            'code': self.code,
            'sort_order': self.sort_order,
            'is_deleted': self.is_deleted,
            'created_by': self.created_by,
            'created_by_username':self.creator.username if self.creator else None,
            'updated_by': self.created_by,
            'updated_by_username':self.updater.username if self.updater else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            # 'abnormal_infos': [abnormal_info.to_dict() for abnormal_info in self.abnormal_infos]
        }


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    subsection_id = db.Column(db.Integer, db.ForeignKey(
        'subsections.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), default='', nullable=False)
    position_id = db.Column(db.Integer,nullable=False,default=1)
    sort_order = db.Column(db.Integer, default=500, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.Integer,db.ForeignKey('accounts.id'), nullable=True)
    updated_by = db.Column(db.Integer,db.ForeignKey('accounts.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(
        timezone(timedelta(hours=9))))
    updated_at = db.Column(
        db.DateTime, default=lambda: datetime.now(
            timezone(timedelta(hours=9))),
        onupdate=lambda: datetime.now(timezone(timedelta(hours=9)))
    )
    creator = db.relationship('Accounts',foreign_keys=[created_by],lazy='joined',backref='created_employee')
    updater = db.relationship('Accounts',foreign_keys=[updated_by],lazy='joined',backref='updated_employee')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subsection_id': self.subsection_id,
            'code': self.code,
            'position':self.position,
            'sort_order': self.sort_order,
            'is_deleted': self.is_deleted,
            'created_by': self.created_by,
            'created_by_username':self.creator.username if self.creator else None,            
            'updated_by': self.created_by,
            'updated_by_username':self.updater.username if self.updater else None,            
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
# class Abnormal_info(db.Model):
#     __tablename__ = 'abnormal_infos'
#     id = db.Column(db.Integer, primary_key=True)
#     subsection_id = db.Column(db.Integer, db.ForeignKey(
#         'subsections.id'), nullable=False)
#     name = db.Column(db.String(100), nullable=False)
#     code = db.Column(db.String(50), default='', nullable=False)
#     position = db.Column(db.Integer,nullable=False,default=1)
#     sort_order = db.Column(db.Integer, default=500, nullable=True)
#     is_deleted = db.Column(db.Boolean, default=False, nullable=False)
#     created_by = db.Column(db.Integer,db.ForeignKey('accounts.id'), nullable=True)
#     updated_by = db.Column(db.Integer,db.ForeignKey('accounts.id'), nullable=True)
#     created_at = db.Column(db.DateTime, default=lambda: datetime.now(
#         timezone(timedelta(hours=9))))
#     updated_at = db.Column(
#         db.DateTime, default=lambda: datetime.now(
#             timezone(timedelta(hours=9))),
#         onupdate=lambda: datetime.now(timezone(timedelta(hours=9)))
#     )
#     creator = db.relationship('Accounts',foreign_keys=[created_by],lazy='joined',backref='created_abnormal_info')
#     updater = db.relationship('Accounts',foreign_keys=[updated_by],lazy='joined',backref='updated_abnormal_info')

#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'subsection_id': self.subsection_id,
#             'code': self.code,
#             'position':self.position,
#             'sort_order': self.sort_order,
#             'is_deleted': self.is_deleted,
#             'created_by': self.created_by,
#             'created_by_username':self.creator.username if self.creator else None,            
#             'updated_by': self.created_by,
#             'updated_by_username':self.updater.username if self.updater else None,            
#             'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
#             'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
#         }    
