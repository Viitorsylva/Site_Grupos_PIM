from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Inicializar banco
def init_db():
    conn = sqlite3.connect("grupos.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS grupos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_projeto TEXT NOT NULL,
                    descricao TEXT,
                    integrantes TEXT,
                    sala INTEGER,
                    status_grupo TEXT,
                    telefone TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    busca = ""
    conn = sqlite3.connect("grupos.db")
    c = conn.cursor()
    if request.method == "POST":
        busca = request.form["busca"]
        c.execute("SELECT * FROM grupos WHERE nome_projeto LIKE ?", ('%' + busca + '%',))
    else:
        c.execute("SELECT * FROM grupos")
    grupos = c.fetchall()
    conn.close()
    return render_template("index.html", grupos=grupos, busca=busca)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome_projeto"]
        descricao = request.form["descricao"]
        integrantes = [request.form.get(f"integrante{i}") for i in range(1,8)]
        integrantes = ", ".join([i for i in integrantes if i])  # até 7 integrantes
        sala = request.form["sala"]
        status = request.form["status_grupo"]
        telefone = request.form["telefone"]

        conn = sqlite3.connect("grupos.db")
        c = conn.cursor()
        c.execute("INSERT INTO grupos (nome_projeto, descricao, integrantes, sala, status_grupo, telefone) VALUES (?, ?, ?, ?, ?, ?)",
                  (nome, descricao, integrantes, sala, status, telefone))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("cadastrar.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = sqlite3.connect("grupos.db")
    c = conn.cursor()
    if request.method == "POST":
        nome = request.form["nome_projeto"]
        descricao = request.form["descricao"]
        integrantes = [request.form.get(f"integrante{i}") for i in range(1,8)]
        integrantes = ", ".join([i for i in integrantes if i])
        sala = request.form["sala"]
        status = request.form["status_grupo"]
        telefone = request.form["telefone"]

        c.execute("UPDATE grupos SET nome_projeto=?, descricao=?, integrantes=?, sala=?, status_grupo=?, telefone=? WHERE id=?",
                  (nome, descricao, integrantes, sala, status, telefone, id))
        conn.commit()
        conn.close()
        return redirect("/")
    else:
        c.execute("SELECT * FROM grupos WHERE id=?", (id,))
        grupo = c.fetchone()
        conn.close()
        return render_template("editar.html", grupo=grupo)

@app.route("/excluir/<int:id>")
def excluir(id):
    conn = sqlite3.connect("grupos.db")
    c = conn.cursor()
    c.execute("DELETE FROM grupos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
