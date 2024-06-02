
import os
from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, send_from_directory, current_app
from app import db
from app.forms import RegistrationForm, LoginForm, ImageUploadForm, RenameFileForm
from app.models import User, Image
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid

main = Blueprint('main', __name__)

# @main.route("/")
# @main.route("/home")
# def home():
#     if current_user.is_authenticated:
#         images = Image.query.filter_by(user_id=current_user.id).all()
#         return render_template('index.html', images=images)
#     return redirect(url_for('main.login'))


@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated:
        images = Image.query.filter_by(user_id=current_user.id).all()
        return render_template('index.html', images=images)
    return redirect(url_for('main.login'))


@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_data = {"email": form.email.data, "password": form.password.data}
        hashed_password = generate_password_hash(user_data['password'])
        user = User(email=user_data['email'], password=hashed_password, active=True)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = ImageUploadForm()
    if form.validate_on_submit():
        file = form.image.data
        if file:
            # Generate a unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(current_user.id))
            os.makedirs(user_folder, exist_ok=True)
            file_path = os.path.join(user_folder, unique_filename)
            file.save(file_path)
            image = Image(file_name=unique_filename, file_path=file_path, owner=current_user)
            db.session.add(image)
            db.session.commit()
            flash('Your image has been uploaded!', 'success')
            return redirect(url_for('main.home'))
    return render_template('upload.html', title='Upload Image', form=form)



@main.route("/image/<int:image_id>/delete", methods=['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    if image.owner != current_user:
        abort(403)
    os.remove(image.file_path)
    db.session.delete(image)
    db.session.commit()
    flash('Your image has been deleted!', 'success')
    return redirect(url_for('main.home'))



@main.route("/image/<int:image_id>/rename", methods=['GET', 'POST'])
@login_required
def rename_image(image_id):
    image = Image.query.get_or_404(image_id)
    if image.owner != current_user:
        abort(403)
    form = RenameFileForm()
    if form.validate_on_submit():
        new_name = secure_filename(form.new_name.data)
        file_name, file_extension = os.path.splitext(image.file_name)
        new_file_name = f"{new_name}{file_extension}"
        user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], str(current_user.id))
        new_file_path = os.path.join(user_folder, new_file_name)
        
        os.rename(image.file_path, new_file_path)
        
        image.file_name = new_file_name
        image.file_path = new_file_path
        db.session.commit()
        flash('Your image has been renamed!', 'success')
        return redirect(url_for('main.home'))
    return render_template('rename.html', title='Rename Image', form=form, image=image)



@main.route("/image/<int:image_id>/download")
@login_required
def download_image(image_id):
    image = Image.query.get_or_404(image_id)
    if image.owner != current_user:
        abort(403)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], image.file_name, as_attachment=True)


@main.route("/delete_account", methods=['POST'])
@login_required
def delete_account():
    user = User.query.get_or_404(current_user.id)
    if user:
        # Delete the user's images
        for image in user.images:
            try:
                os.remove(image.file_path)
            except Exception as e:
                print(f"Error deleting file {image.file_path}: {e}")
            db.session.delete(image)
        
        # Delete the user account
        db.session.delete(user)
        db.session.commit()
        flash('Your account and all associated images have been deleted.', 'info')
        logout_user()
    return redirect(url_for('main.home'))


@main.route("/data")
@login_required
def data_overview():
    print("Accessing data overview")
    users = User.query.all()
    print(f"Users: {users}")
    images = Image.query.all()
    print(f"Images: {images}")
    return render_template('data.html', users=users, images=images)