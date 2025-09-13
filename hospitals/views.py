from django.shortcuts import render
import pdfkit
from django.conf import settings
from django.db.models import Q
from donors.models import DonationRequests, Appointments
import json
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import string
import secrets
import ast
import random
from donors.models import DonationRequests, Appointments
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import StringIO, BytesIO
from xhtml2pdf import pisa
from pypdf import PdfWriter, PdfReader


# Create your views here.


@login_required
def home(request):
    if request.POST:
        pass
    return render(request, "hospital-main-page.html")


def search_donations(request):
    if request.POST:
        pass
    else:
        search_keyword = request.GET.get('keyword', '')
        status = "Approved"
        # Search for donations based on organ type/blood type/donor name
        donations = DonationRequests.objects.filter((Q(organ_type__iexact=search_keyword) | Q(blood_type__startswith=search_keyword) | Q(donor__first_name__iexact=search_keyword) | Q(donor__last_name__iexact=search_keyword)) & Q(donation_status__iexact=status))
        print(donations)
        # Search for donations based on donation id
        if not donations:
            if search_keyword.isdigit():
                donations = DonationRequests.objects.filter(Q(id=int(search_keyword)) & Q(donation_status__iexact=status))

        donation_list = []
        for donation in donations:
            print(donation.donation_status)
            temp_dict = {}
            temp_dict["donor"] = f"{donation.donor.first_name} {donation.donor.last_name}"
            temp_dict["organ"] = donation.organ_type
            temp_dict["donation_id"] = donation.id
            temp_dict["blood_group"] = donation.blood_type
            donation_list.append(temp_dict)
        search_list = json.dumps(donation_list)
        print("hi", search_list)
        return HttpResponse(search_list)


def search_donation_details(request):
    if request.POST:
        pass
    else:
        # Fetching donation details
        donation_id_from_UI = request.GET.get('donation_id', '')
        donations = Appointments.objects.filter(Q(donation_request__id=int(donation_id_from_UI)))
        donation_list = []
        for donation in donations:
            temp_dict = {}
            # Donor details
            temp_dict["user_name"] = donation.donation_request.donor.username
            temp_dict["first_name"] = donation.donation_request.donor.first_name
            temp_dict["last_name"] = donation.donation_request.donor.last_name
            temp_dict["email"] = donation.donation_request.donor.email
            temp_dict["contact_number"] = donation.donation_request.donor.contact_number
            temp_dict["city"] = donation.donation_request.donor.city
            temp_dict["country"] = donation.donation_request.donor.country
            temp_dict["province"] = donation.donation_request.donor.province
            # Donation details
            temp_dict["organ"] = donation.donation_request.organ_type
            temp_dict["donation_id"] = donation.donation_request.id
            temp_dict["blood_group"] = donation.donation_request.blood_type
            temp_dict["donation_status"] = donation.donation_request.donation_status
            temp_dict["approved_by"] = donation.hospital.hospital_name
            temp_dict["family_member_name"] = donation.donation_request.family_relation_name
            temp_dict["family_member_relation"] = donation.donation_request.family_relation
            temp_dict["family_member_contact"] = donation.donation_request.family_contact_number
            donation_list.append(temp_dict)
        donation_details = json.dumps(donation_list)

        return HttpResponse(donation_details)


