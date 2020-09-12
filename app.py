from flask import Flask, request,render_template,jsonify
from flask_restful import Api,Resource
from pymongo import MongoClient

app=Flask(__name__)
api=Api(app)

client=MongoClient('localhost',27017)
db=client.Cafe_X
users=db['Users']
#------------------FUNTION DEFINATIONS PYTHON--------------------------#
def checkuser(username):
    exisits=users.find_one({'username':username})
    if len(exisits)==0:
        return False
    if users.find_one({'username':username}):
        return False
    return False


def Retjson(status,msg):
    retjson={
        'status':status,
        'msg':msg
    }
    return retjson


#--------------------FLASK METHODS-------------------------------------#
@app.route('/',methods=['POST','GET','PUT'])
def Welcome():
    if request.method=='POST' or request.method=='PUT' or request.method=='GET':
        retjson={
            'status':200,
            'msg':'You successfully connected to the Cafe-X api'
        }
        return jsonify(retjson)

@app.route('/register',methods=['POST','GET'])
def Register():
    if request.method!='POST':
        print('yes')
        return jsonify(Retjson(404,'This method is not available'))
    Qjson=request.get_json()
    username=Qjson['username']
    password=Qjson['password']
    if len(username)==0 or len(password)==0:
        return jsonify(Retjson(301,'Username or Password cannot be left Blank'))
    if not checkuser(username):
        return jsonify(Retjson(302,'Username Already exsists'))
    users.insert_one({
        'username':username,
        'password':password
    })
    return jsonify(Retjson(200,'Successfully registered'))
    
@app.route('/login',methods=['POST'])
def Login():
    
    Qjson=request.get_json()
    username=Qjson['username']
    password=Qjson['password']
    if username==None or password==None:
        return jsonify(Retjson(301,'Username or Password cannot be left Blank'))
    if  checkuser(username):
        return jsonify(Retjson(302,'Username Doesn\'t exsists'))
    orgpass=users.find_one({'username':username})['password']
    if orgpass!=password:
        return jsonify(Retjson(303,'Password doesn\' t match'))
    #-----Send the Login successful json along with Main page items -----------------#
    return jsonify(Retjson(200,'Successfully Loged-In'))
if __name__=='__main__':
    app(debug=True)