from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///feed.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
db=SQLAlchemy(app)

class Database(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    Name=db.Column(db.String(20),nullable=False)
    Feedback=db.Column(db.String(500),nullable=False)
    Time=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return f"{self.sno}  {self.Name}  {self.Feedback}"

@app.route("/", methods=["GET","POST"])

def home():
   
    if request.method=="POST":
        name=request.form["name"]
        feedback=request.form["feedback"]

        database=Database(Name=name,Feedback=feedback)

        db.session.add(database)
        db.session.commit()
       

    allFeedback=Database.query.all()
    # print(allFeedback)
    print(request.method)

  
    return render_template("index.html",allFeedback=allFeedback)

@app.route("/display")
def display():
    allFeedback=Database.query.all()
    print(allFeedback)
    return render_template("display.html",allFeedback=allFeedback)
@app.route("/delete/<int:sno>")
def delete(sno):
    database=Database.query.filter_by(sno=sno).first()
    db.session.delete(database)
    db.session.commit()
    return redirect("/")
@app.route("/update/<int:sno>", methods=["GET","POST"])
def update(sno):

    data=Database.query.filter_by(sno=sno).first()
    print("Data=",data)

    if data is None:
        return "Recoord not found", 404
     
     
    if request.method=="POST":

        data.Name=request.form["name"]
        data.Feedback=request.form["feedback"]

        db.session.commit()
        return redirect("/")
    return render_template("update.html",data=data)


   
  

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8000)
