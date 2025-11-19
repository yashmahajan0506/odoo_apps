from odoo import models, fields,api 
import re 
class JobApplication(models.Model):
    
            _name = 'my_job_portal.job.application'
            _description = 'Job Application'
        
            applicant_name = fields.Char(required=True)
            email = fields.Char(required=True)
            phone = fields.Char()
            cv_attachment = fields.Binary("CV Attachment")
            cv_filename = fields.Char()
        
            job_id = fields.Many2one(
                'my_job_portal.job.position',
                string="Applied Job",
                required=True
            )
        
            status = fields.Selection([
                ('draft', 'Draft'),
                ('submitted', 'Submitted'),
                ('shortlisted', 'Shortlisted'),
                ('rejected', 'Rejected'),
                ('hired', 'Hired'),
            ], default='draft', required=True)
            
            # def action_shortlist(self):
            #      for record in self:
            #          record.status = 'shortlisted'  # Change status

            #          # Send email using the template
            #          template = self.env.ref('my_job_portal.mail_template_job_application_shortlisted')
            #          template.send_mail(record.id, force_send=True)

                # SEND EMAIL
                # template = self.env.ref("my_job_portal.mail_template_job_application_shortlisted")
                # template.send_mail(rec.id, force_send=True)

                # # SHOW POPUP SERVER ACTION
                # action = self.env.ref("my_job_portal.server_action_shortlist_email")
                # return action.with_context(active_id=rec.id).run()



            def action_reject(self):
                for rec in self:
                    rec.status  = "rejected"
                    
            def action_hire(self):
                for rec in self:
                    rec.status  = "hired"
    
            email_domain = fields.Char(
                string="Email Domain",
                readonly=True,
                store=True,
                help="Automatically extracted domain from email (e.g., gmail.com)"
                )       
        
            application_ids = fields.One2many(
                 string='Applications',
                 comodel_name='my_job_portal.job.application',
                 inverse_name='job_id',  
                 )

  
            application_count = fields.Integer(
                string='Application Count',
                compute='_compute_application_count',
                store=True,  
                )

            @api.depends('application_ids')
            def _compute_application_count(self):
                 for record in self:
                     record.application_count = len(record.application_ids)
            
            def action_shortlist(self):
             for record in self:
                 record.status = 'shortlisted'

                 
                 template = self.env.ref('my_job_portal.mail_template_job_application_shortlisted')
                 template.send_mail(record.id, force_send=True)
          
            @api.onchange('email')
            def _onchange_email(self):
                if self.email:

                    match = re.search(r'@([\w\.-]+)', self.email.lower())
                    if match:
                        self.email_domain = match.group(1)
                    else:
                        self.email_domain = False
                else:
                    self.email_domain = False
            
            
    # @api.depends()
    # def application_num_count():
