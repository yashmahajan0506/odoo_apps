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


class InvoiceInherit(models.Model):
    _inherit = 'account.move'

    term_conditions = fields.Many2one(
        'wb.so.tnc', string="Account Terms And Conditions")
    po_term_conditions = fields.Many2one(
        'wb.po.tnc', string="Account Terms And Conditions")
    terms_detail = fields.Html(string="Conditions Detail")
    show_in_report = fields.Selection([('yes', 'Yes'),
                                       ('no', 'No')],
                                      required=True, default='yes', string='Display In Reports??')

    @api.onchange('partner_id')
    def onchange_term_con_partner(self):
        if self.partner_id and self.move_type == 'in_invoice':
            self.po_term_conditions = self.partner_id.po_term_conditions.id
            self.terms_detail = self.partner_id.po_terms_detail
        elif self.partner_id and self.move_type == 'out_invoice':
            self.term_conditions = self.partner_id.so_term_conditions.id
            self.terms_detail = self.partner_id.so_terms_detail
        else:
            self.term_conditions = False
            self.po_term_conditions = False
            self.terms_detail = ''

    @api.onchange('term_conditions','po_term_conditions','partner_id')
    def onchange_term_con_so(self):
        if self.term_conditions:
            self.terms_detail = self.term_conditions.terms_con
        elif self.po_term_conditions:
            self.terms_detail = self.po_term_conditions.terms_con
        else:
            self.terms_detail = ''








