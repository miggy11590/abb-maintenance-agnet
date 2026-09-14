# Secure Multimodal Maintenance Intelligence Agent

A RAG-based AI assistant that answers industrial maintenance and troubleshooting
questions using citations from real equipment manuals — built as a solo entry
for the ABB Accelerator 2026 (Theme 2: Multimodal Maintenance Intelligence Agent).

## What it does

Given a technical manual (PDF), the system:
1. Extracts and chunks the manual's text
2. Generates semantic embeddings for each chunk
3. Retrieves the most relevant chunks for a technician's question
4. Uses an LLM to generate a grounded answer, citing which chunks it used
5. Is designed to say "I don't have enough evidence" rather than guess,
   when the manual doesn't contain a relevant answer

## Why this project

Most "chat with your manual" tools stop at basic retrieval. This project's
differentiator is treating the security of that pipeline as a first-class
concern — industrial documentation should be treated as untrusted data, not
as instructions an AI blindly trusts. The system is being built with defenses
against prompt injection (including indirect injection via malicious document
content) and, eventually, role-based access control so that unauthorized users
never have restricted documents even reach the LLM in the first place.

## Current status

**Working:**
- PDF text extraction (`pypdf`)
- Chunking with overlap, to avoid splitting important information across chunk boundaries
- Local, free embeddings via `sentence-transformers` (`all-MiniLM-L6-v2`)
- Vector storage and semantic retrieval via `chromadb`
- Grounded question-answering via Gemini's free API tier, with a system prompt
  constraining answers to retrieved evidence and requiring citations
- Interactive question loop (ask multiple questions per run)
- Initial testing of prompt injection resistance (direct + indirect)

**Not yet built:**
- Authentication / role-based access control
- Audit logging
- OCR and multimodal (image/diagram/table) document support
- Web interface (currently a terminal script)
- Formal threat model documentation
- Output guard layer
-Dedicated prompt injection detection/blocking (currently relies on the
  system prompt and the underlying model's own training — no separate
  input guard checks retrieved content before it reaches the LLM)
## Tech stack

| Purpose | Tool |
|---|---|
| PDF extraction | `pypdf` |
| Embeddings | `sentence-transformers` (local, free) |
| Vector database | `chromadb` |
| LLM | Google Gemini API (free tier) |
| Language | Python |

Stack choices prioritize free/local tools where possible, and are introduced
incrementally rather than all at once — see [Roadmap](#roadmap) below.

## Setup

1. Clone this repo and `cd` into it.
2. Install dependencies:

3. Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com) (no credit card required).
4. Create a `.env` file in the project root:

5. Place a PDF manual at `data/equipment_manual.pdf`.
6. Run:
   
   
## Roadmap

- [ ] Add metadata (page numbers) to chunks for more precise citations
- [ ] Build a basic input guard to flag suspicious content in retrieved chunks
  *before* they reach the LLM, rather than relying on the LLM to resist injection alone
- [ ] Add role-based access control — enforce document permissions before retrieval
- [ ] Add audit logging (query, documents retrieved/denied, security events)
- [ ] Add OCR + multimodal support for scanned pages, tables, and diagrams
- [ ] Wrap the pipeline in a FastAPI backend with a simple web frontend
- [ ] Write up a basic threat model (assets, attackers, attack surfaces, mitigations)

## Disclaimer

This is a learning project and prototype, not a production security tool. It
does not claim to detect or prevent all forms of prompt injection or
unauthorized access — see the Roadmap for what's genuinely implemented versus
still planned.
