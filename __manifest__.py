# -*- coding: utf-8 -*-
{
    'name': """Unique Partner Reference, Product Barcode and Product Reference""",
    'summary': """Set the Reference (Code) on Partners and Product and generate it""",
    'description': """Set the Reference (Code) on Partners and Product and generate it""",
    'author': 'elblasy.app',
    'maintainer': 'elblasy.app',
    'website': 'https://elblasy.app',
    'email': 'app@elblasy.app',
    'support': 'app@elblasy.app',
    'license': 'OPL-1',
    'category': 'base',
    'version': '16.1.0.0',
    'depends': ['base', 'contacts', 'product', 'sale', 'sale_management'],

    'data': [
        'data/ir_sequence_data.xml',
        'views/product_config.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,

}
