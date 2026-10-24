/* Vantastic Transit, site Worker (Workers + Static Assets).

   POST /api/request -> record the form in Lead Landing (ride request, facility account or driver application)
   everything else   -> served from the static assets (ASSETS binding)

   Lead Landing is the ONLY CRM for this business. The Lead Landing workflow on each form
   creates the contact, deal card, call-back task and owner alert email, so the Worker sends no email.
   Form ids are public configuration (no token). Fill them in once the LL sub-account exists,
   or set Worker variables LL_FORM_RIDE / LL_FORM_FACILITY / LL_FORM_DRIVER. */
import { postToLeadLanding } from "./leadlanding-post.js";

const LL_FORMS = {
  ride: "", // "Vantastic Ride Request"
  facility: "", // "Vantastic Facility Account"
  driver: "", // "Vantastic Driver Application"
};
const PHONE_DISPLAY = "(507) 272-4901";

const clean = (v, max = 500) => String(v == null ? "" : v).trim().slice(0, max);

async function readBody(request) {
  const type = request.headers.get("content-type") || "";
  if (type.includes("application/json")) return await request.json().catch(() => ({}));
  const form = await request.formData().catch(() => null);
  return form ? Object.fromEntries(form) : {};
}

function respond(request, ok, status, message, back) {
  if ((request.headers.get("accept") || "").includes("application/json")) {
    return new Response(JSON.stringify({ ok, message }), {
      status,
      headers: { "content-type": "application/json" },
    });
  }
  return Response.redirect(new URL(ok ? "/thanks/" : back, request.url).toString(), 303);
}

async function handleRequest(request, env) {
  const data = await readBody(request);
  const kind = ["ride", "facility", "driver"].includes(data.kind) ? data.kind : "ride";
  const back = { ride: "/#request", facility: "/facilities/#account", driver: "/drive/#apply" }[kind];

  /* Honeypot: real visitors never see or fill this field. Pretend it worked. */
  if (clean(data.website)) return respond(request, true, 200, "ok", back);

  const name = clean(data.name, 120);
  const phone = clean(data.phone, 40);
  const email = clean(data.email, 160);
  if (!name || !phone) return respond(request, false, 400, "Please give your name and a phone number.", back);

  const fields = {
    ride: [
      ["Ride type", clean(data.ride_type, 60)],
      ["Wheelchair", clean(data.wheelchair, 60)],
      ["Pick-up town", clean(data.pickup, 120)],
      ["Going to", clean(data.dropoff, 160)],
      ["Date and time", clean(data.when, 120)],
      ["Round trip", clean(data.round_trip, 20)],
      ["How they pay", clean(data.payer, 60)],
    ],
    facility: [
      ["Organization", clean(data.organization, 160)],
      ["Role", clean(data.role, 80)],
      ["Rides per month (estimate)", clean(data.volume, 40)],
    ],
    driver: [
      ["Lives in", clean(data.town, 120)],
      ["Driver's license years", clean(data.license_years, 20)],
      ["Availability", clean(data.availability, 160)],
    ],
  }[kind];
  const details = [...fields, ["Message", clean(data.message, 2000)]]
    .filter(([, v]) => v)
    .map(([k, v]) => `${k}: ${v}`)
    .join("\n");

  const formId = env[`LL_FORM_${kind.toUpperCase()}`] || LL_FORMS[kind];
  const saved = await postToLeadLanding({
    formId,
    name,
    email,
    phone,
    /* LL forms require the message field, so never send it empty. */
    details: details || `Website ${kind} form`,
    tags: [`website-${kind}`],
    landingPage: clean(data.page, 300),
  });

  if (!saved) return respond(request, false, 502, `Sorry, that didn't go through. Please call us at ${PHONE_DISPLAY}.`, back);
  return respond(request, true, 200, "ok", back);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    /* One address for search engines: www goes to the bare domain. */
    if (url.hostname === "www.vantastictransit.net") {
      url.hostname = "vantastictransit.net";
      return Response.redirect(url.toString(), 301);
    }
    if (url.pathname === "/api/request") {
      if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });
      return handleRequest(request, env);
    }
    return env.ASSETS.fetch(request);
  },
};
