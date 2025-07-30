from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import logging
from datetime import datetime, date
import numpy as np
import matplotlib.pyplot as plt
import io, base64
from langchain_openai import OpenAI  # Si tu veux aussi utiliser OpenAI
from langchain.prompts import PromptTemplate
from langchain_mistralai import ChatMistralAI  # Remplacement de GoogleGenerativeAI par MistralAI
from .models import Demande, Responsable, Historique, Application, Transfert, Audit, Satisfaction
import re
import uuid
from django.db.models import Count, Avg, Max, Min, Q
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'chatbot.html')


@csrf_exempt
def generate_graph(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('fileInput')
        command = request.POST.get('command')

        if not excel_file or not command:
            return JsonResponse({'status': 'error', 'message': 'Fichier ou commande manquant.'})

        if hasattr(excel_file, 'seek'):
            excel_file.seek(0)
        file_name = excel_file.name.lower()

        try:
            if file_name.endswith('.csv'):
                try:
                    df = pd.read_csv(excel_file)
                except UnicodeDecodeError:
                    excel_file.seek(0)
                    df = pd.read_csv(excel_file, encoding='latin1')
                sheet_name = 'csv'
            elif file_name.endswith(('.xlsx', '.xlsm')):
                xls = pd.ExcelFile(excel_file, engine='openpyxl')
                sheet_name = xls.sheet_names[0]
                for name in xls.sheet_names:
                    if name.lower() in command.lower():
                        sheet_name = name
                        break
                df = pd.read_excel(xls, sheet_name=sheet_name, nrows=5000)
            elif file_name.endswith('.xls'):
                xls = pd.ExcelFile(excel_file, engine='xlrd')
                sheet_name = xls.sheet_names[0]
                for name in xls.sheet_names:
                    if name.lower() in command.lower():
                        sheet_name = name
                        break
                df = pd.read_excel(xls, sheet_name=sheet_name, nrows=5000)
            else:
                return JsonResponse({'status': 'error', 'message': 'Format de fichier non supporté. Veuillez fournir un fichier .csv, .xlsx ou .xls.'})

            cmd = command.lower()
            if "barre" in cmd:
                ax = df.plot(kind='bar')
            elif "courbe" in cmd or "line" in cmd:
                ax = df.plot(kind='line')
            elif "secteur" in cmd or "pie" in cmd:
                df.iloc[:, 0].value_counts().plot.pie(autopct='%1.1f%%')
            elif "histogramme" in cmd:
                ax = df.plot(kind='hist')
            else:
                ax = df.plot()

            plt.tight_layout()
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')

            return JsonResponse({'status': 'success', 'image': image_base64, 'sheet': sheet_name})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'})


@csrf_exempt
def analyze_command(request):
    if request.method == "POST":
        text = request.POST.get("text", "")
        conversation_id = request.POST.get("conversation_id")
        if not conversation_id:
            conversation_id = str(uuid.uuid4())

        try:
            llm = ChatMistralAI(
                model="mistral-large-latest",
                mistral_api_key="djGxrn5IJfal6irntxLpfaL2mq8qcRj2"
            )

            prompt = f"""
Analyse la commande utilisateur suivante et génère uniquement du code Python/Django ORM valide.

### 🎯 OBJECTIF :
- Toujours définir une variable **resultat** qui contient la réponse finale.
- Si la réponse est **simple (texte ou nombre)** → `resultat = ...`
- Si la réponse contient **plusieurs colonnes** :
    1️⃣ Définir une variable **colonnes** = liste des noms exacts des colonnes  
    2️⃣ Définir **resultat** = liste de dictionnaires dont les clés correspondent aux colonnes.

 IMPORTANT :
- Lors de l'utilisation de .values() ou .annotate(), ne jamais utiliser comme alias le nom exact d'un champ existant.
- Toujours utiliser un alias différent (ex: date_transfert_value au lieu de date_transfert).


###  BASE DE DONNÉES :

class Responsable(models.Model):
    identifiant = models.CharField(max_length=50, primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)

class Application(models.Model):
    nom_application = models.CharField(max_length=100)
    perimetre = models.CharField(max_length=100, blank=True, null=True)

class Demande(models.Model):
    reference_demande = models.CharField(max_length=50, primary_key=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="demandes")
    date_ouverture = models.DateTimeField()
    date_fermeture = models.DateTimeField(blank=True, null=True)
    categorie = models.CharField(max_length=100)
    commentaire = models.TextField(blank=True, null=True)
    identifiant_demandeur = models.ForeignKey(Responsable, on_delete=models.CASCADE, related_name="demandes")
    orientation = models.CharField(max_length=10, choices=[("refus", "Refus"), ("non", "Non orienté")])

class Transfert(models.Model):
    ref_demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name="transferts")
    identifiant_expert = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True, related_name="transferts_expert")
    identifiant_support = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True, related_name="transferts_support")
    date_transfert = models.DateTimeField()

class Audit(models.Model):
    identifiant_demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name="audits")
    resultat_audit = models.IntegerField()
    identifiant_audit = models.ForeignKey(Responsable, on_delete=models.SET_NULL, null=True, related_name="audits_realises")
    date_audit = models.DateTimeField()

class Satisfaction(models.Model):
    ref_demande = models.ForeignKey(Demande, on_delete=models.CASCADE, related_name="satisfactions")
    score = models.IntegerField()

class Historique(models.Model):
    requete = models.TextField()
    reponse = models.TextField(blank=True, null=True)
    date_requete = models.DateTimeField(auto_now_add=True)
    conversation_id = models.CharField(max_length=100)

---

### EXEMPLES DE REQUÊTES ET RÉPONSES

1️⃣EXEMPLES DE REQUÊTES :
1. "Combien de demandes au total ?"
   resultat = Demande.objects.count()

2. "Qui est le demandeur de la demande DEM0002 ?"
   try:
       demande = Demande.objects.get(reference_demande='DEM0002')
       resultat = f"{{demande.identifiant_demandeur.prenom}} {{demande.identifiant_demandeur.nom}}"
   except ObjectDoesNotExist:
       resultat = "Demande non trouvée"

3. "Combien de demandes par catégorie ?"
   categories = Demande.objects.values('categorie').annotate(nb=Count('reference_demande')).order_by('-nb')
   resultat = "\\n".join([f"{{cat['categorie']}}: {{cat['nb']}} demandes" for cat in categories])

4. "Quel est le score moyen de satisfaction ?"
   score_moyen = Satisfaction.objects.aggregate(avg_score=Avg('score'))['avg_score']
   resultat = f"Score moyen: {{score_moyen:.2f}}" if score_moyen else "Aucune donnée de satisfaction"

5. "Combien de demandes ont été transférées ?"
   resultat = Demande.objects.filter(transferts__isnull=False).distinct().count()

6. "Quelles sont les applications avec le plus de demandes ?"
   apps = Application.objects.annotate(nb_demandes=Count('demandes')).order_by('-nb_demandes')[:5]
   resultat = "\\n".join([f"{{app.nom_application}}: {{app.nb_demandes}} demandes" for app in apps])

7. "Combien d'audits ont été réalisés ce mois ?"
   from datetime import datetime
   current_month = datetime.now().month
   current_year = datetime.now().year
   resultat = Audit.objects.filter(date_audit__month=current_month, date_audit__year=current_year).count()

8. "Quels sont les demandeurs les plus actifs ?"
   demandeurs = Responsable.objects.annotate(nb_demandes=Count('demandes')).filter(nb_demandes__gt=0).order_by('-nb_demandes')[:5]
   resultat = "\\n".join([f"{{d.prenom}} {{d.nom}}: {{d.nb_demandes}} demandes" for d in demandeurs])

9. "Combien de demandes sont encore ouvertes ?"
   resultat = Demande.objects.filter(date_fermeture__isnull=True).count()

10. "Quel est le délai moyen de traitement des demandes fermées ?"
    from django.db.models import F, ExpressionWrapper, fields
    from datetime import timedelta
    demandes_fermees = Demande.objects.filter(date_fermeture__isnull=False).annotate(
        duree=ExpressionWrapper(F('date_fermeture') - F('date_ouverture'), output_field=fields.DurationField())
    )
    if demandes_fermees.exists():
        duree_moyenne = sum([d.duree.total_seconds() for d in demandes_fermees]) / demandes_fermees.count()
        jours = int(duree_moyenne / 86400)
        resultat = f"Délai moyen: {{jours}} jours"
    else:
        resultat = "Aucune demande fermée trouvée"

12. "Affiche toutes les données de la table utilisateurs"
    resultat = "Table 'utilisateurs' non trouvée. Tables disponibles : Responsable, Application, Demande, Transfert, Audit, Satisfaction, Historique"

13- 5 Transfert plus récents : transferts_recents = Transfert.objects.select_related("ref_demande", "identifiant_expert").values(
    reference_demande=F("ref_demande__reference_demande"),
    nom_expert=F("identifiant_expert__nom"),
    date_transfert_value=F("date_transfert")  # ⚠️ Alias différent du champ
).order_by("-date_transfert")[:5] 

### INSTRUCTIONS CRITIQUES :
✅ Toujours utiliser les bons `related_name` :  
- Application → demandes  
- Responsable → demandes  
- Demande → transferts, audits, satisfactions  

✅ Si aucune donnée → `resultat = "Aucun résultat trouvé"`

✅ Jamais afficher **toutes les données** (max 5 à 10 résultats)

✅ Retourne uniquement du code Python valide, sans explication, sans ```python
✅ Définis toujours une variable `resultat`

---

Commande utilisateur : {text}
"""

            result = llm.invoke(prompt)
            code = result.content.strip()
            code = re.sub(r"^```python|^```|```$", "", code, flags=re.MULTILINE).strip()

            # ✅ Correction automatique
            code = code.replace("Count('demande')", "Count('demandes')")
            code = code.replace("Count('application')", "Count('demandes')")
            code = code.replace("Count('responsable')", "Count('demandes')")

            from django.db.models import Count, Avg, Max, Min, Sum, F, ExpressionWrapper, fields
            from datetime import datetime, timedelta

            local_vars = {
                "Demande": Demande,
                "Responsable": Responsable,
                "Application": Application,
                "Transfert": Transfert,
                "Audit": Audit,
                "Satisfaction": Satisfaction,
                "Historique": Historique,
                "Count": Count,
                "Avg": Avg,
                "Max": Max,
                "Min": Min,
                "Sum": Sum,
                "F": F,
                "ExpressionWrapper": ExpressionWrapper,
                "fields": fields,
                "Q": Q,
                "datetime": datetime,
                "timedelta": timedelta,
                "ObjectDoesNotExist": ObjectDoesNotExist,
                "resultat": None,
                "colonnes": None
            }

            try:
                exec(code, {}, local_vars)

                colonnes = local_vars.get("colonnes", None)
                resultat_final = local_vars.get("resultat", None)

                # ✅ Cas 1 : tableau avec colonnes
                if colonnes and isinstance(resultat_final, list):
                    return JsonResponse({
                        "result": resultat_final,
                        "is_table": True,
                        "columns": colonnes,
                        "conversation_id": conversation_id,
                        "status": "success"
                    })

                # ✅ Cas 2 : valeur simple
                return JsonResponse({
                    "result": str(resultat_final),
                    "is_table": False,
                    "conversation_id": conversation_id,
                    "status": "success"
                })

            except Exception as e:
                return JsonResponse({
                    "error": f"Erreur lors de l'exécution : {str(e)}\n\nCode généré :\n{code}",
                    "conversation_id": conversation_id
                }, status=500)

        except Exception as e:
            error_message = f"Erreur d'analyse: {str(e)}"
            Historique.objects.create(
                requete=text,
                reponse=error_message,
                conversation_id=conversation_id
            )
            return JsonResponse({
                "error": error_message,
                "conversation_id": conversation_id
            }, status=500)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def get_conversation_history(request):
    """Récupère l'historique d'une conversation"""
    if request.method == "GET":
        conversation_id = request.GET.get("conversation_id")
        if conversation_id:
            historique = Historique.objects.filter(
                conversation_id=conversation_id
            ).order_by('date_requete').values(
                'requete', 'reponse', 'date_requete'
            )
            return JsonResponse({
                "history": list(historique),
                "conversation_id": conversation_id
            })
    return JsonResponse({"error": "ID de conversation requis"}, status=400)


@csrf_exempt
def chatbot_suggestions(request):
    """Fournit des suggestions de questions pour le chatbot"""
    suggestions = [
        "Combien de demandes au total ?",
        "Quelles sont les catégories de demandes les plus fréquentes ?",
        "Combien de demandes sont encore ouvertes ?",
        "Quel est le score moyen de satisfaction ?",
        "Quels sont les demandeurs les plus actifs ?",
        "Combien de demandes ont été transférées ?",
        "Quelles applications génèrent le plus de demandes ?",
        "Combien d'audits ont été réalisés ce mois ?",
        "Quel est le délai moyen de traitement ?",
        "Combien de demandes ont été refusées ?"
    ]
    
@csrf_exempt
def demandes_per_categorie_chart(request):
    if request.method == "GET":
        from .models import Demande
        from django.db.models import Count
        data = (
            Demande.objects.values('categorie')
            .annotate(count=Count('categorie'))
            .order_by('categorie')
        )
        labels = [item['categorie'] for item in data]
        values = [item['count'] for item in data]
        return JsonResponse({
            'labels': labels,
            'values': values
        })
    return JsonResponse({'error': 'Méthode non autorisée.'}, status=405)