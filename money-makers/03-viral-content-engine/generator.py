"""
Viral Content Carousel & Reel Script Generator
The exact production pipeline behind @viral.coder
"""

import json
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

TEMPLATES_FILE = os.path.join(os.path.dirname(__file__), "templates.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "viral_packet.md")

def generate_packet():
    with open(TEMPLATES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    hooks = data["hooks"]
    topics = data["sample_topics"]

    print("=" * 65)
    print(" 🎬 VIRAL CODER: REEL & CAROUSEL CONTENT GENERATOR")
    print("=" * 65)

    markdown_out = "# 🚀 Viral Developer Content Engine - Production Packet\n\n"
    markdown_out += "> Auto-generated using proven short-form retention & ManyChat DM growth tactics.\n\n"

    for idx, t in enumerate(topics, 1):
        hook = hooks[(idx - 1) % len(hooks)]
        print(f"[{idx}] Generating Content Kit for: {t['topic']} ({t['category']})")

        kit = f"""---
## Content Kit #{idx}: {t['topic']}
**Category:** {t['category']} | **Target Reel Duration:** {t['reel_length']}

### 🎥 Reel Production Script (30-Second Format)

| Timestamp | Visual Screen Action (B-Roll) | Spoken Audio Voiceover | On-Screen Text Overlay |
|---|---|---|---|
| **0:00 - 0:03** | Fast camera push-in to finished running project | "{hook['hook_formula']}" | **{hook['hook_formula']}** |
| **0:03 - 0:10** | Terminal code timelapse + VS Code dark theme | "Most devs waste weeks building generic clones that get ignored by recruiters and clients. Instead, we're combining {', '.join(t['tools'])}." | *Stack: {', '.join(t['tools'])}* |
| **0:10 - 0:20** | Live app demo: clicking buttons, real-time results | "Look at this: with less than 150 lines of code, it handles end-to-end automation in under 2 seconds flat." | *⚡ 100% Automated | 0 Latency* |
| **0:20 - 0:28** | Cursor highlights GitHub repo / star button | "{hook['cta']}" | **👉 {hook['cta']}** |

### 📸 6-Slide Carousel Blueprint (Instagram / LinkedIn)

* **Slide 1 (Hook / Cover):** Bold white text on dark background: *"{hook['hook_formula']}"* + UI mockup preview.
* **Slide 2 (The Problem):** Why the old way is dead (e.g. why basic portfolio projects fail to stand out).
* **Slide 3 (The Architecture):** Simple visual 3-step diagram: Input -> Engine ({t['tools'][0]}) -> Instant Result.
* **Slide 4 (The Code Secret):** Code snippet with glowing syntax highlighting showcasing the key function.
* **Slide 5 (The Monetization/Flex):** How to turn this into a $500 freelance service or portfolio flex.
* **Slide 6 (Call-to-Action):** *"{hook['cta']}"* + Save this post for later.

### 📝 Instagram Caption & Auto-DM Keyword Setup

```text
{hook['hook_formula']} 👇

Save this reel so you don't lose it later 📌

Here is the exact tech stack used:
{chr(10).join(['• ' + x for x in t['tools']])}

Want the complete source code, GitHub repository, and step-by-step setup guide?
👉 {hook['cta']}

#webdeveloper #codinglife #learncoding #javascript #python #programming #softwareengineer #techreels #buildinpublic #sidehustle
```

---
"""
        markdown_out += kit

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_out)

    print(f"\n[+] Production packet generated successfully at:\n    {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_packet()
