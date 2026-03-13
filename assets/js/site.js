document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", (event) => {
    const target = anchor.getAttribute("href");
    if (!target || target === "#") {
      return;
    }

    const section = document.querySelector(target);
    if (!section) {
      return;
    }

    event.preventDefault();
    section.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});
