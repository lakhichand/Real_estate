from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare
from odoo.exceptions import UserError, ValidationError



class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [("check_price", "CHECK(price > 0)", "The price must be strictly positive"),]


    
    price = fields.Float("Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)


    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
        default=False,
    )

   
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True )
    
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", string="Property Type", store=True
    )

    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")


    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                date = offer.create_date.date()
            else:
                date = fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                date = offer.create_date.date()
                offer.date_deadline = date + relativedelta(days=offer.validity)
            else:
                offer.date_deadline = False        
    


    def action_accept(self):

        for i in self:
            i.write({"status" :"accepted"})
            if i.status == "accepted":
                i.property_id.write({ 
                    "state": "offer_accepted",
                    "selling_price": i.price,
                    "buyer_id": i.partner_id.id,
                    })

        
    def action_refuse(self):
        for i in self:
            i.write({"status" :"refused"})

       
    @api.model
    def create(self, vals):
        hii = super().create(vals)
        propertyid = vals.get('property_id')
        property_record = self.env['estate.property'].search([('id','=',propertyid)])
        if  vals['price'] < property_record.best_price:
            raise ValidationError(f"the offer must be higher than {property_record.best_price}")
        return hii






    # def unlink(self, vals):
    #     hello = super().unlink(vals)
    #     print('\n\n\n\n')

    #     print(hello)
    #     print('\n\n\n\n')

    #     return hello   

    # def write(self, vals):
    #     by = super().write(vals)
    #     print('\n\n\n\n')

    #     print(by)
    #     print('\n\n\n\n')

    #     return by       
















  

    ##########################################################  
        # for rec in rec.property_id.offer_ids.filtered(lambda x : x.status != 'accepted'):
        #     rec.status == 'refused'
        ##########################################################
        # for rec in self:
        #     rec.status = "accepted"
        #     for data in (rec.property_id.offer_ids.filtered(lambda x : x.status != 'accepted')):
        #         data.status = "refused"
        ##########################################################

     #######################################
        # if self.status =="refused":
        #     self.property_id.write({
        #         "state": "canceled",
        #         "selling_price": 0,
        #         "buyer_id":False })
        ######################################
        # print(self.("property_id"))
        # for i in self:
        # if i.offer_ids:
        #       for j in i.offer_ids:
        #           print(j.partner_id.name)
        ##########################################################    

      ##################################################
    # @api.model
    # def create(self, vals):
    #     res = super(EstatePropertyOffer, self).create(vals)

    #     for i in res :
    #         print(i.partner_id.name) 

    #     return res    

    #################################################  



 # check it throws error when offer add
    # @api.depends("create_date", "validity")
    # def _compute_date_deadline(self):
    #     for offer in self:
    #         if offer.create_date:
    #             date = offer.create_date.date()
    #         else:
    #             print("no create date")
    #             create_date= fields.Date.today()
    #             offer.date_deadline = create_date + relativedelta(days=offer.validity)

    # def _inverse_date_deadline(self):
    #     for offer in self:
    #         if offer.create_date :
    #             date = offer.create_date.date()
    #             offer.date_deadline = (offer.date_deadline - date).days
    #         else :
    #             fields.Date.today()   

    ###############################################


    # def _inverse_date_deadline(self):
    #     for offer in self:
    #         if offer.create_date :
    #             date = offer.create_date.date()
    #             offer.validity = (offer.date_deadline - date).days
    #         else :
    #             fields.Date.today()

    ################################################

      #     for x in i.property_id.offer_ids:
            #         if x.id != i.id:
            #             x.write({"status": "refused"})
            #         else:
            #             x.write({"status": "accepted"})
            # else:
            #     offer.write({"status": "refused"})

            


