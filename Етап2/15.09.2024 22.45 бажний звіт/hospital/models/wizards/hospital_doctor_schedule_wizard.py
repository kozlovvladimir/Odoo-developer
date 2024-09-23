from odoo import models, fields

class DoctorScheduleWizard(models.TransientModel):
    _name = 'doctor.schedule.wizard'
    _description = 'Wizard to set up doctor schedule for even/odd weeks'

    # Додаємо _rec_name для відображення назви запису
    _rec_name = 'schedule_type'

    doctor_id = fields.Many2one('hospital.doctor', string='Doctor', required=True)

    # Поле для вибору типу розкладу
    schedule_type = fields.Selection([
        ('even', 'Even Week'),
        ('odd', 'Odd Week'),
        ('custom', 'Custom Schedule')
    ], string='Schedule Type', required=True)

    is_even_week = fields.Boolean(string='Even Week Schedule', default=False)
    week_schedule = fields.One2many('doctor.week.schedule.line', 'wizard_id', string='Weekly Schedule')

    def create_schedule(self):
        """Create a schedule for the doctor for even, odd, or custom weeks."""
        for line in self.week_schedule:
            self.env['hospital.doctor.schedule'].create({
                'doctor': self.doctor_id.id,
                'date': line.date,
                'working_hours': line.working_hours
            })
        return True

class DoctorWeekScheduleLine(models.TransientModel):
    _name = 'doctor.week.schedule.line'
    _description = 'Line for doctor weekly schedule'

    wizard_id = fields.Many2one('doctor.schedule.wizard', string='Wizard')
    date = fields.Date(string='Date', required=True)
    working_hours = fields.Float(string='Working Hours', required=True)
