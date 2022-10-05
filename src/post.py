from flask import Blueprint, request, jsonify, redirect
import validators   
from src.database import Post,db, Comment
from flask_jwt_extended import get_jwt_identity, jwt_required
import sys


post= Blueprint("post",__name__,url_prefix="/api/v1/post" )


# register user
@post.route('/', methods = ['POST', 'GET'])

@jwt_required()
def handle_post():
    current_user=get_jwt_identity()  #to post in bookmark we need current user
    if request.method == 'POST':

        data = request.get_json()
        image = data.get('image', '')
        message = data.get('message', '')
        post=Post(image = image, message= message, user_id=current_user)
        db.session.add(post)
        db.session.commit()

        return jsonify({
            'id': post.id,
            'image': post.image,
            'message': post.message,
            'created_at': post.created_at
        }), 201

    else:
        #pagination

        page = request.args.get('page', 1, type =int)
        per_page = request.args.get('per_page', 5, type=int)
#sending back all, make query first, getting the book!!

        post = Post.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)

        # serialize, to get the bookmarks each each, because we wont be able to get the object, so we get them in a list
        data = []

        for post in post.items:
            data.append({
            'id': post.id,
            'image': post.image,
            'message': post.message,
            'created_at': post.created_at
            })
#tell frontend there are other pages, current page
# all these are default values of pagination. 
        meta = {
            "page": post.page,
            "pages": post.pages,
            "total_count": post.total,
            "prev": post.prev_num,
            "next": post.next_num,
            "has_prev": post.has_prev,
            "has_next": post.has_next
        }
#Note: after pagination, our value get sent back to us in key, value pairs, so you would need to loop through the object with .itms i.e your query.

# to get page ?page=1 you need more ?page=1&per_page=11
# having key as data and returning data
        return jsonify({'data':data, 'meta': meta}), 200

#get user

@post.get('/<int:id>')
@jwt_required()
def get_post(id):
    current_user = get_jwt_identity()

    post = Post.query.filter_by(user_id=current_user, id=id).first()

    if not post:
        return jsonify({'message': 'item not found'}), 404


    return jsonify({
            'id': post.id,
            'image': post.image,
            'message': post.message,
            'created_at': post.created_at
    }), 200


@post.route('edit/<int:id>', methods=['PATCH', 'PUT'])
@jwt_required()
def update_post(id):
    current_user = get_jwt_identity()

    data = request.get_json()
    image = data.get('image', '')
    message = data.get('message', '')

#we find the bookmark

    post = Post.query.filter_by(user_id=current_user, id=id).first()
    

    if not post:
        return jsonify({'message': 'item not found'}), 404

    post.image = image
    post.message = message

#no need to add, just commit
    db.session.commit()
#we  need to return
    return jsonify({
            'id': post.id,
            'image': post.image,
            'message': post.message,
            'created_at': post.created_at
    })

@post.route('delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    current_user = get_jwt_identity()

    post = Post.query.filter_by(user_id=current_user, id=id).first()

    if not post:
        return jsonify({'message': 'item not found'}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({
        'message': 'Deleted'
    }), 204

@post.route('post/<int:id>/comment', methods=['POST'])
@jwt_required()
def add_comment(id):
    post = Post.query.filter_by(id=id).first()
    print(post)
    data = request.get_json()
    comment = data.get('comment', '')
    print(comment)
    get_comment = Comment.query.filter_by(post_id=id).first()
    print(get_comment)
    comment_db = Comment(comment=comment)
    
    db.session.add(comment_db)
    db.session.commit()

    return jsonify({
        'success': True,
        'comment': get_comment,
    }), 200

@post.route('post/<int:id>/', methods=['POST'])
@jwt_required()
def like_post(id):
    post = Post.query.filter_by(id=id).first()
    if post.like == False:
        post.like = True

    return jsonify ({
        'success': True,
        'post': post,
        'message': 'Post liked'
    })
