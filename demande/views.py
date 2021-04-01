from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.shortcuts import redirect, render


from .forms import DemandeForm, DemandeTraitementForm
from .models import Demande
# import for view

from io import BytesIO
from django.http import HttpResponse, request
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa



#convert to pdf
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

result = Demande.objects.all()
data = {"result": result}

class ViewPDF(View):
	def get(self, request, *args, **kwargs):
        
		pdf = render_to_pdf('app/pdf_template.html', data)
		return HttpResponse(pdf, content_type='application/pdf')

def ImprimePdf(request, id):
    texts = Demande.objects.get(id=id)
    context = {
        'texts': texts,
    }

    return render_to_pdf('app/pdf_template.html', context)

# Create your views here.

def welcome(request):
    template_name='client.html'
    return render(request , template_name )

@login_required
def welcome_admin(request):
    template_name='index.html'
    nb_dmd=Demande.objects.all().filter(traite=False).count()
    nb_dmdt=Demande.objects.all().filter(traite=True).count()

    context = {'nb_dmd': nb_dmd, 'nb_dmdt': nb_dmdt}
    return render(request , template_name, context )

def login(request):
    template_name='login.html'
    return render(request , template_name )



@login_required
def rapport_mensuel(request):
    template_name='charts.html'
    return render(request , template_name )

def error404(request):
    template_name='404.html'
    return render(request , template_name )

@login_required
def demande_affiche(request):
    query_results=Demande.objects.all().filter(traite=False)
    template_name='tables2.html'
    context={"query_results":query_results}
    return render(request , template_name ,context)


    



@login_required
def demande_traffiche(request):
    query_results=Demande.objects.all().filter(traite=True)
    template_name='tables2.html'
    context={"query_results":query_results}
    return render(request , template_name ,context)



@login_required
def demande_traitement(request, id):
    result= Demande.objects.get(id=id)
    form = DemandeTraitementForm(initial={'date_demande': result.date_demande, 'num_releve': result.num_releve, 'date_frais': result.date_frais, 'code_activite': result.code_activite, 'libelle_activite': result.libelle_activite, 'motif': result.motif, 'quantite': result.quantite, 'pu': result.pu, 'total': result.total, 'urgence': result.urgence, 'traite': result.traite})
    if request.method == "POST":
        form = DemandeTraitementForm(request.POST, instance=result)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/demandes')
            except Exception as e:
                pass
    context = {'form': form, 'result':result}
    return render(request,'traitement-demande.html',context)  



@login_required
def demande_save(request):
     form = DemandeForm(request.POST or None)
     if form.is_valid():
         obj=Demande.objects.create(** form.cleaned_data)
         obj.save()
         form = DemandeForm()
         print('data valid')
     else: 
         print('data is not valid')
     context={'form': form}
     template_name = 'demande.html'
     return render(request, template_name, context)



def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        template_name='index.html'
        login(request, user)
        return render(request,template_name)
    else:
        print('login none ')
        return 0

def logout_view(request):
    logout(request)
    template_name='login.html'
    return render(request, template_name)



def logoutTlogin(request):
    return logout_then_login(request, login_url='/login')




