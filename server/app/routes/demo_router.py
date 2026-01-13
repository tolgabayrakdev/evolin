from flask import Blueprint, jsonify

demo_router = Blueprint("demo", __name__)

@demo_router.route("/", methods=["GET"])
def get_demo():
    return jsonify({"msg": "hello"})