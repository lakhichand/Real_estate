{
	'name': "Estate Account",
    'version': '16.0.0.1.0',
    'category': 'Accounting',
    'description': """
    Description text
    """,
    'depends': [
        'real_estate',
        'account'
       
    ],

    "data": [
        'report/estate_property_templates_inherit.xml',

    ],

    'installable' :True,
    'application' :True,
    'auto_install':True,
}
