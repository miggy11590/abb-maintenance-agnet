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
