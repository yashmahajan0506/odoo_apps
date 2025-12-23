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


class SaleInherate(models.Model):
    _inherit = 'sale.order'

    term_conditions = fields.Many2one(
        'wb.so.tnc', string="Sales Terms And Conditions")
    show_in_report = fields.Selection([('yes', 'Yes'),
                                       ('no', 'No')],
                                      required=True, default='yes',string='Display In Reports??')
    terms_detail = fields.Html(string="Conditions Detail")


    @api.onchange('partner_id')
    def onchange_term_con_partner(self):
        if self.partner_id:
            self.term_conditions = self.partner_id.so_term_conditions.id
            self.terms_detail = self.partner_id.so_terms_detail
        else:
            self.term_conditions = False
            self.terms_detail = ''


    @api.onchange('term_conditions')
    def onchange_term_con_so(self):
        if self.term_conditions:
            self.terms_detail = self.term_conditions.terms_con
        else:
            self.terms_detail = ''
