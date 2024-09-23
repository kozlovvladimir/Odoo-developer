from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'

    name = fields.Char(string='Name', required=True)

    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'The tag name must be unique.')
    ]
