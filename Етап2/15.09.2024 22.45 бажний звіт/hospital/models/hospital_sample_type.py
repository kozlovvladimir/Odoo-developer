from odoo import models, fields

class SampleType(models.Model):
    _name = 'hospital.sample.type'
    _description = 'Sample Type'

    sample_type_name = fields.Char(string='Sample Type Name', required=True)
