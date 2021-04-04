from django.shortcuts import render, get_object_or_404
from .models import Facture, LigneFacture,Client,Fournisseur
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.config import RequestConfig
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Button
from django.urls import reverse
from django.db.models import Sum
from django.db.models import ExpressionWrapper,F,FloatField
from django.conf import settings
from bootstrap_datepicker_plus import DatePickerInput
import datetime
from jchart import Chart
from jchart.config import Axes, DataSet
# Create your views here.

def facture_detail_view(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    context={}
    context['facture'] = facture
    return render(request, 'bill/facture_detail.html', context)


                    # Gestion client ##
class ClientTable(tables.Table):
    action= '<a href="{% url "client_update" pk=record.id %}" class="btn btn-warning">Modifier</a>\
             <a href="{% url "client_delete" pk=record.id %}" class="btn btn-danger">Supprimer</a>\
             <a href="{% url "facture_table" pk=record.id %}" class="btn btn-primary">Factures</a>'   
    ca_client = tables.Column("ca_client") 
    edit   = tables.TemplateColumn(action) 

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
      
        
class ClientView(ListView):
    template_name = 'bill/list.html'
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        table = ClientTable(Client.objects.all().annotate(ca_client=Sum(ExpressionWrapper(F('facture__lignes__qte'),output_field=FloatField()) * F('facture__lignes__produit__prix'))))
        RequestConfig(self.request, paginate={"per_page": 8}).configure(table)
        context['table'] = table
        context['URLCreat']  = "/bill/client_create/"
        context['object'] = 'Client'
        context['title'] = 'La liste des clients :'

        return context

class ClientCreateView(CreateView):
    model = Client
    template_name = 'bill/create.html'
    fields = ['nom', 'prenom', 'adresse','tel','sexe']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit','Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client')
        return form

class ClientUpdateView(UpdateView):
    model =Client
    template_name = 'bill/update.html'
    fields = ['nom', 'prenom', 'adresse','tel','sexe']
    
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['client']=forms.ModelChoiceField(queryset=Client.objects.all(), initial=0)
        form.helper.add_input(Submit('submit','Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client')
        return form


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'bill/delete.html'
    
    def get_success_url(self):
        success_url = reverse('client')
        return success_url

class FactureTable(tables.Table):
    action= '<a href="{% url "facture_table_detail" pk=record.id %}" class="btn btn-warning">Details</a>'
    Total=tables.Column("Total")
    Detail=tables.TemplateColumn(action)
    
    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap4.html"
        fields=['id','date']
      


                   # Gestion Facture ##

class FactureView(DetailView):
    template_name = 'bill/list.html'
    model = Facture
    
    
    def get_context_data(self, **kwargs):
        context = super(FactureView, self).get_context_data(**kwargs)
        
        table = FactureTable(Facture.objects.filter(client_id=self.kwargs.get('pk')).annotate(Total=Sum(F("lignes__produit__prix") * F("lignes__qte"),output_field=FloatField())))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        context['URLCreat']  = "/bill/facture_create/" + str(self.kwargs.get('pk')) + "/"
        context['object'] = 'Facture'
        context['title'] = 'La liste des factures du client ' + str(self.get_object())
        return context
   


class FactureUpdate(UpdateView):
    model = Facture
    fields = ['client', 'date']
    template_name = 'bill/update.html'


class LigneFactureTable(tables.Table):
    action= '<a href="{% url "lignefacture_update" pk=record.id facture_pk=record.facture.id %}" class="btn btn-warning">Modifier</a>\
             <a href="{% url "lignefacture_delete" pk=record.id facture_pk=record.facture.id %}" class="btn btn-danger">Supprimer</a>'
    edit   = tables.TemplateColumn(action)    
    class Meta:
        model = LigneFacture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation','produit__id', 'produit__prix', 'qte' )


class FactureDetailView(DetailView):
    template_name = 'bill/facture_table_detail.html'
    model = Facture
    
    def get_context_data(self, **kwargs):
        context = super(FactureDetailView, self).get_context_data(**kwargs)
        
        table = LigneFactureTable(LigneFacture.objects.filter(facture=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context

class LigneFactureCreateView(CreateView):
    model = LigneFacture
    template_name = 'bill/create.html'
    fields = ['facture', 'produit', 'qte']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture']=forms.ModelChoiceField(queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit','Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk':self.kwargs.get('facture_pk')})
        return form
    def get_context_data(self, **kwargs):
        context = super(LigneFactureCreateView, self).get_context_data(**kwargs)
        context['object'] = 'LigneFacture'
        context['title'] = "Création d'une LigneFacture "
        return context

class LigneFactureUpdateView(UpdateView):
    model = LigneFacture
    template_name = 'bill/update.html'
    fields = ['facture', 'produit', 'qte']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['facture']=forms.ModelChoiceField(queryset=Facture.objects.filter(id=self.kwargs.get('facture_pk')), initial=0)
        form.helper.add_input(Submit('submit','Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table_detail', kwargs={'pk':self.kwargs.get('facture_pk')})
        return form
    def get_context_data(self, **kwargs):
        context = super(LigneFactureUpdateView, self).get_context_data(**kwargs)
        context['object'] = 'LigneFacture'
        context['title'] = "Modification de la LigneFacture "
        return context

class LigneFactureDeleteView(DeleteView):
    model = LigneFacture
    template_name = 'bill/delete.html'
    
    def get_success_url(self):
        self.success_url = reverse('facture_table_detail', kwargs={'pk':self.kwargs.get('facture_pk')})


class FactureCreateView(CreateView):
    model = Facture
    template_name = 'bill/create.html'
    fields = ['client', 'date']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['date'] = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y'),initial=datetime.date.today())
        form.fields['client']=forms.ModelChoiceField(queryset=Client.objects.filter(id=self.kwargs.get('client_pk')), initial=0)
        form.helper.add_input(Submit('submit','Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('facture_table', kwargs={'pk':self.kwargs.get('client_pk')})
        return form
    
    def get_context_data(self, **kwargs):
        context = super(FactureCreateView, self).get_context_data(**kwargs)
        context['object'] = 'Facture'
        context['title'] = "Création d'une facture"

        return context

             # Gestion Fournisseurs 
class FournisseurTable(tables.Table):
    action= '<a href="{% url "fournisseur_update" pk=record.id %}" class="btn btn-warning">Modifier</a>\
             <a href="{% url "fournisseur_delete" pk=record.id %}" class="btn btn-danger">Supprimer</a>'
             
    edit   = tables.TemplateColumn(action) 

    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
      
        
        

class FournisseurView(ListView):
    template_name = 'bill/list.html'
    model = Fournisseur

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        table = FournisseurTable(Fournisseur.objects.all())
        RequestConfig(self.request, paginate={"per_page": 8}).configure(table)
        context['table'] = table
        context['URLCreat']  = "/bill/fournisseur_create/"
        context['object'] = 'Fournisseur'
        context['title'] = 'La liste des fournisseurs :'

        return context

class FournisseurCreateView(CreateView):
    model = Fournisseur
    template_name = 'bill/create.html'
    fields = ['nom', 'prenom', 'adresse','tel','sexe']
    
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit','Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur')
        return form
    
    def get_context_data(self, **kwargs):
        context = super(FournisseurCreateView, self).get_context_data(**kwargs)
        context['object'] = 'Fournisseur'
        context['title'] = "Création d'un fournisseur"

        return context
class FournisseurUpdateView(UpdateView):
    model =Fournisseur
    template_name = 'bill/update.html'
    fields = ['nom', 'prenom', 'adresse','tel','sexe']
    
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit','Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur')
        return form



class FournisseurDeleteView(DeleteView):
    model = Fournisseur
    template_name = 'bill/delete.html'
    
    def get_success_url(self):
        success_url = reverse('fournisseur')
        return success_url
 

class ClientTableDash(tables.Table):   
    ca_client = tables.Column("ca_client")  

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields=('facture__client__nom','facture__client__prenom')


class FournisseurTableDash(tables.Table):   
    ca_fournisseur = tables.Column("ca_fournisseur")  

    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
        fields=('produit__fournisseur__nom','produit__fournisseur__prenom')

def Dash(request):
    context = {}
    fournisseur = FournisseurTableDash(LigneFacture.objects.all().values('produit__fournisseur__nom','produit__fournisseur__prenom').
    annotate(ca_fournisseur=Sum(ExpressionWrapper(F('qte'),output_field=FloatField())*F('produit__prix'))))
    client = ClientTableDash(LigneFacture.objects.all().values('facture__client__nom','facture__client__prenom').
    annotate(ca_client=Sum(ExpressionWrapper(F('qte'),output_field=FloatField())*F('produit__prix'))))
    RequestConfig(request, paginate={"per_page": 10}).configure(client)
    context['client'] = client
    RequestConfig(request, paginate={"per_page": 10}).configure(fournisseur)
    context['fournisseur'] = fournisseur
    context['LineChart']=LineChart()
    context['radar']=RadarChart()

    return render(request, 'bill/Dash.html',context)

    
class LineChart(Chart):
    chart_type = 'line'
    scales = {
        'xAxes': [Axes(type='time', position='bottom')],
    }
    def get_datasets(self, **kwargs):
     factures = Facture.objects.all().values('date').annotate(y=Sum(F("lignes__produit__prix")*F("lignes__qte"),output_field=FloatField()))
     data=factures.annotate(x=F('date')).values('x','y') 
     return[DataSet(
                    type='line',
                    label='Evaluation du chiffre d\'affaire par jour',
                    data=list(data)
                    )]
        
        

class RadarChart(Chart):
    chart_type = 'radar'
    labels = []
    data = []
    produits = LigneFacture.objects.all().values('produit__categorie').annotate(total=Sum(F("produit__prix") * F("qte"),output_field=FloatField()),Categorie=F("produit__categorie__nom"))
    for f in produits:
          labels.append(f['Categorie'])
          data.append(f['total'])
          
    def get_labels(self):
        return self.labels

    

    def get_datasets(self, **kwargs):
        return [
                DataSet(label="le chiffre d'affaire réparti par catégorie de Produit",
                        color=(255, 99, 132),
                        data=self.data )
               ]


        