# -*- coding: UTF-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api


class ShPurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    sh_sec_qty = fields.Float(
        "Secondary Qty",
        digits='Product Unit of Measure'
    )
    sh_sec_uom = fields.Many2one("uom.uom", 'Secondary UOM')
    sh_is_secondary_unit = fields.Boolean(
        "Related Sec Unit",
        related="product_id.sh_is_secondary_unit"
    )
    category_id = fields.Many2one(
        "uom.category",
        "Purchase UOM Category",
        related="product_uom.category_id"
    )
    from_sec_qty = fields.Boolean(default=False)
    from_product_qty = fields.Boolean(default=False)

    @api.onchange('product_qty', 'product_uom')
    def onchange_product_uom_qty_sh(self):
        if self and self.sh_is_secondary_unit and self.sh_sec_uom and not self.from_sec_qty:
            self.from_product_qty = True
            self.sh_sec_qty = self.product_uom._compute_quantity(
                self.product_qty, self.sh_sec_uom
            )

    @api.onchange('sh_sec_qty', 'sh_sec_uom')
    def onchange_sh_sec_qty_sh(self):
        if self and self.sh_is_secondary_unit and self.product_uom and not self.from_product_qty:
            self.from_sec_qty = True
            self.product_qty = self.sh_sec_uom._compute_quantity(
                self.sh_sec_qty, self.product_uom
            )

    @api.onchange('product_id')
    def onchange_secondary_uom(self):
        if self:
            for rec in self:
                if rec.product_id and rec.product_id.sh_is_secondary_unit and rec.product_id.uom_id:
                    rec.sh_sec_uom = rec.product_id.sh_secondary_uom.id
                elif not rec.product_id.sh_is_secondary_unit:
                    rec.sh_sec_uom = False
                    rec.sh_sec_qty = 0.0
