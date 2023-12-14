from odoo import models,Command

class EstateProperty(models.Model):

    _inherit = "estate.property"
    # _inherit = "estate.property.type"

    def action_sold(self):
        for i in self:
            vals = {
                "partner_id":i.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": 1,
                "name" : i.sequence,

                "invoice_line_ids" :[
                    Command.create({
                        # "product_id": 
                        "name": "lucky",
                        "quantity": "1",
                        "price_unit": i.selling_price * 6.0 / 100.0,
                    }),Command.create({
                        "name": "Administrative fees",
                        "quantity": 1.0,
                        "price_unit": 100.0,
                    })]}

        # dest = self.env["account.move"]
        new_record =  self.env["account.move"]
        new_record.create(vals)

        return super().action_sold()    