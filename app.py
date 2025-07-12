from flask import Flask, render_template, request, redirect
from models import db, Application

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        deadline_raw = request.form["deadline"]
        deadline = ""
        if deadline_raw:
            parts = deadline_raw.split("-")  # ['2025', '10', '15']
            deadline = f"{parts[2]}-{parts[1]}-{parts[0]}"  # '15-10-2025'

        new_app = Application(
            university=request.form["university"],
            course=request.form["course"],
            status=request.form["status"],
            deadline=deadline,
            notes=request.form["notes"]
        )
        db.session.add(new_app)
        db.session.commit()
        return redirect("/")

    # FILTER LOGIC (GET request)
    query = Application.query
    keyword = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()

    if keyword:
        query = query.filter(
            (Application.university.ilike(f"%{keyword}%")) |
            (Application.course.ilike(f"%{keyword}%"))
        )
    if status:
        query = query.filter(Application.status == status)

    applications = query.all()
    return render_template("home.html", applications=applications)

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    app_to_edit = Application.query.get_or_404(id)

    if request.method == "POST":
        app_to_edit.university = request.form["university"]
        app_to_edit.course = request.form["course"]
        app_to_edit.status = request.form["status"]

        # Convert from yyyy-mm-dd (HTML input) to dd-mm-yyyy
        deadline_raw = request.form["deadline"]  # e.g. "2025-10-15"
        if deadline_raw:
            parts = deadline_raw.split("-")
            app_to_edit.deadline = f"{parts[2]}-{parts[1]}-{parts[0]}"  # "15-10-2025"
        else:
            app_to_edit.deadline = ""

        app_to_edit.notes = request.form["notes"]

        

        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", app=app_to_edit)

@app.route("/delete/<int:id>")
def delete(id):
    app_to_delete = Application.query.get_or_404(id)
    db.session.delete(app_to_delete)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
