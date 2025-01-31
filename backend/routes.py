from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    # return the loaded list called 'data'
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    # find the URL with the given id, return it back to caller
    picture = next( (pic for pic in data if pic.get('id') == id), None)

    if picture:
        return jsonify(picture), 200 # return picture if found.

    return jsonify({"error": "Picture not found"}), 404 #404 not found

######################################################################
# CREATE A PICTURE
######################################################################


@app.route("/picture", methods=["POST"])
def create_picture():
    # get data from json body
    picture = request.json

    # return 303 if duplicate
    for pic in data:
        if picture['id'] == pic['id']:
            return {
                "Message": f"picture with id {picture['id']} already present"
            }, 302
    data.append(picture)

    return picture, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    
    # get data from json body
    picture = request.json

    for index, pic in enumerate(data):
        if picture['id'] == id:
            data[index] = picture
            return picture, 201

    return {'message': "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):

    for picture in data:
        if picture["id"] == id:
            data.remove(picture)
            return "", 204

    return {"message": "picture not found"}, 404
    