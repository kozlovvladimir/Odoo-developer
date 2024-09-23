# -*- coding: utf-8 -*-
from . import hospital_person
from . import hospital_patient
from . import hospital_doctor
from . import hospital_disease_directory
from . import hospital_appointment
from . import hospital_doctor_schedule
from . import hospital_investigation
from . import hospital_sample_type
from . import hospital_doctor_history
from . import hospital_diagnosis
from . import hospital_disease_directory
from . import hospital_disease_type
from . import hospital_investigation_type
from . import hospital_disease
from . import hospital_disease_report
from . import hospital_disease_report_wizard

# Імпорт візардів з підпапки wizards
from .wizards import hospital_assign_new_doctor_wizard
from .wizards import hospital_reschedule_appointment_wizard
from .wizards import hospital_doctor_schedule_wizard