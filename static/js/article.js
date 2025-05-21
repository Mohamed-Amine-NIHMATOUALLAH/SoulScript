// Script pour la page d'article

document.addEventListener("DOMContentLoaded", function () {
  // Gestion des likes
  const likeBtn = document.querySelector(".like-btn");
  if (likeBtn) {
    likeBtn.addEventListener("click", function () {
      if (!document.body.classList.contains("logged-in")) {
        window.location.href = "/login/?next=" + window.location.pathname;
        return;
      }

      const articleId = this.dataset.articleId;

      fetch(`/article/${articleId}/like/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
            .value,
          "Content-Type": "application/json",
        },
        credentials: "same-origin",
      })
        .then((response) => response.json())
        .then((data) => {
          const likeIcon = likeBtn.querySelector("i");
          const likeCount = likeBtn.querySelector(".like-count");

          if (data.liked) {
            likeBtn.classList.add("liked");
            likeIcon.classList.remove("far");
            likeIcon.classList.add("fas");
          } else {
            likeBtn.classList.remove("liked");
            likeIcon.classList.remove("fas");
            likeIcon.classList.add("far");
          }

          likeCount.textContent = data.total_likes;
        })
        .catch((error) => {
          console.error("Error:", error);
          // Ajouter un message d'erreur visible pour l'utilisateur
          const errorDiv = document.createElement("div");
          errorDiv.className = "alert alert-danger";
          errorDiv.textContent = "Une erreur est survenue. Veuillez réessayer.";
          document.querySelector(".container").prepend(errorDiv);
        });
    });
  }

  // Gestion du partage
  const shareButtons = document.querySelectorAll(".share-btn");
  shareButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const platform = this.dataset.share;
      const url = encodeURIComponent(window.location.href);
      const title = encodeURIComponent(
        document.querySelector(".article-title").textContent
      );

      let shareUrl;
      switch (platform) {
        case "facebook":
          shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
          break;
        case "twitter":
          shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${title}`;
          break;
        case "linkedin":
          shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${url}`;
          break;
      }

      window.open(shareUrl, "_blank", "width=600,height=400");
    });
  });

  // Gestion des commentaires
  const commentForm = document.querySelector(".comment-form form");
  if (commentForm) {
    commentForm.addEventListener("submit", function (e) {
      const textarea = this.querySelector("textarea");
      if (!textarea.value.trim()) {
        e.preventDefault();
        alert("Veuillez écrire un commentaire avant de soumettre.");
      }
    });
  }
});
