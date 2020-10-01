from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.core import mail

from .models import Membre
from .person_finder import LDAP_get_infos

def index(request):
    if request.user.groups.filter(name = 'members of the committee').exists():
        return render(request, 'inscriptions/index.html')
    return HttpResponseRedirect('reject/')

def reject(request):
    return render(request, 'inscriptions/reject.html', {'not_connected_for_sure': 1})

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

            gender = "F"
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
    mail_sending = 1
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
        mail_sending = 0
    
    if inscription_status == 1:
        try:
            subject = "sujet"
            message = """Madame, Monsieur,
C'est avec plaisir que nous avons l'avantage de vous parvenir la présente annonçant votre inscription pour la durée de l'actuelle année académique au sein de notre club: Robopoly.
Vous avez désormais accès à nos locaux, infrastructures et réseaux sociaux réservés aux membres. Notamment le local BM 9139 dont le code de la porte est 060898, notre channel Telegram et notre page Facebook
Afin d'assurer que ce club reste un lieu de rencontre et de partage si convivial, nous vous serons forts gré que vous preniez connaissance de notre règlement disponible sur notre site internet robopoly.epfl.ch et que vous le respectiez.
La situation actuelle, si particulière, nous contraint à diverses mesures de protection pour le bien commun. Aussi, nous vous demandons de bien vouloir respecter les mesures de distanciation et du port du masque. Vous êtes autorisé à venir sur campus, indifféremment du modulo d'identifiant SCIPER, dans nos infrastructures. Ceci ne vous donne en aucun cas un droit à une quelconque autre activité sur site.
C'est avec enthousiasme que nous vous accueillerons dans nos infrastructures, que nous répondront à vos éventuelles questions et requêtes par le biais de nos réseaux sociaux et, en attendant, nous vous présentons l'expression de nos salutations distinguées.
Le comité de Robopoly"""
            from_mail = "pierre.oppliger@robopoly.ch"
            to_mails = [mail]
            
            send_mail(subject, message, from_mail, to_mails)
        except:
            mail_sending = 0
    
    print(inscription_status)
    return render(request, 'inscriptions/save.html', {'inscription_status': inscription_status, 'mail_sending': mail_sending, 'descr_error': descr_error})
