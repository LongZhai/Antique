from flask import render_template, url_for, flash, redirect, request, session
from flask_package import app, db, bcrypt
from flask_package.forms import LoginForm, InventoryForm, SaleForm, TransactionForm
from flask_package.models import User, Inventory, Sales, Transaction
from flask_login import login_user, current_user, logout_user, login_required
from flask_package import d_analysis
import datetime
import dateutil.relativedelta
import os
from datetime import timedelta
from PIL import Image



@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=40)


@app.route("/inv_display")
@login_required
def inventory_display():
    page = request.args.get('page', 1, type=int)
    inv_record = Inventory.query.order_by(Inventory.id.desc()).paginate(page=page, per_page=25)
    return render_template('inv_record.html', title='西臣-销售记录', inv_record=inv_record)


@app.route("/sale_display")
@login_required
def sale_display():
    page = request.args.get('page', 1, type=int)
    sale_record = Sales.query.order_by(Sales.id.desc()).paginate(page=page, per_page=25)
    return render_template('sale_display.html', title='西臣-销售记录', sales=sale_record)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    # register()
    if current_user.is_authenticated:
        return redirect(url_for('sales'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user_name.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'{form.user_name.data}登陆成功', 'success')
            return redirect(url_for('sales'))
        else:
            flash('密码错误', 'danger')
    return render_template('login.html', title='西臣小店-登陆', form=form)


def register():
    db.drop_all()
    db.create_all()
    hashed_password = bcrypt.generate_password_hash('22888').decode('utf-8')
    user = User(username='xichen', email='xichen@qq.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()


@app.route('/sales', methods=['GET', 'POST'])
@login_required
def sales():
    form = SaleForm()
    if form.validate_on_submit():
        inv_record = Inventory.query.filter_by(item_id=form.item_id.data)
        if inv_record[0].remaining >= int(form.t_num.data):
            profit = int(form.t_price.data) - inv_record[0].u_price * int(form.t_num.data)
            new_sale = Sales(item_id=form.item_id.data, how_many=form.t_num.data, t_price=form.t_price.data,
                             u_price=format(int(form.t_price.data)/int(form.t_num.data), '.2f'),
                             profit=format(profit, '.2f'), date=form.sale_date.data)
            inv_record[0].remaining = inv_record[0].remaining - form.t_num.data
            inv_record[0].revenue = inv_record[0].revenue + int(form.t_price.data)

            db.session.add(new_sale)
            db.session.commit()
            return redirect(url_for('sales'))
        else:
            flash(f'{form.item_id.data} 剩余库存: {inv_record[0].remaining}', 'danger')
    sale_records = Sales.query.order_by(Sales.id.desc()).limit(3)
    return render_template('sales.html', title='西臣-销售登记', form=form, sales=sale_records)


@app.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    form = InventoryForm()
    # item = Inventory.query.filter_by(item_id=form.user_name.data).first()

    # image_file = url_for('static', filename='profile_pics/' + current_user.)

    if form.validate_on_submit():
        picture_file = None
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            #record = Inventory.query.filter_by(item_id=form.item_id.data).first()
        new_record = Inventory(item_id=form.item_id.data, how_many=form.t_num.data, t_price=form.t_price.data, revenue=0-form.t_price.data,
                               image=picture_file,remaining=form.t_num.data,
                               u_price=format(int(form.t_price.data)/int(form.t_num.data),'.2f'), date=form.inv_date.data)
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('inventory'))
    inventory_records = Inventory.query.order_by(Inventory.id.desc()).limit(3)

    return render_template('inventory.html', title='西臣-进货登记', form=form, inventory_records=inventory_records)


def save_picture(form_picture):

    picture_path = os.path.join(app.root_path, 'static/profile_pics', form_picture.filename)
    output_size = (90, 120)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return form_picture.filename


@app.route("/sale_display/<int:sale_id>", methods=['GET', 'POST'])
@login_required
def delete_sale(sale_id):
    sale_record = Sales.query.get_or_404(sale_id)
    inv_record = Inventory.query.filter_by(item_id=sale_record.item_id).first()
    inv_record.revenue = inv_record.revenue - sale_record.t_price
    inv_record.remaining = inv_record.remaining + sale_record.how_many
    db.session.delete(sale_record)
    db.session.commit()
    flash('销售记录已被删除!', 'success')
    return redirect(url_for('sale_display'))


@app.route("/inv_display/<int:inv_id>", methods=['GET', 'POST'])
@login_required
def delete_inv(inv_id):
    try:
        inv_record = Inventory.query.get_or_404(inv_id)
        db.session.delete(inv_record)
        db.session.commit()
    except:
        flash('先删除次批货的销售记录', 'danger')
        return redirect(url_for('inventory_display'))
    flash('进货登记已被删除', 'success')
    return redirect(url_for('inventory_display'))


@app.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(amount=form.amount.data, date=form.trans_date.data,
                                  annotation=form.annotation.data, type=form.type.data)
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('transaction_display'))
    trans = Transaction.query.order_by(Transaction.id.desc()).limit(3)
    return render_template('transaction.html', title='西臣-销售登记', form=form, transactions=trans)


@app.route("/trans_display")
@login_required
def transaction_display():
    transactions = Transaction.query.order_by(Transaction.id.desc())
    return render_template('trans_display.html', title='西臣-转账记录', transactions=transactions)


@app.route("/transaction_display/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_trans(id):
    inv_record = Transaction.query.get_or_404(id)
    db.session.delete(inv_record)
    db.session.commit()
    flash('转账记录已被删除', 'success')
    return redirect(url_for('transaction_display'))


@app.route("/analysis")
@login_required
def data_analysis():
    data_list = {}
    amount = [d_analysis.month_income(6, 0), d_analysis.month_inv_amount(6, 0), d_analysis.t_inv_remaining()]
    data_list['t_investment'] = d_analysis.t_investment()
    data_list['PL'] = d_analysis.PL()
    data_list['t_income'] = d_analysis.t_income()
    data_list['remain_cash'] = d_analysis.remain_cash()
    data_list['operation_cost'] = d_analysis.operation_cost()
    data_list['trans_type_one'] = d_analysis.trans_type_one()

    # page = request.args.get('page', 1, type=int)
    # inv_record = Inventory.query.order_by(Inventory.id.desc()).paginate(page=page, per_page=25)
    return render_template('analysis.html', title='西臣-数据分析', data_list=data_list, amount=amount)


@app.route('/line<chart_type>')
def line(chart_type):
    labels = []
    values = []
    now = datetime.datetime.now()
    for x in range(12):
        if chart_type == 'sales':
            labels.append((now + dateutil.relativedelta.relativedelta(months=-x)).strftime("%m"))
            values.append(d_analysis.month_income(x, x-1))
        else:
            labels.append((now + dateutil.relativedelta.relativedelta(months=-x)).strftime("%m"))
            values.append(d_analysis.month_inv_amount(x, x-1))
        # print(values)
    labels.reverse()
    values.reverse()

    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='近六个月销售额', max=max(values), labels=line_labels,
                           values=line_values)


@app.route("/remaining_display")
@login_required
def remaining_display():
    page = request.args.get('page', 1, type=int)
    inv_record = Inventory.query.filter(Inventory.remaining > 0).order_by(Inventory.id.desc()).paginate(page=page, per_page=25)
    return render_template('inv_record.html', title='西臣-销售记录', inv_record=inv_record)