from odoo import models, fields, api, exceptions

class DoctorSchedule(models.Model):
    _name = 'hospital.doctor.schedule'
    _description = 'Doctor Schedule'

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    date = fields.Date(string='Date', required=True)
    working_hours = fields.Float(string='Working Hours', required=True, help="Specify the working hours in a decimal format (e.g., 8.5 for 8:30 AM).")

    @api.constrains('doctor', 'date', 'working_hours')
    def _check_duplicate_working_hours(self):
        """Ensure that the working hours for a doctor on a given date do not overlap."""
        for record in self:
            domain = [
                ('doctor', '=', record.doctor.id),
                ('date', '=', record.date),
                ('id', '!=', record.id)  # exclude the current record from the search
            ]
            conflicting_schedule = self.search(domain)
            if conflicting_schedule:
                raise exceptions.ValidationError(f"The doctor already has working hours scheduled on {record.date}. Please choose another time.")
