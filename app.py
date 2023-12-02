from cs50 import SQL
from flask_session import Session
from flask import Flask, render_template,session, redirect,request
from datetime import datetime
import locale

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "Group_F_CA2_Project"
Session(app)

db = SQL ( "sqlite:///data.db" )
@app.route("/")
def index():
    books = db.execute("select * FROM books")
    booksLen = len(books)
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems= 0
    total=0
    display=0
    if 'user' in session:
        shoppingCart = db.execute("select image, SUM(qty), SUM(subTotal), price, id FROM cart")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        books = db.execute("SELECT * FROM books")
        booksLen = len(books)
        return render_template ("index.html", shoppingCart=shoppingCart, books=books, shopLen=shopLen, booksLen=booksLen, total=total, totItems=totItems, display=display, session=session )
    return render_template ("index.html", books=books, shoppingCart=shoppingCart, booksLen=booksLen, shopLen=shopLen, total=total, totItems=totItems, display=display)

@app.route("/login/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/signup/", methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route("/register/", methods=["GET"])
def registration():
    uname = request.form["uname"]
    pwd = request.form["pwd"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    rows = db.execute( "SELECT * FROM users WHERE username = :username ", username = uname )    
    if len( rows ) > 0:
        return render_template ( "signup.html", msg="Username already exists!" )    
    new = db.execute ( "INSERT INTO users (username, password, fname, lname, email) VALUES (:uname, :pwd, :fname, :lname, :email)",
                    username=uname, password=pwd, fname=fname, lname=lname, email=email )    
    return render_template ( "login.html" )

@app.route("/logout/")
def logout():
    db.execute("delete from cart")
    session.clear()
    return redirect("/")

@app.route("/logged/", methods=["POST"] )
def logged():
    user = request.form["uname"].lower()
    pwd = request.form["pwd"]
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    query = "SELECT * FROM users WHERE username = :user AND password = :pwd"
    rows = db.execute ( query, user=user, pwd=pwd )

    if len(rows) == 1:
        session['user'] = user
        session['time'] = datetime.now( )
        session['uid'] = rows[0]["id"]

    if 'user' in session:
        return redirect ( "/" )
    return render_template ( "login.html", msg="invalid username or password." )
       
@app.route("/purchase_history/")
def history():
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems=0
    total=0
    display=0
    myBooks = db.execute("SELECT * FROM purchases WHERE uid=:uid", uid=session["uid"])
    myBooksLen = len(myBooks)
    return render_template("purchase_history.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session, myBooks=myBooks, myBooksLen=myBooksLen)

@app.route("/cart/")
def cart():
    if 'user' in session:
        totItems, total, display = 0, 0, 0
        shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]    
    return render_template("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)

@app.route("/remove/", methods=["GET"])
def remove():
     out = int(request.args.get("id"))
     db.execute("DELETE from cart WHERE id=:id", id=out)
     totItems, total, display = 0, 0, 0
     shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart")
     shopLen = len(shoppingCart)
     for i in range(shopLen):
        total += shoppingCart[i]["SUM(subTotal)"]
        totItems += shoppingCart[i]["SUM(qty)"]
     display = 1
     return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)


@app.route("/filter/")
def filter():
    if request.args.get('sale'):
        query = request.args.get('sale')
        books = db.execute("SELECT * FROM books WHERE onSale = :query", query=query)
    
    if request.args.get('kind'):
        query = request.args.get('kind')
        books = db.execute("SELECT * FROM books WHERE kind = :query", query=query)
        
    if request.args.get('price'):
        query = request.args.get('price')
        books = db.execute("SELECT * FROM books")
        
    booksLen = len(books)
    
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    if 'user' in session:
        
        shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        
        return render_template ("index.html", shoppingCart=shoppingCart, books=books, shopLen=shopLen, booksLen=booksLen, total=total, totItems=totItems, display=display, session=session )
    
    return render_template ( "index.html", books=books, shoppingCart=shoppingCart, booksLen=booksLen, shopLen=shopLen, total=total, totItems=totItems, display=display)


@app.route("/buy/")
def buy():
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    if session:
        id = int(request.args.get('id'))
        goods = db.execute("SELECT * FROM books WHERE id = :id", id=id)
        
        if(goods[0]["onSale"] == 1):
            price = goods[0]["onSalePrice"]
        else:
            price = goods[0]["price"]
        image = goods[0]["image"]
        subTotal = qty * price
        db.execute("INSERT INTO cart (id, qty, image, price, subTotal) VALUES (:id, :qty, :image, :price, :subTotal)", id=id, qty=qty, image=image, price=price, subTotal=subTotal)
        shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart")
        shopLen = len(shoppingCart)
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
        books = db.execute("SELECT * FROM books")
        booksLen = len(books)
     
        return render_template ("index.html", shoppingCart=shoppingCart, books=books, shopLen=shopLen, booksLen=booksLen, total=total, totItems=totItems, display=display, session=session )


@app.route("/update/")
def update():
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))
    if session:
        id = int(request.args.get('id'))
        db.execute("DELETE FROM cart WHERE id = :id", id=id)
     
        bookitems = db.execute("SELECT * FROM books WHERE id = :id", id=id)
       
        if(bookitems[0]["onSale"] == 1):
            price = bookitems[0]["onSalePrice"]
        else:
            price = bookitems[0]["price"]
        team = bookitems[0]["team"]
        image = bookitems[0]["image"]
        subTotal = qty * price
       
        db.execute("INSERT INTO cart (id, qty,image, price, subTotal) VALUES (:id, :qty,:image, :price, :subTotal)", id=id, qty=qty, image=image, price=price, subTotal=subTotal)
        shoppingCart = db.execute("SELECT image, SUM(qty), SUM(subTotal), price, id FROM cart")
        shopLen = len(shoppingCart)
   
        for i in range(shopLen):
            total += shoppingCart[i]["SUM(subTotal)"]
            totItems += shoppingCart[i]["SUM(qty)"]
       
        return render_template ("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


#if __name__ == '__main__':
    #locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    #app.run()

if __name__ == "__main__":
 app.run(host='0.0.0.0', port='8080') # indent this line
