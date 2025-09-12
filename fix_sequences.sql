-- Fix sequence for hospitals_user table
SELECT setval('hospitals_user_id_seq', (SELECT MAX(id) FROM hospitals_user));

-- Fix sequence for donors_appointments table  
SELECT setval('donors_appointments_id_seq', (SELECT MAX(id) FROM donors_appointments));

-- Fix sequence for donors_donationrequests table
SELECT setval('donors_donationrequests_id_seq', (SELECT MAX(id) FROM donors_donationrequests));