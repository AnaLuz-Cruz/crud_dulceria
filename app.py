# app.py
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)


db = SQLAlchemy()


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'


# Configuración de la base de datos y otras configuraciones
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dulceria.db'
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar seguimiento de modificaciones

# Inicialización de la base de datos
db.init_app(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta principal para mostrar todos los productos
@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('base.html', productos=productos)

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        imagen = request.files['imagen']

        if imagen and allowed_file(imagen.filename):
            imagen_filename = imagen.filename
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))

            nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, imagen=imagen_filename)
            db.session.add(nuevo_producto)
            db.session.commit()
            flash('Producto agregado exitosamente!', 'success')
            return redirect(url_for('index'))
    return render_template('agregar_producto.html')

# Ruta para actualizar un producto
@app.route('/actualizar/<int:id>', methods=['GET', 'POST'])
def actualizar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            if imagen.filename and allowed_file(imagen.filename):
                imagen_filename = imagen.filename
                imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))
                producto.imagen = imagen_filename
        db.session.commit()
        flash('Producto actualizado exitosamente!', 'success')
        return redirect(url_for('index'))
    return render_template('actualizar_producto.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente!', 'success')
    return redirect(url_for('index'))

# Configuración para crear las tablas si no existen
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear las tablas solo si la app se ejecuta
    app.run(debug=True)
