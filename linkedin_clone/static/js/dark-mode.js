// Créer un nouveau fichier pour le mode sombre
document.addEventListener('DOMContentLoaded', function() {
  const darkModeToggle = document.getElementById('darkModeToggle');
  const body = document.body;
  
  // Fonction pour activer le mode sombre
  function enableDarkMode() {
    console.log("Enabling dark mode");
    body.classList.add('dark-mode');
    localStorage.setItem('darkMode', 'enabled');
    if (darkModeToggle) {
      darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
  }
  
  // Fonction pour désactiver le mode sombre
  function disableDarkMode() {
    body.classList.remove('dark-mode');
    localStorage.setItem('darkMode', 'disabled');
    if (darkModeToggle) {
      darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
    }
  }
  
  // Vérifier la préférence enregistrée
  if (localStorage.getItem('darkMode') === 'enabled') {
    enableDarkMode();
  }
  
  // Ajouter l'écouteur d'événement au bouton
  if (darkModeToggle) {
    darkModeToggle.addEventListener('click', function() {
      if (body.classList.contains('dark-mode')) {
        disableDarkMode();
      } else {
        enableDarkMode();
      }
    });
  }
});