@login_required
def fetch_appointments(request):
    if request.POST:
        pass
    else:
        # Fetching appointment details
        print(f"fetching appointments from db for hospital ID: {request.user.id}")
        print(f"Hospital name: {request.user.hospital_name}")
        
        # Debug: Check all appointments first
        all_appointments = Appointments.objects.all()
        print(f"Total appointments in database: {all_appointments.count()}")
        for apt in all_appointments:
            print(f"Appointment ID: {apt.id}, Hospital: {apt.hospital.hospital_name} (ID: {apt.hospital.id}), Status: {apt.appointment_status}")
        
        # Get all appointments for this hospital (not just pending)
        all_hospital_appointments = Appointments.objects.filter(hospital__id=request.user.id)
        print(f"All appointments for this hospital: {all_hospital_appointments.count()}")
        
        # Get pending appointments for this hospital
        status = "Pending"
        appointments = Appointments.objects.filter(hospital__id=request.user.id, appointment_status=status)
        print(f"Pending appointments count: {appointments.count()}")
        print(f"Query: hospital_id={request.user.id}, status={status}")
        
        appointment_list = []
        for appointment in appointments:
            temp_dict = {}
            temp_dict["first_name"] = appointment.donation_request.donor.first_name
            temp_dict["last_name"] = appointment.donation_request.donor.last_name
            # Donation details
            temp_dict["organ"] = appointment.donation_request.organ_type
            temp_dict["donation_id"] = appointment.donation_request.id
            temp_dict["blood_group"] = appointment.donation_request.blood_type
            # Appointment details
            temp_dict["appointment_id"] = appointment.id
            temp_dict["date"] = appointment.date
            temp_dict["time"] = appointment.time
            temp_dict["appointment_status"] = appointment.appointment_status
            appointment_list.append(temp_dict)
        appointment_details = json.dumps(appointment_list)
        print(f"Returning appointment data: {appointment_details}")
        return HttpResponse(appointment_details)


@login_required
def fetch_all_appointments(request):
    """Fetch all appointments for this hospital regardless of status"""
    if request.POST:
        pass
    else:
        print(f"Fetching all appointments for hospital ID: {request.user.id}")
        
        # Get all appointments for this hospital
        appointments = Appointments.objects.filter(hospital__id=request.user.id)
        print(f"Found {appointments.count()} appointments for this hospital")
        
        appointment_list = []
        for appointment in appointments:
            temp_dict = {}
            temp_dict["first_name"] = appointment.donation_request.donor.first_name
            temp_dict["last_name"] = appointment.donation_request.donor.last_name
            temp_dict["email"] = appointment.donation_request.donor.email
            temp_dict["contact_number"] = appointment.donation_request.donor.contact_number
            # Donation details
            temp_dict["organ"] = appointment.donation_request.organ_type
            temp_dict["donation_id"] = appointment.donation_request.id
            temp_dict["blood_group"] = appointment.donation_request.blood_type
            temp_dict["donation_status"] = appointment.donation_request.donation_status
            # Appointment details
            temp_dict["appointment_id"] = appointment.id
            temp_dict["date"] = appointment.date
            temp_dict["time"] = appointment.time
            temp_dict["appointment_status"] = appointment.appointment_status
            temp_dict["hospital_name"] = appointment.hospital.hospital_name
            appointment_list.append(temp_dict)
        
        appointment_details = json.dumps(appointment_list)
        print(f"Returning all appointment data: {appointment_details}")
        return HttpResponse(appointment_details)


@login_required
def fetch_donations(request):
    if request.POST:
        pass
    else:
        donation_status = "Pending"
        appointment_status = "Approved"
        appointments = Appointments.objects.filter(hospital__id=request.user.id, appointment_status=appointment_status, donation_request__donation_status=donation_status)
        appointment_list = []
        for appointment in appointments:
            temp_dict = {}
            temp_dict["first_name"] = appointment.donation_request.donor.first_name
            temp_dict["last_name"] = appointment.donation_request.donor.last_name
            # Donation details
            temp_dict["organ"] = appointment.donation_request.organ_type
            temp_dict["donation_id"] = appointment.donation_request.id
            temp_dict["blood_group"] = appointment.donation_request.blood_type
            # Appointment details
            temp_dict["appointment_id"] = appointment.id
            temp_dict["date"] = appointment.date
            temp_dict["time"] = appointment.time
            temp_dict["appointment_status"] = appointment.appointment_status
            appointment_list.append(temp_dict)
        appointment_details = json.dumps(appointment_list)

        return HttpResponse(appointment_details)


