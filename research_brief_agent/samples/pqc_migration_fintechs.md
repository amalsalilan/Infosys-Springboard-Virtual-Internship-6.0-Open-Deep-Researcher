# Post-Quantum Cryptography Migration Plan for Fintechs
*Date (IST):* 2025-08-24

**Objective:** Define a pragmatic roadmap to achieve crypto-agility and migrate priority systems to PQC while maintaining compliance and uptime.

## Key Questions
- Which data flows are most exposed to harvest-now-decrypt-later risk?
- What PQC algorithms/libraries align with current standards and vendors?
- What rollout waves minimize risk with measurable readiness gates?

## Methodology
- Inventory cryptographic usage across services, SDKs, keys, and certificates.
- Risk-rank data flows; select pilot targets.
- Pilot hybrid KEM/TLS in a canary environment with rollback criteria.
- Define monitoring and regression tests for each migration wave.

## Search Strategy
- NIST PQC finalists/standards; IETF drafts for TLS/KEM guidance.
- Vendor roadmaps (cloud HSMs/KMS, CDNs, API gateways).
- BFSI advisories (RBI, PCI SSC, ISO/IEC).

## Sources to Start
- NIST PQC standards portal  
- IETF TLS + KEM/HYBRID drafts  
- Cloud KMS/HSM vendor docs (AWS/GCP/Azure)  
- RBI and PCI SSC guidance  

## Milestones & Timeline
- **Crypto Inventory & Risk Map** — 2025-09-05: System-by-system crypto usage  
- **Hybrid TLS Pilot** — 2025-09-15: Canary with metrics + rollback  
- **Wave 1 Rollout** — 2025-09-25: Customer-facing APIs with crypto-agility  

## Risks & Mitigations
- **Risk:** Vendor libraries immature  
  **Mitigation:** Abstraction layer; pinned versions; fallback ciphers  
- **Risk:** Performance regressions  
  **Mitigation:** Benchmark; scale capacity; cache session keys  

## Deliverables
- Gantt-level roadmap  
- Risk register with tests/controls  
- Pilot report with latency/throughput benchmarks  
