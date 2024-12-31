import logging
from odoo import http
from odoo.http import request
import json

_logger = logging.getLogger(__name__)

class WebsiteSaleOrder(http.Controller):

    @http.route(["/order/page"], type="http", auth="public", website=True)
    def order_page(self, **kwargs):
        """
        Render the simplified order page with available products.
        Includes search and category filtering functionality.
        """
        try:
            search_query = kwargs.get("search", "").strip()
            category_id = kwargs.get("category_id")

            domain = [
                ("sale_ok", "=", True),  # Ensure product is available for sale
                ("website_published", "=", True)  # Ensure product is published on the website
            ]

            if search_query:
                domain.append(("name", "ilike", search_query))
            if category_id and category_id.isdigit():
                domain.append(("public_categ_ids", "in", [int(category_id)]))

            products = request.env["product.template"].sudo().search(domain)
            categories = request.env["product.public.category"].sudo().search([])

            return request.render("website_saleorder_create.template_homepage", {
                "products": products,
                "categories": categories,
                "current_category": int(category_id) if category_id and category_id.isdigit() else None,
                "search_query": search_query
            })
        except Exception as e:
            _logger.error("Error loading products: %s", e)
            return request.render("website_saleorder_create.template_error_page", {
                "error_message": str(e)
            })

    @http.route(["/order/search"], type="json", auth="public", website=True)
    def search_products(self, search_query=None, category_id=None):
        """
        Handle AJAX search and filter requests.
        """
        try:
            _logger.debug("Search Query: %s, Category ID: %s", search_query, category_id)

            domain = [
                ("sale_ok", "=", True),
                ("website_published", "=", True)
            ]

            if search_query:
                domain.append(("name", "ilike", search_query))
            if category_id and category_id.isdigit():
                domain.append(("public_categ_ids", "in", [int(category_id)]))

            products = request.env["product.template"].sudo().search(domain)

            product_data = [{
                "id": product.id,
                "name": product.name,
                "price": product.list_price,
            } for product in products]

            return {"products": product_data}  # Ensure JSON format
        except Exception as e:
            _logger.error("Error in AJAX search: %s", e)
            return {"error": str(e)}

    @http.route(["/order/submit"], type="http", auth="public", methods=["POST"], website=True, csrf=False)
    def submit_order(self, **kwargs):
        """
        Handle the submission of a simplified order.
        """
        try:
            customer_name = kwargs.get("customer_name")
            customer_phone = kwargs.get("customer_phone")
            product_ids = request.httprequest.form.getlist("product_id")
            quantities = request.httprequest.form.getlist("quantity")

            if not customer_name or not customer_phone:
                raise ValueError("Customer name and phone are required.")

            # Process all products and quantities
            order_lines = []

            for product_id, quantity in zip(product_ids, quantities):
                product_id = product_id.strip()
                quantity = quantity.strip()

                if product_id and product_id.isdigit() and quantity.isdigit() and int(quantity) > 0:
                    order_lines.append((0, 0, {
                        "product_id": int(product_id),
                        "product_uom_qty": int(quantity),
                    }))
                else:
                    _logger.warning(
                        "Skipping invalid or empty entry: product_id=%s, quantity=%s", product_id, quantity
                    )

            if not order_lines:
                raise ValueError("No valid products selected for the order.")

            # Create or find the customer
            partner = request.env["res.partner"].sudo().search([('name', '=', customer_name), ('phone', '=', customer_phone)], limit=1)
            if not partner:
                partner = request.env["res.partner"].sudo().create({
                    "name": customer_name,
                    "phone": customer_phone,
                })

            # Create the sale order
            sale_order = request.env["sale.order"].sudo().create({
                "partner_id": partner.id,
                "order_line": order_lines
            })

            return request.render("website_saleorder_create.template_success_page", {
                "sale_order": sale_order
            })
        except ValueError as ve:
            _logger.error("Validation Error: %s", ve)
            return request.render("website_saleorder_create.template_error_page", {
                "error_message": str(ve)
            })
        except Exception as e:
            _logger.error("Error submitting order: %s", e)
            return request.render("website_saleorder_create.template_error_page", {
                "error_message": str(e)
            })
