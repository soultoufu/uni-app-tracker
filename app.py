from flask import Flask, render_template, request, redirect
from models import db, Application

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        new_app = Application(
            university=request.form["university"],
            course=request.form["course"],
            status=request.form["status"],
            deadline=request.form["deadline"],
            notes=request.form["notes"]
        )
        db.session.add(new_app)
        db.session.commit()
        return redirect("/")  # Refresh to prevent form resubmission

    applications = Application.query.all()
    return render_template("home.html", applications=applications)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
