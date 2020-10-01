A LA TRÈS NOBLE, TRÈS COURAGEUSE, TRES VOLONTAIRE PERSONNE QUI FERA LE DEPLOYEMENT EN PRODUCTION,

Ce dossier contient l'application inscriptions qui, comme son nom l'indique, aide les responsables inscriptions de Robopoly à faire les inscriptions à Robopoly.
Le tout est programmé en python/django. Le coeur de l'application est dans le dossier inscriptions. Afin qu'il puisse être testé, il est accompagné d'un dossier robopoly contenant le site web où la seule application est inscriptions.
Ainsi, la courageuse personne qui fera le déployement en production n'a qu'à rajouter inscriptions aux appliations déjà existantes de Robopoly (si c'est le cas, on m'avait dit que oui).
En principe, cette apllication sera accessible de manière qui devrait ressembler à cela, après votre travail: robopoly.epfl.ch/inscriptions. Ce serait une bonne idée de mettre cette page accessible uniquement si l'utilisateur est loggé par tequila. Si ce n'est pas possible, je rajouterai une page de login à cette application.

L'aperçu des membres inscrits se fait par l'interface admin déjà fournie par django. Ce serait bien si vous pouriez la restituez comme telle car la personne en charge des paiements des cotisations l'utilisera pour donner par la suite les accès à notre local et à nos services.

N'oubliez pas comme d'habitude de ne pas prendre tel quel le mot de passe en production.
Particulièrement dans le settings qui est pour le moment:

\# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rxnsj811!6h9ti72i-my(vl#uqxps@l$67vi5qo2s+*2jm7of5'

\# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True            # not in production !
ALLOWED_HOSTS = ['*']   # not in production !
\# SECURITY WARNING !!!

\# ALLOWED_HOSTS = []    # default configuration for ALLOWED_HOSTS

# nouveau
Les options de mail sont ajoutés. Il y a désormais des utiliateurs qui sont membres de "committee members". Il faut que les utilisateurs qui feront les inscriptions aient un compte dans ce groupe-là.

Bon travail, bonne chance et bon courage
