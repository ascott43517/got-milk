from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.posts import Posts
from app.models.users import Users
import requests
import os
from dotenv import load_dotenv
load_dotenv()

maps_bp = Blueprint("maps", __name__,url_prefix="/maps")
hello_bp = Blueprint("homepage", __name__,url_prefix="/")
posts_bp = Blueprint("posts", __name__, url_prefix="/posts")
users_bp = Blueprint("users", __name__, url_prefix="/users")

maps_api = os.environ.get("MAPS_API")
location_key = os.environ.get("LOCATION_KEY")

@hello_bp.route("", methods=["GET"])
def readme_page():
    return ("Welcome to Got Milk! Valid routes include /posts, /users, /users/user_id/posts and others!")

# CREATE A NEW USER
@users_bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()
    new_user = Users(
        address=request_body["address"],
        username=request_body["username"])

    db.session.add(new_user)
    db.session.commit()

    return ({
            "user_id":new_user.user_id,
            "address":new_user.address,
            "username": new_user.username,
            
        })

# GET A USER BY USERNAME- email
@users_bp.route("/<username>", methods=["GET"])
def get_user(username):
    
    all_users = Users.query.all()
    for user in all_users:
      if user.username == str(username):
        return ({
                "user_id": user.user_id,
                "address": user.address,
                "username":user.username,
                # "posts":user.posts
                
} ) 
    # return ('hi')
        
 
    

# GET LIST OF ALL USers
@users_bp.route("", methods=["GET"])
def get_all_users():
    # retrieve all users from database
    all_users = Users.query.all()
    user_list = []
    for user in all_users:
        user_list.append({
            "user_id" : user.user_id,
            "address": user.address,
            "username": user.username
        })
    return jsonify(user_list)

# UPDATE User INFO
@users_bp.route("/<username>", methods=["PATCH"])
def update_user(username):
    request_body = request.get_json()
    all_users = Users.query.get(request_body["user_id"]["user_id"])

    all_users.address = request_body["address"]
    all_users.username = request_body["username"]
    all_users.user_id = request_body["user_id"]["user_id"]
    
    db.session.commit()
        
    return ({  
       "address": all_users.address,
       "username": all_users.username,
       "user_id": all_users.user_id
              })

# CREATE A NEW POST
@posts_bp.route("", methods=["POST"])
def create_post():
    request_body = request.get_json()
    print(request_body)
    new_post = Posts(
            address=request_body["address"],
            username=request_body["username"],
            # date= request_body["date"],
            user_id= request_body["user_id"],
            formula_name= request_body["formula_name"],
            quantity= request_body["quantity"])


    db.session.add(new_post)
    db.session.commit()

    return ({
            "user_id":new_post.user_id,
            "address":new_post.address,
            "username": new_post.username,
            "date": new_post.date,
            "formula_name": new_post.formula_name,
            "quantity": new_post.quantity,
            "post_id": new_post.post_id,
            "available": new_post.available

    })


# DELETE POST
@posts_bp.route("/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Posts.query.get(post_id)

    db.session.delete(post)
    db.session.commit()

    return make_response(f"Post '{post.post_id}' deleted")

# MARK POST UNAVAILABLE
@posts_bp.route("/<post_id>/unavailable", methods=["PATCH"])
def mark_post_unavailable(post_id):
    post = Posts.query.get(post_id)
    
   
    post.available =  False
    db.session.commit()

    return ({
            "post_id":post.post_id,
            "address":post.address,
            "username": post.username,
            "date": post.date,
            "user_id": post.user_id,
            "formula_name": post.formula_name,
            "quantity": post.quantity,
            "available": post.available

        })


# MARK POST AVAILABLE
@posts_bp.route("/<post_id>/available", methods=["PATCH"])
def mark_post_available(post_id):
    post = Posts.query.get(post_id)
    
   
    post.available =  not post.available
    db.session.commit()

    return ({
            "post_id":post.post_id,
            "address":post.address,
            "username": post.username,
            "date": post.date,
            "user_id": post.user_id,
            "formula_name": post.formula_name,
            "quantity": post.quantity,
            "available": post.available

        })

# UPDATE A POST
@posts_bp.route("/<post_id>", methods=["PATCH"])
def update_post(post_id):
    post = Posts.query.get(post_id)
    
    request_body = request.get_json()
   

    post.address = request_body["address"]
    post.formula_name = request_body["formula_name"]
    post.quantity = request_body["quantity"]
    
    
    db.session.commit()

    return ({
            "post_id":post.post_id,
            "address":post.address,
            "username": post.username,
            "date": post.date,
            "user_id": post.user_id,
            "formula_name": post.formula_name,
            "quantity": post.quantity,

            
        })
# GET LIST OF ALL POSTS
@posts_bp.route("", methods=["GET"])
def get_all_posts():
    # retrieve all posts from database
    all_posts = Posts.query.all()
    post_list = []
    for post in all_posts:
        if post.available == True:
          post_list.append({
            "user_id" : post.user_id,
            "address": post.address,
            "username": post.username,
            "date":post.date,
            "quantity": post.quantity,
            "formula_name": post.formula_name,
            "post_id": post.post_id,
            "available": post.available
        })
        print(post_list)
    return jsonify(post_list)



# GET ALL USERS AND THEIR POSTS
@users_bp.route("/<user_id>/posts",methods=["GET"])
def get_users(user_id):
    #retrieve specific board from database
    user = Users.query.get(user_id)
    # create dictionary for return content
    user_dict = {}
    # create list for card content
    post_list = []
    # build card list
    for post in user.posts:
        post_dict = {
            "user_id" : post.user_id,
            "post_id": post.post_id,
            "address": post.address,
            "username": post.username,
            "quantity": post.quantity,
            "formula_name": post.formula_name,
            "date": post.date,
            "available": post.available,
        }
        post_list.append(post_dict)
    user_dict["user_id"] = user.user_id
    user_dict["address"] = user.address
    user_dict["username"] = user.username
    user_dict["posts"] = post_list
    print(user_dict["posts"])
    return user_dict

# MAPS CALL
@maps_bp.route("", methods=["POST"])
def get_map_directions():
    print(request.get_json())
    request_body = request.get_json(force=True, cache=True)
  
    
    print(request_body)
    # if not origin_query or not destination_query:
    #     return {"message": "must provide origin and destination parameters"}
  

    response = requests.get(
        "https://maps.googleapis.com/maps/api/directions/json?",
        params={"origin": request_body["origin"], "destination": request_body["destination"], "key": maps_api })
    
    return jsonify(response.json())


    # Location LAt Lon CALL
@maps_bp.route("/latlng", methods=["POST"])
def get_latlng():

    request_body = request.get_json()
    print(request_body)
    # loc_query = request_body["q"]
    # if not loc_query:
    #     return {"message": "must provide q parameter (location)"}

    response = requests.get(
        "https://us1.locationiq.com/v1/search.php",
        params={"q": request_body["q"], "key": location_key, "format": "json"}
    )

    print(response.json())

    return jsonify(response.json())