from flask import Flask, render_template, request, redirect, url_for
from mercado_libre_scrapper import scrape_products
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():

    data = pd.read_excel("resultados/productos.xlsx")
    
    productos = data.to_dict(orient="records")

    data["price"] = data["price"].astype(int)
    promedio = int(data["price"].mean())
    mayor = data["price"].max()
    menor = data["price"].min()

    promedio_fmt = f"{promedio:,}".replace(",", ".")
    mayor_fmt = f"{mayor:,}".replace(",", ".")
    menor_fmt = f"{menor:,}".replace(",", ".")

    columnas = ["image", "title", "price", "stars"]
    df_vacio = pd.DataFrame([[None, None, "0", None]], columns=columnas)
    df_vacio.to_excel("resultados/productos.xlsx", index=False)

    return render_template("index.html", productos=productos,promedio=promedio_fmt,mayor=mayor_fmt,menor=menor_fmt)

@app.route("/link", methods=["POST"])
def linkForm():
    link = request.form["link"]
    scrape_products(link)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
