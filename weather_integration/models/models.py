from odoo import models, fields, api, _
from odoo.exceptions import UserError
import requests

class WeatherInfo(models.Model):
    _name = "weather.info"
    _description = "Weather Information"

    name = fields.Char(string="City", required=True)
    temperature = fields.Float(string="Temperature (°C)", readonly=True)
    humidity = fields.Integer(string="Humidity (%)", readonly=True)
    weather_condition = fields.Char(string="Condition", readonly=True)
    last_updated = fields.Datetime(string="Last Updated", readonly=True, default=fields.Datetime.now)

    def action_fetch_weather(self):
        API_KEY = "c9cd2696f2291024bf3865752334216c"

        for record in self:
            if not record.name:
                continue

            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": record.name,
                "appid": API_KEY,
                "units": "metric",
            }

            try:
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 404:
                    raise UserError(_("City '%s' not found. Please check the spelling.") % record.name)
                response.raise_for_status()
                
                data = response.json()
                record.write({
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "weather_condition": data["weather"][0]["description"].title(),
                    "last_updated": fields.Datetime.now(),
                })
            except requests.exceptions.HTTPError as e:
                raise UserError(_("API Error: %s") % str(e))
            except Exception as e:
                raise UserError(_("Unable to fetch weather data. Error: %s") % str(e))
