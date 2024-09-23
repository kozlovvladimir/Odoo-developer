from odoo import models, fields, api, exceptions

class AssignNewDoctorWizard(models.TransientModel):
    _name = 'assign.new.doctor.wizard'
    _description = 'Wizard to reassign patients to a new doctor'

    doctor_id = fields.Many2one('hospital.doctor', string='New Doctor', required=True)
    patient_ids = fields.Many2many('hospital.patient', string='Patients')

    def assign_doctor(self):
        """Mass update the doctor for the selected patients."""
        if not self.patient_ids:
            raise exceptions.UserError('You must select at least one patient.')
        for patient in self.patient_ids:
            patient.write({'doctor': self.doctor_id.id})
        return True
