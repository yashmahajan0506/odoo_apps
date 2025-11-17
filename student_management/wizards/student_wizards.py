from odoo import models, fields, api

class StudentMessageWizard(models.TransientModel):
    _name = 'student.message.wizard'
    _description = 'Wizard to Send Message to Student'

    message = fields.Text(string="Message", required=True)

    def action_send_message(self):
        active_ids = self.env.context.get('active_ids')
        students = self.env['student.student'].browse(active_ids)
        for student in students:
            student.message_post(body=self.message)
        return {'type': 'ir.actions.act_window_close'}
