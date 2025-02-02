# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

from odoo import fields, models


class ProductTemplate(models.Model):
    """Inherit Product Template Model"""
    _inherit = "product.template"

    allow_negative_stock_mrp = fields.Boolean(
        string="Allow Negative Stock",
        help="If this option is not active on this product nor on its "
             "product category and that this product is a stockable product, "
             "then the validation of the related stock moves will be blocked if "
             "the stock level becomes negative with the stock move.",
    )
