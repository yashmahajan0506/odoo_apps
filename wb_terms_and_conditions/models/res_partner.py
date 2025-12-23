# -- coding: utf-8 --
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Wan Buffer Solution (<https://wanbuffer.com/>).
#
#    For Module Support : info@wanbuffer.com  or Call : +91 9638442270
#
##############################################################################
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    so_term_conditions = fields.Many2one(
        'wb.so.tnc', string="Sales Terms And Conditions")

    so_terms_detail = fields.Html(string="Conditions Detail")
    po_term_conditions = fields.Many2one(
        'wb.po.tnc', string="Purchase Terms And Conditions")
    po_terms_detail = fields.Html(string="Conditions Detail")

    @api.onchange('so_term_conditions', 'po_term_conditions')
    def _onchange_term_con_so_and_po(self):
        self.so_terms_detail = self.so_term_conditions.terms_con if self.so_term_conditions else ''
        self.po_terms_detail = self.po_term_conditions.terms_con if self.po_term_conditions else ''


