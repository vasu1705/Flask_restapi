from flask import Flask, request,render_template,jsonify,send_file,send_from_directory
from flask_restful import Api,Resource
from pymongo import MongoClient
import json

app=Flask(__name__)
api=Api(app)

client=MongoClient('localhost',27017)
db=client.Cafe_X
users=db['Users']
#------------------FUNCTION DEFINITIONS PYTHON--------------------------#
def checkuser(username):
    print(username)
    exisits=users.find_one({'username':username})
    if exisits is None:
        return True
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
    email=Qjson['email']
    contact_number=['contact_number']
    
    if len(username)==0 or len(password)==0:
        return jsonify(Retjson(301,'Username or Password cannot be left Blank'))
    if not checkuser(username):
        return jsonify(Retjson(302,'Username Already exsists'))
    users.insert_one({
        'username':username,
        'password':password,
        'email':email,
        'contact_number':contact_number
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



@app.route('/images/<image>')
def get_image(image):
    image='static/'+image
    return send_file(image,mimetype='image/gif')

#                                                    describe the products table 
# product_id              id momngodb
# producr_Name            String 
# product_type            String
# product_Description     String
# product_Maker           String
# product_Ingredients     String
# product_Images          collections/list
# product_reviews         collections/lists
# product_rating          int 
#product_price            int/double    
Product=db['Products']

@app.route('/products',methods=['POST','GET'])
def getproduct():
    T=list(Product.find({},{"_id":0}))
    for x in T:
        if x.get('product_Images',-1)!=-1:
            if len(x['product_Images'])>0:
                temp=[]
                for j in x['product_Images']:
                    #temp.append('http://127.0.0.1:5000/images/'+j)
                    temp.append('http://10.0.2.2:5000/images/'+j)
                    #print(temp)
                x['product_Images'].clear()
                x['product_Images']=temp
    print(T)
    return jsonify(T)

@app.route('/product/add',methods=['POST'])
def addproduct():
    Qjson=request.get_json()
    producr_Name=Qjson['product_name']
    product_type=Qjson['product_type']
    product_Description=Qjson['product_description']
    product_Maker=Qjson['product_maker']
    product_Ingredients=Qjson['product_ingredients']
    product_Images=Qjson['product_images']
    product_price=Qjson['product_price']
    if Product.find({'producr_Name':producr_Name,'product_Maker':product_Maker}) is None:
        return Retjson(305,'You Already Have this product registered')
    try:
        Product.insert({
        'product_Name':producr_Name,
        'product_Type':product_type,
        'product_Description':product_Description,
        'product_Maker':product_Maker,
        'product_Ingredients':product_Ingredients,
        'product_Images': product_Images,
        'product_reviews':{},
        'product_rating':0,
        'product_price':product_price
        })
        return jsonify(Retjson(302,'Item added successfully'))

    except:
        return jsonify(Retjson(302,'Could not Add your Item Server Busy'))
    


if __name__=='__main__':
    app.run(debug=True)