from odoo import models, fields, api

class DiseaseReportWizard(models.TransientModel):
    _name = 'disease.report.wizard'
    _description = 'Wizard for Disease Report by Doctor'

    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    def generate_report(self):
        # Підготовка даних для генерації звіту
        data = {
            'doctor_id': self.doctor_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
        }
        # Виклик шаблону звіту
        return self.env.ref('hospital.disease_report_action').report_action(self, data=data)
