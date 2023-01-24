from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.posts import Posts
from app.models.users import Users

hello_bp = Blueprint("homepage", __name__,url_prefix="/")
posts_bp = Blueprint("posts", __name__, url_prefix="/posts")
users_bp = Blueprint("users", __name__, url_prefix="/users")

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

# UPDATE User INFO
@users_bp.route("/<user_id>", methods=["PATCH"])
def update_user(user_id):
    user = Users.query.get(user_id)
    request_body = request.get_json()

    user.address = request_body["address"]
    user.username = request_body["username"]
    
    db.session.commit()

    return ({
            "user_id":user.user_id,
            "address":user.address,
            "username": user.username,
            
        })

# CREATE A NEW POST
@posts_bp.route("", methods=["POST"])
def create_post():
    request_body = request.get_json()
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

