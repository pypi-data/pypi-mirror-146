from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def write(self, values):
        if 'price_unit' in values:
            self.product_id.write({"label_to_be_printed": True})
        return super(PurchaseOrderLine, self).write(values)
