from odoo import models, fields


class JobPosition(models.Model):
    _name = "my_job_portal.job.position"
    _description = 'Job Position'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    
    name = fields.Char(string='Job Title', required=True, tracking=True)
    description = fields.Html(string='Description')
    department_id = fields.Many2one('hr.department', string='Department')
    total_openings = fields.Integer(string='Total Openings', default=1)
    active = fields.Boolean(string='Active', default=True)