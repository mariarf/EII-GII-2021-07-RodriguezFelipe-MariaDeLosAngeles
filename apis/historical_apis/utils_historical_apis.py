import pytz
from datetime import datetime as dt
from datetime import timedelta as timedelta

class UtilsHistoricalApis():

    def get_format_datetime(self):
        return "%Y-%m-%dT%H:%M:%S"

    def get_str_ny(self):
        return 'America/New_York'

    # Método que convierte una fecha de un formato dado a otro
    def convert_time_str(self, time, from_time, to_time):
        from_time = pytz.timezone(from_time)
        to_time = pytz.timezone(to_time)
        format_datetime = UtilsHistoricalApis().get_format_datetime()

        res = dt.strptime(time, format_datetime)
        res = from_time.localize(res)
        res = res.astimezone(to_time)
        res = res.strftime(format_datetime)
        return res