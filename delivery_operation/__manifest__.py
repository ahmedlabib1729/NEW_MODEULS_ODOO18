{
    'name': 'Delivery Operation',
    'version': '1.0',
    'category': 'Operations',
    'depends': ['base', 'sale', 'hr', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'data/sequence.xml',
        'views/delivery_operation_views.xml',
        'views/city.xml',
        'wizard/payment_wizard_view.xml',
    ],
    'installable': True,
    'application': True,
}
