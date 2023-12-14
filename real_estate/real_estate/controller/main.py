from odoo import http
from odoo.http import request

class Academy(http.Controller):

    # @http.route('/academy/academy/', auth='public')
    # def index(self, **kw):
    #     return http.request.render('real_estate.index', {
    #         'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
    #     })



     # @http.route('/academy/academy/', auth='public', website=True)
     # def index(self, **kw):
     #     Teachers = http.request.env['estate.property']
     #     return http.request.render('real_estate.index', {
     #         'teachers': Teachers.search([])
     #     })


    @http.route('/lucky', auth='public', website=True)
    def index(self, **kw):
        Props = http.request.env['estate.property']
        return http.request.render('real_estate.website_support', {
            'props': Props.search([])
        }) 
