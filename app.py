import os

from flask import Flask, flash, redirect, render_template, request, session, url_for

from auth import auth_bp
import database

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

app.register_blueprint(auth_bp)

database.criar_banco()

def usuario_logado():
    return session.get("usuario_id")

def requerer_login():
    if usuario_logado() is None:
        flash("Faça login para continuar.")
        return redirect(url_for("auth.login"))
    return None

@app.route("/")
def index():
    usuario_id = usuario_logado()
    treinos = database.listar_treinos(usuario_id) if usuario_id is not None else []
    return render_template("index.html", treinos=treinos)

@app.route("/treinos/novo", methods=["GET", "POST"])
def novo_treino():
    resposta = requerer_login()
    if resposta is not None:
        return resposta

    if request.method == "POST":
        titulo = request.form["titulo"]
        tipo = request.form["tipo"]
        duracao = int(request.form["duracao"])
        database.criar_treino(titulo, tipo, duracao, usuario_logado())
        flash("Treino cadastrado.")
        return redirect(url_for("index"))

    return render_template("novo_treino.html")

@app.route("/treinos/<int:treino_id>/editar", methods=["GET", "POST"])
def editar_treino(treino_id):
    resposta = requerer_login()
    if resposta is not None:
        return resposta

    treino = database.buscar_treino(treino_id)
    if treino is None:
        return "Treino não encontrado", 404

    if treino["usuario_id"] != usuario_logado():
        return "Acesso negado"

    if request.method == "POST":
        titulo = request.form["titulo"]
        tipo = request.form["tipo"]
        duracao = int(request.form["duracao"])
        database.atualizar_treino(treino_id, titulo, tipo, duracao)
        flash("Treino atualizado.")
        return redirect(url_for("index"))

    return render_template("editar_treino.html", treino=treino)

@app.post("/treinos/<int:treino_id>/concluir")
def concluir_treino(treino_id):
    resposta = requerer_login()
    if resposta is not None:
        return resposta

    treino = database.buscar_treino(treino_id)
    if treino is None:
        return "Treino não encontrado", 404

    if treino["usuario_id"] != usuario_logado():
        return "Acesso negado"

    database.alternar_concluido(treino_id)
    flash("Status do treino atualizado.")
    return redirect(url_for("index"))

@app.post("/treinos/<int:treino_id>/excluir")
def excluir_treino(treino_id):
    resposta = requerer_login()
    if resposta is not None:
        return resposta

    treino = database.buscar_treino(treino_id)
    if treino is None:
        return "Treino não encontrado", 404

    if treino["usuario_id"] != usuario_logado():
        return "Acesso negado"

    database.excluir_treino(treino_id)
    flash("Treino excluído.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)