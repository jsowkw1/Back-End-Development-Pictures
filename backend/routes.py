"""Flask routes for the Pictures service.

This file is intended to replace ``backend/routes.py`` in the IBM starter
project. The service stores picture records in the module-level ``data`` list,
which is loaded from ``backend/data/pictures.json``.
"""

import json
import os

from flask import jsonify, request

from . import app


SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
with open(json_url, encoding="utf-8") as pictures_file:
    data: list[dict] = json.load(pictures_file)


@app.route("/health")
def health():
    """Report that the service is running."""
    return jsonify(status="OK"), 200


@app.route("/count")
def count():
    """Return the number of picture records."""
    return jsonify(length=len(data)), 200


@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all picture records as a JSON array."""
    return jsonify(data), 200


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return one picture, or a JSON 404 if its ID is unknown."""
    for picture in data:
        if picture.get("id") == id:
            return jsonify(picture), 200
    return jsonify(message="picture not found"), 404


@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a picture unless a record with the same ID already exists."""
    new_picture = request.get_json(silent=True)
    if not isinstance(new_picture, dict) or "id" not in new_picture:
        return jsonify(message="picture must be a JSON object with an id"), 400

    picture_id = new_picture["id"]
    if any(picture.get("id") == picture_id for picture in data):
        return jsonify(Message=f"picture with id {picture_id} already present"), 302

    data.append(new_picture)
    return jsonify(new_picture), 201


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Replace an existing picture record with the JSON request body."""
    updated_picture = request.get_json(silent=True)
    if not isinstance(updated_picture, dict):
        return jsonify(message="picture must be a JSON object"), 400

    for index, picture in enumerate(data):
        if picture.get("id") == id:
            data[index] = updated_picture
            return jsonify(updated_picture), 200

    return jsonify(message="picture not found"), 404


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture and return an empty 204 response."""
    for index, picture in enumerate(data):
        if picture.get("id") == id:
            del data[index]
            return "", 204

    return jsonify(message="picture not found"), 404
