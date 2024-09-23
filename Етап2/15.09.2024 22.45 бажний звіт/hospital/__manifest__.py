# -*- coding: utf-8 -*-
{
    'name': "hospital",
    'summary': "Module for managing hospital operations",
    'description': """
        Hospital management system for tracking doctors, patients, appointments, 
        diagnoses, investigations, and more.
    """,
    'author': "Your Name/Company",
    'website': "https://www.yourcompany.com",
    'category': 'Healthcare',
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],  # Додано 'mail'
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_menus.xml',
        'views/hospital_appointment.xml',
        'views/hospital_assign_new_doctor_wizard.xml',
        'views/hospital_diagnosis.xml',
        'views/hospital_disease_directory.xml',
        'views/hospital_disease_type.xml',
        'views/hospital_doctor.xml',
        'views/hospital_doctor_history.xml',
        'views/hospital_doctor_schedule.xml',
        'views/hospital_doctor_schedule_wizard.xml',
        'views/hospital_patient.xml',
        'views/hospital_person.xml',
        'views/hospital_reschedule_appointment_wizard.xml',
        'views/hospital_sample_type.xml',
        'views/hospital_investigation_type.xml',
        'views/hospital_investigation.xml',
        'views/hospital_disease.xml',
        'views/hospital_disease_report.xml',
        'views/hospital_report_disease_template.xml',
        'views/hospital_disease_report_wizard.xml',
    ],
}
