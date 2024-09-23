from odoo import models, fields

class Person(models.Model):
    _name = 'hospital.person'
    _description = 'Person Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Full Name', required=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    image = fields.Binary(string='Photo')
