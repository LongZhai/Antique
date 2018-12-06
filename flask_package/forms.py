from flask_wtf import FlaskForm
import datetime
from flask_package.models import Inventory
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, DecimalField, SelectField
from wtforms.validators import DataRequired, ValidationError


class LoginForm(FlaskForm):
    user_name = StringField("用户名", validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    remember = BooleanField("记住用户")
    submit = SubmitField("登陆")


class InventoryForm(FlaskForm):
    item_id = IntegerField("id", validators=[DataRequired()])
    t_num = IntegerField("件数", validators=[DataRequired()])
    picture = FileField("照片", validators=[FileAllowed(['jpg', 'png'])])
    t_price = IntegerField("总价", validators=[DataRequired()])
    inv_date = DateField("日期", default=datetime.date.today)
    submit = SubmitField("提交")


class SaleForm(FlaskForm):
    item_id = IntegerField("编号", validators=[DataRequired()])
    test = IntegerField()
    t_num = IntegerField("件数", validators=[DataRequired()])
    t_price = IntegerField("总价", validators=[DataRequired()])
    sale_date = DateField("日期", default=datetime.date.today)
    submit = SubmitField("提交")

    def validate_item_id(self, item_id):
        inv_record = Inventory.query.filter_by(item_id=item_id.data).first()
        if inv_record is None:
            raise ValidationError('进货表里没有序号:'+str(item_id.data))


class TransactionForm(FlaskForm):
    annotation = StringField("转款注释", validators=[DataRequired()])
    trans_date = DateField("日期", default=datetime.date.today)
    type = SelectField('支出类型', choices=[(1, '转账/消费'), (2, '运营支出（如房租）')], coerce=int)
    amount = DecimalField("金额", validators=[DataRequired()])
    submit = SubmitField("提交")
