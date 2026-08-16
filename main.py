from flask import Flask, render_template,request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key="mister_beast"

#configuracion de la base de datos
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///dataset.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    birthdate = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    notas = db.relationship("Nota", backref="usuario",  lazy=True)

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    texto = db.Column(db.String(1000), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)


@app.route("/")
def hello_world():
    return render_template("login.html")



@app.route("/register")
def about():
    return render_template("register.html")

@app.route("/recibir_datos", methods=["POST"])
def registro():
    correo = request.form.get("email")
    password = request.form.get("password")
    nacimiento = request.form.get("birthdate")
    pais = request.form.get("country")
    new_user=Usuario(correo=correo,password=password,birthdate=nacimiento,country=pais)

    db.session.add(new_user)
    db.session.commit()


    return f"""
    Registro con éxito.<br>
    Correo: {correo}<br>
    Contraseña: {password}<br>
    Fecha de nacimiento: {nacimiento}<br>
    País: {pais}
    """

@app.route("/login", methods=["POST"])
def login():
    correo = request.form.get("email")
    password = request.form.get("password")

    usuario_db = Usuario.query.filter_by(correo=correo).first()

    if usuario_db and usuario_db.password==password:
        session["usuario_id"]=usuario_db.id
        return "Bienvenido"
    else:
        return "Correo o contraseña incorrectos"


if __name__ == "__main__":
    app.run(debug=True)