from flask import Blueprint, session, request, abort

from models import APIResponse
from decorators.auth import authenticated
from validation import expect_json
from orm import Trip, Position, db


position_blueprint = Blueprint("position", __name__)


@position_blueprint.route("", methods=["POST", "GET"])
@authenticated
def position():
    user = session.get("user")

    if request.method == "POST":
        data = expect_json({"trip_id": int, "lon": float, "lat": float})

        trip = Trip.query.filter_by(id=data["trip_id"], user_id=user["id"]).first()
        if trip is None:
            abort(400, "Your user does not have access to any trip with that id")
        if not trip.active:
            abort(400, "This trip is not active")

        position = Position(
            lon=data["lon"],
            lat=data["lat"],
            trip_id=data["trip_id"],
            user_id=user["id"],
        )
        db.session.add(position)
        db.session.commit()

        return APIResponse(response=position).serialize()

    return APIResponse().serialize()


@position_blueprint.route("/<int:id>", methods=["GET"])
@authenticated
def position_id(id: int):
    user = session.get("user")
    position = Position.query.filter_by(id=id, user_id=user["id"]).first()

    if position is None:
        abort(404, "No position with that id found")

    return APIResponse(response=position).serialize()
