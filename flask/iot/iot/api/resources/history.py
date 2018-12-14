"""History Resource"""
from datetime import datetime

from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, reqparse

from iot.models.device import Device


class History(Resource):
    """Get: return history data."""
    @staticmethod
    @jwt_required
    def get():
        """Get history data."""
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('start', type=int, required=True)
        parser.add_argument('end', type=int, required=True)
        parser.add_argument('interval', type=int, required=True)
        args = parser.parse_args()

        device = current_user.devices.filter(
            Device.id == args.id).first()
        if not device:
            return {'message': f'Device(id:{args.id}) do not exist'}, 404

        json_data = []  # Empty list
        days_start = datetime.utcfromtimestamp(args.start)
        days_end = datetime.utcfromtimestamp(args.end)
        interval = args.interval

        history_data = device.history_data(days_start, days_end, interval)

        for status in history_data:
            json_data.append(status[0].json_data())

        return json_data
