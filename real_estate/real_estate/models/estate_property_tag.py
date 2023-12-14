from odoo import fields, models

class EstatePropertyTag(models.Model):

    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _order = "name"
   

    name = fields.Char(string="Name", required=True)
    # attribute = fields.Char(string="Attribute")
    color  = fields.Integer(string="Color Index")

    _sql_constraints = [('check_name', 'unique(name)', 'The Name Must Be Unique')]
  
    