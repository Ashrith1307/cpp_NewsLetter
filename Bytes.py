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
    # Basics & I/O
    "Use ios::sync_with_stdio(false); cin.tie(NULL); to speed up cin/cout.",
    "Always use endl carefully; prefer '\\n' since endl also flushes the buffer and slows output.",
    "Use scanf/printf only if you need super-fast I/O, otherwise cin/cout with sync turned off is enough.",
    "Use getline(cin, s) for reading strings with spaces.",
    "Beware of mixing cin >> and getline(); always flush newline properly.",
    
    # Data types
    "Prefer long long (or int64_t) for large values in DSA problems.",
    "Use unsigned long long when working with only non-negative values.",
    "Use fixed << setprecision(n) for printing floating values neatly.",
    "Use __int128 in GCC for handling very large integers in CP.",
    
    # Arrays & Vectors
    "Prefer vector over raw arrays for safety and flexibility.",
    "Use vector<int> v(n, 0) to initialize a vector of size n with zeros.",
    "Use v.reserve(n) if you know the size beforehand to avoid reallocations.",
    "Use emplace_back() instead of push_back() when constructing objects directly.",
    "Access vector safely with at(i), it throws out_of_range exception.",
    "To remove duplicates from a vector: sort(v.begin(), v.end()); v.erase(unique(v.begin(), v.end()), v.end());",
    
    # Strings
    "Use string instead of char arrays for safety.",
    "Use s.substr(l, r-l+1) to extract substring.",
    "Use stoi, stol, stoll to convert string to integer.",
    "Use to_string() to convert numbers to string.",
    "Reverse a string using reverse(s.begin(), s.end()).",
    "Use stringstream for parsing strings into numbers.",
    
    # Pairs & Tuples
    "Use pair<int,int> for storing related values.",
    "Use make_pair(a,b) or {a,b} to construct pairs.",
    "Unpack pairs with auto [x,y] = p; in C++17.",
    "Use tuple<int,int,int> for three values.",
    "Unpack tuple with tie(x,y,z) = tup;",
    
    # Sets & Maps
    "Use unordered_map for O(1) average case lookup.",
    "Use map if you need ordered keys.",
    "Use set for sorted unique elements.",
    "Use multiset when duplicates are allowed in a sorted collection.",
    "Use count() to check if a key exists in set/map.",
    "Use erase(it) for iterator erasure in O(1).",
    "Use lower_bound and upper_bound in set/map for range queries.",
    
    # Algorithms
    "Use sort(v.begin(), v.end()) for sorting.",
    "Use stable_sort if stability is required.",
    "Use max_element and min_element to find largest/smallest elements.",
    "Use accumulate(v.begin(), v.end(), 0) to sum elements of a vector.",
    "Use __gcd(a,b) for gcd in <algorithm>.",
    "Use lcm(a,b) in C++17 for least common multiple.",
    "Use binary_search(v.begin(), v.end(), x) to check presence in sorted vector.",
    "Use next_permutation(v.begin(), v.end()) to generate permutations.",
    "Use rotate(v.begin(), v.begin()+k, v.end()) for array rotation.",
    "Use fill(v.begin(), v.end(), val) to initialize vector with val.",
    
    # Searching & Binary Search
    "Use lower_bound to find first index >= x.",
    "Use upper_bound to find first index > x.",
    "Binary search templates are useful for many problems.",
    "Practice writing binary search for monotonic conditions.",
    
    # Stacks & Queues
    "Use stack<T> for LIFO operations.",
    "Use queue<T> for FIFO operations.",
    "Use deque<T> for double-ended operations.",
    "Use priority_queue<T> as a max-heap by default.",
    "Use priority_queue<T, vector<T>, greater<T>> for min-heap.",
    
    # Graphs
    "Use adjacency list representation with vector<vector<int>>.",
    "Use vector<bool> visited(n, false) for tracking visited nodes.",
    "Use queue for BFS and stack/recursion for DFS.",
    "Use pair<int,int> in queue for BFS with coordinates.",
    "For weighted graphs, use vector<vector<pair<int,int>>> adjacency list.",
    "Use priority_queue for Dijkstra’s algorithm.",
    "Use DSU/Union-Find for disjoint set operations.",
    
    # Dynamic Programming
    "Always define dp arrays globally if large.",
    "Use memoization to optimize recursion.",
    "Use tabulation (bottom-up) for iterative DP.",
    "Initialize dp arrays with -1 using memset for uncomputed values.",
    "Use long long for DP states to avoid overflow.",
    
    # Bit Manipulation
    "Use (x & 1) to check if x is odd.",
    "Use (x >> 1) for dividing by 2 quickly.",
    "Use (x << 1) for multiplying by 2 quickly.",
    "Use __builtin_popcount(x) to count set bits.",
    "Use __builtin_clz(x) to count leading zeros.",
    "Use __builtin_ctz(x) to count trailing zeros.",
    "Use bitset<N> for representing subsets.",
    
    # Math
    "Use pow(a,b) for exponentiation, but beware of floating errors.",
    "Use fast exponentiation for modular power.",
    "Precompute factorials for nCr problems.",
    "Use sieve of Eratosthenes for prime generation.",
    "Use prefix sums for range sum queries.",
    "Use difference array technique for range updates.",
    
    # Advanced STL
    "Use ordered_set (from PBDS) if you need order statistics.",
    "Use multimap for keys with multiple values.",
    "Use deque for sliding window problems.",
    "Use emplace in maps/sets for faster insertions.",
    
    # Debugging
    "Use cerr << var << endl; for debug prints.",
    "Write debug macros to toggle debugging easily.",
    "Check edge cases: empty input, single element, large input.",
    
    # Memory & Optimization
    "Prefer pass by reference to avoid unnecessary copies.",
    "Use const reference when passing large containers.",
    "Avoid recursion depth > 1e5 to prevent stack overflow.",
    "Use iterative DFS/BFS instead of recursive when depth is high.",
    "Use reserve() for vectors when size is known.",
    
    # Misc
    "Use lambda functions for custom sorting.",
    "Always clear() containers before reuse.",
    "Use unique_ptr and shared_ptr for safe memory management.",
    "Learn time complexity of STL operations to avoid TLE.",
    "Practice template functions for reusable code.",
    "Read constraints carefully; they guide solution approach."
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
