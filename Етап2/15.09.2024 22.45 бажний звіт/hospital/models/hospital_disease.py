from odoo import models, fields

class Disease(models.Model):
    _name = 'hospital.disease'
    _description = 'Disease Directory'

    name = fields.Char(string='Disease Name', required=True)
    disease_type = fields.Many2one('hospital.disease.type', string='Disease Type')
    description = fields.Text(string='Description')
