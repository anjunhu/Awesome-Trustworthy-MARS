#!/usr/bin/env python3
"""
crawler.py — Weekly arXiv + OpenReview crawler for MA-RS risks reading list.

Usage:
    python3 crawler.py            # crawl, update papers.json, regenerate README, commit
    python3 crawler.py --dry-run  # crawl only, print new papers, no writes
"""

import argparse
import json
import os
import re
import subprocess
import time
import urllib.request
import urllib.parse
from datetime import date, datetime
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import openreview
    HAS_OPENREVIEW = True
except ImportError:
    HAS_OPENREVIEW = False

try:
    from huggingface_hub import HfApi
    HAS_HUGGINGFACE = True
except ImportError:
    HAS_HUGGINGFACE = False

# ── Config ────────────────────────────────────────────────────────────────────

REPO_DIR = Path(__file__).parent
PAPERS_FILE = REPO_DIR / "papers.json"
README_FILE = REPO_DIR / "README.md"

ARXIV_API = "https://export.arxiv.org/api/query"
OPENREVIEW_API = "https://api2.openreview.net/notes"

# Date window for arXiv submittedDate filter (YYYYMMDD, inclusive)
DATE_FROM = "20250101"
DATE_TO   = "20260331"

# Search groups (all combinations are tried)
SEARCH_GROUPS = {
    "system": [
        "multi-agent recommender",
        "agentic recommendation",
        "LLM-based recommender",
        "multi-agent LLM recommendation",
    ],
    "risk": [
        "adversarial recommender",
        "attack recommender LLM",
        "poisoning recommender agent",
        "prompt injection recommender",
        "jailbreak recommender",
        "privacy recommender LLM",
        "fairness recommender LLM",
        "collusion multi-agent",
        "hallucination recommender agent",
    ],
    "defence": [
        "guardrail multi-agent LLM",
        "defense multi-agent recommender",
        "mitigation agentic recommender",
        "anomaly detection multi-agent LLM",
    ],
}

# Keyword → section mapping (first match wins)
SECTION_RULES = [
    (["prompt injection", "jailbreak", "control-flow hijack", "tool hijack"], "rf1_injection"),
    (["backdoor", "poisoning", "shilling", "fake profile", "data poison"], "rf2_poisoning"),
    (["inter-agent", "agent-in-the-middle", "communication attack", "topology attack", "mcp poison"], "rf3_interagent"),
    (["privacy", "inversion attack", "membership inference", "steganograph", "leakage"], "rf4_privacy"),
    (["cognitive bias", "dark pattern", "bias llm", "popularity bias", "feedback loop bias"], "rf5_bias"),
    (["resource depletion", "availability attack", "recursive blocking", "advertisement embedding"], "rf6_availability"),
    (["collusion", "coordination failure", "deadlock agent"], "collusion"),
    (["fairness", "exposure bias", "feedback loop"], "fairness"),
    (["benchmark", "evaluation", "red-team"], "evaluation"),
    (["guardrail", "defense", "mitigation", "anomaly detection", "safeguard"], "defence"),
    (["survey", "taxonomy", "safety"], "safety_surveys"),
    (["agentcf", "macrec", "macf", "matcha", "agentic recommender", "multi-agent recommender"], "foundational"),
]

KURT_WHEN_RULES = [
    (["training", "backdoor", "poisoning data"], "training"),
    (["offline eval", "benchmark", "simulation"], "offline_eval"),
    (["monitoring", "anomaly", "online"], "monitoring"),
    (["design", "architecture", "framework"], "design"),
]

YASHAR_RF_RULES = [
    (["hallucination", "goal misalignment", "correctness"], "RF1"),
    (["bias", "fairness", "stereotype", "feedback loop"], "RF2"),
    (["privacy", "security", "injection", "jailbreak", "poisoning", "backdoor", "attack"], "RF3"),
    (["tool misuse", "autonomy", "privilege escalation", "infinite loop"], "RF4"),
    (["resource", "latency", "efficiency", "availability"], "RF5"),
    (["collusion", "coordination", "deadlock", "cascade"], "RF6"),
]

