import os
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- Secrets from environment (set these as GitHub Actions secrets) ---
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAILS = [e.strip() for e in os.getenv("RECEIVER_EMAILS", "").split(",") if e.strip()]

# --- Your C++ tips (HTML-safe snippets). Add as many as you like. ---
CPP_TIPS = [
    # keep these short; the template below styles them nicely
    "<b>Prefer <code>std::vector</code> over raw arrays.</b> It's safer, dynamic, and plays well with STL.",
    "Use <b><code>ios::sync_with_stdio(false); cin.tie(nullptr);</code></b> for fast I/O.",
    "Know your containers: <code>unordered_map</code> is avg O(1), <code>map</code> is O(log n).</code>",
    "For min-heap: <code>priority_queue&lt;int, vector&lt;int&gt;, greater&lt;int&gt;&gt; pq;</code>",
    "Binary search helpers: <code>lower_bound</code> (first ≥ x) and <code>upper_bound</code> (first &gt; x).",
    "Use <code>long long</code> for sums/products to avoid overflow in DSA problems.",
    "Prefix sums, freq maps, and two-pointers solve a surprising number of tasks quickly.",
    "Avoid deep recursion on big N; switch to iterative DFS/BFS to prevent stack overflows.",
    "Remove duplicates from a vector: sort → unique → erase.",
    "Use <code>__builtin_popcount</code> / <code>bitset</code> for bit tricks (masks, subsets).",
]

def pick_tip_today() -> str:
    """Rotate tips deterministically by date (no repeats until the list cycles)."""
    today = datetime.date.today().toordinal()
    return CPP_TIPS[today % len(CPP_TIPS)]

def build_html_email(tip_html: str) -> str:
    """Colorful, clean HTML with a code-friendly look."""
    return f"""
<!doctype html>
<html>
  <body style="margin:0;padding:24px;background:#0f172a;font-family:Inter,Segoe UI,Arial,sans-serif;">
    <div style="max-width:680px;margin:0 auto;background:#0b1022;border:1px solid #1f2a44;border-radius:16px;overflow:hidden;">
      <!-- Header -->
      <div style="background:linear-gradient(135deg,#7c3aed,#06b6d4);padding:18px 22px;">
        <h1 style="margin:0;color:#fff;font-size:20px;letter-spacing:.4px;">
          💡 Daily C++ Byte
        </h1>
      </div>

      <!-- Content -->
      <div style="padding:22px 22px 8px 22px;color:#e5e7eb;line-height:1.6;font-size:15px;">
        <p style="margin:0 0 14px 0;">Here’s your tip for today:</p>

        <div style="
            background:#0b122a;
            border:1px solid #223159;
            border-radius:12px;
            padding:14px 16px;
            box-shadow:0 2px 14px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.04);
            ">
          <div style="font-size:15px;color:#dbeafe;">
            {tip_html}
          </div>
        </div>

        <div style="margin-top:16px;padding:12px;border-radius:10px;background:#0a162f;border:1px dashed #22406e;color:#93c5fd;">
          <b>Pro tip:</b> Try to implement a tiny example for each byte you read. Muscle memory beats theory!
        </div>

        <p style="color:#94a3b8;font-size:12px;margin-top:18px;">
          Sent automatically by your Python bot 🤖
        </p>
      </div>
    </div>
  </body>
</html>
""".strip()

def build_text_fallback(tip_html: str) -> str:
    """Plain-text fallback for clients that block HTML."""
    # crude strip of tags; enough for fallback
    return tip_html.replace("<code>", "`").replace("</code>", "`") \
                   .replace("<b>", "").replace("</b>", "") \
                   .replace("&gt;", ">").replace("&lt;", "<") \
                   .replace("&amp;", "&")

def send_email(subject: str, html_body: str, text_body: str) -> None:
    if not (SENDER_EMAIL and EMAIL_PASSWORD and RECEIVER_EMAILS):
        raise RuntimeError("Missing SENDER_EMAIL, EMAIL_PASSWORD, or RECEIVER_EMAILS env vars.")

    # Send each recipient a separate message (nicer + avoids exposing the list)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)

        for rcpt in RECEIVER_EMAILS:
            rcpt = rcpt.strip()
            msg = MIMEMultipart("alternative")
            msg["From"] = SENDER_EMAIL
            msg["To"] = rcpt
            msg["Subject"] = subject
            msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))
            server.sendmail(SENDER_EMAIL, rcpt, msg.as_string())
            print(f"✅ Sent to {rcpt}")

if __name__ == "__main__":
    tip = pick_tip_today()
    html = build_html_email(tip)
    text = build_text_fallback(tip)
    # Include date in subject so you can spot runs easily
    subject = f"Daily C++ Byte • {datetime.date.today().isoformat()}"
    send_email(subject, html, text)
