import os
import requests
import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Usa una variable de entorno

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configuración de la base de datos
db_config = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'control-visita')
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

def get_db_connection():
    """Función para obtener una conexión a la base de datos."""
    try:
        return mysql.connector.connect(**db_config)
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def consultar_dni(dni):
    """Consulta el DNI a través de una API externa."""
    api_url = "https://apiperu.dev/api/dni"
    headers = {
        'Authorization': 'Bearer 1dacc4d91780ee7520e406f731c1bcc513c97938460bd5c475994a7c64ab442f'
    }
    try:
        response = requests.post(api_url, headers=headers, json={'dni': dni})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error al consultar el DNI: {e}")
        return None

def guardar_visitante(visitante_data):
    """Guarda un nuevo visitante en la base de datos."""
    with get_db_connection() as connection:
        if connection is None:
            print("No se pudo conectar a la base de datos para guardar visitante.")
            return None

        cursor = connection.cursor()
        try:
            cursor.execute(
                """INSERT INTO visitantes (dni, nombres, apellido_paterno, apellido_materno, sexo, edad, direccion, placa, playa, destino, tipo_visita)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (visitante_data['dni'], visitante_data['nombres'], visitante_data['apellido_paterno'], 
                 visitante_data['apellido_materno'], visitante_data['sexo'], visitante_data['edad'], 
                 visitante_data['direccion'], visitante_data['placa'], visitante_data['playa'], 
                 visitante_data['destino'], visitante_data['tipo_visita'])
            )
            connection.commit()
            return cursor.lastrowid  # Retorna el ID del visitante registrado
        except mysql.connector.errors.IntegrityError:
            print(f"Error: El DNI {visitante_data['dni']} ya está registrado.")
            return None  # Indica que el DNI ya está registrado
        except Exception as e:
            print(f"Error al guardar visitante: {e}")  # Imprime cualquier otro error
            return None

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/register_visitante', methods=['GET', 'POST'])
@login_required
def register_visitante():
    if request.method == 'POST':
        visitante_data = {
            'dni': request.form['dni'],
            'nombres': request.form['nombres'],
            'apellido_paterno': request.form['apellido_paterno'],
            'apellido_materno': request.form['apellido_materno'],
            'sexo': request.form['sexo'],
            'edad': request.form['edad'],
            'direccion': request.form['direccion'],
            'placa': request.form['placa'],
            'playa': request.form['playa'],
            'destino': request.form['destino'],
            'tipo_visita': request.form['tipo_visita']
        }

        print(f"Datos recibidos: {visitante_data}")

        # Guarda el visitante en la base de datos
        visitante_id = guardar_visitante(visitante_data)

        if visitante_id is None:
            flash('El DNI ya está registrado o hubo un error al registrar.', 'danger')
            return redirect(url_for('register_visitante'))

        flash('Visitante registrado exitosamente.', 'success')
        return redirect(url_for('visitante_detalle', visitante_id=visitante_id))

    return render_template('register_visitante.html')

@app.route('/visitante/<int:visitante_id>')
@login_required
def visitante_detalle(visitante_id):
    with get_db_connection() as connection:
        if connection is None:
            flash('Error al conectar a la base de datos.', 'danger')
            return redirect(url_for('index'))

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM visitantes WHERE id = %s", (visitante_id,))
        visitante = cursor.fetchone()

        if visitante is None:
            flash('Visitante no encontrado', 'danger')
            return redirect(url_for('index'))

    return render_template('visitante_detalle.html', visitante=visitante)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):  # Suponiendo que la contraseña está en la columna 2
            user_obj = User(user[0])  # Suponiendo que el ID está en la columna 0
            login_user(user_obj)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
    
    return render_template('login.html')

@app.route('/recuperar_contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    if request.method == 'POST':
        email = request.form['email']
        flash('Se ha enviado un correo para recuperar la contraseña.', 'success')
        return redirect(url_for('login'))
    
    return render_template('recuperar_contrasena.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        try:
            # Verificar que el usuario no exista
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('El nombre de usuario o el correo electrónico ya están en uso.', 'danger')
                return redirect(url_for('register'))

            # Guardar el nuevo usuario en la base de datos
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", 
                           (username, hashed_password, email))
            conn.commit()

            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))  # Cambia a la ruta de inicio de sesión

        except mysql.connector.Error as err:
            flash(f'Error al conectar a la base de datos: {err}', 'danger')
            return redirect(url_for('register'))

        except Exception as e:
            flash(f'Ocurrió un error inesperado: {e}', 'danger')
            return redirect(url_for('register'))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    return render_template('register.html')

# Ruta de logout
@app.route('/logout')
def logout():
    # Eliminar los datos de sesión del usuario
    session.pop('user_id', None)
    return redirect(url_for('login'))  # Redirige al login o cualquier otra página


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
