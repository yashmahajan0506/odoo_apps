from odoo import models, fields

class Department(models.Model):
    _name = "school.department"
    _description = "Department"

    name = fields.Char(string="Department Name", required=True)
