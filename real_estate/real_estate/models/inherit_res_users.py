from odoo import fields, models

class InheritResUsers(models.Model):

	_inherit = "res.users"
    
	property_ids = fields.One2many(
	       "estate.property", "user_id", string="Properties", domain=[("state", "in", ["offer_accepted","sold"])]
	   )