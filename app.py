from flask import Flask,render_template,request,redirect,session
import pickle
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.secret_key = "secret123"

# load model & stats
model = pickle.load(open("model.pkl","rb"))
stats = pickle.load(open("stats.pkl","rb"))

# ---------------- LOGIN ----------------

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register',methods=['POST'])
def register():
    user = request.form['username']
    password = request.form['password']

    with open("users.txt","a") as f:
        f.write(user + "," + password + "\n")

    return redirect('/')

@app.route('/login',methods=['POST'])
def do_login():
    user = request.form['username']
    password = request.form['password']

    if not os.path.exists("users.txt"):
        open("users.txt","w").close()

    with open("users.txt","r") as f:
        for line in f:
            u,p = line.strip().split(',')
            if u==user and p==password:
                session['user'] = user
                return redirect('/home')

    return "Invalid Login ❌"

# ---------------- HOME ----------------

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template('index.html')

# ---------------- PREDICT ----------------

@app.route('/predict',methods=['POST'])
def predict():

    if 'user' not in session:
        return redirect('/')

    area = int(request.form['area'])
    bedrooms = int(request.form['bedrooms'])
    bathrooms = int(request.form['bathrooms'])
    garage = int(request.form['garage'])

    prediction = model.predict([[area,bedrooms,bathrooms,garage]])[0]

    low = prediction - stats["std"]
    high = prediction + stats["std"]

    # graph generate
    if not os.path.exists("static"):
        os.makedirs("static")

    plt.figure()
    plt.bar(['Low','Predicted','High'],[low,prediction,high])
    plt.title("Price Range")
    plt.savefig("static/user_graph.png")
    plt.close()

    # save history (UTF-8 FIX ✅)
    with open("history.txt","a", encoding="utf-8") as f:
        f.write(f"{session['user']} -> {int(prediction)} INR\n")

    return render_template('index.html',
        prediction_text="₹ {:,.0f}".format(prediction),
        range_text="₹ {:,.0f} - ₹ {:,.0f}".format(low,high),
        show_graph=True)

# ---------------- HISTORY ----------------

@app.route('/history')
def history():

    if not os.path.exists("history.txt"):
        open("history.txt","w").close()

    data = []
    with open("history.txt","r", encoding="utf-8") as f:
        data = f.readlines()

    return render_template('history.html',data=data)

# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)