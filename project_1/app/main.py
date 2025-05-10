from fastapi import FastAPI,Response,status,HTTPException
from fastapi import Body
import models
from typing import Optional
from random import  randrange
import psycopg2.extras
import time
import psycopg2

app= FastAPI()

while True:
    try:

        conn = psycopg2.connect(dbname="FastAPI" ,user="admin" ,password="admin", host="localhost" )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        print("Database connection was successful")
        # SQL query to create 'user' table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS "users" (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        cursor.execute(create_table_query)
        conn.commit()
        print("User table created successfully (if it didn't already exist)")
        
        break

    except Exception as error:
        print("Database connection was not successful")
        print(f"Error is {error}")
        time.sleep(2)



@app.get("/")
def root():
    return {"message": "Hello World back"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    posts = [dict(zip(columns, row)) for row in rows]
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"The post you're looking for is": post}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: models.Post):
    print(post)
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    new_post= cursor.fetchone()
    print("printing new post")
    print(new_post)
    conn.commit()
    return {"data": new_post}



@app.delete("/posts/{id}")
def delete_post_by_id(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post= cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    # my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post_by_id(id:int, post: models.Post):
    cursor.execute("""UPDATE posts set title=%s, content=%s ,published=%s where id= %s RETURNING * """,
                   (post.title, post.content, post.published, (str(id),)))
    updated_post= cursor.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    return {"data": updated_post}

@app.get("/users")
def get_users():
    cursor.execute("""SELECT * FROM users """)
    users_all = cursor.fetchall()
    return users_all

@app.get("/users/{id}", response_model=models.UserOut)
def get_user(id: int):
    cursor.execute("""SELECT * FROM users WHERE id = %s """, (str(id),))
    user = cursor.fetchone()
    user.pop("id")
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return user

@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=models.UserOut)
def create_user(user: models.User):
    print(user)
    cursor.execute("""INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING * """,(user.username, user.email, user.password))
    new_post= cursor.fetchone()
    new_post.pop("id")
    print("printing new user")
    print(new_post)
    conn.commit()
    return new_post