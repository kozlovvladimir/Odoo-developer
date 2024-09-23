from odoo import models, fields, api, exceptions

class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'
    _inherit = 'hospital.person'  # Наслідує від загальної моделі Person

    name = fields.Char(string='Full Name', required=True)
    specialization = fields.Char(string='Specialization', required=True)
    intern = fields.Many2one('hospital.doctor', string="Intern")
    mentor = fields.Many2one('hospital.doctor', string="Mentor")

    @api.constrains('intern', 'mentor')
    def _check_mentor_intern(self):
        """Переконайтеся, що наставник і інтерн — це різні люди."""
        for record in self:
            if record.intern and record.intern == record.mentor:
                raise exceptions.ValidationError("The intern cannot be selected as their own mentor.")

    @api.model
    def create(self, vals):
        return super(Doctor, self).create(vals)

    def write(self, vals):
        return super(Doctor, self).write(vals)
