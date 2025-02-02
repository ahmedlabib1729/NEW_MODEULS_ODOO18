# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).           #
# See LICENSE file for full copyright and licensing details.                 #
#                                                                            #
##############################################################################

{
    'name': "Negative stock not allowed",
    'summary': "Negative stock not allowed | Non-negative Inventory | Zero Inventory | No Negative Stock | Stock Availability Limit",
    'description': """This module used to disallow negative stock from confirm Delivery.""",
    'author': 'Caret IT Solutions Pvt. Ltd.',
    'category': 'Sales',
    'website': 'https://www.caretit.com',
    'support': 'sales@caretit.com',
    'version': '18.0.0.1',
    'license': 'LGPL-3',
    'depends': ['mrp', 'sale_management', 'product'],
    'data': [
        'views/product_template_views.xml'
    ],
    'images': ['static/description/banner.png'],
    'price': 29.00,
    'currency': 'EUR',
    "installable": True,
    "auto_install": False,
    "application": True,
}
