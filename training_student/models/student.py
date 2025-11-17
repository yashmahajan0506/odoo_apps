

from odoo import models, fields, api 
from odoo.exceptions import UserError


class student(models.Model):
    _name = 'student.student'
    _description = 'Student training'

    name = fields.Char(string='name',required=True)
    age=fields.Integer(string='age')
    course=fields.Char(string='course')
    teacher_id=fields.Many2many('training.teacher',string='teachers')
    user_id=fields.Many2one('res.users',string='student')

    state=fields.Selection([
        ('draft','Draft'),
         ('confirmed','Confirmed'),
         ('alumni','Alumni')
    ], string='status' , default='draft')


    def action_draft(self):
        for rec in self:
            rec.state='draft'
    
    def action_confirmed(self):
        for rec in self:
            rec.state='confirmed'

    def action_alumni(self):
        for rec in self:
            rec.state='alumni'
        
    
  
    
    
    # @api.model
    # def create(self, vals):
    #      student = super(student, self).create(vals)
         
         
    #      student.message_post(
    #          body="Student Has Created successfully"
    #          #there are other type also :- like message_type,subject
             
    #      )
        
    #      if not student.user_id:
    #          if not student.email:
    #              raise UserError(("Please enter an email for the student to create a login."))
    
    #          group_student = self.env.ref('training_student.group_student_user', raise_if_not_found=False)
    #          group_internal = self.env.ref('base.group_user', raise_if_not_found=False)
        
            
    #          user_vals = {
    #              'name': student.name,
    #              'login': student.email.lower(),
    #              'email': student.email.lower(),
    #              'password': '1234',
    #              'active': True,
    #              'groups_id': [(6, 0, [group_internal.id, group_student.id])],
    #          }
    #          new_user = self.env['res.users'].sudo().create(user_vals)
    #          student.user_id = new_user.id
    #      return student
    