from flask import render_template, request, redirect, url_for, flash
from main import app, db,bcrypt
from main.models import User,Expense
from main.forms import ExpenseForm,RegisterForm,LoginForm
from flask_login import login_user,logout_user,login_required,current_user
from datetime import datetime, timedelta


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
     hashed_pass=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
     user=User(username=form.username.data,password_hash=hashed_pass)

     db.session.add(user)
     db.session.commit()
     flash(f'Registration successful {form.username.data}! Please log in.', 'success')
     return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
       return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash,form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
         flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ExpenseForm()  # create form

    if form.validate_on_submit():
        expense = Expense(
            title=form.title.data,
            category=form.category.data,
            price=form.price.data,
            quantity=form.quantity.data,
            user_id=current_user.id 
        )
        db.session.add(expense)
        db.session.commit()
        flash('Expense Added!', 'success')
        return redirect(url_for('index'))

    # Filtering expenses
    filter_by = request.args.get('filter', 'all')
    today = datetime.utcnow().date()
    if filter_by == 'day':
        expenses = Expense.query.filter(db.func.date(Expense.date_created) == today).all()
    elif filter_by == 'week':
        start_week = today - timedelta(days=today.weekday())
        expenses = Expense.query.filter(Expense.date_created >= start_week).all()
    elif filter_by == 'month':
        expenses = Expense.query.filter(db.extract('month', Expense.date_created) == today.month).all()
    else:
        expenses = Expense.query.filter_by(user_id=current_user.id).all()

    total_expenses = sum(e.total() for e in expenses)
    categories = {}
    for e in expenses:
        categories[e.category] = categories.get(e.category, 0) + e.total()

    # Pass form to template every time!
    return render_template('index.html',
                           form=form,
                           expenses=expenses,
                           total=total_expenses,
                           categories=categories)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_expense(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        expense.title = request.form['title']
        expense.category = request.form['category']
        expense.price = float(request.form['price'])
        expense.quantity = int(request.form['quantity'])
        db.session.commit()
        flash('Expense Updated Successfully!', 'info')
        return redirect(url_for('index'))
    return render_template('add.html', expense=expense)

@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense Deleted Successfully!', 'danger')
    return redirect(url_for('index'))


