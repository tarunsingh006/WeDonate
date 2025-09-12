import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'organ_donation.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT setval('hospitals_user_id_seq', (SELECT COALESCE(MAX(id), 1) FROM hospitals_user));")
    cursor.execute("SELECT setval('donors_appointments_id_seq', (SELECT COALESCE(MAX(id), 1) FROM donors_appointments));")
    cursor.execute("SELECT setval('donors_donationrequests_id_seq', (SELECT COALESCE(MAX(id), 1) FROM donors_donationrequests));")
    
print("Sequences fixed successfully!")