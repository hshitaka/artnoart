(() => {
  "use strict";

  const statusEl = document.getElementById("dwet-status");
  const nav = document.getElementById("site-nav");
  const toggle = document.querySelector(".nav-toggle");
  const sections = [...document.querySelectorAll("main section[id]")];
  const navLinks = [...document.querySelectorAll(".site-nav a[href^='#']")];
  let statusTimer = 0;
  let activeAudio = null;
  let activeTrack = null;

  function announce(message, isError = false) {
    if (!statusEl) return;
    statusEl.textContent = message;
    statusEl.classList.toggle("is-error", Boolean(isError));
    statusEl.classList.add("is-visible");
    window.clearTimeout(statusTimer);
    statusTimer = window.setTimeout(() => {
      statusEl.classList.remove("is-visible");
    }, 3200);
  }

  function filenameFromUrl(url) {
    try {
      return decodeURIComponent(new URL(url, window.location.href).pathname.split("/").pop() || "download");
    } catch {
      return "download";
    }
  }

  const DWET = {
    catalogUrl: "assets/downloads/catalog.json",

    async loadCatalog() {
      const response = await fetch(this.catalogUrl, { cache: "no-store" });
      if (!response.ok) {
        throw new Error(`Catalogue indisponible (${response.status})`);
      }
      return response.json();
    },

    direct(url, filename) {
      const name = filename || filenameFromUrl(url);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", name);
      link.rel = "noopener";
      document.body.append(link);
      link.click();
      link.remove();
      return { ok: true, mode: "direct", url, filename: name };
    },

    async fetchBlob(url, filename) {
      const name = filename || filenameFromUrl(url);
      const response = await fetch(url, { cache: "no-store" });
      if (!response.ok) {
        throw new Error(`Échec fetch ${response.status} — ${url}`);
      }
      const blob = await response.blob();
      if (!blob.size) {
        throw new Error(`Fichier vide : ${url}`);
      }
      const objectUrl = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = objectUrl;
      link.download = name;
      document.body.append(link);
      link.click();
      link.remove();
      window.setTimeout(() => URL.revokeObjectURL(objectUrl), 1500);
      return {
        ok: true,
        mode: "fetch",
        url,
        filename: name,
        bytes: blob.size,
        type: blob.type || "application/octet-stream",
      };
    },

    async download(url, filename, mode = "direct") {
      if (mode === "fetch") {
        return this.fetchBlob(url, filename);
      }
      return this.direct(url, filename);
    },
  };

  window.DWET = DWET;

  function setExpanded(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    nav.classList.toggle("is-open", open);
  }

  toggle?.addEventListener("click", () => {
    setExpanded(toggle.getAttribute("aria-expanded") !== "true");
  });

  nav?.addEventListener("click", (event) => {
    if (event.target.closest("a")) setExpanded(false);
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") setExpanded(false);
  });

  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      const id = visible.target.id;
      navLinks.forEach((link) => {
        const current = link.hash === `#${id}`;
        if (current) link.setAttribute("aria-current", "page");
        else link.removeAttribute("aria-current");
      });
    },
    { rootMargin: "-35% 0px -50% 0px", threshold: [0.15, 0.4, 0.7] }
  );
  sections.forEach((section) => observer.observe(section));

  function stopPlayback() {
    if (activeAudio) {
      activeAudio.pause();
      activeAudio.src = "";
    }
    activeTrack?.classList.remove("is-playing");
    const playingButton = activeTrack?.querySelector(".play");
    if (playingButton) {
      const label = playingButton.getAttribute("aria-label") || "";
      playingButton.setAttribute("aria-label", label.replace(/^Pause/, "Lire"));
    }
    activeAudio = null;
    activeTrack = null;
  }

  document.querySelectorAll(".track .play").forEach((button) => {
    button.addEventListener("click", async () => {
      const track = button.closest(".track");
      const src = track?.dataset.src;
      if (!src) return;

      if (activeTrack === track && activeAudio && !activeAudio.paused) {
        stopPlayback();
        return;
      }

      stopPlayback();
      const audio = new Audio(src);
      audio.preload = "auto";
      activeAudio = audio;
      activeTrack = track;
      track.classList.add("is-playing");
      button.setAttribute("aria-label", (button.getAttribute("aria-label") || "Lire").replace(/^Lire/, "Pause"));
      audio.addEventListener("ended", stopPlayback, { once: true });
      audio.addEventListener("error", () => {
        stopPlayback();
        announce("Lecture impossible pour cet extrait.", true);
      }, { once: true });
      try {
        await audio.play();
      } catch {
        stopPlayback();
        announce("Le navigateur a bloqué la lecture automatique.", true);
      }
    });
  });

  document.addEventListener("click", async (event) => {
    const trigger = event.target.closest("[data-dwet-mode]");
    if (!trigger) return;

    const mode = trigger.dataset.dwetMode;
    const url = trigger.getAttribute("href") || trigger.dataset.src;
    const filename = trigger.dataset.filename;
    if (!url) return;

    if (mode === "direct" && trigger.tagName === "A") {
      announce(`Voie directe : ${filename || filenameFromUrl(url)}`);
      return;
    }

    event.preventDefault();
    try {
      const result = await DWET.download(url, filename, mode);
      announce(`Voie ${result.mode} : ${result.filename}${result.bytes ? ` · ${result.bytes} octets` : ""}`);
    } catch (error) {
      announce(error instanceof Error ? error.message : "Téléchargement impossible", true);
    }
  });
})();