@login_required
def fetch_all_pending_donations(request):
    """Fetch all pending donation requests, regardless of appointment status"""
    if request.POST:
        pass
    else:
        # Get all pending donation requests
        donation_status = "Pending"
        donations = DonationRequests.objects.filter(donation_status=donation_status)
        
        print(f"Found {donations.count()} pending donation requests")
        
        donation_list = []
        for donation in donations:
            temp_dict = {}
            temp_dict["first_name"] = donation.donor.first_name
            temp_dict["last_name"] = donation.donor.last_name
            temp_dict["email"] = donation.donor.email
            temp_dict["contact_number"] = donation.donor.contact_number
            temp_dict["city"] = donation.donor.city
            temp_dict["province"] = donation.donor.province
            # Donation details
            temp_dict["organ"] = donation.organ_type
            temp_dict["donation_id"] = donation.id
            temp_dict["blood_group"] = donation.blood_type
            temp_dict["donation_status"] = donation.donation_status
            temp_dict["family_member_name"] = donation.family_relation_name
            temp_dict["family_member_relation"] = donation.family_relation
            temp_dict["family_member_contact"] = donation.family_contact_number
            temp_dict["donated_before"] = donation.donated_before
            temp_dict["family_consent"] = donation.family_consent
            temp_dict["request_date"] = donation.request_datetime.strftime("%Y-%m-%d %H:%M")
            
            # Check if appointment exists
            try:
                appointment = Appointments.objects.get(donation_request=donation)
                temp_dict["has_appointment"] = True
                temp_dict["appointment_status"] = appointment.appointment_status
                temp_dict["appointment_date"] = appointment.date
                temp_dict["appointment_time"] = appointment.time
            except Appointments.DoesNotExist:
                temp_dict["has_appointment"] = False
                temp_dict["appointment_status"] = "No Appointment"
            
            donation_list.append(temp_dict)
        
        donation_details = json.dumps(donation_list)
        print(f"Returning donation data: {donation_details}")
        return HttpResponse(donation_details)


def hospital_register(request):

    # If method is post
    if request.POST:
        user = User()
        user.username = request.POST.get("username", "")
        user.set_password(request.POST.get("password", ""))
        user.email = request.POST.get("email", "")
        user.hospital_name = request.POST.get("hospital_name", "")
        user.city = request.POST.get("city", "")
        user.province = request.POST.get("province", "")
        user.country = request.POST.get("country", "")
        user.contact_number = request.POST.get("contact_number", "")
        user.is_staff = True
        user.save()
        return redirect('hospital-login')

    return render(request, "hospital-registration.html")

def hospital_login(request):
    if request.POST:
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                if user.is_staff:

                 #                msg = """Logged in successfully. The homepage is with the other developer who is working on it. But,
                                        # the remaining functionality works the exact same way it does on donor side. Hence, you
                                        # are being redirected to same login page."""
                    login(request, user)
                    return redirect(request.POST.get("next", "home"))
        else:
            msg = "Invalid password"
            fail = 1
            return render(request, "hospital-login.html", {"fail": fail, "msg": msg})

    return render(request, "hospital-login.html")


