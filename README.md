# Risks and Trustworthiness of Multi-Agent Recommender Systems
> A living, auto-updated reading list. Taxonomy follows the **RecSys '26 tutorial** and the **_FnTrendsIR_ book chapter**. Updated weekly by automated crawler.

**Last updated:** 2026-07-01

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

### Risk Taxonomy

Risks are classified by the **single-agent isolation test**: an agent retains its full tool and memory interface, but no other agents consume or produce its messages.
- **Amplified (A)**: risk exists in single-agent settings but worsens under composition.
- **Emergent (E)**: risk only arises through agent interaction.

**Threat tiers** determine evaluation scope:

| Tier | Description | Evaluation scope |
|------|-------------|-----------------|
| Drift | System dynamics cause degradation without adversary | Component |
| Misalignment | Internal agent exploits its position | Interaction |
| Compromise | External attacker corrupts one or more agents | Composition |

### Evaluation Framework

Evaluation is organised by **scope** and **setting**:

| Scope | Offline | Online |
|-------|---------|--------|
| **Component** | Per-agent constraint checks, recommender metrics, adversarial prompting | Behavioural drift detection |
| **Interaction** | Red-teaming of agent pairs, protocol checks, counterfactual analysis | Inter-agent message trace monitoring |
| **Composition** | End-to-end stress tests, fairness audits, collusion audits | System-level KPIs, incident reconstruction |

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
| **Securing AI Agents Against Prompt Injection Attacks** — Zhuang et al. | arXiv 2025 | [2511.15759](https://arxiv.org/abs/2511.15759) | — | `A` `risk:rf1` `type:A` |
| **Multi-Agent Systems Execute Arbitrary Malicious Code** — Debenedetti et al. | arXiv 2025 | [2503.12188](https://arxiv.org/abs/2503.12188) | — | `E` `risk:rf1` `risk:rf3` `type:E` `topic:code-execution` |
| **Breaking and Fixing Defenses Against Control-Flow Hijacking in Multi-Agent Systems** — Debenedetti et al. | arXiv 2025 | [2510.17276](https://arxiv.org/abs/2510.17276) | — | `E` `risk:rf1` `risk:rf3` `type:E` `topic:control-flow` |
| **Jailbreaking LLMs via Iterative Tool-Disguised Attacks via RL** — Chen et al. | arXiv 2026 | [2601.05466](https://arxiv.org/abs/2601.05466) | — | `A` `risk:rf1` `type:A` `topic:tool-misuse` `topic:rl` |
| **INJECAGENT: Benchmarking Indirect Prompt Injections in LLM Agents** — Zhan et al. | ACL Findings 2024 | [2403.02691](https://arxiv.org/abs/2403.02691) | [GitHub](https://github.com/uiuc-kang-lab/InjecAgent) | `A` `risk:rf1` `type:A` `topic:benchmark` `topic:indirect-injection` |
| **A Systematic Evaluation of Prompt Injection and Jailbreak Vulnerabilities** — Pasquini et al. | arXiv 2025 | [2505.04806](https://arxiv.org/abs/2505.04806) | — | `A` `risk:rf1` `type:A` `topic:benchmark` |
| **A Real-World Case Study of Attacking ChatGPT via Lightweight Prompt Injection** — Yu et al. | arXiv 2025 | [2504.16125](https://arxiv.org/abs/2504.16125) | — | `A` `risk:rf1` `type:A` `topic:real-world` |
| **Demystifying Prompt Injection Attacks on Agentic AI Coding Editors** — Anonymous | arXiv 2025 | [2509.22040](https://arxiv.org/abs/2509.22040) | — | `A` `risk:rf1` `type:A` `topic:tool-misuse` |
| **Exploit Tool Invocation Prompt for Tool Behavior Hijacking** — Anonymous | arXiv 2025 | [2509.05755](https://arxiv.org/abs/2509.05755) | — | `E` `risk:rf1` `risk:rf3` `type:E` `topic:tool-misuse` |
| **Retrieval-Augmented Review Generation for Poisoning Recommender Systems** — Shiyi Yang, Xinshu Li, Guanglin Zhou et al. | arXiv 2025 | [2508.15252](https://arxiv.org/abs/2508.15252) | classical adversarial RecSys | `A` `component` `compromise` |
| **Penetration Testing of Agentic AI: A Comparative Security Analysis Across Models and Frameworks** — Viet K. Nguyen, Mohammad I. Husain | arXiv 2025 | [2512.14860](https://arxiv.org/abs/2512.14860) | — | `A` `component` `compromise` |
| **It's the Thought that Counts: Evaluating the Attempts of Frontier LLMs to Persuade on Harmful Topics** — Matthew Kowal, Jasper Timm, Jean-Francois Godbout et al. | arXiv 2025 | [2506.02873](https://arxiv.org/abs/2506.02873) | — | `A` `component` `compromise` |
| **Exploring Approaches for Detecting Memorization of Recommender System Data in Large Language Models** — Antonio Colacicco, Vito Guida, Dario Di Palma et al. | arXiv 2026 | [2601.02002](https://arxiv.org/abs/2601.02002) | — | `A` `component` `compromise` |
| **Autonomous Agents on Blockchains: Standards, Execution Models, and Trust Boundaries** — Saad Alqithami | arXiv 2026 | [2601.04583](https://arxiv.org/abs/2601.04583) | — | `E` `composition` `compromise` |

---

## 3. Risk Family 2 — Data Poisoning & Backdoor Attacks

> **Tutorial taxonomy**: Entry point = Training data / Item content; Propagation = Feedback loops + Memory substrate; **_FnTrendsIR_**: Privacy & Security (RF3). Risk type: **A**.

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **BadRec: Exploring Backdoor Attack and Defense for LLM-empowered Recommendations** — Ning et al. | arXiv 2025 | [2504.11182](https://arxiv.org/abs/2504.11182) | — | `A` `risk:rf2` `type:A` `topic:backdoor` `topic:recsys` `topic:defence` |
| **LoRec: Large Language Model for Robust Sequential Recommendation against Poisoning Attacks** — Wang et al. | SIGIR 2024 | [2401.17723](https://arxiv.org/abs/2401.17723) | — | `A` `risk:rf2` `type:A` `topic:recsys` `topic:sequential` `topic:defence` |
| **Manipulating Recommender Systems: A Survey of Poisoning Attacks and Countermeasures** — Nguyen et al. | arXiv 2024 | [2404.14942](https://arxiv.org/abs/2404.14942) | — | `A` `risk:rf2` `type:A` `topic:survey` `topic:recsys` |
| **A Survey on Adversarial Recommender Systems** — Deldjoo et al. | ACM CSUR 2021 | [2005.10322](https://arxiv.org/abs/2005.10322) | [DOI](https://doi.org/10.1145/3439729) | `A` `risk:rf2` `type:A` `topic:survey` `topic:recsys` |
| **Shilling Recommender Systems by Generating Side-feature-aware Fake User Profiles** — Anonymous | arXiv 2025 | [2509.17918](https://arxiv.org/abs/2509.17918) | — | `A` `risk:rf2` `type:A` `topic:shilling` `topic:recsys` |
| **LLM-Powered Audits Expose Shilling Attacks in Recommender Systems** — Anonymous | arXiv 2025 | [2509.24961](https://arxiv.org/abs/2509.24961) | — | `A` `risk:rf2` `type:A` `topic:shilling` `topic:recsys` `topic:defence` |
| **DrunkAgent: Stealthy Memory Corruption in LLM-Powered Recommender Agents** — Yang et al. | arXiv 2025 | [2503.23804](https://arxiv.org/abs/2503.23804) | — | `A` `risk:rf2` `risk:rf3` `type:A` `topic:memory` `topic:recsys` |
| **Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases** — Anonymous | arXiv 2024 | [2407.12784](https://arxiv.org/abs/2407.12784) | — | `A` `risk:rf2` `type:A` `topic:memory` `topic:rag` |
| **Human-Imperceptible Retrieval Poisoning Attacks in LLM-Powered Applications** — Anonymous | arXiv 2024 | [2404.17196](https://arxiv.org/abs/2404.17196) | — | `A` `risk:rf2` `type:A` `topic:rag` `topic:retrieval` |
| **Improving the Shortest Plank: Vulnerability-Aware Adversarial Training
  for Robust Recommender System** — Kaike Zhang, Qi Cao, Yunfan Wu et al. | arXiv 2024 | [2409.17476](https://arxiv.org/abs/2409.17476) | via HuggingFace Papers | `A` `component` `compromise` |
| **The Misattribution Gap: When Memory Poisoning Looks Like Model Failure in Agentic AI Systems** — Tanzim Ahad, Ismail Hossain, Md Jahangir Alam et al. | arXiv 2026 | [2605.22842](https://arxiv.org/abs/2605.22842) | — | `E` `composition` `compromise` |
| **LoReTTA: A Low Resource Framework To Poison Continuous Time Dynamic Graphs** — Himanshu Pal, Venkata Sai Pranav Bachina, Ankit Gangwal et al. | arXiv 2025 | [2511.07379](https://arxiv.org/abs/2511.07379) | classical adversarial RecSys | `A` `component` `compromise` |
| **Enhancing Robustness of Graph Neural Networks through p-Laplacian** — Anuj Kumar Sirohi, Subhanu Halder, Kabir Kumar et al. | arXiv 2025 | [2511.06143](https://arxiv.org/abs/2511.06143) | classical adversarial RecSys | `A` `component` `compromise` |
| **Controllable and Stealthy Shilling Attacks via Dispersive Latent Diffusion** — Shutong Qiao, Wei Yuan, Junliang Yu et al. | arXiv 2025 | [2508.01987](https://arxiv.org/abs/2508.01987) | classical adversarial RecSys | `A` `component` `compromise` |
| **AUV-Fusion: Cross-Modal Adversarial Fusion of User Interactions and Visual Perturbations Against VARS** — Hai Ling, Tianchi Wang, Xiaohao Liu et al. | arXiv 2025 | [2507.22880](https://arxiv.org/abs/2507.22880) | classical adversarial RecSys | `A` `component` `compromise` |
| **Spattack: Subgroup Poisoning Attacks on Federated Recommender Systems** — Bo Yan, Yurong Hao, Dingqi Liu et al. | arXiv 2025 | [2507.06258](https://arxiv.org/abs/2507.06258) | classical adversarial RecSys | `A` `component` `compromise` |
| **IndirectAD: Practical Data Poisoning Attacks against Recommender Systems for Item Promotion** — Zihao Wang, Tianhao Mao, XiaoFeng Wang et al. | arXiv 2025 | [2511.05845](https://arxiv.org/abs/2511.05845) | classical adversarial RecSys | `A` `component` `compromise` |
| **Stealthy LLM-Driven Data Poisoning Attacks Against Embedding-Based Retrieval-Augmented Recommender Systems** — Fatemeh Nazary, Yashar Deldjoo, Tommaso Di Noia et al. | arXiv 2025 | [2505.05196](https://arxiv.org/abs/2505.05196) | classical adversarial RecSys | `A` `component` `compromise` |
| **Diversity-aware Dual-promotion Poisoning Attack on Sequential Recommendation** — Yuchuan Zhao, Tong Chen, Junliang Yu et al. | arXiv 2025 | [2504.06586](https://arxiv.org/abs/2504.06586) | classical adversarial RecSys | `A` `component` `compromise` |
| **Exploiting Meta-Learning-based Poisoning Attacks for Graph Link Prediction** — Mingchen Li, Di Zhuang, Keyu Chen et al. | arXiv 2025 | [2504.06492](https://arxiv.org/abs/2504.06492) | classical adversarial RecSys | `A` `component` `compromise` |
| **Poison-RAG: Adversarial Data Poisoning Attacks on Retrieval-Augmented Generation in Recommender Systems** — Fatemeh Nazary, Yashar Deldjoo, Tommaso di Noia | arXiv 2025 | [2501.11759](https://arxiv.org/abs/2501.11759) | classical adversarial RecSys | `A` `component` `compromise` |
| **Single-Node Trigger Backdoor Attacks in Graph-Based Recommendation Systems** — Runze Li, Di Jin, Xiaobao Wang et al. | arXiv 2025 | [2506.08401](https://arxiv.org/abs/2506.08401) | classical adversarial RecSys | `A` `component` `compromise` |
| **LLM-Based User Simulation for Low-Knowledge Shilling Attacks on Recommender Systems** — Shengkang Gu, Jiahao Liu, Dongsheng Li et al. | arXiv 2025 | [2505.13528](https://arxiv.org/abs/2505.13528) | classical adversarial RecSys | `E` `component` `compromise` |
| **Membership Inference Attacks on LLM-based Recommender Systems** — Jiajie He, Min-Chun Chen, Xintong Chen et al. | arXiv 2025 | [2508.18665](https://arxiv.org/abs/2508.18665) | — | `A` `component` `compromise` |

---

## 4. Risk Family 3 — Inter-Agent Communication Attacks

> **Tutorial taxonomy**: Entry point = Protocol/Communication layer; Propagation = Message passing + Topology; **_FnTrendsIR_**: Coordination Failure & Collusion (RF6). Risk type: **E** (emergent).

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Red-Teaming LLM Multi-Agent Systems via Communication Attacks (AiTM)** — Chen et al. | arXiv 2025 | [2502.14847](https://arxiv.org/abs/2502.14847) | — | `E` `risk:rf3` `type:E` `topic:aitm` |
| **Topology-Aware Multi-Hop Attacks on LLM-Based Multi-Agent Systems** — Anonymous | arXiv 2025 | [2512.04129](https://arxiv.org/abs/2512.04129) | — | `E` `risk:rf3` `type:E` `topic:topology` |
| **Breaking Pragmatic Multi-Agent LLM Systems with Optimized Prompt Attacks** — Gu et al. | arXiv 2025 | [2504.00218](https://arxiv.org/abs/2504.00218) | — | `E` `risk:rf3` `type:E` `topic:optimisation` |
| **Contagious Recursive Blocking Attacks on Multi-Agent Systems (Corba)** — Anonymous | arXiv 2025 | [2502.14529](https://arxiv.org/abs/2502.14529) | — | `E` `risk:rf3` `risk:rf6` `type:E` `topic:dos` |
| **A Multi-round Adaptive Stealthy Tampering Framework for LLM-MAS** — Anonymous | arXiv 2025 | [2508.03125](https://arxiv.org/abs/2508.03125) | — | `E` `risk:rf3` `type:E` `topic:stealthy` |
| **Security Analysis of Agentic AI Communication Protocols** — Louck et al. | arXiv 2025 | [2511.03841](https://arxiv.org/abs/2511.03841) | — | `E` `risk:rf3` `type:E` `topic:protocol` |
| **The Trust Paradox in LLM-Based Multi-Agent Systems** — Xu et al. | arXiv 2025 | [2510.18563](https://arxiv.org/abs/2510.18563) | — | `E` `risk:rf3` `type:E` `topic:trust` |
| **Systems Security Foundations for Agentic Computing** — Christodorescu et al. | arXiv 2025 | [2512.01295](https://arxiv.org/abs/2512.01295) | — | `E` `risk:rf3` `risk:rf1` `type:E` `topic:systems-security` |
| **A Benchmark for Tool Poisoning Attack on Real-World MCP Servers** — Anonymous | arXiv 2025 | [2508.14925](https://arxiv.org/abs/2508.14925) | — | `E` `risk:rf3` `risk:rf1` `risk:rf2` `type:E` `topic:mcp` `topic:tool-misuse` |
| **A Safety-Aware Role-Orchestrated Multi-Agent LLM Framework for Behavioral Health Communication Simulation** — Ha Na Cho | arXiv 2026 | [2604.00249](https://arxiv.org/abs/2604.00249) | — | `E` |

---

## 5. Risk Family 4 — Privacy & Inversion Attacks

> **Tutorial taxonomy**: Entry point = Agent/Memory layer; Propagation = Shared memory + Output logits; **_FnTrendsIR_**: Privacy & Security (RF3). Risk type: **A** + **E** (compositional leakage in MA).

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Privacy Risks of LLM-Empowered Recommender Systems: An Inversion Attack Perspective** — Wang et al. | RecSys 2025 | [2508.03703](https://arxiv.org/abs/2508.03703) | — | `A` `risk:rf4` `risk:rf2` `type:A` `topic:inversion` `topic:recsys` |
| **The Sum Leaks More Than Its Parts: Compositional Privacy Risks in Multi-Agent Collaboration** — Anonymous | arXiv 2025 | [2509.14284](https://arxiv.org/abs/2509.14284) | — | `E` `risk:rf4` `risk:rf3` `type:E` `topic:compositional` |
| **Your Language Model Can Secretly Be a Steganographic Privacy Leaking Agent (TrojanStego)** — Anonymous | arXiv 2025 | [2505.20118](https://arxiv.org/abs/2505.20118) | — | `A` `risk:rf4` `type:A` `topic:steganography` |
| **A Privacy-Enhanced Development Paradigm for Multi-Agent Collaboration Systems** — Anonymous | arXiv 2025 | [2505.04799](https://arxiv.org/abs/2505.04799) | — | `A` `risk:rf4` `type:A` `topic:defence` |
| **The 1st Workshop on Human-Centered Recommender Systems** — Kaike Zhang, Yunfan Wu, Yougang lyu et al. | arXiv 2024 | [2411.14760](https://arxiv.org/abs/2411.14760) | via HuggingFace Papers | `A` `component` `drift` |
| **Robust Recommender System: A Survey and Future Directions** — Kaike Zhang, Qi Cao, Fei Sun et al. | arXiv 2023 | [2309.02057](https://arxiv.org/abs/2309.02057) | via HuggingFace Papers | `A` `component` `compromise` |
| **FedAU2: Attribute Unlearning for User-Level Federated Recommender Systems with Adaptive and Robust Adversarial Training** — Yuyuan Li, Junjie Fang, Fengyuan Yu et al. | arXiv 2025 | [2511.22872](https://arxiv.org/abs/2511.22872) | classical adversarial RecSys | `A` `component` `compromise` |
| **ADAGE: Active Defenses Against GNN Extraction** — Jing Xu, Franziska Boenisch, Adam Dziedzic | arXiv 2025 | [2503.00065](https://arxiv.org/abs/2503.00065) | classical adversarial RecSys | `A` `component` `compromise` |
| **RAID: An In-Training Defense against Attribute Inference Attacks in Recommender Systems** — Xiaohua Feng, Yuyuan Li, Fengyuan Yu et al. | arXiv 2025 | [2504.11510](https://arxiv.org/abs/2504.11510) | classical adversarial RecSys | `A` `component` `compromise` |
| **Membership Inference Attack against Large Language Model-based Recommendation Systems: A New Distillation-based Paradigm** — Li Cuihong, Huang Xiaowen, Yin Chuanhuan et al. | arXiv 2025 | [2511.14763](https://arxiv.org/abs/2511.14763) | — | `A` `component` `compromise` |
| **LLM4MEA: Data-free Model Extraction Attacks on Sequential Recommenders via Large Language Models** — Shilong Zhao, Fei Sun, Kaike Zhang et al. | arXiv 2025 | [2507.16969](https://arxiv.org/abs/2507.16969) | — | `A` `component` `compromise` |
| **From AutoRecSys to AutoRecLab: A Call to Build, Evaluate, and Govern Autonomous Recommender-Systems Research Labs** — Joeran Beel, Bela Gipp, Tobias Vente et al. | arXiv 2025 | [2510.18104](https://arxiv.org/abs/2510.18104) | — | `A` `composition` `drift` |
| **Customized Retrieval-Augmented Generation with LLM for Debiasing Recommendation Unlearning** — Haichao Zhang, Chong Zhang, Peiyu Hu et al. | arXiv 2025 | [2511.05494](https://arxiv.org/abs/2511.05494) | — | `A` `component` `drift` |
| **Audit the Whisper: Detecting Steganographic Collusion in Multi-Agent LLMs** — Om Tailor | arXiv 2025 | [2510.04303](https://arxiv.org/abs/2510.04303) | — | `E` `composition` `misalignment` |
| **AGENTSAFE: A Unified Framework for Ethical Assurance and Governance in Agentic AI** — Rafflesia Khan, Declan Joyce, Mansura Habiba | arXiv 2025 | [2512.03180](https://arxiv.org/abs/2512.03180) | — | `E` `composition` `drift` |
| **Lightweight Fairness for LLM-Based Recommendations via Kernelized Projection and Gated Adapters** — Nan Cui, Wendy Hui Wang, Yue Ning | arXiv 2026 | [2603.23780](https://arxiv.org/abs/2603.23780) | — | `A` `component` `drift` |
| **Attack by Unlearning: Unlearning-Induced Adversarial Attacks on Graph Neural Networks** — Jiahao Zhang, Yilong Wang, Suhang Wang | arXiv 2026 | [2603.18570](https://arxiv.org/abs/2603.18570) | — | `A` `component` `compromise` |
| **FeDecider: An LLM-Based Framework for Federated Cross-Domain Recommendation** — Xinrui He, Ting-Wei Li, Tianxin Wei et al. | arXiv 2026 | [2602.16034](https://arxiv.org/abs/2602.16034) | — | `A` `component` `drift` |

---

## 6. Risk Family 5 — Cognitive Bias & Dark Patterns

> **Tutorial taxonomy**: Entry point = Objective/Stakeholder layer; Propagation = Output generation + User interaction; **_FnTrendsIR_**: Bias & Fairness (RF2). Risk type: **A** (amplified by LLM fluency).

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Bias Beware: The Impact of Cognitive Biases on LLM-Driven Product Recommendations** — Krasniqi et al. | EMNLP 2025 | [2502.01349](https://arxiv.org/abs/2502.01349) | — | `A` `risk:rf5` `type:A` `topic:cognitive-bias` `topic:recsys` |
| **DarkBench: Benchmarking Dark Patterns in Large Language Models** — Kran et al. | arXiv 2025 | [2503.10728](https://arxiv.org/abs/2503.10728) | — | `A` `risk:rf5` `type:A` `topic:dark-patterns` `topic:benchmark` |
| **An Inconspicuous Attack to Bias LLM Responses** — Anonymous | arXiv 2024 | [2406.04755](https://arxiv.org/abs/2406.04755) | — | `A` `risk:rf5` `type:A` `topic:stealthy` |
| **Quantifying Cognitive Bias Induction in LLM-Generated Content** — Anonymous | arXiv 2025 | [2507.03194](https://arxiv.org/abs/2507.03194) | — | `A` `risk:rf5` `type:A` `topic:cognitive-bias` |
| **Understanding Biases in ChatGPT-based Recommender Systems** — Anonymous | arXiv 2024 | [2401.10545](https://arxiv.org/abs/2401.10545) | — | `A` `risk:rf5` `type:A` `topic:recsys` |
| **Stereotype or Personalization? User Identity Biases Chatbot Recommendations** — Anonymous | arXiv 2024 | [2410.05613](https://arxiv.org/abs/2410.05613) | — | `A` `risk:rf5` `type:A` `topic:recsys` `topic:stereotype` |
| **Bias Mitigation for AI-Feedback Loops in Recommender Systems** — Anonymous | arXiv 2025 | [2509.00109](https://arxiv.org/abs/2509.00109) | — | `A` `risk:rf5` `risk:rf6` `type:A` `topic:feedback-loop` `topic:recsys` |
| **Aligning Recommendations with User Popularity Preferences** — Mona Schirmer, Anton Thielmann, Pola Schwöbel et al. | arXiv 2026 | [2604.01036](https://arxiv.org/abs/2604.01036) | — | `A` |
| **LLM as Explainable Re-Ranker for Recommendation System** — Yaqi Wang, Haojia Sun, Shuting Zhang | arXiv 2025 | [2512.03439](https://arxiv.org/abs/2512.03439) | — | `A` `component` `drift` |
| **Toward Safe and Human-Aligned Game Conversational Recommendation via Multi-Agent Decomposition** — Zheng Hui, Xiaokai Wei, Yexi Jiang et al. | arXiv 2025 | [2504.20094](https://arxiv.org/abs/2504.20094) | — | `A` `component` `compromise` |
| **HELM: A Human-Centered Evaluation Framework for LLM-Powered Recommender Systems** — Sushant Mehta | arXiv 2026 | [2601.19197](https://arxiv.org/abs/2601.19197) | — | `A` `component` `drift` |
| **Bridging Semantic Understanding and Popularity Bias with LLMs** — Renqiang Luo, Dong Zhang, Yupeng Gao et al. | arXiv 2026 | [2601.09478](https://arxiv.org/abs/2601.09478) | — | `A` `component` `drift` |

---

## 7. Risk Family 6 — Availability & Resource Depletion

> **Tutorial taxonomy**: Entry point = Execution layer; Propagation = Tool-action chains + Recursive spawning; **_FnTrendsIR_**: Resource Exhaustion & Efficiency (RF5). Risk type: **E** (emergent in multi-agent).

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Advertisement Embedding Attacks Against Large Language Models** — Anonymous | arXiv 2025 | [2508.17674](https://arxiv.org/abs/2508.17674) | — | `E` `risk:rf6` `risk:rf1` `type:E` `topic:advertising` |

---

## 8. Collusion in Multi-Agent Systems

> **Tutorial taxonomy**: Emergent risk in Role-based and Decentralised topologies; **_FnTrendsIR_**: Coordination Failure & Collusion (RF6). Risk type: **E**.

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **A Survey of Collusion Risk in LLM-Powered Multi-Agent Systems** — Ghaemi | NeurIPS WS 2025 | [OpenReview](https://openreview.net/forum?id=Ylh8617Qyd) | — | `E` `risk:rf6` `type:E` `topic:survey` `topic:collusion` |
| **Studying Coordination and Collusion in Multi-Agent LLM Code Reviews** — Anonymous | OpenReview 2025 | [OpenReview](https://openreview.net/forum?id=CdZaamCf5Y) | — | `E` `risk:rf6` `type:E` `topic:collusion` |
| **Exposing Multi-Agent Collusion Risks in AI-Based Healthcare** — Anonymous | arXiv 2025 | [2512.03097](https://arxiv.org/abs/2512.03097) | — | `E` `risk:rf6` `type:E` `topic:collusion` `domain:healthcare` |
| **Beyond Single-Agent Safety: A Taxonomy of Risks in LLM-to-LLM Interactions** — Bisconti et al. | arXiv 2025 | [2512.02682](https://arxiv.org/abs/2512.02682) | — | `E` `risk:rf6` `risk:rf3` `type:E` `topic:taxonomy` |
| **Emergent Social Intelligence Risks in Generative Multi-Agent Systems** — Yue Huang, Yu Jiang, Wenjie Wang, Haomin Zhuang, Xiaonan Luo, Yuchen Ma, Zhangchen Xu, Zichen Chen, Nuno Moniz, Zinan Lin, Pin-Yu Chen, Nitesh V Chawla, Nouha Dziri, Huan Sun, Xiangliang Zhang | arXiv 2026 | [2603.27771](https://arxiv.org/abs/2603.27771) | [GitHub](https://github.com/HowieHwong/RiskLab) | `E` `type:E` `topic:collusion` `topic:social-intelligence` `topo:decentralised` `tier:strategic` |
| **HARP: Measuring Harm Amplification in Multi-Agent LLM Systems** — Md Hafizur Rahman, Zafaryab Haider, Tanzim Mahfuz et al. | arXiv 2026 | [2605.27489](https://arxiv.org/abs/2605.27489) | — | `E` `composition` `compromise` |
| **Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs** — Marcantonio Bracale Syrnikov, Federico Pierucci, Marcello Galisai et al. | arXiv 2026 | [2601.11369](https://arxiv.org/abs/2601.11369) | — | `E` `composition` `misalignment` |

---

## 9. Fairness, Feedback Loops & Exposure Bias

> **Tutorial taxonomy**: Objective/Stakeholder layer; **_FnTrendsIR_**: Bias & Fairness (RF2). Risk type: **A**.

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Retrieval Augmented Conversational Recommendation with Reinforcement Learning** — Zhenrui Yue, Honglei Zhuang, Zhen Qin et al. | arXiv 2026 | [2604.04457](https://arxiv.org/abs/2604.04457) | — | — |
| **Beyond Static Best-of-N: Bayesian List-wise Alignment for LLM-based Recommendation** — Ruijun Chen, Chongming Gao, Jiawei Chen et al. | arXiv 2026 | [2605.04559](https://arxiv.org/abs/2605.04559) | — | `A` `component` `drift` |
| **Multi-Agent Large Language Models for Conversational Task-Solving** — Jonas Becker | arXiv 2024 | [2410.22932](https://arxiv.org/abs/2410.22932) | via HuggingFace Papers | `E` `component` `drift` |
| **The 2nd Workshop on Human-Centered Recommender Systems** — Kaike Zhang, Jiakai Tang, Du Su et al. | arXiv 2025 | [2511.19979](https://arxiv.org/abs/2511.19979) | — | `A` `component` `drift` |
| **UFO: Unfair-to-Fair Evolving Mitigates Unfairness in LLM-based Recommender Systems via Self-Play Fine-tuning** — Jiaming Zhang, Yuyuan Li, Xiaohua Feng et al. | arXiv 2025 | [2511.18342](https://arxiv.org/abs/2511.18342) | — | `A` `component` `drift` |
| **Music Recommendation with Large Language Models: Challenges, Opportunities, and Evaluation** — Elena V. Epure, Yashar Deldjoo, Bruno Sguerra et al. | arXiv 2025 | [2511.16478](https://arxiv.org/abs/2511.16478) | — | `A` `component` `drift` |
| **Vectorized Context-Aware Embeddings for GAT-Based Collaborative Filtering** — Danial Ebrat, Sepideh Ahmadian, Luis Rueda | arXiv 2025 | [2510.26461](https://arxiv.org/abs/2510.26461) | — | `A` `component` `drift` |
| **Does LLM Focus on the Right Words? Mitigating Context Bias in LLM-based Recommenders** — Bohao Wang, Jiawei Chen, Feng Liu et al. | arXiv 2025 | [2510.10978](https://arxiv.org/abs/2510.10978) | — | `A` `component` `drift` |
| **Ethical AI prompt recommendations in large language models using collaborative filtering** — Jordan Nelson, Almas Baimagambetov, Konstantinos Avgerinakis et al. | arXiv 2025 | [2510.06924](https://arxiv.org/abs/2510.06924) | — | `A` `component` `drift` |
| **Where Should I Study? Biased Language Models Decide! Evaluating Fairness in LMs for Academic Recommendations** — Krithi Shailya, Akhilesh Kumar Mishra, Gokul S Krishnan et al. | arXiv 2025 | [2509.04498](https://arxiv.org/abs/2509.04498) | — | `A` `component` `drift` |
| **Revealing Potential Biases in LLM-Based Recommender Systems in the Cold Start Setting** — Alexandre Andre, Gauthier Roy, Eva Dyer et al. | arXiv 2025 | [2508.20401](https://arxiv.org/abs/2508.20401) | — | `A` `component` `drift` |
| **PerFairX: Is There a Balance Between Fairness and Personality in Large Language Model Recommendations?** — Chandan Kumar Sah | arXiv 2025 | [2509.08829](https://arxiv.org/abs/2509.08829) | — | `A` `component` `drift` |
| **ViLLA-MMBench: A Unified Benchmark Suite for LLM-Augmented Multimodal Movie Recommendation** — Fatemeh Nazary, Ali Tourani, Yashar Deldjoo et al. | arXiv 2025 | [2508.04206](https://arxiv.org/abs/2508.04206) | — | `A` `component` `drift` |
| **Breaking User-Centric Agency: A Tri-Party Framework for Agent-Based Recommendation** — Yaxin Gong, Chongming Gao, Chenxiao Fan et al. | arXiv 2026 | [2603.10673](https://arxiv.org/abs/2603.10673) | — | `A` `component` `drift` |
| **Ablation Study of a Fairness Auditing Agentic System for Bias Mitigation in Early-Onset Colorectal Cancer Detection** — Amalia Ionescu, Jose Guadalupe Hernandez, Jui-Hsuan Chang et al. | arXiv 2026 | [2603.17179](https://arxiv.org/abs/2603.17179) | — | `A` `composition` `drift` |
| **LLMs as Orchestrators: Constraint-Compliant Multi-Agent Optimization for Recommendation Systems** — Guilin Zhang, Kai Zhao, Jeffrey Friedman et al. | arXiv 2026 | [2601.19121](https://arxiv.org/abs/2601.19121) | — | `A` `component` `drift` |
| **Can Fairness Be Prompted? Prompt-Based Debiasing Strategies in High-Stakes Recommendations** — Mihaela Rotar, Theresia Veronika Rampisela, Maria Maistro | arXiv 2026 | [2603.12935](https://arxiv.org/abs/2603.12935) | — | `A` `component` `drift` |
| **Uncertainty and Fairness Awareness in LLM-Based Recommendation Systems** — Chandan Kumar Sah, Xiaoli Lian, Li Zhang et al. | arXiv 2026 | [2602.02582](https://arxiv.org/abs/2602.02582) | — | `A` `component` `drift` |
| **Towards Fair Large Language Model-based Recommender Systems without Costly Retraining** — Jin Li, Huilin Gu, Shoujin Wang et al. | arXiv 2026 | [2601.17492](https://arxiv.org/abs/2601.17492) | — | `A` `component` `drift` |

---

## 10. Evaluation & Benchmarking

> **Evaluation framework**: Component / Interaction / Composition scope × Offline / Online setting.

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Why Do Multi-Agent LLM Systems Fail?** — Cemri et al. | arXiv 2025 | [2503.13657](https://arxiv.org/abs/2503.13657) | — | `E` `topic:evaluation` `topic:failure-taxonomy` |
| **AgentLeak: A Full-Stack Benchmark for Privacy Leakage in Multi-Agent LLM Systems** — Anonymous | arXiv 2026 | [2602.11510](https://arxiv.org/abs/2602.11510) | — | `E` `risk:rf4` `type:E` `topic:benchmark` `topic:full-stack` |
| **Multi-Agent LLM Governance for Safe Two-Timescale Reinforcement Learning in SDN-IoT Defense** — Saeid Jamshidi, Negar Shahabi, Foutse Khomh et al. | arXiv 2026 | [2604.01127](https://arxiv.org/abs/2604.01127) | — | — |
| **Towards Position-Robust Talent Recommendation via Large Language Models** — Silin Du, Hongyan Liu | arXiv 2026 | [2604.02200](https://arxiv.org/abs/2604.02200) | — | `A` |
| **Bilateral Intent-Enhanced Sequential Recommendation with Embedding Perturbation-Based Contrastive Learning** — Shanfan Zhang, Yongyi Lin, Yuan Rao | arXiv 2026 | [2604.02833](https://arxiv.org/abs/2604.02833) | — | — |
| **ERASE: Benchmarking Feature Selection Methods for Deep Recommender
  Systems** — Pengyue Jia, Yejing Wang, Zhaocheng Du et al. | arXiv 2024 | [2403.12660](https://arxiv.org/abs/2403.12660) | via HuggingFace Papers | `component` `drift` |
| **CogRec: A Cognitive Recommender Agent Fusing Large Language Models and Soar for Explainable Recommendation** — Jiaxin Hu, Tao Wang, Bingsan Yang et al. | arXiv 2025 | [2512.24113](https://arxiv.org/abs/2512.24113) | — | `A` `component` `compromise` |
| **The Mental World of Large Language Models in Recommendation: A Benchmark on Association, Personalization, and Knowledgeability** — Guangneng Hu | arXiv 2025 | [2512.17389](https://arxiv.org/abs/2512.17389) | — | `A` `component` `drift` |
| **Reveal Hidden Pitfalls and Navigate Next Generation of Vector Similarity Search from Task-Centric Views** — Tingyang Chen, Cong Fu, Jiahua Wu et al. | arXiv 2025 | [2512.12980](https://arxiv.org/abs/2512.12980) | — | `composition` `drift` |
| **Combining LLM Semantic Reasoning with GNN Structural Modeling for Multi-View Multi-Label Feature Selection** — Zhiqi Chen, Yuzhou Liu, Jiarui Liu et al. | arXiv 2025 | [2511.08008](https://arxiv.org/abs/2511.08008) | — | `component` `drift` |
| **ECKGBench: Benchmarking Large Language Models in E-commerce Leveraging Knowledge Graph** — Langming Liu, Haibin Chen, Yuhao Wang et al. | arXiv 2025 | [2503.15990](https://arxiv.org/abs/2503.15990) | — | `A` `component` `drift` |
| **MARCO: A Cooperative Knowledge Transfer Framework for Personalized Cross-domain Recommendations** — Lili Xie, Yi Zhang, Ruihong Qiu et al. | arXiv 2025 | [2510.04508](https://arxiv.org/abs/2510.04508) | — | `component` `drift` |
| **Doctorina MedBench: End-to-End Evaluation of Agent-Based Medical AI** — Anna Kozlova, Stanislau Salavei, Pavel Satalkin et al. | arXiv 2026 | [2603.25821](https://arxiv.org/abs/2603.25821) | — | `composition` `drift` |
| **LLMAR: A Tuning-Free Recommendation Framework for Sparse and Text-Rich Industrial Domains** — Ryogo Hishikawa, Ichiro Kataoka, Shinya Yuda | arXiv 2026 | [2604.16379](https://arxiv.org/abs/2604.16379) | — | `A` `component` `drift` |
| **MATRAG: Multi-Agent Transparent Retrieval-Augmented Generation for Explainable Recommendations** — Sushant Mehta | arXiv 2026 | [2604.20848](https://arxiv.org/abs/2604.20848) | — | `component` `drift` |
| **RobustExplain: Evaluating Robustness of LLM-Based Explanation Agents for Recommendation** — Guilin Zhang, Kai Zhao, Jeffrey Friedman et al. | arXiv 2026 | [2601.19120](https://arxiv.org/abs/2601.19120) | — | `component` `drift` |
| **Length-Adaptive Interest Network for Balancing Long and Short Sequence Modeling in CTR Prediction** — Zhicheng Zhang, Zhaocheng Du, Jieming Zhu et al. | arXiv 2026 | [2601.19142](https://arxiv.org/abs/2601.19142) | — | `A` `component` `drift` |

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
| **Agentic AI Frameworks: Architectures, Protocols, and Design Challenges** — Hana Derouiche, Zaki Brahmi, Haithem Mazeni | arXiv 2025 | [2508.10146](https://arxiv.org/abs/2508.10146) | via HuggingFace Papers | `composition` `drift` |
| **Two is Better than One: Efficient Ensemble Defense for Robust and Compact Models** — Yoojin Jung, Byung Cheol Song | arXiv 2025 | [2504.04747](https://arxiv.org/abs/2504.04747) | classical adversarial RecSys | `A` `component` `compromise` |
| **ASTRA: Agentic Steerability and Risk Assessment Framework** — Itay Hazan, Yael Mathov, Guy Shtar et al. | arXiv 2025 | [2511.18114](https://arxiv.org/abs/2511.18114) | — | `component` `compromise` |
| **Simulating Filter Bubble on Short-video Recommender System with Large Language Model Agents** — Nicholas Sukiennik, Haoyu Wang, Zailin Zeng et al. | arXiv 2025 | [2504.08742](https://arxiv.org/abs/2504.08742) | — | `A` `component` `drift` |
| **Explainable and Fine-Grained Safeguarding of LLM Multi-Agent Systems via Bi-Level Graph Anomaly Detection** — Junjun Pan, Yixin Liu, Rui Miao et al. | arXiv 2025 | [2512.18733](https://arxiv.org/abs/2512.18733) | — | `component` `compromise` |
| **CITED: A Decision Boundary-Aware Signature for GNNs Towards Model Extraction Defense** — Bolin Shen, Md Shamim Seraj, Zhan Cheng et al. | arXiv 2026 | [2602.20418](https://arxiv.org/abs/2602.20418) | — | `component` `compromise` |

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
| **MI9 -- Agent Intelligence Protocol: Runtime Governance for Agentic AI
  Systems** — Charles L. Wang, Trisha Singhal, Ameya Kelkar et al. | arXiv 2025 | [2508.03858](https://arxiv.org/abs/2508.03858) | via HuggingFace Papers | `E` `component` `drift` |
| **Control Plane as a Tool: A Scalable Design Pattern for Agentic AI
  Systems** — Sivasathivel Kandasamy | arXiv 2025 | [2505.06817](https://arxiv.org/abs/2505.06817) | via HuggingFace Papers | `component` `drift` |

---

## 15. Uncategorised / New Additions

> Papers added by crawler awaiting manual tagging.

| Paper | Venue | arXiv | Notes | Tags |
|----|----|----|----|----|
| **Let the Agent Steer: Closed-Loop Ranking Optimization via Influence Exchange** — Yin Cheng, Liao Zhou, Xiyu Liang et al. | arXiv 2026 | [2603.27765](https://arxiv.org/abs/2603.27765) | — | `A` |
| **Unbiased Recommender Learning from Missing-Not-At-Random Implicit
  Feedback** — Yuta Saito, Suguru Yaginuma, Yuta Nishino et al. | arXiv 2019 | [1909.03601](https://arxiv.org/abs/1909.03601) | via HuggingFace Papers | `A` `component` `drift` |
| **Large Language Models are Competitive Near Cold-start Recommenders for
  Language- and Item-based Preferences** — Scott Sanner, Krisztian Balog, Filip Radlinski et al. | arXiv 2023 | [2307.14225](https://arxiv.org/abs/2307.14225) | via HuggingFace Papers | `A` `component` `drift` |
| **Matrix-Free Two-to-Infinity and One-to-Two Norms Estimation** — Askar Tsyganov, Evgeny Frolov, Sergey Samsonov et al. | arXiv 2025 | [2508.04444](https://arxiv.org/abs/2508.04444) | classical adversarial RecSys | `A` `component` `compromise` |
| **Navigating the Black Box: Leveraging LLMs for Effective Text-Level Graph Injection Attacks** — Yuefei Lyu, Chaozhuo Li, Xi Zhang et al. | arXiv 2025 | [2506.13276](https://arxiv.org/abs/2506.13276) | classical adversarial RecSys | `A` `component` `compromise` |
| **Invariance Matters: Empowering Social Recommendation via Graph Invariant Learning** — Yonghui Yang, Le Wu, Yuxin Liao et al. | arXiv 2025 | [2504.10432](https://arxiv.org/abs/2504.10432) | classical adversarial RecSys | `A` `component` `compromise` |
| **Towards Efficient Hypergraph and Multi-LLM Agent Recommender Systems** — Tendai Mukande, Esraa Ali, Annalina Caputo et al. | arXiv 2025 | [2512.06590](https://arxiv.org/abs/2512.06590) | — | `A` `component` `drift` |
| **Agentic Explainable Artificial Intelligence (Agentic XAI) Approach To Explore Better Explanation** — Tomoaki Yamaguchi, Yutong Zhou, Masahiro Ryo et al. | arXiv 2025 | [2512.21066](https://arxiv.org/abs/2512.21066) | — | `A` `component` `misalignment` |
| **Selective LLM-Guided Regularization for Enhancing Recommendation Models** — Shanglin Yang, Zhan Shi | arXiv 2025 | [2512.21526](https://arxiv.org/abs/2512.21526) | — | `A` `component` `drift` |
| **STEP: Stepwise Curriculum Learning for Context-Knowledge Fusion in Conversational Recommendation** — Zhenye Yang, Jinpeng Chen, Huan Li et al. | arXiv 2025 | [2508.10669](https://arxiv.org/abs/2508.10669) | — | `A` `component` `drift` |
| **Multi-agents based User Values Mining for Recommendation** — Lijian Chen, Wei Yuan, Tong Chen et al. | arXiv 2025 | [2505.00981](https://arxiv.org/abs/2505.00981) | — | `A` `component` `drift` |
| **Bridging Legal Knowledge and AI: Retrieval-Augmented Generation with Vector Stores, Knowledge Graphs, and Hierarchical Non-negative Matrix Factorization** — Ryan C. Barron, Maksim E. Eren, Olga M. Serafimova et al. | arXiv 2025 | [2502.20364](https://arxiv.org/abs/2502.20364) | — | `A` `component` `drift` |
| **Journalism-Guided Agentic In-Context Learning for News Stance Detection** — Dahyun Lee, Jonghyeon Choi, Jiyoung Han et al. | arXiv 2025 | [2507.11049](https://arxiv.org/abs/2507.11049) | — | `A` `component` `drift` |
| **Hijacking online reviews: sparse manipulation and behavioral buffering in popularity-biased rating systems** — Itsuki Fujisaki, Kunhao Yang | arXiv 2026 | [2604.13049](https://arxiv.org/abs/2604.13049) | — | `A` `component` `compromise` |
| **VLM2Rec: Resolving Modality Collapse in Vision-Language Model Embedders for Multimodal Sequential Recommendation** — Junyoung Kim, Woojoo Kim, Jaehyung Lim et al. | arXiv 2026 | [2603.17450](https://arxiv.org/abs/2603.17450) | — | `component` `drift` |
| **Best-of-Both-Worlds Multi-Dueling Bandits: Unified Algorithms for Stochastic and Adversarial Preferences under Condorcet and Borda Objectives** — S Akash, Pratik Gajane, Jawar Singh | arXiv 2026 | [2603.18972](https://arxiv.org/abs/2603.18972) | — | `A` `component` `compromise` |
| **A Cognitive Distribution and Behavior-Consistent Framework for Black-Box Attacks on Recommender Systems** — Hongyue Zhang, Mingming Li, Dongqin Liu et al. | arXiv 2026 | [2602.10633](https://arxiv.org/abs/2602.10633) | — | `A` `component` `compromise` |
| **The Behavioral Fabric of LLM-Powered GUI Agents: Human Values and Interaction Outcomes** — Simret Araya Gebreegziabher, Yukun Yang, Charles Chiang et al. | arXiv 2026 | [2601.16356](https://arxiv.org/abs/2601.16356) | — | `A` `component` `drift` |
| **AMEM4Rec: Leveraging Cross-User Similarity for Memory Evolution in Agentic LLM Recommenders** — Minh-Duc Nguyen, Hai-Dang Kieu, Dung D. Le | arXiv 2026 | [2602.08837](https://arxiv.org/abs/2602.08837) | — | `A` `composition` `drift` |

---

## How to Contribute / Crawler Notes

This README is maintained by `crawler.py` in this repository. The crawler:

1. Queries the **arXiv API** daily for new papers matching the taxonomy keywords
2. Checks **OpenReview** for workshop/conference submissions (requires authentication)
3. Crawls **HuggingFace Papers** for community-curated arXiv papers with GitHub links
4. Tags each paper against the **scope** (component/interaction/composition), **threat tier** (drift/misalignment/compromise), and **risk type** (amplified/emergent)
5. Saves unfiltered results to `raw_crawl.json`, then filters for relevance
6. Commits the updated README automatically via GitHub Actions

**To add a paper manually**: edit `papers.json` and run `python3 crawler.py --no-crawl`.

**Last crawler run**: 2026-07-01
