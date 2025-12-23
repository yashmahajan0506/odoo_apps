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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    term_conditions = fields.Many2one(
        'wb.po.tnc', string="Purchase Terms And Conditions")
    terms_detail = fields.Html(string="Conditions Detail",)
    show_in_report = fields.Selection([('yes', 'Yes'),
                                       ('no', 'No')],
                                      required=True, default='yes', string='Display In Reports??')

    @api.onchange('partner_id')
    def onchange_term_con_partner(self):
        if self.partner_id:
            print("\n ifff")
            print("\n self.partner_id.po_term_conditions.id",self.partner_id.po_term_conditions.id)
            print("\n self.terms_detail",self.partner_id.po_terms_detail)
            self.term_conditions = self.partner_id.po_term_conditions.id
            self.terms_detail = self.partner_id.po_terms_detail
        else:
            self.term_conditions = False
            self.terms_detail = ''


    

    @api.onchange('term_conditions')
    def onchange_term_con_so(self):
        if self.term_conditions:
            self.terms_detail = self.term_conditions.terms_con
        else:
            self.terms_detail = ''

