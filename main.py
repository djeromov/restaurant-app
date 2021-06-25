import os

from flask import Flask, render_template, request, redirect, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from gfs_models import User, Restaurant
import gcs_module as GCS

from forms import LoginForm, ChangeMenuForm, NewUserForm, AddImageForm, WhatsappPhoneForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')


#flask-login stuff 
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    return User.get(username)

#puts restaurant variable in all templates so you can use restaurant.whatsapp_phone and restaurant.menu
@app.context_processor
def inject_user():
    return dict(restaurant=Restaurant())

@app.route('/')
def home():
    user_image_urls = GCS.image_urls()
    return render_template('index.html', user_image_urls=user_image_urls)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if '_user_id' in session:
        flash('Ya estas autenticado')
        return redirect('/user')
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if not user:
            flash("Credenciales invalidos")
            return redirect('/login')
            
        # user should be an instance of your `User` class
        login_user(user)

        flash('Entraste la cuenta con éxito')

        return redirect('/dashboard')

    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def user():
    menu_form = ChangeMenuForm(obj=Restaurant())

    if menu_form.validate_on_submit():

        user_input = request.form['menu']
        Restaurant.set_menu(user_input)
        flash('Menu editado con éxito')

        return redirect('/dashboard')

    return render_template('dashboard.html', menu_form=menu_form)


@app.route('/images', methods=['GET', 'POST'])
@login_required
def images():
    #used prefix of img because there is always one hidden blob in buckets, not sure why
    blobs = GCS.user_blobs()

    add_image_form = AddImageForm()
    if add_image_form.validate_on_submit():
        if add_image_form.photo_file.data:
            image_file = request.files['photo_file']
            response = GCS.process_image(image_file)
            if response.ok:
                flash('Imagen subido')
            else:
                flash('Imagen invalido')
            return redirect('/images')


    return render_template('images.html', blobs=blobs, add_image_form=add_image_form)


@app.route('/delete')
@login_required
def delete():
    blob_name = request.args['blob-name']
    GCS.delete_blob(blob_name)
    flash('Imagen eliminado')
    return redirect('/images')


@app.route('/edit-whatsapp-number', methods=['GET', 'POST'])
@login_required
def edit_wa_num():
    #obj parameter is used to prepopulate values in form
    #in this case Restaurant() object has property whatsapp_phone to pull value from
    form = WhatsappPhoneForm(obj=Restaurant())

    if form.validate_on_submit():
        updated_whatsapp_phone = form.whatsapp_phone.data
        Restaurant.set_whatsapp_phone(updated_whatsapp_phone)
        flash('Numero de WhatsApp actualizado')
        return redirect('/dashboard')

    return render_template('edit-wa-num.html', form=form)


@app.route('/users')
@login_required
def users():
    if not current_user.is_admin:
        flash('No esta permitido gestionar usuarios')
        return redirect('/')
    users = User.get_all()
    return render_template('users.html', users=users)

@app.route('/users/create', methods=['GET', 'POST'])
@login_required
def register():
    if not current_user.is_admin:
        flash('No esta permitido crear usuarios')
        return redirect('/')
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        is_admin = form.is_admin.data
        User.register(username, password, is_admin)
        flash('Usuario creado')
        return redirect('/users')
        
    return render_template('create-user.html', form=form)


@app.route('/<username>/delete')
@login_required
def delete_user(username):
    #edge case if a user deletes themselves
    if username == current_user.username:
        flash('No se puede eliminar se mismo')
        return redirect('/users')
    #edge case if a user deletes themselves
    if not current_user.is_admin:
        flash('No esta permitido eliminar usuarios')
        return redirect('/')
    deleted = User.delete(username)
    if deleted:
        flash('Usuario eliminado')
    return redirect('/users')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Saliste de la cuenta')
    return redirect('/')

