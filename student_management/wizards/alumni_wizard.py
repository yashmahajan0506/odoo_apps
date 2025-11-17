from odoo import models, fields, api

class StudentAlumniWizard(models.TransientModel):
    _name = 'student.alumni.wizard'
    _description = 'Alumni Reason Wizard'

    reason = fields.Text(string="Reason", required=True)
    student_id = fields.Many2one('student.student', string="Student")

    def action_confirm(self):
        self.ensure_one()
        
        active_id = self.env.context.get('active_id')
        
        print("\n active_id ", active_id)
 
        self.env['student.alumni.reason'].create({
            'name': self.reason,
            'student_id': self.student_id.id,
        })
   
        self.student_id.state = 'alumni'
      
        self.student_id.message_post(body=f"Moved to alumni. Reason: {self.reason}")
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
