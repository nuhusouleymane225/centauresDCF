from django.db import models
from django.conf import settings
from django_currentuser.db.models import CurrentUserField


class Chauffeur(models.Model):

    nom_prenom = models.CharField(max_length=150)
    code_matricule = models.CharField(max_length=10)
    est_actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "chauffeur"
        verbose_name_plural = "chauffeurs"

    def __str__(self):
        return f"{self.nom_prenom} - {self.code_matricule}"


class Motif(models.Model):

    libelle = models.CharField(max_length=150)

    class Meta:
        verbose_name = "motif"
        verbose_name_plural = "motifs"

    def __str__(self):
        return self.libelle


directionActChoix = [
    ('DGE', 'Dir. Générale(DGE)'),
    ('DCF', 'Dir. Financière(DCF)'),
    ('DRH', 'Dir. RH(DRH)'),
    ('DEX', 'Dir. Exploitation(DEX)'),
    ('DET', 'Dir. Technique(DET)'),
    ('DCM', 'Dir. Commerciale(DCM)'),
    ('SMG', 'Moyens Generaux(SMG)'),
    ('FHY', 'fret Hydrocarbure(FHY)'),
    ('FSB', 'fret boisson(FSB)'),
    ('FHP', 'fret huile de palm(FHP)'),
    ('FTC', 'fret conteneurs(FTC)'),
    ('FCS', 'fret canne à sucre(FCS)'),
    ('FDI', 'fret divers(FDI)'),
    ('LEV', 'levage(LEV)'),
    ('LOC', 'location de surfaces(LOC)'),
    ('SDI', 'services divers(SDI)'),
    ('RAV', 'revenus à ventiler(RAV)'),
    ('PAF', 'Prestation Accessoir(PAF)'),
    ('COL', 'fret Colis lourds(COL)'),

]

codeActivite = [
    ('DGE', 'DGE'),
    ('DCF', 'DCF'),
    ('DRH', 'DRH'),
    ('DEX', 'DEX'),
    ('DET', 'DET'),
    ('DCM', 'DCM'),
    ('SMG', 'SMG'),
    ('FHY', 'FHY'),
    ('FSB', 'FSB'),
    ('FHP', 'FHP'),
    ('FTC', 'FTC'),
    ('FCS', 'FCS'),
    ('FDI', 'FDI'),
    ('LEV', 'LEV'),
    ('LOC', 'LOC'),
    ('SDI', 'SDI'),
    ('RAV', 'RAV'),
    ('PAF', 'PAF'),
    ('COL', 'COL'),

]


axeAnalyseChoix = [
    ('200', 'Batiment et charge locative'),
    ('210', 'Voyage & deplacement'),
    ('220', 'Fourniture & consommable de bureau'),
    ('230', 'Charge personnel'),
    ('240', 'Quote-part depreciation immo'),
    ('250', 'Personnel & services exterieur'),
    ('260', 'Relation exterieur'),
    ('270', 'Impôt & taxes'),
    ('280', 'Autres charges directions et service'),
    ('900', "Recette d'exploitation"),
    ('910', 'Frais/Opération (frais voyages)'),
    ('920', 'Papier administratif-CR'),
    ('930', "Main d'oevre dédiée"),
    ('940', 'Quote-part amortissement CR et autres'),
    ('950', 'Entretien & reparation CR'),
    ('960', 'Frais generaux'),


]

agenceChoix = [
    ('0000', 'Siège'),
    ('0001', 'Abidjan (agence principale)'),
    ('0002', 'Bouaflé'),
    ('0003', 'San-Pedro'),
    ('0007', 'Bouaké'),
    ('0008', 'Yamoussoukro'),
    ('0009', 'Ferké'),
    ('0010', 'Minautores'),


]

# Create your models here.


class Demande(models.Model):
    urgenceChoix = [
        ('A Exécuter Immediatement', 'A Exécuter Immediatement'),
        ('A Exécuter Dans Les Plus Brefs Délais',
         'A Exécuter Dans Les Plus Brefs Délais'),
        ('Peut Etre Reporté', 'Peut Etre Reporté'),
    ]

    num_releve = models.CharField(
        max_length=20, verbose_name='Numéro de relevé')

    
    created_by = CurrentUserField(verbose_name='Nom du demandeur')
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.CASCADE)
    code_vehicule = models.CharField(
        null=True, max_length=50, verbose_name='Code véhicule')
    code_remorque = models.CharField(
        max_length=50, verbose_name='Code remorque')
    imat_vehicule = models.CharField(
        max_length=50, verbose_name='Imat. véhicule')
    imat_remorque = models.CharField(
        max_length=50, verbose_name='Imat. Remorque')
    date_frais = models.DateField(null=True, verbose_name='Date de frais')
    date_demande = models.DateField(
        auto_now_add=False, verbose_name='Date de demande')
    # code activite analytique
    code_activite = models.CharField(
        max_length=150, choices=codeActivite, verbose_name='Code Activité')
    libelle_activite = models.CharField(
        max_length=255, choices=directionActChoix, verbose_name='Libelle')
    quantite = models.IntegerField(default=1)
    pu = models.FloatField(default=0.00, verbose_name='Prix unitaire')
    total = models.FloatField()
    urgence = models.CharField(choices=urgenceChoix, max_length=255)
    traite = models.BooleanField(default=False)
    motif = models.ForeignKey(
        Motif, verbose_name="MOTIF", on_delete=models.CASCADE, default="")

    # les autres element de l'analytique
    agence = models.CharField(choices=agenceChoix, max_length=255)
    a_rembourser = models.BooleanField(default=False)
    axe_analyse = models.CharField(choices=axeAnalyseChoix, max_length=255)

    def get_total_prix(self):
        return self.quantite * self.pu

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_detail_url(self):
        return f"traitement/{self.id}"

    def __str__(self):
        return f"{self.id} - {self.created_by}"

    
