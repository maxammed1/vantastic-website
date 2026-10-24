/* Sends a form without leaving the page, then goes to the thank-you page.
   Without JavaScript the form posts normally and the Worker redirects. */
(function () {
  document.querySelectorAll("form.lead-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = form.querySelector(".form-status");
      var button = form.querySelector("button[type=submit]");
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });
      data.page = location.href;
      button.disabled = true;
      status.className = "form-status";
      status.textContent = "Sending...";
      fetch(form.action, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data),
      })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (res) {
          if (res.ok) { location.href = "/thanks/"; return; }
          throw new Error(res.message || "");
        })
        .catch(function (err) {
          button.disabled = false;
          status.className = "form-status error";
          status.textContent = err.message || "Sorry, that didn't go through. Please call us at (507) 272-4901.";
        });
    });
  });
})();
