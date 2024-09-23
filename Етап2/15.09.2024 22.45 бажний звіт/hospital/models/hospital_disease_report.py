from odoo import models, fields, api


class DiseaseReport(models.Model):
    _name = 'hospital.disease.report'
    _description = 'Звіт по хворобам за місяць'

    disease_name = fields.Char(string="Хвороба")
    diagnosis_count = fields.Integer(string="Кількість діагнозів")

    @api.model
    def generate_report(self, start_date, end_date):
        # Пошук діагнозів за обраний період
        diagnoses = self.env['hospital.diagnosis'].search([
            ('date', '>=', start_date),
            ('date', '<=', end_date)
        ])
        diseases = {}

        # Підрахунок кількості діагнозів для кожної хвороби
        for diagnosis in diagnoses:
            disease_name = diagnosis.disease_id.name
            if disease_name in diseases:
                diseases[disease_name] += 1
            else:
                diseases[disease_name] = 1

        # Збір даних для створення записів звіту
        records = []
        for disease, count in diseases.items():
            records.append({
                'disease_name': disease,
                'diagnosis_count': count
            })

        # Створення записів у моделі hospital.disease.report
        if records:
            self.create(records)

        return True