def fetch_appointment_details(request):
    if request.POST:
        pass
    else:
        # Fetching appointment details
        appointment_id_from_UI = request.GET.get('appointment_id', '')
        print('appointment id', appointment_id_from_UI)
        appointments = Appointments.objects.filter(Q(id=int(appointment_id_from_UI)))
        appointment_list = []
        for appointment in appointments:
            # Donor details
            temp_dict = {}
            temp_dict["first_name"] = appointment.donation_request.donor.first_name
            temp_dict["last_name"] = appointment.donation_request.donor.last_name
            temp_dict["email"] = appointment.donation_request.donor.email
            temp_dict["contact_number"] = appointment.donation_request.donor.contact_number
            temp_dict["city"] = appointment.donation_request.donor.city
            temp_dict["country"] = appointment.donation_request.donor.country
            temp_dict["province"] = appointment.donation_request.donor.province
            # Donation details
            temp_dict["organ"] = appointment.donation_request.organ_type
            temp_dict["donation_id"] = appointment.donation_request.id
            temp_dict["blood_group"] = appointment.donation_request.blood_type
            temp_dict["donation_status"] = appointment.donation_request.donation_status
            temp_dict["family_member_name"] = appointment.donation_request.family_relation_name
            temp_dict["family_member_relation"] = appointment.donation_request.family_relation
            temp_dict["family_member_contact"] = appointment.donation_request.family_contact_number
            # Appointment details
            temp_dict["appointment_id"] = appointment.id
            temp_dict["date"] = appointment.date
            temp_dict["time"] = appointment.time
            temp_dict["appointment_status"] = appointment.appointment_status
            appointment_list.append(temp_dict)
        appointment_details = json.dumps(appointment_list)
        return HttpResponse(appointment_details)


def fetch_donation_details(request):
    if request.POST:
        pass
    else:
        # Fetching donation details
        donation_id_from_UI = request.GET.get('donation_id', '')
        print('donation id', donation_id_from_UI)
        donations = DonationRequests.objects.filter(Q(id=int(donation_id_from_UI)))
        donation_list = []
        for donation in donations:
            # Donor details
            temp_dict = {}
            temp_dict["first_name"] = donation.donor.first_name
            temp_dict["last_name"] = donation.donor.last_name
            temp_dict["email"] = donation.donor.email
            temp_dict["contact_number"] = donation.donor.contact_number
            temp_dict["city"] = donation.donor.city
            temp_dict["country"] = donation.donor.country
            temp_dict["province"] = donation.donor.province
            # Donation details
            temp_dict["organ"] = donation.organ_type
            temp_dict["donation_id"] = donation.id
            temp_dict["blood_group"] = donation.blood_type
            temp_dict["donation_status"] = donation.donation_status
            temp_dict["family_member_name"] = donation.family_relation_name
            temp_dict["family_member_relation"] = donation.family_relation
            temp_dict["family_member_contact"] = donation.family_contact_number

            donation_list.append(temp_dict)
        donation_details = json.dumps(donation_list)
        return HttpResponse(donation_details)


@csrf_exempt
def approve_appointments(request):
    if request.POST:
        appointment_id_from_UI = request.POST.get('ID', '')
        actionToPerform = request.POST.get('action', '')
        print('appointment id', appointment_id_from_UI)
        print('actionToPerform', actionToPerform)
        appointments = get_object_or_404(Appointments, id=appointment_id_from_UI)
        appointments.appointment_status = actionToPerform
        appointments.save(update_fields=["appointment_status"])
    return HttpResponse("success")


@csrf_exempt
def approve_donations(request):
    if request.POST:
        donation_id_from_UI = request.POST.get('ID', '')
        actionToPerform = request.POST.get('action', '')
        print('donation id', donation_id_from_UI)
        print('actionToPerform', actionToPerform)
        donation = get_object_or_404(DonationRequests, id=donation_id_from_UI)
        donation.donation_status = actionToPerform
        donation.save(update_fields=["donation_status"])
    return HttpResponse("success")


