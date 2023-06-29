from flask import Flask, render_template, redirect, url_for, request,flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, IntegerField, FloatField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flaskext.mysql import MySQL
from sqlalchemy import create_engine
import os
import requests
import folium
from folium.features import DivIcon
import pandas as pd

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:abduabdu@127.0.0.1:3306/dining'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

mysql = MySQL()
mysql.init_app(app)
# conn = mysql.connect()
# cursor = mysql.connection.cursor()

engine = create_engine('mysql+pymysql://abduabdu:abduabdu@34.27.20.160:3306/dining')
# engine = create_engine('mysql+pymysql://root:abduabdu@127.0.0.1:3306/dining')
connection = engine.raw_connection()
cursor = connection.cursor()

class InsertStud(FlaskForm):
    studentID = StringField(label = 'Enter the student ID:')
    studentName = StringField(label = 'Enter the name of the student:')
    studentRestriction = StringField(label = "Enter the student's dietary restriction ID")
    submitted = SubmitField(label = 'Submit')

class SearchMeal(FlaskForm):
    studentRestriction = StringField(label = 'Enter restriction ID to search:')
    submitted = SubmitField(label = 'Submit')

class UpdateName(FlaskForm):
    studentID = StringField(label = 'Enter your student ID:')
    studentName = StringField(label = 'Enter new name to update:')
    submitted = SubmitField(label = 'Submit')
    
class DeleteMeal(FlaskForm):
    studentID = StringField(label = 'Enter student ID to delete:')
    submitted = SubmitField(label = 'Submit')
    
class AdvancedQuery1(FlaskForm):
    submitted = SubmitField(label = 'Submit')
    
class AdvancedQuery2(FlaskForm):
    submitted = SubmitField(label = 'Submit')

class AdvancedDatabaseProgram(FlaskForm):
    mealID = StringField(label = 'Enter meal ID to search:')
    submitted = SubmitField(label = 'Submit')

class SearchRestrictions(FlaskForm):
    studentRestriction = StringField(label = 'Enter restriction ID to search:')
    submitted = SubmitField(label = 'Submit')

class CreativeComp(FlaskForm):
    street = StringField(label = "Enter your street address: ")
    city = StringField(label = "Enter your city: ")
    state = StringField(label = "Enter your state: ")
    postalcode = StringField(label = "Enter your ZIP code: ")
    dorm = StringField(label = "Enter your destination: ")
    transit = StringField(label = "Enter your preferred mode of transit: ")
    submitted = SubmitField(label = 'Submit')


@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/insertmain.html', methods = ['GET', 'POST'])
def insert():
    insform = InsertStud()
    if insform.validate_on_submit():
        studid = insform.studentID.data
        studnm = insform.studentName.data
        studrst = insform.studentRestriction.data
        cursor.execute("INSERT INTO Student VALUES (%s, %s, %s);", (studid, studnm, studrst))
        connection.commit()
        # data = cursor.fetchall()
        return render_template('home.html')
    return render_template('insertmain.html', form = insform)
       
@app.route('/deletemain.html', methods = ['GET', 'POST'])
def delete():
            
    delform = DeleteMeal()
    if delform.validate_on_submit():
        studid = delform.studentID.data
        cursor.execute("DELETE FROM Student WHERE StudentID=%s", (studid))
        connection.commit()
        # data = cursor.fetchall()
        return render_template('home.html')
    return render_template('deletemain.html', form = delform)

@app.route('/searchmain.html', methods = ['GET', 'POST'])
def search():

    searchform = SearchMeal()
    if searchform.validate_on_submit():
        restid = searchform.studentRestriction.data
        cursor.execute("SELECT StudentID, StudentName, Restrictions FROM Student WHERE Restrictions = %s", (restid))
        connection.commit()
        data = cursor.fetchall()
        return render_template('resultsmain.html', data = data)
    return render_template('searchmain.html', form = searchform)


@app.route('/updatemain.html', methods = ['GET', 'POST'])
def update():

    updform = UpdateName()
    if updform.validate_on_submit():
        studid = updform.studentID.data
        studnm = updform.studentName.data
        cursor.execute("UPDATE Student SET StudentName = %s WHERE StudentID = %s;", (studnm, studid))
        connection.commit()
        # data = cursor.fetchall()
        return render_template('home.html')
    return render_template('updatemain.html', form = updform)

    
@app.route('/resultsq1.html', methods = ['GET', 'POST'])
def q1():
    cursor.execute("SELECT DISTINCT h.Name FROM DiningHall h NATURAL JOIN Menu WHERE MenuID IN (SELECT DISTINCT MenuID FROM DiningHall NATURAL JOIN Menu GROUP BY MenuID HAVING count(*) > 1) ORDER BY h.Name ASC LIMIT 15")
    
    # cursor.execute("SELECT DISTINCT h.Name FROM DiningHall h NATURAL JOIN Menu NATURAL JOIN Meal WHERE MealID IN (SELECT MealID FROM DiningHall NATURAL JOIN Menu NATURAL JOIN Meal GROUP BY MealID HAVING count(*) > 1) ORDER BY h.Name ASC LIMIT 15")

    connection.commit()
    data = cursor.fetchall()
    return render_template('resultsq1.html', data = data)

