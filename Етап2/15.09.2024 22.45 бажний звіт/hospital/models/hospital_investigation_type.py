from odoo import models, fields

class InvestigationType(models.Model):
    _name = 'hospital.investigation.type'
    _description = 'Investigation Type'

    name = fields.Char(string='Investigation Type', required=True)
    description = fields.Text(string='Description')
