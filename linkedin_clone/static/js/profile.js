// Script pour la page de profil

document.addEventListener('DOMContentLoaded', function() {
    // Gestion des onglets
    const tabLinks = document.querySelectorAll('.nav-link');
    const tabContents = document.querySelectorAll('.tab-pane');
    
    tabLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Désactiver tous les onglets
            tabLinks.forEach(l => l.classList.remove('active'));
            tabContents.forEach(c => {
                c.classList.remove('show');
                c.classList.remove('active');
            });
            
            // Activer l'onglet cliqué
            this.classList.add('active');
            const target = this.getAttribute('href');
            document.querySelector(target).classList.add('show');
            document.querySelector(target).classList.add('active');
        });
    });
    
    // Gestion de la suppression de documents
    const deleteDocumentBtns = document.querySelectorAll('.delete-document');
    deleteDocumentBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (confirm('Êtes-vous sûr de vouloir supprimer ce document ?')) {
                const documentId = this.dataset.id;
                
                fetch(`/document/${documentId}/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/json'
                    },
                    credentials: 'same-origin'
                })
                .then(response => {
                    if (response.ok) {
                        // Supprimer l'élément du DOM
                        this.closest('.document-item').remove();
                        
                        // Afficher un message de succès
                        const alertDiv = document.createElement('div');
                        alertDiv.className = 'alert alert-success';
                        alertDiv.textContent = 'Document supprimé avec succès.';
                        document.querySelector('.documents-list').prepend(alertDiv);
                        
                        // Supprimer le message après 3 secondes
                        setTimeout(() => {
                            alertDiv.remove();
                        }, 3000);
                    } else {
                        throw new Error('Erreur lors de la suppression du document');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Une erreur est survenue lors de la suppression du document.');
                });
            }
        });
    });
    
    // Prévisualisation de l'image de profil
    const imageInput = document.querySelector('#id_image');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.createElement('img');
                    preview.src = e.target.result;
                    preview.className = 'img-preview';
                    preview.style.maxWidth = '100%';
                    preview.style.maxHeight = '200px';
                    preview.style.marginTop = '10px';
                    
                    const previewContainer = imageInput.parentElement;
                    const existingPreview = previewContainer.querySelector('.img-preview');
                    if (existingPreview) {
                        existingPreview.remove();
                    }
                    
                    previewContainer.appendChild(preview);
                };
                reader.readAsDataURL(file);
            }
        });
    }
});