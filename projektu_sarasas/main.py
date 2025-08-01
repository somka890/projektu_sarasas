from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projektai.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


class Projektas(db.Model):
    __tablename__ = 'projektas'

    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column(db.String(100), nullable=False)
    kaina = db.Column(db.Float, nullable=False)
    sukurimo_data = db.Column(db.DateTime, default=datetime.datetime.now)

    @property
    def kaina_su_pvm(self):
        return round(self.kaina * 1.21 )

    def __repr__(self):
        return f"<Projektas {self.pavadinimas}, {self.kaina} EUR>"


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    projektai = Projektas.query.all()
    return render_template('index.html', projektas_rows=projektai)

@app.route("/search")
def search():
    search_text = request.args.get("q") #facebook.com/search?q=Int
    if search_text:
        projektai = Projektas.query.filter(Projektas.pavadinimas.ilike("%" + search_text + "%")).all()
    else:
        projektai =  Projektas.query.all()
    return render_template('search.html', projektas_rows=projektai, search_text=search_text)

@app.route("/prideti", methods=["GET", "POST"])
def prideti():
    if request.method == "POST":
        pavadinimas = request.form.get("pavadinimas")
        kaina = float(request.form.get("kaina"))
        db.session.add(Projektas(pavadinimas=pavadinimas, kaina=kaina))
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("prideti.html")


@app.route("/trinti/<int:project_id>", methods=["POST"])
def trinti(project_id):
    projektas = Projektas.query.get_or_404(project_id)
    db.session.delete(projektas)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/redaguoti/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    projektas = Projektas.query.get_or_404(project_id)

    if request.method == "POST":
        projektas.pavadinimas = request.form.get("pavadinimas")
        projektas.kaina = float(request.form.get("kaina"))
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("redaguoti.html", projektas=projektas)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