RISK_TYPE_RULES = [
    (["emergent", "inter-agent", "collusion", "cascad", "topology"], "E"),
    (["amplified", "single-agent", "bias", "privacy", "poisoning", "injection"], "A"),
]

# Relevance: paper must match at least one term from EACH group (AND logic)
RELEVANCE_SYSTEM = [
    "recommender system", "recommendation system", "recsys",
    "multi-agent recommender", "agentic recommender",
    "llm-based recommender", "llm recommender",
    "multi-agent llm", "llm multi-agent",
    "agentic ai system", "llm agent system",
    "collaborative filtering", "personalized recommendation",
]

RELEVANCE_RISK = [
    "prompt injection", "jailbreak", "adversarial attack",
    "data poisoning", "backdoor", "privacy leakage", "membership inference",
    "collusion", "fairness", "bias", "hallucination",
    "tool misuse", "memory poisoning", "inter-agent attack",
    "agent security", "guardrail", "red-team", "red team",
    "trustworthy", "robustness", "safety", "vulnerability",
]


def is_relevant(title: str, abstract: str) -> bool:
    combined = f"{title} {abstract}".lower()
    has_system = any(kw in combined for kw in RELEVANCE_SYSTEM)
    has_risk = any(kw in combined for kw in RELEVANCE_RISK)
    return has_system and has_risk


# ── Helpers ───────────────────────────────────────────────────────────────────

def _match_rules(text: str, rules: list) -> str | None:
    text_lower = text.lower()
    for keywords, label in rules:
        if any(k in text_lower for k in keywords):
            return label
    return None


def classify_paper(title: str, abstract: str) -> dict:
    combined = f"{title} {abstract}".lower()
    return {
        "section": _match_rules(combined, SECTION_RULES) or "misc",
        "kurt_when": _match_rules(combined, KURT_WHEN_RULES) or "deployment",
        "yashar_rf": _match_rules(combined, YASHAR_RF_RULES),
        "risk_type": _match_rules(combined, RISK_TYPE_RULES),
    }


def load_papers() -> list:
    if PAPERS_FILE.exists():
        return json.loads(PAPERS_FILE.read_text())
    return []


def save_papers(papers: list):
    PAPERS_FILE.write_text(json.dumps(papers, indent=2))


def known_ids(papers: list) -> set:
    ids = set()
    for p in papers:
        ids.add(p.get("id", ""))
        if p.get("arxiv_id"):
            ids.add(p["arxiv_id"])
    return ids


# ── arXiv crawler ─────────────────────────────────────────────────────────────

