/* Post a lead into Lead Landing. Never throws; returns true only when LL accepted it.
   Per-submission tags are filtered server side against the form's allowedTags. */
const LEADLANDING_BASE = "https://www.lead-landing.com/api/forms";

/**
 * @returns {Promise<boolean>} true only when LeadLanding accepted the lead.
 * Never throws.
 */
export async function postToLeadLanding({ formId, name, email, phone, details, tags, landingPage, fields, dealValueCents }) {
  if (!formId) {
    console.log("leadlanding skipped: no form id configured");
    return false;
  }
  try {
    const res = await fetch(`${LEADLANDING_BASE}/${formId}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        values: {
          name: name || "",
          email: email || "",
          phone: phone || "",
          message: details || "",
          ...(fields || {}),
        },
        ...(typeof dealValueCents === "number" ? { dealValueCents } : {}),
        tags: tags || [],
        /* `source` is NOT a key LeadLanding accepts and is silently discarded.
           It reads only utmSource, utmMedium, utmCampaign, utmContent, utmTerm,
           fbclid, gclid, landingPage and referrer. */
        attribution: {
          landingPage: landingPage || "",
          utmSource: "website-form",
        },
      }),
    });
    if (!res.ok) {
      console.log(`leadlanding submit failed: ${res.status} ${await res.text().catch(() => "")}`);
      return false;
    }
    return true;
  } catch (e) {
    console.log(`leadlanding submit threw: ${String(e)}`);
    return false;
  }
}
