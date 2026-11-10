/* Section tabs: on a narrow screen the row scrolls sideways. Bring the current page to the middle, and show a fade on
   each edge that has more tabs beyond it. Nothing here is needed on wide screens, where the row wraps instead. */
(function () {
  // the header wraps on narrow screens, so the tabs stick below its real height
  const head = document.querySelector(".site-head");
  const setHead = () => head && document.documentElement.style.setProperty("--head-h", head.offsetHeight + "px");
  setHead();
  addEventListener("resize", setHead);

  const list = document.querySelector(".st-list");
  if (!list) return;
  const cur = list.querySelector('[aria-current="page"]');
  if (cur && list.scrollWidth > list.clientWidth) {
    const r = cur.getBoundingClientRect(), box = list.getBoundingClientRect();
    list.scrollLeft += r.left - box.left - (box.width - r.width) / 2;
  }
  const edges = () => {
    list.classList.toggle("at-end", list.scrollLeft + list.clientWidth >= list.scrollWidth - 4);
    list.classList.toggle("not-start", list.scrollLeft > 4);
  };
  list.addEventListener("scroll", edges, { passive: true });
  addEventListener("resize", edges);
  edges();
})();
