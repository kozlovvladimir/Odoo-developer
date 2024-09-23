from odoo import models, fields, api, exceptions

class RescheduleAppointmentWizard(models.TransientModel):
    _name = 'reschedule.appointment.wizard'
    _description = 'Wizard to reschedule an appointment'

    appointment_id = fields.Many2one('hospital.appointment', string='Appointment', required=True)
    new_doctor_id = fields.Many2one('hospital.doctor', string='New Doctor')
    new_date = fields.Datetime(string='New Appointment Date')

    @api.constrains('new_date')
    def _check_future_date(self):
        """Ensure that the new date is in the future."""
        if self.new_date and self.new_date < fields.Datetime.now():
            raise exceptions.ValidationError("You cannot set the appointment in the past.")

    def reschedule_appointment(self):
        """Reschedule the appointment with new doctor or date."""
        if not self.new_doctor_id and not self.new_date:
            raise exceptions.UserError('You must provide a new doctor or a new date.')
        vals = {}
        if self.new_doctor_id:
            vals['doctor'] = self.new_doctor_id.id
        if self.new_date:
            vals['appointment_date'] = self.new_date
        self.appointment_id.write(vals)
        return True
