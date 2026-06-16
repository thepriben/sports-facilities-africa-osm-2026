// ---------- Compteurs animés ----------
function animateCount(el, target) {
  const dur = 1400;
  const start = performance.now();
  const fmt = (n) => n.toLocaleString("fr-FR");
  function tick(now) {
    const p = Math.min((now - start) / dur, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = fmt(Math.round(target * eased));
    if (p < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

const statObserver = new IntersectionObserver((entries, obs) => {
  entries.forEach((e) => {
    if (!e.isIntersecting) return;
    const target = parseInt(e.target.dataset.count, 10);
    animateCount(e.target.querySelector(".stat__num"), target);
    obs.unobserve(e.target);
  });
}, { threshold: 0.4 });

document.querySelectorAll(".stat").forEach((s) => statObserver.observe(s));

// ---------- Révélation au scroll ----------
document.querySelectorAll(".section, .card, .stat").forEach((el) => el.classList.add("reveal"));
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) {
      e.target.classList.add("is-visible");
      revealObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

// ---------- Graphique de distribution ----------
fetch("data/sport_counts.json")
  .then((r) => r.json())
  .then((data) => {
    const top = data.top.slice(0, 15);
    const labels = top.map((d) => d.label);
    const values = top.map((d) => d.count);

    const note = document.getElementById("chartNote");
    if (note) {
      note.textContent =
        `${data.total_sites.toLocaleString("fr-FR")} équipements · ` +
        `${data.distinct_sports} sports distincts · instantané du ${data.snapshot_date}.`;
    }

    const ctx = document.getElementById("sportsChart");
    if (!ctx || typeof Chart === "undefined") return;

    const css = getComputedStyle(document.documentElement);
    const accent = css.getPropertyValue("--accent").trim() || "#ff6b3d";
    const muted = css.getPropertyValue("--muted").trim() || "#9aa6b8";
    const line = css.getPropertyValue("--line").trim() || "#283042";

    new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [{
          label: "Nombre de sites",
          data: values,
          backgroundColor: accent,
          borderRadius: 6,
          maxBarThickness: 26,
        }],
      },
      options: {
        indexAxis: "y",
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (c) => ` ${c.parsed.x.toLocaleString("fr-FR")} sites`,
            },
          },
        },
        scales: {
          x: {
            ticks: { color: muted, callback: (v) => v.toLocaleString("fr-FR") },
            grid: { color: line },
          },
          y: {
            ticks: { color: "#e9edf3", font: { size: 12 } },
            grid: { display: false },
          },
        },
      },
    });
  })
  .catch((err) => console.error("Chargement des données échoué :", err));