@login_required
def fetch_counts(request):
    if request.POST:
        pass
    else:
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"Hospital ID: {request.user.id}, Hospital Name: {request.user.hospital_name}")
        
        # Debug: Check all appointments and their hospital associations
        all_appointments = Appointments.objects.all()
        print(f"All appointments in DB: {all_appointments.count()}")
        for apt in all_appointments:
            print(f"Apt ID: {apt.id}, Hospital: {apt.hospital.hospital_name} (ID: {apt.hospital.id}), Status: {apt.appointment_status}")
        
        from datetime import datetime
        from django.utils import timezone
        
        # Get current month start
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        appointment_count = Appointments.objects.filter(hospital__id=request.user.id, appointment_status="Pending").count()
        donation_count = Appointments.objects.filter(hospital__id=request.user.id, appointment_status="Approved", donation_request__donation_status="Pending").count()
        all_pending_donations = DonationRequests.objects.filter(donation_status="Pending").count()
        
        # Monthly statistics
        approved_appointments_month = Appointments.objects.filter(
            hospital__id=request.user.id, 
            appointment_status="Approved"
        ).count()
        
        lives_saved = DonationRequests.objects.filter(donation_status="Approved").count()
        total_donors = DonationRequests.objects.values('donor').distinct().count()
        
        temp_dict = {
            "appointment_count": appointment_count,
            "donation_count": donation_count,
            "all_pending_donations": all_pending_donations,
            "approved_appointments_month": approved_appointments_month,
            "lives_saved": lives_saved,
            "total_donors": total_donors
        }
        
        return HttpResponse(json.dumps([temp_dict]))


def send_mail(send_from, send_to, subject, body_of_msg, files=[],
              server="localhost", port=587, username='', password='',
              use_tls=True):
    message = MIMEMultipart()
    message['From'] = send_from
    message['To'] = send_to
    message['Date'] = formatdate(localtime=True)
    message['Subject'] = subject
    message.attach(MIMEText(body_of_msg))
    smtp = smtplib.SMTP(server, port)
    if use_tls:
        smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to, message.as_string())
    smtp.quit()


def hospital_forgot_password(request):
    success = 0
    if request.POST:
        username = request.POST.get("username", "")
        try:
            user = User.objects.get(username=username)
            email = user.email
            password = random.randint(1000000, 999999999999)
            user.set_password(password)
            user.save()
            send_mail("foodatdalteam@gmail.com", email, "Password reset for your organ donation account",
                      """Your request to change password has been processed.\nThis is your new password: {}\n
                            If you wish to change password, please go to your user profile and change it.""".format(password),
                      server="smtp.gmail.com", username="foodatdalteam@gmail.com", password="foodatdal")
            success = 1
            msg = "Success. Check your registered email for new password!"
            return render(request, "hospital-forgot-password.html", {"success": success, "msg": msg})
        except:
            success = 1
            msg = "User does not exist!"
            return render(request, "hospital-forgot-password.html", {"success": success, "msg": msg})

    return render(request, "hospital-forgot-password.html", {"success": success})


def form_to_PDF(request, donor_id=1):

    donation_request = DonationRequests.objects.get(id=donor_id)
    user = donation_request.donor
    donations = DonationRequests.objects.filter(donor=user)
    template = get_template("user-details.html")
    html = template.render({'user': user, 'donors': donations})
    config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF)
    try:
        pdf = pdfkit.from_string(html, False, configuration=config)
    except Exception as e:
        print(e)
        pass
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    userpdf = PdfFileReader(BytesIO(pdf))
    usermedicaldoc = donation_request.upload_medical_doc.read()
    usermedbytes = BytesIO(usermedicaldoc)
    usermedicalpdf = PdfFileReader(usermedbytes)
    merger = PdfFileMerger()
    merger.append(userpdf)
    merger.append(usermedicalpdf)
    merger.write(response)
    return response


def email_donor(request, donor_id=1):
    donor = DonationRequests.objects.get(id=donor_id).donor
    send_mail("foodatdalteam@gmail.com", donor.email, "Organ Donation",
              """You've been requested by {} to donate organ. Thanks!""".format(request.user.hospital_name),
              server="smtp.gmail.com", username="foodatdalteam@gmail.com", password="foodatdal")
    return HttpResponse("Success")


def get_user_details(request):
    if request.POST:
        pass
    else:
        user_details = []
        temp_dict = {}
        hospital = User.objects.get(id=request.user.id)
        temp_dict["hospital_name"] = hospital.hospital_name
        temp_dict["hospital_email"] = hospital.email
        temp_dict["hospital_city"] = hospital.city
        temp_dict["hospital_province"] = hospital.province
        temp_dict["hospital_contact"] = hospital.contact_number
        user_details.append(temp_dict)
        user_json = json.dumps(user_details)
    return HttpResponse(user_json)


