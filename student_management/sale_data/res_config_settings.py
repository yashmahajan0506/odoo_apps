# from odoo import models, fields

# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'

#     enable_student_report = fields.Boolean(string="Enable Student Report Printing")

#     def action_print_student_report(self):
#         # You can customize what data to print, here we print all active students
#         students = self.env['student.student'].search([])
#         return self.env.ref('student_management.student_report_action').report_action(students)
