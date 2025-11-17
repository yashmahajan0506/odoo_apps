# from odoo import http
# from odoo.http import request
# import werkzeug

# class StudentQuickController(http.Controller):

#     @http.route('/student/new', type='http', auth='public', website=True)
#     def student_quick_form(self, **kw):
        
#         return request.render('custom_student_quick.student_quick_form_template', {})

#     @http.route('/student/new/create', type='http', auth='public', methods=['POST'], csrf=True, website=True)
#     def student_create(self, **post):
   
#         name = post.get('name')
#         email = post.get('email')
#         if not name:
#             return request.redirect('/student/new?error=Name+is+required')

       
#         student = request.env['student.student'].sudo().create({
#             'name': name,
#             'email': email or False,
#         })

       
#         redirect_url = f"/web#id={student.id}&model=student.student&view_type=form"
#         return werkzeug.utils.redirect(redirect_url)