@csrf_exempt
def update_user_details(request):
    if request.POST:
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        city = request.POST.get('city', '')
        contact = request.POST.get('contact', '')
        province = request.POST.get('province', '')
        user = User.objects.get(id=request.user.id)
        user.email = request.POST.get('email', '')
        user.hospital_name = request.POST.get('name', '')
        user.city = request.POST.get('city', '')
        user.province = request.POST.get('province', '')
        user.contact_number = request.POST.get('contact', '')
        print("about to save...")
        user.save()
    return HttpResponse("success")


@csrf_exempt
def update_pwd_details(request):
    if request.POST:
        user = authenticate(username=request.user.username, password=request.POST.get("old_password", ""))
        if user is not None:
            user.set_password(request.POST.get("new_password", ""))
            print("about to save password...")
            user.save(update_fields=["password"])
    return HttpResponse("success")

def hospital_logout(request):
    logout(request)
    return redirect("hospital-login")

@csrf_exempt
def add_requirement(request):
    if request.POST:
        from ml_matching.models import HospitalOrganRequirement
        
        req = HospitalOrganRequirement(
            hospital=request.user,
            organ_type=request.POST.get('organ_type'),
            blood_type=request.POST.get('blood_type'),
            patient_age=int(request.POST.get('patient_age')),
            patient_weight=float(request.POST.get('patient_weight')),
            urgency_level=request.POST.get('urgency_level'),
            additional_notes=request.POST.get('additional_notes', '')
        )
        req.save()
        return HttpResponse('success')
    return HttpResponse('error')

@login_required
def get_requirements(request):
    from ml_matching.models import HospitalOrganRequirement
    
    requirements = HospitalOrganRequirement.objects.filter(hospital=request.user, is_active=True)
    req_list = []
    
    for req in requirements:
        req_list.append({
            'id': req.id,
            'organ_type': req.organ_type,
            'blood_type': req.blood_type,
            'patient_age': req.patient_age,
            'patient_weight': req.patient_weight,
            'urgency_level': req.urgency_level,
            'additional_notes': req.additional_notes
        })
    
    return HttpResponse(json.dumps(req_list))

@csrf_exempt
def delete_requirement(request):
    if request.POST:
        from ml_matching.models import HospitalOrganRequirement
        
        req_id = request.POST.get('id')
        try:
            req = HospitalOrganRequirement.objects.get(id=req_id, hospital=request.user)
            req.delete()
            return HttpResponse('success')
        except:
            return HttpResponse('error')
    return HttpResponse('error')

