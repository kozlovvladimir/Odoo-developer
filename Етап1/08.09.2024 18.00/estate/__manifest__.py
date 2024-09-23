{
    'name': 'Real Estate',
    'version': '1.0',
    'category': 'Uncategorized',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',  # Файл з правами доступу
        'views/estate_property_type_views.xml',  # Подання для моделі estate.property.type
        'views/estate_property_views.xml',  # Подання для моделі estate.property
        'views/estate_property_offer_views.xml',  # Подання для моделі estate.property.offer
        'views/estate_property_tag_views.xml',  # Подання для моделі estate.property.tag
        'views/estate_property_res_users_views.xml',
        'views/estate_menus.xml',  # Меню модуля
    ],
    'installable': True,  # Модуль може бути встановлений
    'application': True,  # Модуль є додатком (відображається у головному меню)
    'license': 'LGPL-3',  # Ліцензія модуля
}
