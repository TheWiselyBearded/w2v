/* World2Vision — small progressive enhancements. No dependencies. */
(function () {
  // Mobile navigation drawer
  var burger = document.getElementById("burger");
  var scrim = document.getElementById("scrim");
  function closeNav() { document.body.classList.remove("nav-open"); }
  if (burger) {
    burger.addEventListener("click", function () {
      document.body.classList.toggle("nav-open");
    });
  }
  if (scrim) scrim.addEventListener("click", closeNav);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeNav();
  });
  // Close the drawer after tapping a link
  document.querySelectorAll(".sidebar a").forEach(function (a) {
    a.addEventListener("click", closeNav);
  });

  // Reading-progress rail
  var bar = document.getElementById("progress");
  if (bar) {
    var tick = function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      var pct = max > 0 ? (h.scrollTop || document.body.scrollTop) / max : 0;
      bar.style.width = (pct * 100).toFixed(1) + "%";
    };
    document.addEventListener("scroll", tick, { passive: true });
    tick();
  }
})();
