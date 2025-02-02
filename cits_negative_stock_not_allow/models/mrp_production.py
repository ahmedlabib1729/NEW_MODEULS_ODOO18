# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo.exceptions import ValidationError
from odoo import models, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        for line in self.move_raw_ids:
            product = line.product_id
            quantity = line.product_uom_qty
            if product.allow_negative_stock_mrp:
                continue
            quant_obj = self.env['stock.quant'].search([
                ('product_id', '=', product.id),
                ('on_hand', '=', True),
            ])
            quant_total_avail_quantity = sum(quant_obj.mapped('inventory_quantity_auto_apply'))
            if quantity > quant_total_avail_quantity:
                raise ValidationError(
                    _("You cannot validate delivery for the product '%s' because "
                      "the stock level would become negative and negative stock "
                      "is not allowed for this product.")
                    % (product.display_name)
                )
        return res
