from cs50 import SQL
import sqlite3
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
          if(shoppingCart[i]["SUM(subTotal)"] is not None):
            total += shoppingCart[i]["SUM(subTotal)"]
          if(shoppingCart[i]["SUM(qty)"] is not None):
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

@app.route("/register/", methods=["POST"])
def registration():
    uname = request.form["uname"]
    pwd = request.form["pwd"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    rows = db.execute( "SELECT * FROM users WHERE username = :username ", username = uname )    
    if len( rows ) > 0:
        return render_template ( "signup.html", msg="Username already exists!" )    
    new = db.execute ( "INSERT INTO users (username, password, fname, lname, email) VALUES (:username, :password, :fname, :lname, :email)",
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
    
    print(rows)
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
    myBooks = db.execute("SELECT * FROM purchases WHERE id=:uid", uid=session["uid"])
    myBooksLen = len(myBooks)
    return render_template("purchase_history.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session, myBooks=myBooks, myBooksLen=myBooksLen)


@app.route("/checkout/")
def checkout():
    shoppingCart = []
    shopLen = len(shoppingCart)
    totItems=0
    total=0
    display=0
    cart = db.execute("SELECT * FROM cart")
    
    for item in cart:
        try:     
                db.execute("INSERT INTO purchases (id, uid, image, quantity, date) VALUES (:id, :uid, :image, :qty, :date)",
                id=item['id'], uid=session['uid'], image=item['image'], qty=item['qty'], date=datetime.now())

        except Exception as e:
        # Handle exceptions, print or log the error
           print(f"Error: {e}")


    return redirect('/purchase_history/')

@app.route("/cart/")
def cart():
    if 'user' in session:
        totItems, total, display = 0, 0, 0
        shoppingCart = db.execute("SELECT * FROM cart")
        shopLen = len(shoppingCart)
        for item in shoppingCart:
            subtotal = item["subTotal"]
            qty = item["qty"]

            if subtotal is not None:
                total += subtotal
            if qty is not None:
                totItems += qty

        return render_template("cart.html", shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session)

@app.route("/remove/", methods=["GET"])
def remove():
     out = int(request.args.get("id"))
     db.execute("DELETE from cart WHERE id=:id", id=out)
     totItems, total, display = 0, 0, 0
     shoppingCart = db.execute("SELECT * FROM cart")
     shopLen = len(shoppingCart)
     for i in range(shopLen):
          if shoppingCart[i]["subTotal"] is not None and shoppingCart[i]["qty"] is not None:
                total +=  shoppingCart[i]["subTotal"]
                totItems +=  shoppingCart[i]["qty"]
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
    totItems, total, display = 0, 0, 0
    qty = int(request.args.get('quantity'))

    if session:
        id = int(request.args.get('id'))
        goods = db.execute("SELECT * FROM books WHERE id = :id", id=id)

        if goods and goods[0]["onSale"] == 1:
            price = goods[0]["onSalePrice"]
        else:
            price = goods[0]["price"]

        image = goods[0]["image"]
        subTotal = qty * price

        # Start a new transaction
        with sqlite3.connect("data.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            try:
                # Try to insert the item into the cart
                cursor.execute("INSERT INTO cart (id, qty, image, price, subTotal) VALUES (?, ?, ?, ?, ?)",
                               (id, qty, image, price, subTotal))
            except sqlite3.IntegrityError as e:
                # Handle the unique constraint violation
                if "UNIQUE constraint failed: cart.id" in str(e):
                    # Rollback the ongoing transaction
                    conn.rollback()
                    # Update the quantity instead
                    cursor.execute("UPDATE cart SET qty = qty + ? WHERE id = ?", (qty, id))
                else:
                    # Handle other database errors
                    print(f"Database error: {e}")
                    # You might want to do something more meaningful here, like logging the error or providing a user-friendly message

            # Commit the transaction
            conn.commit()

            # Fetch the updated cart after the insertion or update
            shoppingCart = cursor.execute("SELECT image, SUM(qty) as total_qty, SUM(subTotal) as total_subtotal, price, id FROM cart GROUP BY id").fetchall()

            # Calculate total and total items in the cart
            total = sum(item["total_subtotal"] for item in shoppingCart)
            totItems = sum(item["total_qty"] for item in shoppingCart)

            books = db.execute("SELECT * FROM books")
            booksLen = len(books)

            return render_template("index.html", shoppingCart=shoppingCart, books=books, shopLen=len(shoppingCart), booksLen=booksLen, total=total, totItems=totItems, display=display, session=session)

@app.route("/update/")
def update():
    shoppingCart = {}
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

        image = bookitems[0]["image"]
        subTotal = qty * price
       
    
        db.execute("INSERT INTO cart (id, qty,image, price, subTotal) VALUES (:id, :qty,:image, :price, :subTotal)", id=id, qty=qty, image=image, price=price, subTotal=subTotal)
        shoppingCart = db.execute("SELECT * FROM cart")
        shopLen = len(shoppingCart)
        
        print('work',shoppingCart[0])
    
        for i in range(shopLen):
            total += shoppingCart[i]['subTotal']
            totItems += shoppingCart[i]['qty']
        
        print(total,totItems)
        return render_template ("cart.html",subTotal=subTotal, shoppingCart=shoppingCart, shopLen=shopLen, total=total, totItems=totItems, display=display, session=session )


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    app.run(debug=True)