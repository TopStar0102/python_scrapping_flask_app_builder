from model import MovieModel
from view import app, db

def main():
    model = MovieModel()
    records = model.fetch_data()
    if records is None:
        print("Error: could not fetch data")
        return

    result = model.save_to_db(records)
    if not result:
        print("Error: could not save data to database")
        return

    print(f"{len(records)} movies saved to database")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        main()
