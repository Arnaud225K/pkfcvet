function handleAddToCartClick(productSlug, productName) {
    // 1. Préparer la modale de confirmation
    document.getElementById('add_product_name').textContent = productName;

    // 2. Appeler la fonction qui ajoute réellement au panier
    // (Cette fonction est déjà dans votre script)
    add_to_cart(productSlug);

    // 3. Exécuter tous les scripts de tracking
    // On les met dans un bloc try...catch pour que le site ne crashe pas si gtag ou yaCounter n'existent pas.
    try {
        if (typeof gtag === 'function') {
            gtag('event', 'oformit_zayavku', { 
                'event_category': 'send_ zayavka_kategoriya', 
                'event_action': 'click' 
            });
        }
    } catch (e) {
        console.warn("Erreur lors de l'appel à gtag:", e);
    }

    try {
        if (typeof yaCounter45142059 !== 'undefined' && typeof yaCounter45142059.reachGoal === 'function') {
            yaCounter45142059.reachGoal('button_zayavka_kategoriya');
        }
    } catch (e) {
        console.warn("Erreur lors de l'appel à yaCounter:", e);
    }
}
window.handleAddToCartClick = handleAddToCartClick;

// Le code s'exécute uniquement lorsque le document HTML est entièrement chargé.
$(document).ready(function() {

    // =========================================================================
    // SECTION 1: LECTURE DES URLS ET CONFIGURATION D'AJAX (CSRF)
    // =========================================================================
    
    // Lire les URLs générées par Django depuis le "pont" de données dans le HTML
    const URLS = JSON.parse(document.getElementById('js-urls').textContent);

    // Fonction pour récupérer le cookie CSRF (standard Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Configuration de jQuery pour envoyer le token CSRF avec toutes les requêtes POST
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // =========================================================================
    // SECTION 2: GESTIONNAIRE DE FORMULAIRE AJAX UNIVERSEL
    // =========================================================================
    
    // Ce seul gestionnaire s'applique à TOUS les formulaires avec class="ajax-form"
    $('.ajax-form').on('submit', function(event) {
        event.preventDefault();

        const form = this;
        const submitButton = $(form).find('button[type="submit"]');
        const formData = new FormData(form);

        submitButton.prop('disabled', true);
        $(form).find('.error-field').text(''); 

        $.ajax({
            url: $(form).attr('action'),
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function(data) {
                if (data.status === 'success') {
                    if (data.redirect_url) {
                        // Si le serveur nous dit de rediriger (ex: panier, demande de prix)
                        window.location.href = data.redirect_url;
                    } else {
                        // Sinon, c'est un formulaire de contact simple (ex: rappel)
                        alert('Заявка успешно отправлена!');
                        form.reset();
                        $(form).closest('.modal').modal('hide');
                    }
                }
            },
            error: function(xhr) {
                if (xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.errors) {
                    const errors = JSON.parse(xhr.responseJSON.errors);
                    // Afficher les erreurs spécifiques à chaque champ
                    for (const fieldName in errors) {
                        const message = errors[fieldName][0].message;
                        // On trouve le champ d'erreur grâce à l'attribut data-field-name
                        $(form).find(`.error-field[data-field-name="${fieldName}"]`).text(message);
                    }
                } else {
                    alert('Произошла ошибка сервера. Пожалуйста, попробуйте еще раз.');
                }
            },
            complete: function() {
                submitButton.prop('disabled', false); // Réactiver le bouton
            }
        });
    });



    // =========================================================================
    // SECTION 3: FONCTIONS GLOBALES (POUR COMPATIBILITÉ on_click)
    // =========================================================================
    

    window.add_to_cart = function(productSlug) {
        console.log("--- add_to_cart() appelée ---");

        const csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        
        if (!productSlug) {
            console.error("ERREUR JS: Le slug du produit est manquant. Arrêt.");
            return;
        }
        console.log("Slug reçu:", productSlug);

        // Préparation des données du formulaire
        const formData = new FormData();
        formData.append('product_slug', productSlug);
        formData.append('quantity', '1');
        formData.append('csrfmiddlewaretoken', csrftoken); 
        
        console.log("Données préparées pour l'envoi:", {
            product_slug: formData.get('product_slug'),
            quantity: formData.get('quantity')
        });

        $.ajax({
            url: URLS.send_form_order,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            
            beforeSend: function() {
                console.log("Envoi de la requête AJAX à:", URLS.send_form_order);
            },
            
            success: function(data) {
                console.log("--- Réponse AJAX reçue (succès) ---");
                console.log("Données de la réponse:", data);

                if (data.status === 'added') {
                    console.log("Statut 'added' confirmé. Appel de get_cart_count() et affichage de la modale.");
                    get_cart_count();
                    $('#modal-buy').modal('show');
                } else {
                    console.warn("Réponse de succès, mais statut inattendu:", data.status);
                    alert('Réponse inattendue du serveur.');
                }
            },
            
            error: function(xhr, status, error) {
                console.error("--- Réponse AJAX reçue (ERREUR) ---");
                console.error("Statut HTTP:", xhr.status);
                console.error("Réponse brute:", xhr.responseText);
                
                if (xhr.status === 400 && xhr.responseJSON && xhr.responseJSON.errors) {
                    const errors = JSON.parse(xhr.responseJSON.errors);
                    let errorMessage = "Erreur de validation du formulaire (voir console pour détails):\n";
                    for (const field in errors) {
                        errorMessage += `- ${errors[field][0].message}\n`;
                    }
                    alert(errorMessage);
                } else {
                    alert('Erreur serveur lors de l\'ajout au panier. Vérifiez la console pour plus de détails.');
                }
            }
        });
    };


    window.delete_product = function(itemId) {
        console.log("Tentative de suppression de l'article avec ID:", itemId);

        if (!itemId) {
            console.error("L'ID de l'article est manquant.");
            return;
        }

        // 1. Cibler le bon formulaire en utilisant l'ID unique
        const form = document.getElementById('form_delete_' + itemId);
        if (!form) {
            console.error("Formulaire de suppression non trouvé pour l'ID:", itemId);
            return;
        }
        
        // 2. Récupérer les données du formulaire
        const formData = new FormData(form);

        // 3. Envoyer la requête AJAX
        $.ajax({
            url: URLS.send_form_order,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function(data) {
                console.log("Réponse du serveur (suppression):", data);
                if (data.status === 'deleted' && data.item_id) {
                    // Succès ! Mettre à jour l'interface
                    get_cart_count();

                    // Cacher et supprimer la ligne du produit
                    $('#item_id_' + data.item_id).fadeOut('slow', function(){ 
                        $(this).remove();
                        // Vérifier si le panier est vide après la suppression
                        if ($('.product-in-order').length === 0) {
                            $('#cart_items_box').hide();
                            $('#cart_empty').show();
                        }
                    });
                } else {
                    alert('La suppression a échoué. Réponse inattendue du serveur.');
                }
            },
            error: function(xhr) {
                alert('Erreur lors de la suppression du produit.');
                console.error(xhr.responseText);
            }
        });
    };

    window.get_filter_url = function() {
        const formData = new FormData($('#filter_form').get(0));
        $.ajax({
            url: URLS.get_filter_url, // Utiliser l'URL lue depuis le HTML
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            success: function(data) {
                if (data.url) {
                    location.href = data.url;
                }
            },
            error: function(xhr) {
                alert('Возникла ошибка при фильтрации.');
            }
        });
    };

    window.get_cart_count = function() {
        $.ajax({
            url: URLS.get_cart_count, // Utiliser l'URL lue depuis le HTML
            method: "GET",
            success: function(data) {
                $('.cart_item_count').text(data.cart_item_count || 0);
                // ... (le reste de votre logique get_cart_count)
            }
        });
    };


    // =========================================================================
    // SECTION 4: APPEL INITIAL
    // =========================================================================
    
    // Mettre à jour le compteur du panier au chargement de la page.
    get_cart_count();

});