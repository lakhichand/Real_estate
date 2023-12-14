from odoo import fields, models , api


class EstatePropertyType(models.Model):

    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "sequence, name"
    _sql_constraints = [('check_name', 'unique(name)', 'The Name Must Be Unique')]

    
    name = fields.Char(string="Name" ,required=True)
    sequence = fields.Integer(string="Sequence" , default=10)
    color  = fields.Integer(string="Color Index")


    model_ids = fields.One2many("estate.property", "property_type_id", string="Properties")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    
    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")



    # @api.depends()
    # def _compute_offer_count(self):
    #     for i in self:
    #         if i.offer_ids:
    #             for y in i.offer_ids:
    #                 total_offer = y.mapped("property_type_id") 
    #                 self.offer_count += len(total_offer)


    @api.depends()
    def _compute_offer_count(self):
        for prop_type in self:
                offer_cal = self.env['estate.property.offer'].search_count([
                    ('property_id.state', '!=', 'canceled'),
                    ('property_type_id', '=', prop_type.id)
                ])
                prop_type.offer_count = offer_cal                
                
    ##########################################################
    # @api.depends()
    # def _compute_offer(self):
    #     for i in self:
    #         if i.offer_ids:
    #             total_offer = 0  
    #             for y in i.offer_ids:
    #                 total_offer += len(y.mapped("property_type_id"))  
    #             i.offer_count = total_offer  
    #         else:
    #             i.offer_count = 0  
    ##########################################################        
    # @api.depends()
    # def _compute_offer(self):
    #     for prop_type in self:
    #             offer_count = self.env['estate.property.offer'].search_count([
    #                 ('property_id.state', '!=', 'canceled'),
    #                 ('property_type_id', '=', prop_type.id)
    #             ])
    #             prop_type.offer_count = offer_count
    ##########################################################
    # @api.depends('offer_ids')
    # def _compute_offer_count(self):
    #     for property_type in self:
    #         property_type.offer_count = len(property_type.offer_ids)


    

