import os
import requests
import pymysql
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("api_key")
db_user = os.getenv("user")
db_password = os.getenv("password")
db_name = "movie_db"

url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en"
response = requests.get(url)

data = response.json()

if 'genres' in data:
    print("Number of genres found:", len(data['genres']))
else:
    print("No genres key found in response")
    exit()

# Connect to MySQL using pymysql
print("Testing DB connection...")
db = pymysql.connect(
    host="localhost",
    user=db_user,
    password=db_password,
    database=db_name,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()
print("Connection successful!")

# Insert genres into the table
for genre in data['genres']:
    genre_id = genre['id']
    genre_name = genre['name']
    print(f"Inserting genre: {genre_id} - {genre_name}")
    cursor.execute(
        "INSERT INTO genres (genre_id, genre_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE genre_name=%s",
        (genre_id, genre_name, genre_name)
    )

db.commit()
cursor.close()
db.close()

print("Genres table populated successfully!")