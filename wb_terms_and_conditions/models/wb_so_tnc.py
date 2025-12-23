# -- coding: utf-8 --
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Wan Buffer Solution (<https://wanbuffer.com/>).
#
#    For Module Support : info@wanbuffer.com  or Call : +91 9638442270
#
##############################################################################

from odoo import fields, models


class WbSoTermsAndCon(models.Model):
    _name = 'wb.so.tnc'
    _description = "Wb So Tnc"

    name = fields.Char('Terms', translate=True)
    terms_con = fields.Html(string="Terms & Conditions", translate=True)
    company_ids = fields.Many2many('res.company', string='Company', required=True)
