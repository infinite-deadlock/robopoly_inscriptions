from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from .models import Membre
from .person_finder import LDAP_get_infos

def index(request):
    return render(request, 'inscriptions/index.html')

def validation(request):
    sciper_is_known = 0
    try:
        sciper_is_known = int(request.POST['sciper_is_known'])
    except:
        sciper_is_known = 0

    sciper = 0
    first_name = ""
    name = ""
    mail = ""
    phone_number = ""
    gender = ""
    section = ""
    if sciper_is_known == 1:
        try:
            sciper = request.POST['sciper']
            infos = LDAP_get_infos(sciper)

            gender = "F"                    # ladies first
            if infos[0] == "Monsieur":
                gender = "M"

            first_name, name, mail, section = infos[1], infos[2], infos[3], infos[4]

            # if we cannot retrieve the names, consider that LDAP fail
            if len(first_name) <= 0 or len(name) <= 0:
                raise("LDAP fail")
        except:
            sciper_is_known = 2
    
    try:
        phone_number = str(request.POST['phone_number'])
    except:
        phone_number = ""
    return render(  request,
                    'inscriptions/validation.html',
                    {
                        'sciper_is_known': sciper_is_known,
                        'sciper': sciper,
                        'first_name': first_name,
                        'name': name,
                        'mail': mail,
                        'phone_number': phone_number,
                        'gender': gender,
                        'section': section
                    }
                )

def save(request):
    inscription_status = 1
    descr_error = ''
    try:
        if not request.POST['sciper'].isnumeric():
            descr_error = 'le sciper n\'est pas une nombre: ' + request.POST['sciper']
            raise
        sciper = int(request.POST['sciper'])
        if sciper <= 0:
            descr_error = 'le sciper est invalide: sciper = ' + str(sciper)
            raise

        first_name = request.POST['first_name']
        if len(first_name) <= 0:
            descr_error = 'les prénoms sont invalides'
            raise

        name = request.POST['name']
        if len(name) <= 0:
            descr_error = 'le nom est invalide'
            raise

        mail = request.POST['mail']
        if len(mail) <= 0:
            descr_error = 'le mail est invalide'
            raise
        
        phone_number = request.POST['phone_number']
        if len(phone_number) <= 0:
            phone_number = '-'

        title = request.POST['gender']
        if title != 'Monsieur' and title != 'Madame':
            descr_error = 'ce genre ne convient pas à la base de données: ' + title
            raise

        section = request.POST['section']
        if len(section) <= 0:
            section = '-'

        print(sciper, first_name, name, mail, phone_number, title, section)
        new_member = Membre(sciper=sciper, first_name=first_name, name=name, mail=mail, phone_number=phone_number, title=title, section=section)
        new_member.save()
    except:
        if len(descr_error) <= 0:
            descr_error = 'sauvegarde impossible'
        inscription_status = 0
    print(inscription_status)
    return render(request, 'inscriptions/save.html', {'inscription_status': inscription_status, 'descr_error': descr_error})
