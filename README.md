# Risks and Trustworthiness of Multi-Agent Recommender Systems
> A living, auto-updated reading list. Taxonomy follows the **RecSys '26 tutorial** and the **_FnTrendsIR_ book chapter**. Updated weekly by automated crawler.

**Last updated:** 2026-04-04

---

## Table of Contents
1. [Taxonomy Overview](#taxonomy-overview)
2. [Foundational MA-RS Papers](#1-foundational-ma-rs-papers)
3. [Risk Family 1 — Prompt Injection & Jailbreaking](#2-risk-family-1--prompt-injection--jailbreaking)
4. [Risk Family 2 — Data Poisoning & Backdoor Attacks](#3-risk-family-2--data-poisoning--backdoor-attacks)
5. [Risk Family 3 — Inter-Agent Communication Attacks](#4-risk-family-3--inter-agent-communication-attacks)
6. [Risk Family 4 — Privacy & Inversion Attacks](#5-risk-family-4--privacy--inversion-attacks)
7. [Risk Family 5 — Cognitive Bias & Dark Patterns](#6-risk-family-5--cognitive-bias--dark-patterns)
8. [Risk Family 6 — Availability & Resource Depletion](#7-risk-family-6--availability--resource-depletion)
9. [Collusion in Multi-Agent Systems](#8-collusion-in-multi-agent-systems)
10. [Fairness, Feedback Loops & Exposure Bias](#9-fairness-feedback-loops--exposure-bias)
11. [Evaluation & Benchmarking](#10-evaluation--benchmarking)
12. [Defence Mechanisms & Mitigations](#11-defence-mechanisms--mitigations)
13. [Broad Safety Surveys (Background)](#13-broad-safety-surveys-background)
14. [How to Contribute / Crawler Notes](#how-to-contribute--crawler-notes)

---

## Taxonomy Overview

### Tutorial Taxonomy (RecSys '26)

The tutorial organises risks along **three axes**:

| Axis | Dimension | Values |
|------|-----------|--------|
| **When** | Lifecycle phase | Data/Design → Training → Offline Eval → Deployment → Monitoring |
| **What** | System target | User modelling · Ranking/Policy · Interaction · Tools/Actions · Memory · Protocols |
| **How** | Propagation mechanism | Topology · Comm protocol · Memory substrate · Alignment method · Safety controls |

**Amplified (A) vs Emergent (E) risks** — a risk is *amplified* if it exists in single-agent settings but worsens under composition; *emergent* if it only arises through agent interaction.

**Five architectural topologies** and their primary failure modes:

| Topology | Characteristic failure |
|----------|----------------------|
| Hierarchical delegation | Single point of failure; planner compromise |
| Ensemble aggregation | Correlated errors; exposure concentration |
| Tool-augmented workflow | Injection & tool misuse |
| Role-based specialists | Incentive conflicts; safety bypass |
| Decentralised ecosystem | Collusion & strategic gaming |

**Six evaluation levels (L1–L6):**
L1 Unit tests → L2 Protocol/guardrails → L3 Integration → L4 Red-teaming → L5 Stress tests → L6 Online monitoring

### _FnTrendsIR_ Taxonomy (Incremental Risk View)

| Generation | New risks introduced | Amplified risks |
|------------|---------------------|-----------------|
| LLM-RecSys | Hallucination, prompt injection | Bias, privacy leakage, opacity |
| Agentic RecSys (single) | Tool misuse, infinite loops, autonomy over-reach | Goal misalignment, manipulation |
| Multi-Agent RecSys | Coordination failure, collusion, error cascades, role ambiguity | Accountability gaps, latency, privacy |

**Six risk families (_FnTrendsIR_ chapter structure):**
1. Correctness (Hallucination & Goal Misalignment)
2. Bias & Fairness
3. Privacy & Security
4. Tool Misuse & Autonomy Over-Reach
5. Resource Exhaustion & Efficiency
6. Coordination Failure & Collusion

---

## 1. Foundational MA-RS Papers

> Papers defining multi-agent recommender architectures — the systems whose risks we study.

| Paper | Venue | arXiv | Code | Tags |
|----|----|----|----|----|
| **AgentCF: Collaborative Learning with Autonomous Language Agents for Recommender Systems** — Zhang et al. | WWW 2024 | [2310.09233](https://arxiv.org/abs/2310.09233) | — | `type:A` `topic:user-modelling` `topic:recsys` |
| **MACRec: A Multi-Agent Collaboration Framework for Recommendation** — Wang et al. | arXiv 2024 | [2402.15235](https://arxiv.org/abs/2402.15235) | — | `type:A` `topic:recsys` `topic:hierarchical` |
| **Orchestrating Users and Items for Agentic Recommendations (MACF)** — Wu et al. | arXiv 2025 | [2511.18413](https://arxiv.org/abs/2511.18413) | — | `type:A` `topic:recsys` `topic:decentralised` |
| **Towards Agentic Recommender Systems in the Era of Multimodal LLMs** — Li et al. | arXiv 2025 | [2503.16734](https://arxiv.org/abs/2503.16734) | — | `type:A` `topic:recsys` `topic:multimodal` |
| **A Survey on LLM-powered Agents for Recommender Systems** — Anonymous | arXiv 2025 | [2502.10050](https://arxiv.org/abs/2502.10050) | — | `topic:survey` `topic:recsys` |
| **Definitions, Perspectives, and Open Challenges of Multi-Agent Recommender Systems** — Yousefi et al. | arXiv 2025 | [2507.02097](https://arxiv.org/abs/2507.02097) | — | `topic:survey` `topic:recsys` |
| **No-Human in the Loop: Agentic Evaluation at Scale for Recommendation** — Zhang et al. | NeurIPS WS 2025 | [2511.03051](https://arxiv.org/abs/2511.03051) | — | `topic:evaluation` `topic:recsys` |

---

## 2. Risk Family 1 — Prompt Injection & Jailbreaking

> **Tutorial taxonomy**: Entry point = Input/Retrieval layer; Propagation = Message passing + Tool-action chains; **_FnTrendsIR_**: Privacy & Security (RF3). Risk type: **A** (amplified) + **E** (emergent via cascading).

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Securing AI Agents Against Prompt Injection Attacks** — Zhuang et al. | arXiv 2025 | [2511.15759](https://arxiv.org/abs/2511.15759) | — | `risk:rf1` `type:A` |
| **Multi-Agent Systems Execute Arbitrary Malicious Code** — Debenedetti et al. | arXiv 2025 | [2503.12188](https://arxiv.org/abs/2503.12188) | — | `risk:rf1` `risk:rf3` `type:E` `topic:code-execution` |
| **Breaking and Fixing Defenses Against Control-Flow Hijacking in Multi-Agent Systems** — Debenedetti et al. | arXiv 2025 | [2510.17276](https://arxiv.org/abs/2510.17276) | — | `risk:rf1` `risk:rf3` `type:E` `topic:control-flow` |
| **Jailbreaking LLMs via Iterative Tool-Disguised Attacks via RL** — Chen et al. | arXiv 2026 | [2601.05466](https://arxiv.org/abs/2601.05466) | — | `risk:rf1` `type:A` `topic:tool-misuse` `topic:rl` |
| **INJECAGENT: Benchmarking Indirect Prompt Injections in LLM Agents** — Zhan et al. | ACL Findings 2024 | [2403.02691](https://arxiv.org/abs/2403.02691) | [GitHub](https://github.com/uiuc-kang-lab/InjecAgent) | `risk:rf1` `type:A` `topic:benchmark` `topic:indirect-injection` |
| **A Systematic Evaluation of Prompt Injection and Jailbreak Vulnerabilities** — Pasquini et al. | arXiv 2025 | [2505.04806](https://arxiv.org/abs/2505.04806) | — | `risk:rf1` `type:A` `topic:benchmark` |
| **A Real-World Case Study of Attacking ChatGPT via Lightweight Prompt Injection** — Yu et al. | arXiv 2026 | [2504.16125](https://arxiv.org/abs/2504.16125) | — | `risk:rf1` `type:A` `topic:real-world` |
| **Demystifying Prompt Injection Attacks on Agentic AI Coding Editors** — Anonymous | arXiv 2025 | [2509.22040](https://arxiv.org/abs/2509.22040) | — | `risk:rf1` `type:A` `topic:tool-misuse` |
| **Exploit Tool Invocation Prompt for Tool Behavior Hijacking** — Anonymous | arXiv 2025 | [2509.05755](https://arxiv.org/abs/2509.05755) | — | `risk:rf1` `risk:rf3` `type:E` `topic:tool-misuse` |

---

## 3. Risk Family 2 — Data Poisoning & Backdoor Attacks

> **Tutorial taxonomy**: Entry point = Training data / Item content; Propagation = Feedback loops + Memory substrate; **_FnTrendsIR_**: Privacy & Security (RF3). Risk type: **A**.

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **BadRec: Exploring Backdoor Attack and Defense for LLM-empowered Recommendations** — Ning et al. | arXiv 2025 | [2504.11182](https://arxiv.org/abs/2504.11182) | — | `risk:rf2` `type:A` `topic:backdoor` `topic:recsys` `topic:defence` |
| **LoRec: Large Language Model for Robust Sequential Recommendation against Poisoning Attacks** — Wang et al. | SIGIR 2024 | [2401.17723](https://arxiv.org/abs/2401.17723) | — | `risk:rf2` `type:A` `topic:recsys` `topic:sequential` `topic:defence` |
| **Manipulating Recommender Systems: A Survey of Poisoning Attacks and Countermeasures** — Nguyen et al. | arXiv 2024 | [2404.14942](https://arxiv.org/abs/2404.14942) | — | `risk:rf2` `type:A` `topic:survey` `topic:recsys` |
| **A Survey on Adversarial Recommender Systems** — Deldjoo et al. | ACM CSUR 2021 | [2005.10322](https://arxiv.org/abs/2005.10322) | [DOI](https://doi.org/10.1145/3439729) | `risk:rf2` `type:A` `topic:survey` `topic:recsys` |
| **Shilling Recommender Systems by Generating Side-feature-aware Fake User Profiles** — Anonymous | arXiv 2025 | [2509.17918](https://arxiv.org/abs/2509.17918) | — | `risk:rf2` `type:A` `topic:shilling` `topic:recsys` |
| **LLM-Powered Audits Expose Shilling Attacks in Recommender Systems** — Anonymous | arXiv 2025 | [2509.24961](https://arxiv.org/abs/2509.24961) | — | `risk:rf2` `type:A` `topic:shilling` `topic:recsys` `topic:defence` |
| **DrunkAgent: Stealthy Memory Corruption in LLM-Powered Recommender Agents** — Yang et al. | arXiv 2025 | [2503.23804](https://arxiv.org/abs/2503.23804) | — | `risk:rf2` `risk:rf3` `type:A` `topic:memory` `topic:recsys` |
| **Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases** — Anonymous | arXiv 2025 | [2407.12784](https://arxiv.org/abs/2407.12784) | — | `risk:rf2` `type:A` `topic:memory` `topic:rag` |
| **Human-Imperceptible Retrieval Poisoning Attacks in LLM-Powered Applications** — Anonymous | arXiv 2024 | [2404.17196](https://arxiv.org/abs/2404.17196) | — | `risk:rf2` `type:A` `topic:rag` `topic:retrieval` |

---

## 4. Risk Family 3 — Inter-Agent Communication Attacks

> **Tutorial taxonomy**: Entry point = Protocol/Communication layer; Propagation = Message passing + Topology; **_FnTrendsIR_**: Coordination Failure & Collusion (RF6). Risk type: **E** (emergent).

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Red-Teaming LLM Multi-Agent Systems via Communication Attacks (AiTM)** — Chen et al. | arXiv 2025 | [2502.14847](https://arxiv.org/abs/2502.14847) | — | `risk:rf3` `type:E` `topic:aitm` |
| **Topology-Aware Multi-Hop Attacks on LLM-Based Multi-Agent Systems** — Anonymous | arXiv 2025 | [2512.04129](https://arxiv.org/abs/2512.04129) | — | `risk:rf3` `type:E` `topic:topology` |
| **Breaking Pragmatic Multi-Agent LLM Systems with Optimized Prompt Attacks** — Gu et al. | arXiv 2025 | [2504.00218](https://arxiv.org/abs/2504.00218) | — | `risk:rf3` `type:E` `topic:optimisation` |
| **Contagious Recursive Blocking Attacks on Multi-Agent Systems (Corba)** — Anonymous | arXiv 2025 | [2502.14529](https://arxiv.org/abs/2502.14529) | — | `risk:rf3` `risk:rf6` `type:E` `topic:dos` |
| **A Multi-round Adaptive Stealthy Tampering Framework for LLM-MAS** — Anonymous | arXiv 2025 | [2508.03125](https://arxiv.org/abs/2508.03125) | — | `risk:rf3` `type:E` `topic:stealthy` |
| **Security Analysis of Agentic AI Communication Protocols** — Louck et al. | arXiv 2025 | [2511.03841](https://arxiv.org/abs/2511.03841) | — | `risk:rf3` `type:E` `topic:protocol` |
| **The Trust Paradox in LLM-Based Multi-Agent Systems** — Xu et al. | arXiv 2025 | [2510.18563](https://arxiv.org/abs/2510.18563) | — | `risk:rf3` `type:E` `topic:trust` |
| **Systems Security Foundations for Agentic Computing** — Christodorescu et al. | arXiv 2025 | [2512.01295](https://arxiv.org/abs/2512.01295) | — | `risk:rf3` `risk:rf1` `type:E` `topic:systems-security` |
| **A Benchmark for Tool Poisoning Attack on Real-World MCP Servers** — Anonymous | arXiv 2025 | [2508.14925](https://arxiv.org/abs/2508.14925) | — | `risk:rf3` `risk:rf1` `risk:rf2` `type:E` `topic:mcp` `topic:tool-misuse` |
| **A Safety-Aware Role-Orchestrated Multi-Agent LLM Framework for Behavioral Health Communication Simulation** — Ha Na Cho | arXiv 2026 | [2604.00249](https://arxiv.org/abs/2604.00249) | — | — |

---

## 5. Risk Family 4 — Privacy & Inversion Attacks

> **Tutorial taxonomy**: Entry point = Agent/Memory layer; Propagation = Shared memory + Output logits; **_FnTrendsIR_**: Privacy & Security (RF3). Risk type: **A** + **E** (compositional leakage in MA).

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Privacy Risks of LLM-Empowered Recommender Systems: An Inversion Attack Perspective** — Wang et al. | RecSys 2025 | [2508.03703](https://arxiv.org/abs/2508.03703) | — | `risk:rf4` `risk:rf2` `type:A` `topic:inversion` `topic:recsys` |
| **The Sum Leaks More Than Its Parts: Compositional Privacy Risks in Multi-Agent Collaboration** — Anonymous | arXiv 2025 | [2509.14284](https://arxiv.org/abs/2509.14284) | — | `risk:rf4` `risk:rf3` `type:E` `topic:compositional` |
| **Your Language Model Can Secretly Be a Steganographic Privacy Leaking Agent (TrojanStego)** — Anonymous | arXiv 2025 | [2505.20118](https://arxiv.org/abs/2505.20118) | — | `risk:rf4` `type:A` `topic:steganography` |
| **A Privacy-Enhanced Development Paradigm for Multi-Agent Collaboration Systems** — Anonymous | arXiv 2025 | [2505.04799](https://arxiv.org/abs/2505.04799) | — | `risk:rf4` `type:A` `topic:defence` |

---

## 6. Risk Family 5 — Cognitive Bias & Dark Patterns

> **Tutorial taxonomy**: Entry point = Objective/Stakeholder layer; Propagation = Output generation + User interaction; **_FnTrendsIR_**: Bias & Fairness (RF2). Risk type: **A** (amplified by LLM fluency).

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Bias Beware: The Impact of Cognitive Biases on LLM-Driven Product Recommendations** — Krasniqi et al. | EMNLP 2025 | [2502.01349](https://arxiv.org/abs/2502.01349) | — | `risk:rf5` `type:A` `topic:cognitive-bias` `topic:recsys` |
| **DarkBench: Benchmarking Dark Patterns in Large Language Models** — Kran et al. | arXiv 2025 | [2503.10728](https://arxiv.org/abs/2503.10728) | — | `risk:rf5` `type:A` `topic:dark-patterns` `topic:benchmark` |
| **An Inconspicuous Attack to Bias LLM Responses** — Anonymous | arXiv 2025 | [2406.04755](https://arxiv.org/abs/2406.04755) | — | `risk:rf5` `type:A` `topic:stealthy` |
| **Quantifying Cognitive Bias Induction in LLM-Generated Content** — Anonymous | arXiv 2025 | [2507.03194](https://arxiv.org/abs/2507.03194) | — | `risk:rf5` `type:A` `topic:cognitive-bias` |
| **Understanding Biases in ChatGPT-based Recommender Systems** — Anonymous | arXiv 2024 | [2401.10545](https://arxiv.org/abs/2401.10545) | — | `risk:rf5` `type:A` `topic:recsys` |
| **Stereotype or Personalization? User Identity Biases Chatbot Recommendations** — Anonymous | arXiv 2024 | [2410.05613](https://arxiv.org/abs/2410.05613) | — | `risk:rf5` `type:A` `topic:recsys` `topic:stereotype` |
| **Bias Mitigation for AI-Feedback Loops in Recommender Systems** — Anonymous | arXiv 2025 | [2509.00109](https://arxiv.org/abs/2509.00109) | — | `risk:rf5` `risk:rf6` `type:A` `topic:feedback-loop` `topic:recsys` |
| **Aligning Recommendations with User Popularity Preferences** — Mona Schirmer, Anton Thielmann, Pola Schwöbel et al. | arXiv 2026 | [2604.01036](https://arxiv.org/abs/2604.01036) | — | — |

---

## 7. Risk Family 6 — Availability & Resource Depletion

> **Tutorial taxonomy**: Entry point = Execution layer; Propagation = Tool-action chains + Recursive spawning; **_FnTrendsIR_**: Resource Exhaustion & Efficiency (RF5). Risk type: **E** (emergent in multi-agent).

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Advertisement Embedding Attacks Against Large Language Models** — Anonymous | arXiv 2025 | [2508.17674](https://arxiv.org/abs/2508.17674) | — | `risk:rf6` `risk:rf1` `type:E` `topic:advertising` |

---

## 8. Collusion in Multi-Agent Systems

> **Tutorial taxonomy**: Emergent risk in Role-based and Decentralised topologies; **_FnTrendsIR_**: Coordination Failure & Collusion (RF6). Risk type: **E**.

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **A Survey of Collusion Risk in LLM-Powered Multi-Agent Systems** — Ghaemi | NeurIPS WS 2025 | [OpenReview](https://openreview.net/forum?id=Ylh8617Qyd) | — | `risk:rf6` `type:E` `topic:survey` `topic:collusion` |
| **Studying Coordination and Collusion in Multi-Agent LLM Code Reviews** — Anonymous | OpenReview 2025 | [OpenReview](https://openreview.net/forum?id=CdZaamCf5Y) | — | `risk:rf6` `type:E` `topic:collusion` |
| **Exposing Multi-Agent Collusion Risks in AI-Based Healthcare** — Anonymous | arXiv 2025 | [2512.03097](https://arxiv.org/abs/2512.03097) | — | `risk:rf6` `type:E` `topic:collusion` `domain:healthcare` |
| **Beyond Single-Agent Safety: A Taxonomy of Risks in LLM-to-LLM Interactions** — Bisconti et al. | arXiv 2025 | [2512.02682](https://arxiv.org/abs/2512.02682) | — | `risk:rf6` `risk:rf3` `type:E` `topic:taxonomy` |
| **Emergent Social Intelligence Risks in Generative Multi-Agent Systems** — Yue Huang, Yu Jiang, Wenjie Wang, Haomin Zhuang, Xiaonan Luo, Yuchen Ma, Zhangchen Xu, Zichen Chen, Nuno Moniz, Zinan Lin, Pin-Yu Chen, Nitesh V Chawla, Nouha Dziri, Huan Sun, Xiangliang Zhang | arXiv 2026 | [2603.27771](https://arxiv.org/abs/2603.27771) | [GitHub](https://github.com/HowieHwong/RiskLab) | `type:E` `topic:collusion` `topic:social-intelligence` `topo:decentralised` `tier:strategic` |

---

## 10. Evaluation & Benchmarking

> **Tutorial taxonomy**: L1–L6 evaluation ladder. **_FnTrendsIR_**: cross-cutting.

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Why Do Multi-Agent LLM Systems Fail?** — Cemri et al. | arXiv 2025 | [2503.13657](https://arxiv.org/abs/2503.13657) | — | `topic:evaluation` `topic:failure-taxonomy` |
| **AgentLeak: A Full-Stack Benchmark for Privacy Leakage in Multi-Agent LLM Systems** — Anonymous | arXiv 2026 | [2602.11510](https://arxiv.org/abs/2602.11510) | — | `risk:rf4` `type:E` `topic:benchmark` `topic:full-stack` |
| **Multi-Agent LLM Governance for Safe Two-Timescale Reinforcement Learning in SDN-IoT Defense** — Saeid Jamshidi, Negar Shahabi, Foutse Khomh et al. | arXiv 2026 | [2604.01127](https://arxiv.org/abs/2604.01127) | — | — |
| **Towards Position-Robust Talent Recommendation via Large Language Models** — Silin Du, Hongyan Liu | arXiv 2026 | [2604.02200](https://arxiv.org/abs/2604.02200) | — | — |

---

## 11. Defence Mechanisms & Mitigations

> Organised by lifecycle stage: design-time → runtime → post-deployment.

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **LlamaFirewall: An Open Source Guardrail System for Building Secure AI Agents** — Meta AI | arXiv 2025 | [2505.03574](https://arxiv.org/abs/2505.03574) | — | `topic:defence` `topic:guardrail` `risk:rf1` |
| **PeerGuard: Defending Multi-Agent Systems Against Backdoor Attacks Through Mutual Reasoning** — Anonymous | arXiv 2025 | [2505.11642](https://arxiv.org/abs/2505.11642) | — | `topic:defence` `risk:rf2` `topic:mutual-reasoning` |
| **GUARDIAN: Safeguarding LLM Multi-Agent Collaborations with Temporal Graph Modeling** — Anonymous | arXiv 2025 | [2505.19234](https://arxiv.org/abs/2505.19234) | — | `topic:defence` `risk:rf3` `topic:graph` `topic:monitoring` |
| **Safeguarding Multi-Agent Collaboration Through Credit-Based Dynamic Threat Detection** — Anonymous | arXiv 2025 | [2510.16219](https://arxiv.org/abs/2510.16219) | — | `topic:defence` `risk:rf3` `topic:trust` |
| **SentinelAgent: Graph-based Anomaly Detection in LLM-based Multi-Agent Systems** — He et al. | arXiv 2025 | [2505.24201](https://arxiv.org/abs/2505.24201) | — | `topic:defence` `risk:rf3` `topic:graph` `topic:monitoring` |
| **A Review of Trust, Risk, and Security Management in LLM-based Agentic MAS (TRiSM)** — Anonymous | arXiv 2025 | [2506.04133](https://arxiv.org/abs/2506.04133) | — | `topic:defence` `topic:survey` `topic:governance` |
| **Securing Agentic AI: A Comprehensive Threat Model and Mitigation Framework** — Narajala & Narayan | arXiv 2025 | [2504.19956](https://arxiv.org/abs/2504.19956) | — | `topic:defence` `topic:threat-model` `topic:evaluation` |
| **Towards Secure Systems of Interacting AI Agents** — Anonymous | arXiv 2025 | [2505.02077](https://arxiv.org/abs/2505.02077) | — | `topic:defence` `topic:formal` |
| **With a Little Help From My Friends: Collective Manipulation in Risk-Controlling Recommender Systems** — Giovanni De Toni, Cristian Consonni, Erasmo Purificato et al. | arXiv 2026 | [2603.28476](https://arxiv.org/abs/2603.28476) | — | — |

---

## 13. Broad Safety Surveys (Background)

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Agentic AI Needs a Systems Theory** — Miehling et al. | arXiv 2025 | [2503.00237](https://arxiv.org/abs/2503.00237) | — | `topic:systems-theory` `topic:formal` |
| **A Comprehensive Survey in LLM(-Agent) Full Stack Safety** — Wang et al. | arXiv 2025 | [2504.15585](https://arxiv.org/abs/2504.15585) | — | `topic:survey` |
| **Safety at Scale: A Comprehensive Survey of Large Model and Agent Safety** — Ma et al. | arXiv 2025 | [2502.05206](https://arxiv.org/abs/2502.05206) | — | `topic:survey` |
| **Agentic AI Security: Threats, Defenses, Evaluation** — Chhabra et al. | arXiv 2025 | [2510.23883](https://arxiv.org/abs/2510.23883) | — | `topic:survey` |
| **A Guide to Known Attacks and Impacts** — Anonymous | arXiv 2025 | [2506.23296](https://arxiv.org/abs/2506.23296) | — | `topic:incident-catalogue` |
| **A Taxonomy of Systemic Risks from General-Purpose AI** — Anonymous | arXiv 2024 | [2412.07780](https://arxiv.org/abs/2412.07780) | — | `topic:taxonomy` `topic:systemic-risk` |

---

## 15. Uncategorised / New Additions

> Papers added by crawler awaiting manual tagging.

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Let the Agent Steer: Closed-Loop Ranking Optimization via Influence Exchange** — Yin Cheng, Liao Zhou, Xiyu Liang et al. | arXiv 2026 | [2603.27765](https://arxiv.org/abs/2603.27765) | — | — |

---

## How to Contribute / Crawler Notes

This README is maintained by `crawler.py` in this repository. The crawler:

1. Queries the **arXiv API** daily for new papers matching the taxonomy keywords
2. Checks **OpenReview** for workshop/conference submissions (requires authentication)
3. Crawls **HuggingFace Papers** for community-curated arXiv papers with GitHub links
4. Tags each paper against the **When × What × How** axes and the **six risk families**
5. Saves unfiltered results to `raw_crawl.json`, then filters for relevance
6. Commits the updated README automatically via GitHub Actions

**To add a paper manually**: edit `papers.json` and run `python3 crawler.py --no-crawl`.

**Last crawler run**: 2026-04-04
