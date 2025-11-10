from odoo import models
import io
import base64
from openpyxl import Workbook

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_export_sale_excel(self):
        for order in self:
          
            wb = Workbook()
            ws = wb.active
            ws.title = "Sale Order Details"

            ws.append(["Field", "Value"])
            ws.append(["Order Name", order.name or ""])
            ws.append(["Customer", order.partner_id.name or ""])
            ws.append(["Order Date", str(order.date_order.date()) if order.date_order else ""])
            ws.append(["Payment Terms", order.payment_term_id.name or ""])
            ws.append(["Total Amount", order.amount_total])
            ws.append(["Status", order.state])
            ws.append(["Salesperson", order.user_id.name or ""])

       
            fp = io.BytesIO()
            wb.save(fp)
            fp.seek(0)
            data = base64.b64encode(fp.read())
            fp.close()

           
            attachment = self.env['ir.attachment'].create({
                'name': f"{order.name}_details.xlsx",
                'type': 'binary',
                'datas': data,
                'res_model': 'sale.orde r',
                'res_id': order.id,
                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            })
            
            return {
                'type': 'ir.actions.act_url',
                'url': f'/web/content/{attachment.id}?download=true',
                'target': 'new',
            }