@login_required
def find_ml_matches(request):
    from ml_matching.models import HospitalOrganRequirement
    from ml_matching.matching_algorithm import OrganMatchingML
    
    try:
        # Initialize ML matching
        ml_matcher = OrganMatchingML()
        
        # Get search parameters
        req_id = request.GET.get('requirement_id')
        filter_organ = request.GET.get('organ_type')
        filter_blood = request.GET.get('blood_type')
        min_score = int(request.GET.get('min_score', 0))
        
        print(f"ML Matching request: req_id={req_id}, organ={filter_organ}, blood={filter_blood}, min_score={min_score}")
        
        # Build donation filter
        donation_filter = {'donation_status': 'Pending'}
        if filter_organ:
            donation_filter['organ_type'] = filter_organ
        if filter_blood:
            donation_filter['blood_type'] = filter_blood
        
        donations = DonationRequests.objects.filter(**donation_filter)
        print(f"Found {donations.count()} donations with filter: {donation_filter}")
        
        matches = []
        
        # Determine hospital requirement
        hospital_req = None
        if req_id:
            try:
                requirement = HospitalOrganRequirement.objects.get(id=req_id, hospital=request.user)
                hospital_req = {
                    'blood_type': requirement.blood_type,
                    'organ_type': requirement.organ_type,
                    'patient_age': requirement.patient_age,
                    'patient_weight': requirement.patient_weight,
                    'urgency_level': requirement.urgency_level
                }
                print(f"Using requirement: {hospital_req}")
            except HospitalOrganRequirement.DoesNotExist:
                print(f"Requirement {req_id} not found")
        
        # If no specific requirement, use filter values or defaults
        if not hospital_req:
            hospital_req = {
                'blood_type': filter_blood or 'O+',
                'organ_type': filter_organ or 'Kidney',
                'patient_age': 35,
                'patient_weight': 70,
                'urgency_level': 'Medium'
            }
            print(f"Using default requirement: {hospital_req}")
        
        # Calculate matches for each donation
        for donation in donations:
            donor_data = {
                'blood_type': donation.blood_type,
                'organ_type': donation.organ_type,
                'age': 30,
                'weight': 70,
                'smoking_status': False,
                'alcohol_consumption': False
            }
            
            compatibility_score = ml_matcher.calculate_compatibility_score(donor_data, hospital_req)
            print(f"Donor {donation.donor.first_name}: {donor_data['organ_type']} {donor_data['blood_type']} -> Score: {compatibility_score}")
            
            if compatibility_score >= min_score:
                matches.append({
                    'donor_id': donation.donor.id,
                    'donor_name': f"{donation.donor.first_name} {donation.donor.last_name}",
                    'organ_type': donation.organ_type,
                    'blood_type': donation.blood_type,
                    'compatibility_score': int(compatibility_score),
                    'ml_probability': min(compatibility_score / 100, 1.0),
                    'donor_city': donation.donor.city or 'Unknown'
                })
        
        # Sort by compatibility score
        matches.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        print(f"Returning {len(matches)} matches")
        return HttpResponse(json.dumps(matches[:10]))
        
    except Exception as e:
        print(f"Error in ML matching: {e}")
        import traceback
        traceback.print_exc()
        return HttpResponse(json.dumps([]))

def test_endpoint(request):
    return HttpResponse("Hospital URLs are working!")

@login_required
def test_dashboard(request):
    return render(request, "hospital-test.html")

@login_required
def donation_details(request, donation_id):
    """Get detailed information about a specific donation"""
    try:
        donation = DonationRequests.objects.get(id=donation_id)
        
        details = {
            "donation_id": donation.id,
            "first_name": donation.donor.first_name,
            "last_name": donation.donor.last_name,
            "email": donation.donor.email,
            "contact": donation.donor.contact_number,
            "organ": donation.organ_type,
            "blood_group": donation.blood_type,
            "age": getattr(donation.donor, 'age', 'N/A'),
            "weight": getattr(donation.donor, 'weight', 'N/A'),
            "city": donation.donor.city,
            "province": donation.donor.province,
            "medical_history": getattr(donation, 'medical_history', None),
            "donation_status": donation.donation_status
        }
        
        return HttpResponse(json.dumps(details))
    except DonationRequests.DoesNotExist:
        return HttpResponse(json.dumps({"error": "Donation not found"}), status=404)

@login_required
def appointment_details(request, appointment_id):
    """Get detailed information about a specific appointment"""
    try:
        appointment = Appointments.objects.get(id=appointment_id)
        
        details = {
            "appointment_id": appointment.id,
            "first_name": appointment.donation_request.donor.first_name,
            "last_name": appointment.donation_request.donor.last_name,
            "email": appointment.donation_request.donor.email,
            "contact": appointment.donation_request.donor.contact_number,
            "organ": appointment.donation_request.organ_type,
            "date": str(appointment.date),
            "time": str(appointment.time),
            "appointment_status": appointment.appointment_status,
            "notes": getattr(appointment, 'notes', None)
        }
        
        return HttpResponse(json.dumps(details))
    except Appointments.DoesNotExist:
        return HttpResponse(json.dumps({"error": "Appointment not found"}), status=404)
