# MedCAD Digital Library
### National Digital Supply Network for the NHS

A desktop application prototype demonstrating a governance-controlled digital supply chain for additive manufacturing (3D printing) of non-patient contact medical equipment components across NHS Trusts.

---

## Overview

MedCAD addresses the problem of equipment downtime in NHS hospitals by enabling rapid, local fabrication of eligible replacement parts — bypassing traditional OEM lead times of 14+ days in favour of sub-24-hour turnaround through certified regional AM (Additive Manufacturing) hubs.

The platform connects three key actors:

| Actor | Role |
|---|---|
| **OEM Suppliers** | Upload verified, cryptographically signed CAD files |
| **NHS Trusts** | Browse the digital catalog and dispatch fabrication requests |
| **Regional AM Hubs** | Fabricate parts with full QA traceability |

---

## Interfaces

### Interface 1 — Landing Page (`interface 1.py`)
The public-facing entry point to the MedCAD hub. Displays the platform mission, a workflow summary, and core capability cards (OEM authorization, non-patient contact focus, ISO/ASTM 52920 audit compliance). Includes Log In and Sign Up actions.

### Interface 2 — Hospital Ordering Portal (`interface 2.py`)
The Trust-facing catalog browser. Hospital engineering staff can search OEM-authorized components, view detailed part specifications (geometry, manufacturing constraints, logistics), and dispatch a fabrication request to their nearest approved AM hub.

Example part shown: **Ventilator Monitor Bracket (MC-104)** — reduces lead time from 14 days (OEM) to under 24 hours.

### Interface 3 — Digital Quality & Traceability Passport (`interface 3.py`)
A per-order compliance record that logs the complete digital thread:
- OEM CAD file authentication (SHA-256 hash verification)
- Trust authorization
- Manufacturing parameters (material, process, layer height)
- Post-process QA results

Liability is clearly apportioned between OEM, fabrication hub, and requesting Trust per ISO/ASTM 52920.

---

## Requirements

- Python 3.8+
- `tkinter` (included in standard Python distributions)

No external dependencies required.

---

## Running the Interfaces

Each interface is a standalone script:

```bash
python "interface 1.py"   # Landing Page
python "interface 2.py"   # Hospital Ordering Portal
python "interface 3.py"   # Compliance Passport
```

---

## Compliance & Governance

- **Standard:** ISO/ASTM 52920 (Additive Manufacturing — Quality Management)
- **Material qualification:** ISO 10993 (biocompatibility for non-patient contact use)
- **Dimensional tolerances:** ISO 2768-mK
- **File integrity:** SHA-256 hash verification on all OEM-uploaded CAD files
- **Scope:** Non-patient contact components only (brackets, housings, mounts, clamps, handles)

---

## Project Context

Built for **Amplify 2026** — a design challenge focused on resilient NHS supply chains through digital manufacturing.

© 2026 MedCAD Digital Library | Partnered with NHS
