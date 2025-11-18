// === Footer year ===
document.getElementById("year").textContent = new Date().getFullYear();

// === GitHub repos ===

(async function loadGitHubRepos() {
  const container = document.getElementById("githubRepos");
  if (!container) return;

  const username = container.getAttribute("data-github-username");
  if (!username || username === "YOUR_GITHUB_USERNAME") {
    container.innerHTML =
      '<p class="muted">Set your GitHub username in <code>data-github-username</code> to show your latest repositories.</p>';
    return;
  }

  try {
    const res = await fetch(
      `https://api.github.com/users/${encodeURIComponent(
        username
      )}/repos?sort=updated&per_page=6`
    );

    if (!res.ok) {
      throw new Error("GitHub API error");
    }

    const repos = await res.json();

    if (!repos.length) {
      container.innerHTML =
        '<p class="muted">No public repositories found yet.</p>';
      return;
    }

    container.innerHTML = "";

    repos.forEach((repo) => {
      const card = document.createElement("article");
      card.className = "project-card";

      const name = document.createElement("h3");
      name.textContent = repo.name;

      const desc = document.createElement("p");
      desc.textContent =
        repo.description || "No description provided for this repository.";

      const meta = document.createElement("div");
      meta.className = "project-meta";

      if (repo.language) {
        const lang = document.createElement("span");
        lang.textContent = repo.language;
        meta.appendChild(lang);
      }

      const updated = document.createElement("span");
      const date = new Date(repo.updated_at);
      updated.textContent = `Updated ${date.toLocaleDateString()}`;
      meta.appendChild(updated);

      const links = document.createElement("div");
      links.className = "project-links";

      const link = document.createElement("a");
      link.href = repo.html_url;
      link.target = "_blank";
      link.rel = "noopener";
      link.textContent = "View on GitHub";
      links.appendChild(link);

      card.appendChild(name);
      card.appendChild(desc);
      card.appendChild(meta);
      card.appendChild(links);

      container.appendChild(card);
    });
  } catch (err) {
    console.error(err);
    container.innerHTML =
      '<p class="muted">Could not load repositories from GitHub right now.</p>';
  }
})();

// === Contact form -> mailto ===
document.getElementById("contactForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const name = this.name.value.trim();
  const email = this.email.value.trim();
  const message = this.message.value.trim();

  if (!name || !email || !message) return;

  const subject = encodeURIComponent("Contact from esberg.dev portfolio");
  const body = encodeURIComponent(
    `Name: ${name}\nEmail: ${email}\n\n${message}`
  );

  window.location.href = `mailto:theo@esberg.dev?subject=${subject}&body=${body}`;
});
