from odoo import models, fields, api, exceptions
from datetime import datetime


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Doctor Appointment'

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment_date = fields.Datetime(string='Appointment Date and Time', required=True)
    diagnosis = fields.Many2one('hospital.diagnosis', string='Diagnosis')
    recommendations = fields.Text(string='Recommendations')
    is_done = fields.Boolean(string='Is Appointment Done', default=False)

    @api.constrains('doctor', 'appointment_date')
    def _check_duplicate_appointment(self):
        """Ensure there are no duplicate appointments for the same doctor at the same time."""
        for record in self:
            domain = [
                ('doctor', '=', record.doctor.id),
                ('appointment_date', '=', record.appointment_date),
                ('id', '!=', record.id)  # exclude the current record from the search
            ]
            conflicting_appointments = self.search_count(domain)
            if conflicting_appointments > 0:
                raise exceptions.ValidationError('An appointment with the same doctor at this time already exists.')

    @api.model
    def create(self, vals):
        """Prevent creation of appointments in the past."""
        if vals.get('appointment_date'):
            # Якщо значення дати вже є об'єктом типу datetime, конвертація не потрібна
            appointment_date = vals['appointment_date']
            if isinstance(appointment_date, str):
                appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d %H:%M:%S')

            if appointment_date < datetime.now():
                raise exceptions.ValidationError('You cannot create an appointment in the past.')
        return super(Appointment, self).create(vals)

    def write(self, vals):
        """Prevent modification of past or completed appointments."""
        for record in self:
            if record.is_done:
                raise exceptions.ValidationError('You cannot modify an appointment that is already done.')

            if 'appointment_date' in vals:
                appointment_date = vals['appointment_date']
                # Якщо значення дати є рядком, конвертуємо його
                if isinstance(appointment_date, str):
                    appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d %H:%M:%S')

                # Порівнюємо з поточною датою
                if appointment_date < datetime.now():
                    raise exceptions.ValidationError('You cannot change the appointment to a past date.')

        return super(Appointment, self).write(vals)
