const header = document.querySelector("[data-header]");
const toggle = document.querySelector("[data-menu-toggle]");
const nav = document.querySelector("[data-nav]");
const navLinks = [...document.querySelectorAll(".site-nav a")];
const sections = [...document.querySelectorAll("main section[id]")];
const revealItems = [...document.querySelectorAll(".reveal")];

function setHeaderState() {
  header?.classList.toggle("is-scrolled", window.scrollY > 12);
}

function setActiveLink(id) {
  navLinks.forEach((link) => {
    link.classList.toggle("is-active", link.getAttribute("href") === `#${id}`);
  });
}

function setActiveFromHash() {
  const id = window.location.hash.slice(1) || "inicio";
  setActiveLink(id);
}

function alignHashTarget() {
  const id = window.location.hash.slice(1);
  if (!id) return;

  const target = document.getElementById(id);
  if (!target) return;

  target.scrollIntoView({ block: "start" });
  requestAnimationFrame(revealVisibleItems);
}

function closeMenu() {
  nav?.classList.remove("is-open");
  toggle?.setAttribute("aria-expanded", "false");
}

toggle?.addEventListener("click", () => {
  const isOpen = nav?.classList.toggle("is-open");
  toggle.setAttribute("aria-expanded", String(Boolean(isOpen)));
});

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    closeMenu();
    const id = link.getAttribute("href")?.slice(1);
    if (id) setActiveLink(id);
  });
});

window.addEventListener("scroll", setHeaderState, { passive: true });
window.addEventListener("hashchange", () => {
  setActiveFromHash();
  requestAnimationFrame(alignHashTarget);
});
setHeaderState();
setActiveFromHash();

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.05, rootMargin: "0px 0px -3% 0px" }
);

revealItems.forEach((item) => revealObserver.observe(item));

function revealVisibleItems() {
  revealItems.forEach((item) => {
    const rect = item.getBoundingClientRect();
    if (rect.top < window.innerHeight && rect.bottom > 0) {
      item.classList.add("is-visible");
    }
  });
}

requestAnimationFrame(revealVisibleItems);
window.addEventListener("load", () => {
  revealVisibleItems();
  requestAnimationFrame(alignHashTarget);
  window.setTimeout(alignHashTarget, 350);
  window.setTimeout(alignHashTarget, 1200);
  window.setTimeout(alignHashTarget, 2200);
});

function setActiveFromScroll() {
  const offset = window.innerHeight * 0.32;
  const current = sections.reduce((active, section) => {
    return section.offsetTop - offset <= window.scrollY ? section : active;
  }, sections[0]);

  if (current) setActiveLink(current.id);
}

window.addEventListener("scroll", setActiveFromScroll, { passive: true });
setActiveFromScroll();
