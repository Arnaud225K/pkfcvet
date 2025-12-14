import re
from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps
from django.utils.html import smart_urlquote

# --- MODÈLES À METTRE À JOUR ---
# Listez ici tous les modèles qui ont un ou plusieurs HTMLField de TinyMCE
# Le format est ('nom_app.NomModele', ['nom_champ_html_1', 'nom_champ_html_2'])
MODELS_WITH_TINYMCE = [
    ('menu.MenuCatalog', ['description']),
    # ('menu.Product', ['description']),
    # ('Filials.Filials', ['req', 'comment']),
    # ('News.News', ['full_text']), # Exemple, ajoutez vos autres modèles
]

# --- URL DE L'IMAGE PAR DÉFAUT ---
# Adaptez le chemin si nécessaire
DEFAULT_IMAGE_URL_PATH = 'defaults/default_image.jpg'


class Command(BaseCommand):
    help = 'Analyse le contenu des HTMLFields (TinyMCE) et remplace les URLs des images.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("--- Début du script de remplacement des images dans TinyMCE ---"))

        # 1. Construire l'URL complète de l'image par défaut
        # smart_urlquote s'assure que l'URL est correctement encodée
        default_image_url = smart_urlquote(f"{settings.MEDIA_URL}{DEFAULT_IMAGE_URL_PATH}")
        self.stdout.write(f"Utilisation de l'URL de remplacement : {default_image_url}")

        # 2. Définir l'expression régulière pour trouver les balises <img>
        # Cette regex est conçue pour trouver l'attribut src, même s'il y a d'autres attributs
        img_src_pattern = re.compile(r'<img([^>]+?)src=([\'"])(.*?)\2', re.IGNORECASE)

        total_replacements = 0

        # 3. Parcourir tous les modèles configurés
        for app_model_str, field_names in MODELS_WITH_TINYMCE:
            try:
                model = apps.get_model(app_model_str)
                self.stdout.write(self.style.SUCCESS(f"\nTraitement du modèle : {app_model_str}"))
            except LookupError:
                self.stdout.write(self.style.WARNING(f"Modèle {app_model_str} non trouvé. Ignoré."))
                continue

            queryset = model.objects.exclude(**{f'{field_names[0]}__isnull': True}).exclude(**{f'{field_names[0]}__exact': ''})
            
            for field_name in field_names:
                model_updated_count = 0
                
                # On ne prend que les objets où le champ n'est pas vide
                objects_to_check = queryset.exclude(**{f'{field_name}__isnull': True}).exclude(**{f'{field_name}__exact': ''})
                
                self.stdout.write(f"  - Vérification du champ '{field_name}' sur {objects_to_check.count()} objets...")
                
                for obj in objects_to_check:
                    original_html = getattr(obj, field_name)
                    
                    # On cherche toutes les balises <img> dans le HTML
                    # re.sub() est parfait pour trouver et remplacer
                    # Le lambda permet de ne remplacer que la partie 'src'
                    modified_html, num_subs = img_src_pattern.subn(
                        lambda m: f'<img{m.group(1)}src="{default_image_url}"',
                        original_html
                    )

                    # Si des remplacements ont été faits, on sauvegarde l'objet
                    if num_subs > 0:
                        setattr(obj, field_name, modified_html)
                        obj.save(update_fields=[field_name])
                        model_updated_count += 1
                        total_replacements += num_subs
                        self.stdout.write(f"    -> Remplacé {num_subs} image(s) dans l'objet ID {obj.pk}")

                if model_updated_count > 0:
                    self.stdout.write(self.style.NOTICE(f"  --> {model_updated_count} objets mis à jour pour le champ '{field_name}'."))

        self.stdout.write(self.style.SUCCESS(f"\n--- Script terminé. Total de {total_replacements} URLs d'images remplacées. ---"))