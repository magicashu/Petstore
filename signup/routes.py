from signup import app
from flask import Flask,render_template,url_for,flash,request,redirect,session
from flask_bcrypt import Bcrypt
from wtforms import Form
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from flask import Flask,render_template,url_for,flash,request,redirect
from flask_login import LoginManager,login_user, current_user, logout_user, login_required
from signup.form import PostForm
from bson.json_util import dumps, loads

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
app.secret_key = "a95077b4fb8e1e1f55b7da8957220d38"
@app.route("/")
def home():
    return render_template('layout.html')

@app.route("/register",methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
        confirm_password = request.form.get('re_pass')
        hash_pass = bcrypt.generate_password_hash(password).decode('utf-8')

        mongo.db.users.insert_one({
            'username' : username,
            'name': name,
            'email' : email,
            'password' : hash_pass
        })
        flash('Account created successfully','success')


    return render_template('register.html',title='Register')

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]

        found_user = mongo.db.users.find_one({"email": email})
        if found_user:
            if bcrypt.check_password_hash(found_user['password'], password):
                session['username'] = found_user['username']
                session['email'] = found_user['email']


                flash("Login Successful!", "success")
                return redirect(url_for("home"))
            else:
                flash("Login failed. Please try again!", "danger")
        else:
            flash("Sorry User not found", "danger")
    return render_template('login.html',title='Login')

@app.route("/send_link/",methods = ['POST'])
def send_link():
    if request.method == 'POST':
        email = request.form['email']
        found_user = mongo.db.users.find_one({'email':email})

    if found_user:
        msg = Message("Password Reset Link",
              sender ="ashuujadhav200@gmail.com",
              recipents=[email])
        
        token = str(random.randint(111111,999999))

        mongo.db.users.update_one({ 'email': email}, {'$set':{ 'password_token':token }})

        msg_string = "<h5>Use below link to reset password<h5> <br> http://localhost:5000/change_password/"+token
        msg.html = msg_string
        mail.send(msg)
        flash("Password reset link is sent on your email","success")
        return redirect(url_for('login'))
    else:
        flash("No user found with this email ID","danger")
        return redirect(url_for('login'))

@app.route('/reset_password/<token>',methods = ['POST','GET'])
def reset_password(token):
    found_user = mongo.db.users.find_one( { 'password_token': token } )

    if found_user:
        if request.method == "POST":
            password = request.form['password']
            hash_pass = bcrypt.generate_password_hash(password).decode('utf-8')

            mongo.db.users.update_one( { 'password_token' : token }, { '$set': { 'password': hash_pass , 'password_token' : 'none' } } )
            flash("Password Reset successfully","success")
            return redirect(url_for('login'))
    else:
        flash("Password reset link is invalid", "danger")
        return redirect(url_for('login'))
    return render_template("reset_password.html",token=token)


@app.route('/new_pet',methods = ['POST','GET'])
@login_required
def new_pet():
    if request.method == 'POST':
        photu = request.form.get('photu')
        type = request.form.get('type')
        sex = request.form.get('sex')
        age = request.form.get('age')
        wa = request.form.get('wa')
        breed = request.form.get('breed')
        price = request.form.get('price')
        description = request.form.get('description')

        mongo.db.pets.insert_one({
            'photu': photu,
            'type' : type,
            'sex' : sex,
            'age' : age,
            'wa' : wa,
            'breed' : breed,
            'price' : price,
            'description' : description
        })
        flash('Post created successfully','success')
           
       
    return render_template('post_animals.html', title='New Post')

@app.route('/new_accessory',methods = ['POST','GET'])
@login_required
def new_accessory():
    if request.method == 'POST':
        pr_photu = request.form.get('pr_photu')
        pr_name = request.form.get('pr_name')
        pr_price = request.form.get('pr_price')
        pr_discount = request.form.get('pr_discount') 
        pr_discription = request.form.get('pr_discription')

        mongo.db.accessories.insert_one({
            'pr_photu': pr_photu,
            'pr_name' : pr_name,
            'pr_price' : pr_price,
            'pr_discount' : pr_discount,
            'pr_discription' : pr_discription
        })
        flash('Post created successfully','success')
           
       
    return render_template('post_accessories.html', title='New Post')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/cart")
def cart():
    return render_template('cart.html')

@app.route('/accessories')
def accessories(accessory_type=None, color=None):
    #todo getall data from db
    query_filter = {
        "accessory_type":accessory_type,
        "color":color
    }
    data = mongo.db.accessories.find()
    list_data = []
    for doc in data:
        list_data.append(doc)
    return render_template('acccessories.html',data=list_data)

@app.route("/dogs")
def dogs():
    return render_template('dogs.html')

@app.route("/birds")
def birds():
    return render_template('birds.html')

@app.route("/cats")
def cats():
    return render_template('cats.html')

@app.route('/pets')
def pets(pets_type=None):
    data_pets = mongo.db.pets.find()
    list_pets = []
    for pet in data_pets:
        list_pets.append(pet)
        print("Ewwwwwwww",pet)
    return render_template('pets.html',data_pets=list_pets)