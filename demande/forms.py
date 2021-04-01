from django.db.models import fields
from django.forms import ModelForm, CheckboxInput, TextInput, DateInput
from django.forms.widgets import Select


from .models import Demande

class DemandeForm(ModelForm):
    class Meta:
        model = Demande
        exclude = ['traite', 'imat_vehicule', 'num_releve', 'created_by', 'id', 'code_vehicule', 'code_remorque', 'imat_remorque', 'agence', 'axe_analyse']
        widgets={

            'num_releve ': TextInput(attrs={'Placeholder': 'Numéro de relevé', 'class': 'form-control', 'autocomplete': 'off'}),
            'chauffeur ': Select(attrs={'class': 'form-control'}),
            'date_frais ': DateInput(attrs={'type':'date', 'class': 'form-control'}),
            'date_demande': DateInput(attrs={'type':'date', 'class': 'form-control'}),
            'code_activite ': Select(attrs={'class': 'form-control'}),
            'libelle_activite ': Select(attrs={'class': 'form-control'}),
            'a_rembourser': CheckboxInput
        }




class DemandeTraitementForm(ModelForm):
    class Meta:
        model = Demande
        exclude = ['created_by']
        widgets={

            'num_releve ': TextInput(attrs={'Placeholder': 'Numéro de relevé', 'class': 'form-control', 'autocomplete': 'off'}),
            'chauffeur ': Select(attrs={'Placeholder': 'Chauffeur', 'class': 'form-control'}),
            'date_frais ': DateInput(attrs={'type':'date', "format": "dd/mm/yyyy", 'class': 'form-control'}),
            #'date_frais ': DatePicker(options={"format": "mm/dd/yyyy","autoclose": True}),
            'date_demande ': DateInput(attrs={'type':'date', "format": "dd/mm/yyyy", 'class': 'form-control'}),
            #'date_demande ': DatePicker(options={"format": "mm/dd/yyyy","autoclose": True}),
            'code_activite ': Select(attrs={'class': 'form-control'}),
            'agence ': Select(attrs={'class': 'form-control'}),
            'axe_analyse ': Select(attrs={'class': 'form-control'}),
            'libelle_activite ': Select(attrs={'class': 'form-control'}),
            'traite': CheckboxInput(),
            'a_rembourser':  CheckboxInput

        } 