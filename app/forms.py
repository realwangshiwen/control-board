from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import (StringField, PasswordField, BooleanField, SubmitField,
                     SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User, Task
from app import usets

import sqlite3
import os

here = os.path.dirname(__file__)


def employees_query(items_to_find=[], **given_values):
    """

    Returns:
        ((...),(...),(...),)
    """
    lst = []
    if not isinstance(items_to_find, list):
        lst.append(items_to_find)
        items_to_find = lst
    find_items = ', '.join(items_to_find) if items_to_find else '*'
    where_stms = ' AND '.join([f"{k}='{v}'" for k, v in given_values.items()])
    if where_stms:
        where_stms = 'where ' + where_stms
    db_path = os.path.abspath(os.path.join(here, '../instance/employees.db'))
    db_czdp = sqlite3.connect(db_path)
    cr = db_czdp.cursor()
    cr.execute(f"SELECT {find_items} FROM employees {where_stms}")
    result = cr.fetchall()
    db_czdp.close()
    return tuple(zip(*result))


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    remember = BooleanField()
    login_submit = SubmitField()


class ConfirmForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email(message='邮箱不合法。')])
    submit = SubmitField()

    def validate_username(self, username):
        users = User.query.all()
        user = User.query.filter_by(username=username.data).first()
        if user not in users:
            raise ValidationError('OA号不存在。')

    def validate_email(self, email):
        if self.email.errors:
            raise ValidationError()
        users = User.query.all()
        user = User.query.filter_by(email=email.data).first()

        if user not in users:
            raise ValidationError('邮箱不存在。')


class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email(message='邮箱不合法。')])
    password = PasswordField(validators=[DataRequired()])
    password2 = PasswordField(
        validators=[DataRequired(), EqualTo('password', message='两次密码输入不一致。')])
    register_submit = SubmitField()
    employees = employees_query(['OA', '电子邮箱', 'Access'])

    def validate_username(self, username):
        if not str(username.data).isdigit():
            raise ValidationError('用户名不合法，请使用OA号。')
        oa = username.data
        if oa not in self.employees[0] or not self.employees[2][self.employees[0].index(oa)]:            
        #     raise ValidationError(f"{oa}可能是外部人员，不允许注册。")
        # else:
        #     access = self.employees[2][self.employees[0].index(oa)]
        #     if not access:
            raise ValidationError(f"{oa}没有权限，请联系管理员。")
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('此OA号已被注册。')

    def validate_email(self, email):
        if self.email.errors:
            raise ValidationError()

        if self.email.data not in self.employees[1]:
            raise ValidationError('请使用正确的公司邮箱。')

        username_id = self.employees[0].index(self.username.data)
        email_id = self.employees[1].index(email.data)
        if username_id != email_id:
            raise ValidationError('OA和邮箱不匹配。')
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已被注册。')

    def clear_errors(self):
        self.username.errors = ()
        self.email.errors = ()
        self.password2.errors = ()


class ResetPasswordFormCold(FlaskForm):
    new_password = PasswordField(validators=[DataRequired()])
    new_password2 = PasswordField(
        validators=[DataRequired(), EqualTo('new_password', message='两次密码输入不一致。')])
    reset_submit = SubmitField()


class ResetPassWordForm(FlaskForm):
    old_password = PasswordField(validators=[DataRequired()])
    new_password = PasswordField(validators=[DataRequired()])
    new_password2 = PasswordField(
        validators=[DataRequired(), EqualTo('new_password', message='两次密码输入不一致。')])
    reset_submit = SubmitField()


class NewTaskForm(FlaskForm):
    uset_bladed = usets[0]    
    taskname = StringField(validators=[DataRequired()])
    bladed = FileField(validators=[FileAllowed(uset_bladed), FileRequired()])
    add_to_git = BooleanField()
    create_submit = SubmitField()
    turbine_platform = SelectField(coerce=str)
    turbine_model = SelectField(coerce=str)
    blade_model = SelectField(coerce=str)
    tower_type = SelectField(coerce=str)
    

class EditTaskForm(FlaskForm):
    uset_bladed = usets[0]
    taskname = StringField(validators=[DataRequired()])
    bladed = FileField(validators=[FileAllowed(uset_bladed)])
    turbine_platform = SelectField(coerce=str)
    turbine_model = SelectField(coerce=str)
    blade_model = SelectField(coerce=str)
    tower_type = SelectField(coerce=str)
    modify_submit = SubmitField()


class DeleteTaskForm(FlaskForm):
    taskname = StringField(validators=[DataRequired()])
    delete_files = BooleanField()
    delete_submit = SubmitField()


class WorkingForm(FlaskForm):
    save_submit = SubmitField()
    download_submit = SubmitField()