@app.route('/resultsq2.html', methods = ['GET', 'POST'])
def q2():
    cursor.execute("SELECT DISTINCT r.RestrictionID FROM Student s NATURAL JOIN Restriction r GROUP BY r.RestrictionID HAVING COUNT(s.StudentID) > 1 ORDER BY RestrictionID ASC LIMIT 15")
    connection.commit()
    data = cursor.fetchall()
    return render_template('resultsq2.html', data = data)

@app.route('/advdbprog.html', methods = ['GET', 'POST'])
def adbp():
    advprogform = AdvancedDatabaseProgram()
    if advprogform.validate_on_submit():
        mealid = advprogform.mealID.data

        can_del = True
        students_starved = 0

        result_args = cursor.callproc('checkForRemovable', (mealid, can_del, students_starved))

        if result_args[1]:
            data = "Yes!"
        else:
            data = "No!"

        return render_template('resultsadv.html', data=data, students_num=result_args[2])
    return render_template('advdbprog.html', form = advprogform)

@app.route('/search_rests.html', methods = ['GET', 'POST'])
def search_rests():

    searchform = SearchRestrictions()
    if searchform.validate_on_submit():
        restid = searchform.studentRestriction.data
        cursor.execute("SELECT RestrictionID, RestrictionName, Status FROM Restriction WHERE RestrictionID = %s", (restid))
        connection.commit()
        data = cursor.fetchall()
        return render_template('rests_resultsmain.html', data = data)
    return render_template('search_rests.html', form = searchform)

def create_map(response):

    size = len(response.json()["features"][0]["properties"]["legs"][0]["steps"])

    steps = ""

    for x in range(size):
        steps = steps + response.json()["features"][0]["properties"]["legs"][0]["steps"][x]["instruction"]["text"] + '\n'
        
    mls = response.json()['features'][0]['geometry']['coordinates']
    points = [(i[1], i[0]) for i in mls[0]]
    m = folium.Map()
    
    for point in [points[0], points[-1]]:
        folium.Marker(point).add_to(m)
        
    folium.PolyLine(points, weight=5, opacity=1).add_to(m)
    
    df = pd.DataFrame(mls[0]).rename(columns={0:'Lon', 1:'Lat'})[['Lat', 'Lon']]
    sw = df[['Lat', 'Lon']].min().values.tolist()
    ne = df[['Lat', 'Lon']].max().values.tolist()

    folium.map.Marker(
        [40.11, -88.23],
        icon=DivIcon(
            icon_size=(250,36),
            icon_anchor=(0,0),
            html='<div style="font-size: 20pt">{{steps}}</div>',
            )
        ).add_to(m)

    m.fit_bounds([sw, ne])
    return m

@app.route('/creativecomp.html', methods = ['GET', 'POST'])
def creative_comp():

    searchform = CreativeComp()
    if searchform.validate_on_submit():
        street = searchform.street.data
        city = searchform.city.data
        state = searchform.state.data
        postalcode = searchform.postalcode.data
        dorm = searchform.dorm.data
        transit = searchform.transit.data

        url = "https://forward-reverse-geocoding.p.rapidapi.com/v1/forward"

        querystring = {"street":street,"city":city,"state":state,"postalcode":postalcode,"country":"USA","accept-language":"en","polygon_threshold":"0.0"}
        
        headers = {
            "X-RapidAPI-Key": "a22cb29f8amsh799716d46afa3a3p1c884bjsn80124ec802a9",
            "X-RapidAPI-Host": "forward-reverse-geocoding.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        json_response = response.json()

        coordinates = json_response[0]['lat']+','+json_response[0]['lon']
            
        url2 = "https://route-and-directions.p.rapidapi.com/v1/routing"

        # dorm = input("Enter your destination: ")
        # transit = input("Enter your preffered mode of transit: ")
            
        if dorm == "ISR":
            querystring2 = {"waypoints":coordinates+"|40.10956,-88.22078","mode":transit}

        if dorm == "IKE":
            querystring2 = {"waypoints":coordinates+"|40.10376,-88.23536","mode":transit}
                
        if dorm == "LAR":
            querystring2 = {"waypoints":coordinates+"|40.10422,-88.21999","mode":transit}
                
        headers2 = {
            "X-RapidAPI-Key": "a22cb29f8amsh799716d46afa3a3p1c884bjsn80124ec802a9",
            "X-RapidAPI-Host": "route-and-directions.p.rapidapi.com"
        }
            
        response2 = requests.request("GET", url2, headers=headers2, params=querystring2)
        
        m = create_map(response2)
        m.save('./templates/route_map.html')

        return render_template('route_map.html')
    return render_template('creativecomp.html', form = searchform)
    

# print("BEFORE")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

# print("AFTER")