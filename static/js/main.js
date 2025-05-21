document.addEventListener("DOMContentLoaded", function () {
  // Animations au défilement
  const animateOnScroll = function () {
    const elements = document.querySelectorAll(".fade-in-up");

    elements.forEach((element) => {
      const elementPosition = element.getBoundingClientRect().top;
      const windowHeight = window.innerHeight;

      if (elementPosition < windowHeight - 50) {
        element.classList.add("visible");
      }
    });
  };

  window.addEventListener("scroll", animateOnScroll);
  animateOnScroll(); // Exécuter une fois au chargement

  // Gestion des likes
  // Gestion des likes
  const likeButtons = document.querySelectorAll(".like-button");
  likeButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      const articleId = this.dataset.id;
      const likeCount = document.querySelector(`.like-count-${articleId}`);
      const likeIcon = this.querySelector("i");

      fetch(`/like/${articleId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          likeCount.textContent = data.total_likes;

          // Animation de like
          likeCount.classList.add("pulse");
          setTimeout(() => {
            likeCount.classList.remove("pulse");
          }, 500);

          if (data.liked) {
            // L'utilisateur aime maintenant l'article
            likeIcon.className = ""; // Réinitialiser toutes les classes
            likeIcon.classList.add("fas", "fa-heart", "text-danger");
            button.classList.add("liked");
          } else {
            // L'utilisateur n'aime plus l'article
            likeIcon.className = ""; // Réinitialiser toutes les classes
            likeIcon.classList.add("far", "fa-heart");
            button.classList.remove("liked");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          // Afficher un message d'erreur à l'utilisateur
          alert(
            "Une erreur est survenue lors de l'action \"J'aime\". Veuillez réessayer."
          );
        });
    });
  });

  // Gestion des commentaires
  const commentForms = document.querySelectorAll(".comment-form");
  commentForms.forEach((form) => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const articleId = this.dataset.id;
      const commentInput = this.querySelector(".comment-input");
      const commentsList = document.querySelector(
        `.comments-list-${articleId}`
      );
      const commentCount = document.querySelector(
        `.comment-count-${articleId}`
      );

      if (commentInput.value.trim() === "") return;

      fetch(`/comment/${articleId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: commentInput.value,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Ajouter le nouveau commentaire à la liste
            const newComment = document.createElement("div");
            newComment.className = "comment mb-3 fade-in";
            newComment.innerHTML = `
                        <div class="d-flex">
                            <img src="${data.author_image}" alt="${data.author}" class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
                            <div>
                                <div class="fw-bold">${data.author}</div>
                                <div>${data.content}</div>
                                <small class="text-muted">À l'instant</small>
                            </div>
                        </div>
                    `;

            // Si aucun commentaire, supprimer le message "Aucun commentaire"
            if (commentsList.querySelector(".text-muted")) {
              commentsList.innerHTML = "";
            }

            commentsList.appendChild(newComment);

            // Animation du nouveau commentaire
            setTimeout(() => {
              newComment.classList.add("visible");
            }, 10);

            // Mettre à jour le compteur de commentaires
            commentCount.textContent = data.total_comments;
            commentCount.classList.add("pulse");
            setTimeout(() => {
              commentCount.classList.remove("pulse");
            }, 500);

            // Réinitialiser le formulaire
            commentInput.value = "";
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  });

  // Toggle pour afficher/masquer les commentaires
  const commentToggles = document.querySelectorAll(".toggle-comments");
  commentToggles.forEach((toggle) => {
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      const articleId = this.dataset.id;
      const commentsSection = document.querySelector(
        `.comments-section-${articleId}`
      );

      if (
        commentsSection.style.display === "none" ||
        commentsSection.style.display === ""
      ) {
        commentsSection.style.display = "block";
        this.innerHTML = '<i class="fas fa-comment me-1"></i> Masquer';

        // Animation d'ouverture
        commentsSection.style.opacity = "0";
        commentsSection.style.transform = "translateY(-10px)";
        setTimeout(() => {
          commentsSection.style.opacity = "1";
          commentsSection.style.transform = "translateY(0)";
        }, 10);
      } else {
        commentsSection.style.opacity = "1";
        commentsSection.style.transform = "translateY(0)";
        setTimeout(() => {
          commentsSection.style.opacity = "0";
          commentsSection.style.transform = "translateY(-10px)";
          setTimeout(() => {
            commentsSection.style.display = "none";
            this.innerHTML = '<i class="far fa-comment me-1"></i> Commentaires';
          }, 300);
        }, 10);
      }
    });
  });

  // Gestion de la suppression de documents
  const deleteButtons = document.querySelectorAll(".delete-document");
  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      if (confirm("Êtes-vous sûr de vouloir supprimer ce document?")) {
        const documentId = this.dataset.id;
        const documentCard = this.closest(".document-card");

        fetch(`/delete-document/${documentId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              // Animation de suppression
              documentCard.style.opacity = "0";
              documentCard.style.transform = "translateX(20px)";
              setTimeout(() => {
                documentCard.remove();
              }, 300);
            }
          })
          .catch((error) => console.error("Error:", error));
      }
    });
  });

  // Fonction pour obtenir le cookie CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Effet de survol pour les cartes
  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    card.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-5px)";
    });

    card.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0)";
    });
  });

  // Animations CSS supplémentaires
  document.head.insertAdjacentHTML(
    "beforeend",
    `
        <style>
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.2); }
                100% { transform: scale(1); }
            }
            
            .pulse {
                animation: pulse 0.5s ease-in-out;
            }
            
            .fade-in-up {
                opacity: 0;
                transform: translateY(20px);
                transition: opacity 0.5s ease, transform 0.5s ease;
            }
            
            .fade-in-up.visible {
                opacity: 1;
                transform: translateY(0);
            }
            
            .liked {
                animation: pulse 0.5s ease-in-out;
            }
        </style>
    `
  );

  // Gestion du mode sombre - DÉPLACER CE CODE ICI, À L'INTÉRIEUR DE L'ÉVÉNEMENT DOMContentLoaded
  const darkModeToggle = document.getElementById("darkModeToggle");
  if (darkModeToggle) {
    const body = document.body;

    // Vérifier si le mode sombre est déjà activé dans localStorage
    if (localStorage.getItem("darkMode") === "enabled") {
      body.classList.add("dark-mode");
      darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    // Gérer le basculement du mode sombre
    darkModeToggle.addEventListener("click", () => {
      console.log("Bouton de mode sombre cliqué");
      console.log("Mode sombre actuel:", body.classList.contains("dark-mode"));

      if (body.classList.contains("dark-mode")) {
        console.log("Désactivation du mode sombre");
        body.classList.remove("dark-mode");
        localStorage.setItem("darkMode", "disabled");
        darkModeToggle.innerHTML = '<i class="fas fa-moon"></i>';
      } else {
        console.log("Activation du mode sombre");
        body.classList.add("dark-mode");
        localStorage.setItem("darkMode", "enabled");
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i>';
      }

      console.log("Nouveau mode sombre:", body.classList.contains("dark-mode"));
    });
  }

  // Pagination infinie - DÉPLACER CE CODE ÉGALEMENT À L'INTÉRIEUR
  const articleContainer = document.querySelector(".article-container");
  if (articleContainer) {
    let page = 2; // Commencer à la page 2 car la page 1 est déjà chargée
    let loading = false;
    let hasMore = true;

    function loadMoreArticles() {
      if (loading || !hasMore) return;

      loading = true;
      const spinner = document.createElement("div");
      spinner.className = "text-center my-4";
      spinner.innerHTML =
        '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Chargement...</span></div>';
      articleContainer.appendChild(spinner);

      fetch(`?page=${page}`)
        .then((response) => response.text())
        .then((html) => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, "text/html");
          const newArticles = doc.querySelectorAll(".article-card");

          spinner.remove();

          if (newArticles.length === 0) {
            hasMore = false;
            return;
          }

          newArticles.forEach((article) => {
            articleContainer.appendChild(article.cloneNode(true));
          });

          page++;
          loading = false;
        })
        .catch((error) => {
          console.error("Erreur:", error);
          spinner.remove();
          loading = false;
        });
    }

    // Détecter quand l'utilisateur atteint le bas de la page
    window.addEventListener("scroll", () => {
      if (
        window.innerHeight + window.scrollY >=
        document.body.offsetHeight - 500
      ) {
        loadMoreArticles();
      }
    });
  }

  // Fonction fetchWithCSRF - DÉPLACER ÉGALEMENT
  function fetchWithCSRF(url, options = {}) {
    const csrftoken = getCookie("csrftoken");

    // Définir les en-têtes par défaut
    const headers = {
      "X-CSRFToken": csrftoken,
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };

    // Fusionner avec les options fournies
    return fetch(url, {
      ...options,
      headers,
    });
  }
});

// Nettoyer les préférences de mode sombre (à ajouter au début du fichier)
document.addEventListener("DOMContentLoaded", function () {
  localStorage.removeItem("darkMode");
});
