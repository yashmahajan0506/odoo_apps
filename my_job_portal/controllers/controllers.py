# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import base64


class WebsiteJobs(http.Controller):


        @http.route(['/jobs'], type='http', auth="public", website=True)
        def job_list(self, **kw):
            jobs = request.env['my_job_portal.job.position'].sudo().search([('active', '=', True)])
            return request.render("my_job_portal.job_list_template", {"jobs": jobs})


        @http.route(['/jobs/apply/<int:job_id>'], type='http', auth='public', website=True)
        def apply_form(self, job_id, **kwargs):

            Job = request.env['my_job_portal.job.position'].sudo().browse(job_id)

          
            if not Job or not Job.active:
                return request.redirect('/jobs')

            return request.render('my_job_portal.job_apply_template', {
                'job': Job,
            })


        @http.route(['/jobs/apply/submit'], type='http', auth='public', methods=['POST'], website=True)
        def apply_submit(self, **post):

            JobObj = request.env['my_job_portal.job.position'].sudo().browse(int(post.get("job_id")))

         
            if not JobObj or not JobObj.active:
                return request.redirect('/jobs')

          
            cv_file = post.get('cv')
            cv_binary = False
            cv_filename = False

            if cv_file:
                cv_binary = base64.b64encode(cv_file.read())
                cv_filename = cv_file.filename

          
            app = request.env['my_job_portal.job.application'].sudo().create({
                'applicant_name': post.get('name'),
                'email': post.get('email'),
                'phone': post.get('phone'),
                'cv_attachment': cv_binary,
                'cv_filename': cv_filename,
                'job_id': int(post.get('job_id')),
                'status': 'submitted',
            })

     
            return request.render('my_job_portal.job_apply_success', {
                'application': app,
            })