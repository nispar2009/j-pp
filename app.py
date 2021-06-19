from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask("__main__")
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jokes.db"

class Jokes (db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    question = db.Column(
        db.String,
        nullable = False
    )
    answer = db.Column(
        db.String,
        nullable = False
    )

class Ratings (db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    username = db.Column(
        db.String,
        nullable = False
    )
    feedback = db.Column(
        db.String,
        nullable = False
    )
    stars = db.Column(
        db.String,
        nullable = False
    )

class Blog (db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    title = db.Column(
        db.String,
        nullable = False
    )
    content = db.Column(
        db.String,
        nullable = False
    )

@app.route("/")
def index():
    return(render_template(
        "index.html",
        jokes = Jokes.query.all()
    ))

@app.route("/addJoke", methods=[
    "GET",
    "POST"
])
def addJoke():
    if request.method == "POST":
        jokeQuestion = request.form["question"]
        jokeAnswer = request.form["answer"]

        newJoke = Jokes(question = jokeQuestion, answer = jokeAnswer)

        try:
            db.session.add(newJoke)
            db.session.commit()
            return(redirect("/"))
        except:
            return("There was an error.")

    else:
        return(render_template("addJoke.html"))

@app.route("/jokeDetails/<int:id>")
def jokeDetails(id):
    joke = Jokes.query.get_or_404(id)
    return(render_template("jokeDetails.html", joke = joke))

@app.route("/deleteJoke/<int:id>")
def deleteJoke(id):
    joke = Jokes.query.get_or_404(id)
    try:
        db.session.delete(joke)
        db.session.commit()
        return(redirect("/"))
    except:
        return("There was an error.")

@app.route("/updateJoke/<int:id>", methods = [
    "GET",
    "POST"
])
def updateJoke(id):
    joke = Jokes.query.get_or_404(id)
    if request.method == "POST":
        joke.question = request.form["question"]
        joke.answer = request.form["answer"]

        try:
            db.session.commit()
            return(redirect("/"))
        except:
            return("There was an error.")

    else:
        return(render_template("updateJoke.html", joke = joke))

@app.route("/ratings", methods = [
    "GET",
    "POST"
])
def ratings():
    if request.method == "POST":
        user = request.form["user"]
        fb = request.form["fb"]
        stars = request.form["stars"]

        newRating = Ratings(
            username = user,
            feedback = fb,
            stars = stars
        )

        try:
            db.session.add(newRating)
            db.session.commit()
            return(redirect("/ratings"))
        except:
            return("There was an error.")
    else:
        return(render_template("ratings.html", ratings = Ratings.query.all()))

@app.route("/addBlogPost", methods = [
    "GET",
    "POST"
])
def addBlogPost():
    if request.method == "POST":
        password = request.form["pw"]
        title = request.form["title"]
        content = request.form["content"]

        if password == "77131477":
            newBlogPost = Blog(
                title = title,
                content = content
            )
            try:
                db.session.add(newBlogPost)
                db.session.commit()
                return(redirect("/blog"))
            except:
                return("There was an error.")
        else:
            return("Wrong password!")

    else:
        return(render_template("addBlogPost.html"))

@app.route("/blog")
def blog():
    return(render_template("blog.html", posts = Blog.query.all()))

@app.route("/blogPost/<int:id>")
def blogPost(id):
    post = Blog.query.get_or_404(id)
    return(render_template("blogPost.html", post = post))

@app.route("/search")
def search():
    q = request.args.get("q")
    if q:
        jokes = Jokes.query.filter(
            Jokes.question.contains(q) |
            Jokes.answer.contains(q)
        )
        return(render_template("search.html", jokes = jokes, q=q))
    else:
        return(redirect("/"))

if __name__ == "__main__":
    app.run(debug = True)