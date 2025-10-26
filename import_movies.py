import os
import csv
import pymysql
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("user")
db_password = os.getenv("password")
db_name = "movie_db"
csv_file = "dataset/movies.csv"

try:
    db = pymysql.connect(
        host="localhost",
        user=db_user,
        password=db_password,
        database=db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    print("DB connection successful!")

    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie_id = int(row['id'])
            title = row['title']
            release_year = row['release_date'] or None

            #insert movie
            cursor.execute(
                "INSERT INTO movies (movie_id, title, release_year) VALUES (%s, %s, %s) "
                "ON DUPLICATE KEY UPDATE title=%s, release_year=%s",
                (movie_id, title, release_year, title, release_year)
            )

            #insert genre mappings
            genre_ids = row['genre_ids'].strip("[]").split(",")
            for genreID in genre_ids:
                if genreID.strip():
                    cursor.execute(
                        "INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s) "
                        "ON DUPLICATE KEY UPDATE movie_id=movie_id",
                        (movie_id, int(genreID))
                    )

    db.commit()
    print("Movies and movie_genres populated successfully!")

except pymysql.MySQLError as e:
    print("DB error:", e)

finally:
    if cursor:
        cursor.close()
    if db:
        db.close()