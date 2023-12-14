from odoo import api, fields, models , exceptions
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta, time



class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Real Estate Property"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK (expected_price > 0)',
         'The expected price must be strictly positive.'),
        
    ]
   
    
    name = fields.Char(string ="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From",default=lambda self: fields.Datetime.today()+timedelta(days=90), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", copy=False, readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    img = fields.Image("Image")
    garden_orientation = fields.Selection(
        selection=[
            ("n", "North"),
            ("s", "South"),
            ("e", "East"),
            ("w", "West"),
        ],
        string="Garden Orientation",
    )
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
        compute="_compute_state",
        store=True
    )
    total_area =fields.Integer(string="Total Area" ,compute="_compute_total_area")
    best_price =fields.Integer(string="Best Price" , default=0.0 , compute="_compute_best_price") 

    active = fields.Boolean(string="Active", default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type" ,required=True)    
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags" ,domain="[('id', '=', False)]")    
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    user_id = fields.Many2one("res.users", string="Salesman" ,default = lambda self: self.env.user)
    color = fields.Integer(string="color")
    image = fields.Binary(string='Property Image')

    sequence = fields.Char(
        string="Sequence",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('estate.property.sequence')
    )
        

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for i in self:
            i.total_area = i.living_area + i.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):   
        print(self.offer_ids.partner_id)      
        max = 0
        values =self.mapped("offer_ids.price")
        for i in values:
            if i > max:
                max = i;

        self.best_price = max    


    @api.onchange("garden")
    def _onchange_garden(self):
        # print('\n\n\n\n\n\n', self.expected_price + self.selling_price)
        for i in self:
            if i.garden:
                i.garden_area=10
                i.garden_orientation="n"
            else:
                i.garden_area=0
                i.garden_orientation=False
    

    def action_sold(self):
        print('\n\n\n\n\n\n\n\n')
        if self.state == 'canceled':
            raise UserError("Canceled properties cannot be sold.")
        return self.write({"state": "sold"})   
        
    def action_cancel(self):
        if self.state == 'sold':
            raise ValidationError("Sold properties cannot be canceled")  
        return self.write({"state" : "canceled"})


    @api.constrains('selling_price')
    def _check_selling_price(self):
        for i in (self):
            if i.offer_ids:
                if i.selling_price < i.expected_price * 90 / 100 :
                    raise ValidationError("The selling price must be at least 90 percent of the expected price")


    @api.depends("offer_ids")
    def _compute_state(self):
        print("working state function")
        for i in self:
            if i.offer_ids:
               i.state = "offer_received" 

   
    @api.ondelete(at_uninstall=False)
    def function(self):
        for i in self:
            if i.state not in ['new', 'canceled']:
                raise exceptions.ValidationError("You can only delete properties with 'New' or 'Canceled' state.")



     ##########################################################
    # @api.depends("offer_ids")
    # def _compute_best_price(self):
    #     lst = []
    #     for i in self:
    #         i.best_price = 0
    #         if i.offer_ids:
    #             for j in i.offer_ids:
    #                 print(j.price)
    #                 lst.append(j.price)
    #             i.best_price = max(lst)
    ######################################################## 
    #      for prop in self:
    # prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0
    ########################################################
    # error code lucky try to do 
    # new = 0
    # for i in self.offer_ids:
    #     if new <i.price
    #        new = i.price
    # i.best_price = new  
    ########################################################
    # important code for understanding viru tecah us about accessing data from database
    #     lst = []
    # for i in self:
    #     i.best_price = 0
    #     if i.offer_ids:
    #         for j in i.offer_ids:
    #             print(j.partner_id.name)
    ##########################################################        

    ########################################
    # def action_do_something(self):
    #    for record in self:
    #        record.name = "Something"
    #    return True            
    # def action_sold(self):
    #    for i in self:
    #        if i.state == "new" && i.cancel == true
    ##########################################################    

     ################################################
    # crud method
    # @api.model
    # def unlink(self):
    #     for i in self:
    #         if i.state not in ['new', 'canceled']:
    #             raise ValidationError("Cannot delete properties with states other than 'New' or 'Canceled'.")
    #     # return super(EstateProperty, self).unlink()  
    #     return super().unlink()
    ################################################
    # @api.model
    # def ondelete(self, vals):
    #     # Add your custom business logic here
    #     # if 'state' in vals and vals['state'] not in ['new', 'canceled']:
    #     # if vals.get('state') not in ['new', 'canceled']:
    #     for i in self:
    #         if i.state not in ['new', 'canceled']:
    #             raise ValidationError("You can only delete properties with 'New' or 'Canceled' state.")
    #     # Call the parent create method to complete the creation
    #     return super(EstateProperty, self).unlink(vals) 
    ################################################ 
    # @api.ondelete(at_uninstall=False)
    # def unlink(self):
    #     for i in self:
    #         if i.state not in ['new', 'canceled']:
    #             raise exceptions.ValidationError("You can only delete properties with 'New' or 'Canceled' state.")
    #     return super(EstateProperty, self).unlink()
    ##########################################################

# <field name="group_project_stages"/>
#                                 <div class="content-group" attrs="{'invisible': [('group_project_stages', '=', False)]}">