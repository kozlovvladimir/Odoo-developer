from odoo import models, fields, api
from datetime import date

class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient'
    _inherit = 'hospital.person'  # Наслідує від загальної моделі Person

    # Поле для дати народження
    birth_date = fields.Date(string='Date of Birth', required=True)

    # Поле для віку пацієнта (обчислюється автоматично)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    # Дані паспорта
    passport_data = fields.Char(string='Passport Data')

    # Поле для вибору пов'язаного контакту (з інших пацієнтів)
    related_contact = fields.Many2one(
        'hospital.patient',
        string='Related Contact',
        help="Select a related contact from other patients",
        domain="[('id', '!=', id)]",  # Не включати самого пацієнта
        context={'no_create': True}  # Правильна передача словника для context
    )

    # Лікар, відповідальний за пацієнта
    doctor = fields.Many2one('hospital.doctor', string='Personal Doctor')

    @api.depends('birth_date')
    def _compute_age(self):
        """Автоматично обчислює вік на основі дати народження."""
        for record in self:
            if record.birth_date:
                today = date.today()
                birth_date = record.birth_date
                # Обчислення віку пацієнта на основі дати народження
                record.age = today.year - birth_date.year - (
                    (today.month, today.day) < (birth_date.month, birth_date.day)
                )
            else:
                record.age = 0
