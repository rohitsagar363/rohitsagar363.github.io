document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", (event) => {
    const target = anchor.getAttribute("href");
    if (!target || target === "#") {
      return;
    }

    const element = document.querySelector(target);
    if (!element) {
      return;
    }

    event.preventDefault();
    element.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});
