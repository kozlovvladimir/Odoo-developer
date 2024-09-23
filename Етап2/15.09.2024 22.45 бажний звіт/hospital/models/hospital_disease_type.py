from odoo import models, fields

class DiseaseType(models.Model):
    _name = 'hospital.disease.type'
    _description = 'Disease Type'

    name = fields.Char(string='Disease Type Name', required=True)