def arxiv_search(query: str, max_results: int = 20,
                 date_from: str = DATE_FROM, date_to: str = DATE_TO) -> list:
    # arXiv date filter format: [YYYYMMDD0000 TO YYYYMMDD2359]
    date_filter = f"submittedDate:[{date_from}0000 TO {date_to}2359]"
    params = urllib.parse.urlencode({
        "search_query": f"all:{query} AND {date_filter}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = f"{ARXIV_API}?{params}"
    
    # Retry with exponential backoff on rate limit
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AwesomeTrustworthyMARS/1.0 (research crawler)"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                xml = resp.read()
            time.sleep(5)  # arXiv requests 3s minimum, we use 5s to be safe
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                wait = 10 * (2 ** attempt)  # 10s, 20s
                print(f"    Rate limited, waiting {wait}s...")
                time.sleep(wait)
                continue
            print(f"  [arXiv] request failed for '{query}': {e}")
            return []
        except Exception as e:
            print(f"  [arXiv] request failed for '{query}': {e}")
            return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml)
    results = []
    for entry in root.findall("atom:entry", ns):
        arxiv_id_raw = entry.find("atom:id", ns).text or ""
        arxiv_id = arxiv_id_raw.split("/abs/")[-1].split("v")[0]
        title = (entry.find("atom:title", ns).text or "").strip().replace("\n", " ")
        abstract = (entry.find("atom:summary", ns).text or "").strip().replace("\n", " ")
        authors_els = entry.findall("atom:author/atom:name", ns)
        authors = ", ".join(a.text for a in authors_els[:3])
        if len(authors_els) > 3:
            authors += " et al."
        published = (entry.find("atom:published", ns).text or "")[:7]  # YYYY-MM
        results.append({
            "id": arxiv_id,
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "published": published,
        })
    return results


def crawl_arxiv(existing_ids: set, date_from: str = DATE_FROM, date_to: str = DATE_TO, 
                filter_relevance: bool = True) -> list:
    """Crawl arXiv. If filter_relevance=False, returns all results (high recall)."""
    new_papers = []
    seen_this_run = set()
    for group, queries in SEARCH_GROUPS.items():
        for query in queries:
            print(f"  [arXiv] searching: {query}  ({date_from}–{date_to})")
            results = arxiv_search(query, max_results=15, date_from=date_from, date_to=date_to)
            for r in results:
                aid = r["id"]
                if aid in existing_ids or aid in seen_this_run:
                    continue
                if filter_relevance and not is_relevant(r["title"], r["abstract"]):
                    continue
                seen_this_run.add(aid)
                tags = classify_paper(r["title"], r["abstract"])
                paper = {
                    "id": aid,
                    "title": r["title"],
                    "authors": r["authors"],
                    "venue": f"arXiv {r['published'][:4]}",
                    "section": tags["section"],
                    "risk_type": tags["risk_type"],
                    "kurt_when": tags["kurt_when"],
                    "kurt_what": None,
                    "kurt_how": None,
                    "yashar_rf": tags["yashar_rf"],
                    "github": None,
                    "doi": None,
                    "notes": "",
                    "is_relevant": is_relevant(r["title"], r["abstract"]) if not filter_relevance else True,
                }
                new_papers.append(paper)
                status = "NEW" if filter_relevance else "RAW"
                print(f"    + {status}: [{aid}] {r['title'][:70]}")
    return new_papers


# ── OpenReview crawler ────────────────────────────────────────────────────────

# Search specific venues where MA-RS papers are likely
OPENREVIEW_VENUES = [
    "NeurIPS.cc/2025/Conference",
    "ICLR.cc/2026/Conference",
    "RecSys.org/2025/Conference",
]

OR_KEYWORDS = [
    "multi-agent", "recommender", "LLM", "agent",
    "collusion", "prompt injection", "privacy",
]


def crawl_openreview(existing_ids: set, filter_relevance: bool = True) -> list:
    """Crawl OpenReview. Requires OPENREVIEW_USERNAME and OPENREVIEW_PASSWORD env vars."""
    if not HAS_OPENREVIEW:
        print("  [OpenReview] openreview-py not installed, skipping. Install with: pip install openreview-py")
        return []
    
    username = os.environ.get('OPENREVIEW_USERNAME')
    password = os.environ.get('OPENREVIEW_PASSWORD')
    
    if not username or not password:
        print("  [OpenReview] Skipping (set OPENREVIEW_USERNAME and OPENREVIEW_PASSWORD env vars to enable)")
        return []
    
    new_papers = []
    try:
        client = openreview.api.OpenReviewClient(
            baseurl='https://api2.openreview.net',
            username=username,
            password=password
        )
    except Exception as e:
        print(f"  [OpenReview] Failed to authenticate: {e}")
        return []
    
    # Search by venue submissions
    for venue_id in OPENREVIEW_VENUES:
        try:
            print(f"  [OpenReview] searching venue: {venue_id}")
            venue_group = client.get_group(venue_id)
            submission_name = venue_group.content.get('submission_name', {}).get('value', 'Submission')
            notes = list(client.get_all_notes(invitation=f'{venue_id}/-/{submission_name}'))
            time.sleep(3)
            
            for note in notes:
                title = note.content.get('title', {})
                title = title.get('value', title) if isinstance(title, dict) else title
                if not title:
                    continue
                    
                # Check if title/abstract contains any of our keywords
                abstract = note.content.get('abstract', {})
                abstract = abstract.get('value', abstract) if isinstance(abstract, dict) else abstract
                abstract = abstract or ""
                combined = f"{title} {abstract}".lower()
                if not any(kw in combined for kw in OR_KEYWORDS):
                    continue
                
                or_id = note.id
                lookup_key = f"openreview_{or_id}"
                if lookup_key in existing_ids:
                    continue
                
                if filter_relevance and not is_relevant(title, abstract):
                    continue
                    
                tags = classify_paper(title, abstract)
                paper = {
                    "id": lookup_key,
                    "title": title,
                    "authors": "Anonymous",
                    "venue": f"OpenReview {venue_id.split('/')[1]}",
                    "section": tags["section"],
                    "risk_type": tags["risk_type"],
                    "kurt_when": tags["kurt_when"],
                    "kurt_what": None,
                    "kurt_how": None,
                    "yashar_rf": tags["yashar_rf"],
                    "github": None,
                    "doi": None,
                    "openreview": f"https://openreview.net/forum?id={or_id}",
                    "notes": "",
                    "is_relevant": is_relevant(title, abstract) if not filter_relevance else True,
                }
                new_papers.append(paper)
                status = "NEW" if filter_relevance else "RAW"
                print(f"    + {status} [OpenReview]: {title[:70]}")
                
        except Exception as e:
            print(f"  [OpenReview] venue {venue_id} failed: {e}")
            continue
    
    return new_papers


# ── HuggingFace Papers crawler ───────────────────────────────────────────────

def crawl_huggingface(existing_ids: set, filter_relevance: bool = True, days_back: int = 30) -> list:
    """Crawl HuggingFace Papers (arXiv papers with community metadata)."""
    if not HAS_HUGGINGFACE:
        print("  [HuggingFace] huggingface_hub not installed, skipping. Install with: pip install huggingface_hub")
        return []
    
    new_papers = []
    try:
        api = HfApi()
        # HF Papers are arXiv papers, so search by keywords in title
        for keyword in ["multi-agent", "recommender", "LLM agent", "agentic"]:
            try:
                print(f"  [HuggingFace] searching: {keyword}")
                papers = api.list_papers(search=keyword, limit=50)
                time.sleep(2)
                
                for paper in papers:
                    # HF paper IDs are arXiv IDs
                    arxiv_id = paper.id
                    if arxiv_id in existing_ids:
                        continue
                    
                    title = paper.title or ""
                    abstract = getattr(paper, 'summary', '') or ""
                    
                    # Check relevance
                    if filter_relevance and not is_relevant(title, abstract):
                        continue
                    
                    # Get authors
                    authors = getattr(paper, 'authors', [])
                    if authors:
                        author_str = ", ".join(a.name for a in authors[:3])
                        if len(authors) > 3:
                            author_str += " et al."
                    else:
                        author_str = "Unknown"
                    
                    # Get GitHub link if available
                    github_url = None
                    if hasattr(paper, 'github_url') and paper.github_url:
                        github_url = paper.github_url
                    
                    tags = classify_paper(title, abstract)
                    paper_entry = {
                        "id": arxiv_id,
                        "title": title,
                        "authors": author_str,
                        "venue": f"arXiv {getattr(paper, 'published', '')[:4] or '2026'}",
                        "section": tags["section"],
                        "risk_type": tags["risk_type"],
                        "kurt_when": tags["kurt_when"],
                        "kurt_what": None,
                        "kurt_how": None,
                        "yashar_rf": tags["yashar_rf"],
                        "github": github_url,
                        "doi": None,
                        "notes": "via HuggingFace Papers",
                        "is_relevant": is_relevant(title, abstract) if not filter_relevance else True,
                    }
                    new_papers.append(paper_entry)
                    status = "NEW" if filter_relevance else "RAW"
                    print(f"    + {status} [HF]: {title[:70]}")
                    
            except Exception as e:
                print(f"  [HuggingFace] search '{keyword}' failed: {e}")
                continue
                
    except Exception as e:
        print(f"  [HuggingFace] Failed to initialize: {e}")
    
    return new_papers


# ── README generator ──────────────────────────────────────────────────────────

SECTION_META = {
    "foundational": {
        "heading": "1. Foundational MA-RS Papers",
        "blurb": "> Papers defining multi-agent recommender architectures — the systems whose risks we study.",
        "cols": ["Paper", "Venue", "arXiv", "Code", "Tags"],
    },
    "rf1_injection": {
        "heading": "2. Risk Family 1 — Prompt Injection & Jailbreaking",
        "blurb": ("> **Tutorial taxonomy**: Entry point = Input/Retrieval layer; Propagation = Message passing + Tool-action chains; "
                  "**_FnTrendsIR_**: Privacy & Security (RF3). Risk type: **A** (amplified) + **E** (emergent via cascading)."),
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "rf2_poisoning": {
        "heading": "3. Risk Family 2 — Data Poisoning & Backdoor Attacks",
        "blurb": ("> **Tutorial taxonomy**: Entry point = Training data / Item content; Propagation = Feedback loops + Memory substrate; "
                  "**_FnTrendsIR_**: Privacy & Security (RF3). Risk type: **A**."),
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "rf3_interagent": {
        "heading": "4. Risk Family 3 — Inter-Agent Communication Attacks",
        "blurb": ("> **Tutorial taxonomy**: Entry point = Protocol/Communication layer; Propagation = Message passing + Topology; "
                  "**_FnTrendsIR_**: Coordination Failure & Collusion (RF6). Risk type: **E** (emergent)."),
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "rf4_privacy": {
        "heading": "5. Risk Family 4 — Privacy & Inversion Attacks",
        "blurb": ("> **Tutorial taxonomy**: Entry point = Agent/Memory layer; Propagation = Shared memory + Output logits; "
                  "**_FnTrendsIR_**: Privacy & Security (RF3). Risk type: **A** + **E** (compositional leakage in MA)."),
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "rf5_bias": {
        "heading": "6. Risk Family 5 — Cognitive Bias & Dark Patterns",
        "blurb": ("> **Tutorial taxonomy**: Entry point = Objective/Stakeholder layer; Propagation = Output generation + User interaction; "
                  "**_FnTrendsIR_**: Bias & Fairness (RF2). Risk type: **A** (amplified by LLM fluency)."),
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "rf6_availability": {
        "heading": "7. Risk Family 6 — Availability & Resource Depletion",
        "blurb": ("> **Tutorial taxonomy**: Entry point = Execution layer; Propagation = Tool-action chains + Recursive spawning; "
                  "**_FnTrendsIR_**: Resource Exhaustion & Efficiency (RF5). Risk type: **E** (emergent in multi-agent)."),
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "collusion": {
        "heading": "8. Collusion in Multi-Agent Systems",
        "blurb": ("> **Tutorial taxonomy**: Emergent risk in Role-based and Decentralised topologies; "
                  "**_FnTrendsIR_**: Coordination Failure & Collusion (RF6). Risk type: **E**."),
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "fairness": {
        "heading": "9. Fairness, Feedback Loops & Exposure Bias",
        "blurb": "> **Tutorial taxonomy**: Objective/Stakeholder layer; **_FnTrendsIR_**: Bias & Fairness (RF2). Risk type: **A**.",
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "evaluation": {
        "heading": "10. Evaluation & Benchmarking",
        "blurb": "> **Tutorial taxonomy**: L1–L6 evaluation ladder. **_FnTrendsIR_**: cross-cutting.",
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "defence": {
        "heading": "11. Defence Mechanisms & Mitigations",
        "blurb": "> Organised by lifecycle stage: design-time → runtime → post-deployment.",
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "safety_surveys": {
        "heading": "13. Broad Safety Surveys (Background)",
        "blurb": "",
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
    "misc": {
        "heading": "15. Uncategorised / New Additions",
        "blurb": "> Papers added by crawler awaiting manual tagging.",
        "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"],
    },
}

SECTION_ORDER = [
    "foundational", "rf1_injection", "rf2_poisoning", "rf3_interagent",
    "rf4_privacy", "rf5_bias", "rf6_availability", "collusion",
    "fairness", "evaluation", "defence", "safety_surveys", "misc",
]


def paper_to_row(p: dict) -> str:
    title = p.get("title", "Unknown")
    authors = p.get("authors", "")
    venue = p.get("venue", "")
    notes = p.get("notes", "")

    pid = p.get("id", "")
    if pid and not pid.startswith("openreview_"):
        arxiv_link = f"[{pid}](https://arxiv.org/abs/{pid})"
    elif p.get("openreview"):
        arxiv_link = f"[OpenReview]({p['openreview']})"
    else:
        arxiv_link = "—"

    extras = []
    if p.get("github"):
        extras.append(f"[GitHub]({p['github']})")
    if p.get("doi"):
        extras.append(f"[DOI](https://doi.org/{p['doi']})")
    notes_str = " · ".join(extras) if extras else (notes or "—")

    tags = p.get("tags", [])
    tag_str = " ".join(f"`{t}`" for t in tags) if tags else "—"

    paper_cell = f"**{title}** — {authors}" if authors else f"**{title}**"
    return f"| {paper_cell} | {venue} | {arxiv_link} | {notes_str} | {tag_str} |"


def generate_readme(papers: list) -> str:
    today = date.today().isoformat()
    by_section: dict[str, list] = {s: [] for s in SECTION_ORDER}
    for p in papers:
        sec = p.get("section", "misc")
        if sec not in by_section:
            by_section.setdefault("misc", []).append(p)
        else:
            by_section[sec].append(p)

    lines = [
        "# Risks and Trustworthiness of Multi-Agent Recommender Systems",
        "> A living, auto-updated reading list. Taxonomy follows the **RecSys '26 tutorial** and the **_FnTrendsIR_ book chapter**. Updated weekly by automated crawler.",
        "",
        f"**Last updated:** {today}",
        "",
        "---",
        "",
        "## Table of Contents",
        "1. [Taxonomy Overview](#taxonomy-overview)",
        "2. [Foundational MA-RS Papers](#1-foundational-ma-rs-papers)",
        "3. [Risk Family 1 — Prompt Injection & Jailbreaking](#2-risk-family-1--prompt-injection--jailbreaking)",
        "4. [Risk Family 2 — Data Poisoning & Backdoor Attacks](#3-risk-family-2--data-poisoning--backdoor-attacks)",
        "5. [Risk Family 3 — Inter-Agent Communication Attacks](#4-risk-family-3--inter-agent-communication-attacks)",
        "6. [Risk Family 4 — Privacy & Inversion Attacks](#5-risk-family-4--privacy--inversion-attacks)",
        "7. [Risk Family 5 — Cognitive Bias & Dark Patterns](#6-risk-family-5--cognitive-bias--dark-patterns)",
        "8. [Risk Family 6 — Availability & Resource Depletion](#7-risk-family-6--availability--resource-depletion)",
        "9. [Collusion in Multi-Agent Systems](#8-collusion-in-multi-agent-systems)",
        "10. [Fairness, Feedback Loops & Exposure Bias](#9-fairness-feedback-loops--exposure-bias)",
        "11. [Evaluation & Benchmarking](#10-evaluation--benchmarking)",
        "12. [Defence Mechanisms & Mitigations](#11-defence-mechanisms--mitigations)",
        "13. [Broad Safety Surveys (Background)](#13-broad-safety-surveys-background)",
        "14. [How to Contribute / Crawler Notes](#how-to-contribute--crawler-notes)",
        "",
        "---",
        "",
        "## Taxonomy Overview",
        "",
        "### Tutorial Taxonomy (RecSys '26)",
        "",
        "The tutorial organises risks along **three axes**:",
        "",
        "| Axis | Dimension | Values |",
        "|------|-----------|--------|",
        "| **When** | Lifecycle phase | Data/Design → Training → Offline Eval → Deployment → Monitoring |",
        "| **What** | System target | User modelling · Ranking/Policy · Interaction · Tools/Actions · Memory · Protocols |",
        "| **How** | Propagation mechanism | Topology · Comm protocol · Memory substrate · Alignment method · Safety controls |",
        "",
        "**Amplified (A) vs Emergent (E) risks** — a risk is *amplified* if it exists in single-agent settings but worsens "
        "under composition; *emergent* if it only arises through agent interaction.",
        "",
        "**Five architectural topologies** and their primary failure modes:",
        "",
        "| Topology | Characteristic failure |",
        "|----------|----------------------|",
        "| Hierarchical delegation | Single point of failure; planner compromise |",
        "| Ensemble aggregation | Correlated errors; exposure concentration |",
        "| Tool-augmented workflow | Injection & tool misuse |",
        "| Role-based specialists | Incentive conflicts; safety bypass |",
        "| Decentralised ecosystem | Collusion & strategic gaming |",
        "",
        "**Six evaluation levels (L1–L6):**",
        "L1 Unit tests → L2 Protocol/guardrails → L3 Integration → L4 Red-teaming → L5 Stress tests → L6 Online monitoring",
        "",
        "### _FnTrendsIR_ Taxonomy (Incremental Risk View)",
        "",
        "| Generation | New risks introduced | Amplified risks |",
        "|------------|---------------------|-----------------|",
        "| LLM-RecSys | Hallucination, prompt injection | Bias, privacy leakage, opacity |",
        "| Agentic RecSys (single) | Tool misuse, infinite loops, autonomy over-reach | Goal misalignment, manipulation |",
        "| Multi-Agent RecSys | Coordination failure, collusion, error cascades, role ambiguity | Accountability gaps, latency, privacy |",
        "",
        "**Six risk families (_FnTrendsIR_ chapter structure):**",
        "1. Correctness (Hallucination & Goal Misalignment)",
        "2. Bias & Fairness",
        "3. Privacy & Security",
        "4. Tool Misuse & Autonomy Over-Reach",
        "5. Resource Exhaustion & Efficiency",
        "6. Coordination Failure & Collusion",
        "",
        "---",
        "",
    ]

    for sec in SECTION_ORDER:
        papers_in_sec = by_section.get(sec, [])
        if not papers_in_sec:
            continue
        meta = SECTION_META.get(sec, {"heading": sec, "blurb": "", "cols": ["Paper", "Venue", "arXiv", "Notes", "Tags"]})
        lines.append(f"## {meta['heading']}")
        lines.append("")
        if meta["blurb"]:
            lines.append(meta["blurb"])
            lines.append("")
        cols = meta["cols"]
        lines.append("| " + " | ".join(cols) + " |")
        lines.append("|" + "|".join(["----"] * len(cols)) + "|")
        for p in papers_in_sec:
            lines.append(paper_to_row(p))
        lines.append("")
        lines.append("---")
        lines.append("")

    lines += [
        "## How to Contribute / Crawler Notes",
        "",
        "This README is maintained by `crawler.py` in this repository. The crawler:",
        "",
        "1. Queries the **arXiv API** daily for new papers matching the taxonomy keywords",
        "2. Checks **OpenReview** for workshop/conference submissions (requires authentication)",
        "3. Crawls **HuggingFace Papers** for community-curated arXiv papers with GitHub links",
        "4. Tags each paper against the **When × What × How** axes and the **six risk families**",
        "5. Saves unfiltered results to `raw_crawl.json`, then filters for relevance",
        "6. Commits the updated README automatically via GitHub Actions",
        "",
        "**To add a paper manually**: edit `papers.json` and run `python3 crawler.py --no-crawl`.",
        "",
        f"**Last crawler run**: {today}",
    ]

    return "\n".join(lines) + "\n"


# ── Git commit ────────────────────────────────────────────────────────────────

def git_commit(n_new: int):
    today = date.today().isoformat()
    msg = f"docs: weekly crawler update {today} (+{n_new} new papers)"
    subprocess.run(["git", "-C", str(REPO_DIR), "add", "README.md", "papers.json"], check=True)
    result = subprocess.run(
        ["git", "-C", str(REPO_DIR), "diff", "--cached", "--quiet"],
        capture_output=True
    )
    if result.returncode == 0:
        print("Nothing changed — no commit needed.")
        return
    subprocess.run(["git", "-C", str(REPO_DIR), "commit", "-m", msg], check=True)
    print(f"Committed: {msg}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Crawl only, no writes")
    parser.add_argument("--no-crawl", action="store_true", help="Skip crawling, just regenerate README from papers.json")
    parser.add_argument("--no-commit", action="store_true", help="Write files but skip git commit")
    parser.add_argument("--save-raw", metavar="FILE", help="Save unfiltered crawl results to JSON before relevance filtering")
    parser.add_argument("--from", dest="date_from", default=DATE_FROM, metavar="YYYYMMDD",
                        help=f"Start of arXiv date window (default: {DATE_FROM})")
    parser.add_argument("--to", dest="date_to", default=DATE_TO, metavar="YYYYMMDD",
                        help=f"End of arXiv date window (default: {DATE_TO})")
    args = parser.parse_args()

    papers = load_papers()
    existing = known_ids(papers)
    new_papers = []

    if not args.no_crawl:
        if args.save_raw:
            # Stage 1: High-recall grab (no filtering)
            print(f"=== Stage 1: High-recall crawl (unfiltered) [{args.date_from}–{args.date_to}] ===")
            raw_papers = []
            raw_papers += crawl_arxiv(existing, date_from=args.date_from, date_to=args.date_to, filter_relevance=False)
            raw_papers += crawl_openreview(existing, filter_relevance=False)
            raw_papers += crawl_huggingface(existing, filter_relevance=False)
            Path(args.save_raw).write_text(json.dumps(raw_papers, indent=2))
            print(f"\nStage 1 complete: {len(raw_papers)} raw papers saved to {args.save_raw}")
            
            # Stage 2: Precision filter
            print(f"\n=== Stage 2: Filtering for relevance ===")
            new_papers = [p for p in raw_papers if p.get("is_relevant", True)]
            print(f"Stage 2 complete: {len(new_papers)} relevant papers (filtered from {len(raw_papers)} raw)")
        else:
            # Single-stage: filtered crawl only
            print(f"=== Crawling arXiv (filtered) [{args.date_from}–{args.date_to}] ===")
            new_papers += crawl_arxiv(existing, date_from=args.date_from, date_to=args.date_to, filter_relevance=True)
            print(f"\n=== Crawling OpenReview (filtered) ===")
            new_papers += crawl_openreview(existing, filter_relevance=True)
            print(f"\n=== Crawling HuggingFace Papers (filtered) ===")
            new_papers += crawl_huggingface(existing, filter_relevance=True)
            print(f"\nFound {len(new_papers)} new papers.")

    if args.dry_run:
        print("\n[dry-run] Not writing anything.")
        return

    papers = papers + new_papers
    save_papers(papers)
    print(f"papers.json updated ({len(papers)} total).")

    readme = generate_readme(papers)
    README_FILE.write_text(readme)
    print(f"README.md regenerated.")

    if not args.no_commit:
        git_commit(len(new_papers))


if __name__ == "__main__":
    main()
