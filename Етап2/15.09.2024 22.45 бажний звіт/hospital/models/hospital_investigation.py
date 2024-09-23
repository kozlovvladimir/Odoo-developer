from odoo import models, fields

class Investigation(models.Model):
    _name = 'hospital.investigation'
    _description = 'Medical Investigation'

    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    investigation_type = fields.Many2one('hospital.investigation.type', string='Investigation Type', required=True)
    doctor = fields.Many2one('hospital.doctor', string='Assigned Doctor', required=True)
    sample = fields.Many2one('hospital.sample.type', string='Sample Type', required=True)
    conclusions = fields.Text(string='Conclusions')
    investigation_date = fields.Datetime(string='Investigation Date', default=fields.Datetime.now, required=True)
