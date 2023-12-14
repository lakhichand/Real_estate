from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class AddOffer(models.TransientModel):

    _name = "add.offer"
    _description = "add offer to the properties"

    
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

    date_deadline = fields.Date(string="Deadline")

   
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)

    property_ids = fields.Many2many("estate.property", string="Properties")

    def add_offer_action(self):

        active_ids = self._context.get("active_ids")
        print("\n\n\n\n\n\n\n\n\n,hello");
        print(active_ids)
        print(self)
        print("\n\n\n\n\n\n\n\n\n,hello");
        
        for property_id in active_ids:
            property_record = self.env["estate.property"].browse(property_id)
            # print(property_record)
            
            offer_vals = {
                "price": self.price,
                "validity": self.validity,
                "status": self.status,
                "date_deadline": self.date_deadline,
                "partner_id": self.partner_id.id,
                "property_id": property_id,
            }

            self.env["estate.property.offer"].create(offer_vals)
            
            # property_record.write({
            #     "state": "offer_received",
            #     "best_price": self.price,
            # })

	    

        # offer_vals_list = []

        # for i in self.property_ids:
        #     offer_val = {
        #         'price': i.expected_price,
        #         'partner_id': i.buyer_id.id,
        #         'validity': i.validity,  # You can set the validity as needed
        #         'date_deadline': i.date_deadline,  # You can set the date deadline as needed
        #         'status': i.status,  # You can set the initial status as needed
        #         'property_id': i.id,
        #     }


    
        # def add_offer_action(self):

            # active_id = self._context.get('active_ids')
            # print(active_id)
            # update = self.env['estate.property'].browse(active_id)
            # print(update)


           
