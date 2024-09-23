from odoo import models, fields

class EstatePropertyResUsers(models.Model):
    _inherit = 'res.users'  # Наслідуємо існуючу модель res.users

    property_ids = fields.One2many(
        'estate.property',  # Модель нерухомості (estate.property)
        'salesman_id',  # Поле в estate.property, яке пов'язує нерухомість з користувачем
        string='Properties',
        domain=[('state', 'in', ['new', 'offer_received'])]  # Домен для фільтрації доступних об'єктів
    )
