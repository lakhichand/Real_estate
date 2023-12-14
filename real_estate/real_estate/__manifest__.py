{
	'name': "Real Estate",
    'version': '16.0.0.1.0',
    'author': "Author Lucky",
    'category': 'Real Estate/Brokerage', 
    'description': """
    Description text
    """,
    "depends" : ["mail","website"],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/add_offer_view.xml',
        'views/estate_property_view.xml',
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_offer_view.xml",
        "views/inherit_res_users_view.xml",
        "report/estate_property_reports.xml",
        "report/estate_property_templates.xml",
        "controller/main_view.xml",
        
    ],

    "demo": [
        "demo/estate_property_type_data.xml",
        
        "demo/estate_property_data.xml",

        "demo/estate_property_offer_data.xml",
        # "demo/sequence_data.xml",


       
    ],

    'installable' :True,
    'application' :True,
    'auto_install':False,
    'pre_init_hook': '_pre_init_hook',
    'post_init_hook': '_post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}

