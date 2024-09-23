from odoo import models, fields, api, exceptions


class Diagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Diagnosis'

    # Поле id буде додане Odoo автоматично
    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    disease = fields.Many2one('hospital.disease', string='Disease', required=True)
    treatment = fields.Text(string='Treatment')
    diagnosis_date = fields.Date(string='Diagnosis Date', default=fields.Date.context_today, required=True)
    mentor_comment = fields.Text(string="Mentor's Comment", help="Comments from the mentor if the doctor is an intern.")

    @api.model
    def create(self, vals):
        # Отримання лікаря, вказаного в діагнозі
        doctor_id = vals.get('doctor')
        doctor = self.env['hospital.doctor'].browse(doctor_id)

        # Перевірка: якщо лікар є інтерном, ментор має залишити коментар
        if doctor.intern and not vals.get('mentor_comment'):
            raise exceptions.ValidationError("Mentor's comment is required for an intern's diagnosis.")

        # Створення запису діагнозу
        return super(Diagnosis, self).create(vals)

    def write(self, vals):
        # Якщо в оновленні передано поле doctor, тоді виконуємо перевірку
        if 'doctor' in vals:
            doctor_id = vals.get('doctor')
            doctor = self.env['hospital.doctor'].browse(doctor_id)

            # Перевірка: якщо лікар є інтерном, ментор має залишити коментар
            if doctor.intern and not vals.get('mentor_comment'):
                raise exceptions.ValidationError("Mentor's comment is required for an intern's diagnosis.")

        # Оновлення запису діагнозу
        return super(Diagnosis, self).write(vals)
