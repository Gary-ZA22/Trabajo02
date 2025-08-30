import os
import pandas as pd
from flask import Flask, request, render_template, redirect, url_for, flash
from sqlalchemy import create_engine

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Conexión MySQL
engine = create_engine("mysql+pymysql://root:@localhost/tienda_alpaca_dw")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("No se seleccionó archivo")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("Archivo vacío")
        return redirect(url_for("index"))

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        try:
            df = pd.read_csv(filepath, sep=";")

            # Insertar en tabla existente
            df.to_sql("dim_clientes", con=engine, if_exists="append", index=False)

            flash("✅ Datos cargados correctamente a la base de datos.")
        except Exception as e:
            flash(f" Error al cargar datos: {e}")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
