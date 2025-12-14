import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from django.apps import apps
import shutil

# --- MODÈLES À METTRE À JOUR ---
# Listez ici tous les modèles qui ont un ou plusieurs ImageField
# Le format est ('nom_app.NomModele', ['nom_champ_image_1', 'nom_champ_image_2'])
MODELS_WITH_IMAGES = [
    # ('menu.Product', ['image', 'image_dop']),
    ('menu.MenuCatalog', ['image']),
    # ('Filials.Filials', ['image']),
    # ('slider.Slider', ['image']),
    # Ajoutez d'autres modèles si j'en ai oublié
    # ('photogallery.PhotoGallery', ['image']),
    # ('awards.Award', ['image']),
]

# --- CHEMIN DE L'IMAGE PAR DÉFAUT ---
# Adaptez ce chemin si nécessaire
DEFAULT_IMAGE_PATH_RELATIVE = 'defaults/default_imo.webp'


class Command(BaseCommand):
    help = 'Remplace tous les ImageFields existants par une image par défaut.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("--- Début du script de remplacement des images ---"))

        # 1. Préparer l'image par défaut
        default_image_full_path = os.path.join(settings.MEDIA_ROOT, DEFAULT_IMAGE_PATH_RELATIVE)
        
        if not os.path.exists(default_image_full_path):
            self.stdout.write(self.style.ERROR(f"ERREUR: L'image par défaut est introuvable à l'emplacement : {default_image_full_path}"))
            self.stdout.write(self.style.ERROR("Veuillez vérifier le chemin dans le script et vous assurer que l'image existe."))
            return

        self.stdout.write(f"Utilisation de l'image par défaut : {default_image_full_path}")

        # 2. Parcourir tous les modèles configurés
        for app_model_str, field_names in MODELS_WITH_IMAGES:
            try:
                model = apps.get_model(app_model_str)
                self.stdout.write(self.style.SUCCESS(f"\nTraitement du modèle : {app_model_str}"))
            except LookupError:
                self.stdout.write(self.style.WARNING(f"Modèle {app_model_str} non trouvé. Ignoré."))
                continue

            # Récupérer tous les objets de ce modèle
            queryset = model.objects.all()
            total_objects = queryset.count()
            self.stdout.write(f"Trouvé {total_objects} objets à vérifier.")
            
            updated_count = 0

            # 3. Parcourir tous les champs d'image pour ce modèle
            for field_name in field_names:
                for obj in queryset:
                    image_field = getattr(obj, field_name)

                    # Vérifier si l'objet a une image
                    if image_field and image_field.name:
                        
                        # Ne pas remplacer si c'est déjà l'image par défaut
                        if image_field.name == DEFAULT_IMAGE_PATH_RELATIVE:
                            continue

                        original_path = image_field.path
                        self.stdout.write(f"  - Remplacement de '{image_field.name}' pour l'objet ID {obj.pk}...")
                        
                        # Remplacer le contenu du fichier sur le disque
                        try:
                            # Copier l'image par défaut par-dessus l'ancienne
                            shutil.copyfile(default_image_full_path, original_path)
                            updated_count += 1
                        except FileNotFoundError:
                            # Le fichier n'existait pas sur le disque, on l'assigne simplement
                            image_field.name = DEFAULT_IMAGE_PATH_RELATIVE
                            obj.save()
                            updated_count += 1
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f"    ! Erreur lors de la copie du fichier pour l'ID {obj.pk}: {e}"))
            
            if updated_count > 0:
                self.stdout.write(self.style.SUCCESS(f"-> {updated_count} images mises à jour pour {app_model_str}."))
            else:
                 self.stdout.write(f"-> Aucune image à mettre à jour pour {app_model_str}.")


        self.stdout.write(self.style.SUCCESS("\n--- Script terminé avec succès ! ---"))