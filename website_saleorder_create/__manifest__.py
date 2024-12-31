# -*- coding: utf-8 -*-
{
    'name': "website_saleorder_create",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base' , 'website' , 'sale' , 'website_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/template_error_page.xml',
        'views/template_success_page.xml',
        'views/product_templates.xml'
    ],



    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

