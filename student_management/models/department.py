from odoo import models, fields

class WeatherCity(models.Model):
    _name = "weather.city"
    _description = "Weather City"

    name = fields.Char(required=True)
    latitude = fields.Float()
    longitude = fields.Float()

    temperature = fields.Float(readonly=True)
    humidity = fields.Integer(readonly=True)
    description = fields.Char(readonly=True)
    last_updated = fields.Datetime(readonly=True)
