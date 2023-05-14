from flask import Flask
from flask_appbuilder import AppBuilder
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.views import ModelView
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://your_username:your_password@localhost/your_database"
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.String(200), unique=True, nullable=False)
    title = db.Column(db.String(200), unique=True, nullable=False)
    released = db.Column(db.Date, nullable=False)
    director = db.Column(db.String(200))

    def __repr__(self):
        return f"<Movie {self.title}>"

appbuilder = AppBuilder(app, db.session)

class MovieView(ModelView):
    datamodel = SQLAInterface(Movie)
    list_columns = ["title", "released", "director"]
    add_columns = ["imdb_id", "title", "released", "director"]
    edit_columns = add_columns

db.create_all()

appbuilder.add_view(
    MovieView,
    "Movies",
    icon="fa-film",
    category="Data",
    category_icon="fa-database",
)

if __name__ == "__main__":
    app.run(debug=True)
