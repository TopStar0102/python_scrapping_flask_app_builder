import requests
import json
import psycopg2

class MovieModel:
    def __init__(self):
        self.url = "https://query.wikidata.org/sparql"
        self.params = {
            "format": "json",
            "query": """
                SELECT ?item ?imdb_id ?title ?released ?director
                WHERE {
                    ?item wdt:P31 wd:Q11424 .
                    ?item wdt:P345 ?imdb_id .
                    ?item rdfs:label ?title .
                    ?item wdt:P577 ?released .
                    OPTIONAL {
                        ?item wdt:P57 ?dir.
                        ?dir rdfs:label ?director.
                        FILTER(lang(?director) = 'en')
                    }
                    FILTER(lang(?title) = 'en')
                    FILTER(year(?released)>=2013)
                } ORDER BY DESC(?released)
            """,
        }

    def fetch_data(self):
        try:
            response = requests.get(url=self.url, params=self.params)
            if response.status_code == 200:
                return json.loads(response.content)["results"]["bindings"]
        except Exception as e:
            print(e)
            return None

    def save_to_db(self, records):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="flask_test",
                user="root",
                password="")
            cursor = conn.cursor()
            for record in records:
                imdb_id = record["imdb_id"]["value"].split("/")[-1]
                title = record["title"]["value"]
                released = record["released"]["value"]
                director = ""
                if "director" in record:
                    director = record["director"]["value"]

                query = f"""
                    INSERT INTO movies(imdb_id, title, released, director)
                    VALUES('{imdb_id}', '{title}', '{released}', '{director}')
                    ON CONFLICT (imdb_id)
                    DO UPDATE SET title='{title}', released='{released}', director='{director}'
                """
                cursor.execute(query)
            conn.commit()
            return True
        except Exception as e:
            print(e)
            return False
