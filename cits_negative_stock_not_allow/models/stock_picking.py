# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo.exceptions import ValidationError
from odoo import models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """
        This method ensures that stock levels are checked before validating
        stock moves to prevent the creation of invoices for products if their
        stock levels would become negative, and if the product does not allow
        negative stock levels.
        """
        for line in self.move_ids_without_package:
            product = line.product_id
            quantity = line.product_uom_qty
            if product.allow_negative_stock_mrp or self.picking_type_code == 'incoming':
                continue
            if product.tracking == 'lot':
                move = line.mapped('move_line_ids')
                valid_move = move.filtered(
                    lambda d: d.lot_id.product_qty > d.quantity)
                qty = sum(valid_move.mapped('lot_id').mapped('product_qty'))
                if quantity > qty:
                    raise ValidationError(
                        _("You cannot validate delivery for the product '%s' because "
                          "the stock level would become negative and negative stock "
                          "is not allowed for this product." % product.display_name))
            else:
                if quantity > product.qty_available:
                    raise ValidationError(
                        _("You cannot validate delivery for the product '%s' because "
                          "the stock level would become negative and negative stock "
                          "is not allowed for this product." % product.display_name))

        return super(StockPicking, self).button_validate()
