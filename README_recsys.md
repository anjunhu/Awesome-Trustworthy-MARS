# Risks and Trustworthiness of Multi-Agent Recommender Systems
## RecSys-Focused Reading List

> **Scope**: Papers where a *recommender system* is the primary subject — user modelling,
> item ranking, preference elicitation, or personalised suggestion. General MAS/LLM security
> papers that do not target RS are excluded here; they appear in the full [`README.md`](README.md).
>
> Taxonomy: the **RecSys '26 tutorial** · the **_FnTrendsIR_ book chapter**
>
> **Last updated:** 2026-03-30 | 19 papers

---

## Table of Contents
1. [Foundational MA-RS Architectures](#1-foundational-ma-rs-architectures)
2. [Data Poisoning & Backdoor Attacks on RS](#2-data-poisoning--backdoor-attacks-on-rs)
3. [Privacy & Inversion Attacks on RS](#3-privacy--inversion-attacks-on-rs)
4. [Cognitive Bias & Dark Patterns in RS](#4-cognitive-bias--dark-patterns-in-rs)
5. [Evaluation & Benchmarking for RS](#5-evaluation--benchmarking-for-rs)
6. [Cross-Cutting Notes](#6-cross-cutting-notes)

---

## 1. Foundational MA-RS Architectures

| Paper | Venue | arXiv | Notes |
|-------|-------|-------|-------|
| **AgentCF**: Collaborative Learning with Autonomous Language Agents for Recommender Systems — Zhang et al. | WWW 2024 | [2310.09233](https://arxiv.org/abs/2310.09233) | User & item agents; collaborative simulation |
| **MACRec**: A Multi-Agent Collaboration Framework for Recommendation — Wang et al. | arXiv 2024 | [2402.15235](https://arxiv.org/abs/2402.15235) | Hierarchical planner + analyst agents |
| **MACF**: Orchestrating Users and Items for Agentic Recommendations — Wu et al. | arXiv 2025 | [2511.18413](https://arxiv.org/abs/2511.18413) | Dynamic agent recruitment |
| Towards Agentic Recommender Systems in the Era of Multimodal LLMs — Li et al. | arXiv 2025 | [2503.16734](https://arxiv.org/abs/2503.16734) | LoA taxonomy for RS; multimodal agents |
| A Survey on LLM-powered Agents for Recommender Systems | arXiv 2025 | [2502.10050](https://arxiv.org/abs/2502.10050) | Comprehensive survey |
| Definitions, Perspectives, and Open Challenges of Multi-Agent Recommender Systems — Yousefi et al. | arXiv 2025 | [2507.02097](https://arxiv.org/abs/2507.02097) | Formal MA-RS definition; open problems |
| No-Human in the Loop: Agentic Evaluation at Scale for Recommendation — Zhang et al. | NeurIPS WS 2025 | [2511.03051](https://arxiv.org/abs/2511.03051) | Automated agentic eval pipeline for RS |

---

## 2. Data Poisoning & Backdoor Attacks on RS

> **Tutorial**: Entry = Training data / Item content; Propagation = Feedback loops + Memory substrate
> **_FnTrendsIR_**: RF3 (Privacy & Security) · Risk type: **A**

| Paper | Venue | arXiv | Notes |
|-------|-------|-------|-------|
| **BadRec**: Backdoor Attack and Defense for LLM-empowered Recommendations — Ning et al. | arXiv 2025 | [2504.11182](https://arxiv.org/abs/2504.11182) | 1% poisoning sufficient; P-Scanner defense |
| **LoRec**: Robust Sequential Recommendation against Poisoning Attacks — Wang et al. | SIGIR 2024 | [2401.17723](https://arxiv.org/abs/2401.17723) | LLM-enhanced calibration defense |
| Manipulating Recommender Systems: A Survey of Poisoning Attacks — Nguyen et al. | arXiv 2024 | [2404.14942](https://arxiv.org/abs/2404.14942) | Survey of attack/defense landscape |
| A Survey on Adversarial Recommender Systems — Deldjoo et al. | ACM CSUR 2021 | [2005.10322](https://arxiv.org/abs/2005.10322) | Foundational survey; [DOI](https://doi.org/10.1145/3439729) |
| Shilling RS by Generating Side-feature-aware Fake User Profiles | arXiv 2025 | [2509.17918](https://arxiv.org/abs/2509.17918) | LLM-generated fake profiles |
| LLM-Powered Audits Expose Shilling Attacks in RS | arXiv 2025 | [2509.24961](https://arxiv.org/abs/2509.24961) | LLM-based shilling detection |
| **DrunkAgent**: Stealthy Memory Corruption in LLM-Powered Recommender Agents — Yang et al. | arXiv 2025 | [2503.23804](https://arxiv.org/abs/2503.23804) | ⚠️ *Also RF3*: memory poisoned via inter-agent channel |

---

## 3. Privacy & Inversion Attacks on RS

> **Tutorial**: Entry = Agent/Memory layer; Propagation = Shared memory + Output logits
> **_FnTrendsIR_**: RF3 (Privacy & Security) · Risk type: **A**

| Paper | Venue | arXiv | Notes |
|-------|-------|-------|-------|
| Privacy Risks of LLM-Empowered RS: An Inversion Attack Perspective — Wang et al. | RecSys 2025 | [2508.03703](https://arxiv.org/abs/2508.03703) | 65% item recovery; 87% demographic inference. ⚠️ *Also RF2*: extraction is simultaneously a data attack |

---

## 4. Cognitive Bias & Dark Patterns in RS

> **Tutorial**: Entry = Objective/Stakeholder layer; Propagation = Output generation + User interaction
> **_FnTrendsIR_**: RF2 (Bias & Fairness) · Risk type: **A**

| Paper | Venue | arXiv | Notes |
|-------|-------|-------|-------|
| Bias Beware: Cognitive Biases in LLM-Driven Product Recommendations — Krasniqi et al. | EMNLP 2025 | [2502.01349](https://arxiv.org/abs/2502.01349) | Anchoring, framing, social proof as attack vectors |
| Understanding Biases in ChatGPT-based Recommender Systems | arXiv 2024 | [2401.10545](https://arxiv.org/abs/2401.10545) | Position, popularity, recency bias |
| Stereotype or Personalization? User Identity Biases Chatbot Recommendations | arXiv 2024 | [2410.05613](https://arxiv.org/abs/2410.05613) | Identity-based recommendation skew |
| Bias Mitigation for AI-Feedback Loops in Recommender Systems | arXiv 2025 | [2509.00109](https://arxiv.org/abs/2509.00109) | ⚠️ *Also RF6*: sustained bias amplification degrades availability |

---

## 5. Evaluation & Benchmarking for RS

| Paper | Venue | arXiv | Notes |
|-------|-------|-------|-------|
| No-Human in the Loop: Agentic Evaluation at Scale for Recommendation | NeurIPS WS 2025 | [2511.03051](https://arxiv.org/abs/2511.03051) | Also in §1 |
| AgentRecBench: Benchmarking LLM Agent-based Personalized RS | OpenReview 2025 | [OpenReview](https://openreview.net/forum?id=fm77rDf9JS) | Utility benchmark |
| CFaiRLLM: Consumer Fairness Evaluation in LLM-RS | OpenReview 2025 | [OpenReview](https://openreview.net/forum?id=9B4eJxZyJy) | Fairness benchmark |

---

## 6. Cross-Reference: Papers Spanning Multiple Risk Families

Papers are placed in their **primary** section above. The table below lists those that also contribute substantially to a second risk family, with full tags for filtering.

| Paper | arXiv | Primary | Also covers | Tags |
|-------|-------|---------|-------------|------|
| **DrunkAgent**: Stealthy Memory Corruption in LLM-Powered Recommender Agents | [2503.23804](https://arxiv.org/abs/2503.23804) | RF2 Poisoning | RF3 Inter-agent | `risk:rf2` `risk:rf3` `type:A` `topic:memory` `topic:recsys` |
| Privacy Risks of LLM-Empowered RS: An Inversion Attack Perspective | [2508.03703](https://arxiv.org/abs/2508.03703) | RF4 Privacy | RF2 Poisoning | `risk:rf4` `risk:rf2` `type:A` `topic:inversion` `topic:recsys` |
| Bias Mitigation for AI-Feedback Loops in Recommender Systems | [2509.00109](https://arxiv.org/abs/2509.00109) | RF5 Bias | RF6 Availability | `risk:rf5` `risk:rf6` `type:A` `topic:feedback-loop` `topic:recsys` |

