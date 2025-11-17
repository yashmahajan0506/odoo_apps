from odoo import fields, models, api

class Teacher(models.Model):
    _name = 'training.teacher'
    _description = 'Training Teacher'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    expertise = fields.Char(string='Expertise')
    student_ids = fields.Many2many('student.student', string='Students')
    student_count = fields.Integer(string='Student Count', compute='_compute_student_count')

    @api.depends('student_ids')
    def _compute_student_count(self):
        for rec in self:
            rec.student_count = len(rec.student_ids)

    @api.model
    def create(self, vals):
        record = super(Teacher, self).create(vals)
        if not record.user_id:
            user = self.env['res.users'].create({
                'name': record.name,
                'login': record.name.lower().replace(' ', '_') + '@teacher.com',
                'groups_id': [(6, 0, [self.env.ref('training_student.group_teacher_user').id])]
            })
            record.user_id = user.id
        return record

        