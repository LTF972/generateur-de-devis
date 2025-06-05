from .models import Client

def clients_list(request):
    """
    Ajoute la liste des clients au contexte global.
    """
    if request.user.is_authenticated:
        return {
            'clients': Client.objects.all().order_by('nom')
        }
    return {'clients': []} 