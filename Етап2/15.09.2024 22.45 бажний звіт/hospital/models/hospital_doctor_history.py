from odoo import models, fields, api

DOCTOR_HISTORY_MODEL = 'hospital.doctor.history'

class DoctorHistory(models.Model):
    _name = DOCTOR_HISTORY_MODEL
    _description = 'Doctor Assignment History'

    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    assignment_date = fields.Date(string='Assignment Date', default=fields.Date.context_today, required=True)

class Patient(models.Model):
    _inherit = 'hospital.patient'

    doctor = fields.Many2one('hospital.doctor', string='Personal Doctor')

    @api.model
    def create(self, vals):
        """Override the create method to add doctor history on patient creation."""
        patient = super(Patient, self).create(vals)
        if vals.get('doctor'):
            self.env[DOCTOR_HISTORY_MODEL].create({
                'patient': patient.id,
                'doctor': vals['doctor'],
                'assignment_date': fields.Date.context_today(self)
            })
        return patient

    def write(self, vals):
        """Override the write method to track doctor changes in the history."""
        for record in self:
            if 'doctor' in vals and vals['doctor'] != record.doctor.id:
                self.env[DOCTOR_HISTORY_MODEL].create({
                    'patient': record.id,
                    'doctor': vals['doctor'],
                    'assignment_date': fields.Date.context_today(self)
                })
        return super(Patient, self).write(vals)
