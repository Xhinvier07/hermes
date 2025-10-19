# Hermes — Send. Sense. Shape.

Hermes blends sentiment analysis and intelligent text generation to help you understand and shape tone. Paste or write text, get immediate sentiment feedback with confidence scores and highlighted cues, then generate polished or tone-shifted rewrites — all in a clean, minimal interface.

## Project overview

**Goal:** build web app (Streamlit) that performs:

- **Aspect-aware sentiment analysis** (label + confidence + aspects/topics)
- **Dynamic text generation** that can produce novel outputs (not selected from predefined arrays) in short / medium / long lengths, controlled by a requested sentiment (positive / negative / neutral) and number of variations
- **Support for multiple interchangeable models** (local & API-backed) and flexible filtering/options for production-quality demos

This README documents the project purpose, features, architecture, development roadmap, testing guidance, and governance so you can implement Hermes in clear stages.

## Key features (end goal)

### Sentiment Analyzer

- Binary/ternary/continuous sentiment outputs (positive / neutral / negative / score)
- Aspect extraction & aspect-level sentiment (e.g., "battery: negative", "design: positive")
- Token-level highlights to explain influential words
- Confidence scoring and basic calibration information

### Dynamic Text Generator

- **Modes:** Paraphrase, Flip sentiment, Polish / Formalize, Custom prompt
- **Length options:** Short / Medium / Long
- **Sentiment control:** positive / negative / neutral — generation guided toward the selected sentiment
- **N variations:** request any number of unique outputs (not limited to a fixed array)
- **Sampling control** to ensure diversity (temperature, top_k, top_p, repetition penalties)
- Mark outputs with generation provenance (local model vs remote API)

### Model flexibility

- Swap models at runtime (DistilBERT/RoBERTa/XLM-R for analysis; GPT-2 / GPT-Neo / API LLMs for generation)
- Model selection UI and lightweight model wrapper for consistent I/O

### UX & productivity

- Clean dark-themed Streamlit UI (Hermes branding)
- Session history, export (CSV/JSON), and copy-to-clipboard

## Recommended models & components

### Sentiment & aspect extraction

- **Quick prototyping:** `distilbert-base-uncased-finetuned-sst-2-english` (binary/ternary)
- **Higher accuracy:** `roberta-large-mnli` or RoBERTa finetuned models
- **Aspect extraction approaches:**
  - Sequence labeling model (BIO tags) that extracts aspect spans
  - Classifier over extracted aspects for aspect-level polarity
  - Lightweight rule-based fallback (noun-phrase extraction + lexicon) for quick demo

### Generation

- **Local offline:** GPT-2 / GPT-Neo (good for small demos but lower quality)
- **Cloud/high quality:** OpenAI GPT / Anthropic / other LLM API (best for production-like rewrites)
- Use sampling parameters (temperature, top_k/top_p) to produce diverse, dynamic outputs rather than pulling from a fixed response list

### Explainability

- **Lightweight:** lexicon highlighting + token importance proportional to model logits
- **Advanced:** SHAP / LIME for token-level contribution (optional; heavier)

## How dynamic generation will work (no arrays)

To ensure outputs are **generated** (not chosen from preset arrays):

1. **Prompt engineering:** construct a prompt template that includes:

   - the original text
   - desired target sentiment label
   - requested style/length instructions (short/medium/long)
   - optional constraints (avoid X, preserve Y)

2. **Sampling-based decoding:** use stochastic decoding (temperature > 0, top_p or top_k sampling) so repeated requests yield unique outputs.

3. **Diversity controls:** allow repeat_penalty / top_k / top_p adjustments; for strict sentiment adherence, add sentiment-check loop (post-generation filter & re-sample if polarity mismatch).

4. **Number of variations:** when the user requests n outputs, call the generation model n times (or use batched sampling) with small seed/temperature perturbations to produce diverse and novel outputs.

5. **Validation:** run a light-weight sentiment classifier on generations to ensure outputs match the requested sentiment; if not, retry generation with stronger guidance or sampling settings.

This pipeline avoids using a static set of canned rewrites and produces novel text each time.

## Roadmap & stage deliverables

### Stage 0 — Research & planning

- Finalize MVP scope, UX wireframes, model shortlist, privacy note
- Create small test corpus (positive/neutral/negative, domain-specific examples)

### Stage 1 — Model prototype (CLI / notebook)

- Validate sentiment model outputs on test corpus (labels & confidence)
- Validate basic prompt templates for generation (short/med/long) using a generator model
- **Deliverable:** evaluation notes & recommended default models

### Stage 2 — Minimal Streamlit Analyzer (MVP)

- Single-page UI: text input, Analyze button, label + confidence + token highlights, history
- **Deliverable:** Deployed local Streamlit with analysis only

### Stage 3 — Add Generator & Controls

- Add generation UI: sentiment selector, length selector, n variations, sampling settings
- Implement dynamic generation pipeline (prompting + sampling + validation)
- **Deliverable:** In-app generation that produces novel outputs per request

### Stage 4 — Aspect Sentiment & Explainability

- Add aspect extraction module & per-aspect sentiment display
- Implement token-level explainability (lexicon/SHAP fallback)
- **Deliverable:** detailed result card per input showing aspects and reasons

### Stage 5 — Model switching & fine-tuning

- Add model selection UI, and scripts for lightweight fine-tuning with user-supplied CSV
- **Deliverable:** ability to test alternate models & apply small-domain adaptions

### Stage 6 — Persistence, analytics & deployment

- Session DB (SQLite or opt-in cloud store), analytics dashboard, export
- Dockerize & deploy (Streamlit Cloud / VPS)
- **Deliverable:** public demo + README, demo GIF, testing report

## Testing & evaluation

### Unit & integration tests

- Inference sanity checks (model returns expected labels for controlled sentences)
- Generation integrity (output length/sentiment matches requested constraints)
- UI flow smoke tests (analyze → generate → save/export)

### Evaluation datasets

Curate a 50–200 sentence test set including:

- Short sentiments, long reviews, sarcastic examples, mixed sentiment, domain-specific examples
- Aspect-labeled samples for aspect sentiment evaluation

### Metrics

- **Sentiment:** accuracy, precision/recall/F1 on labeled test set
- **Generation:** qualitative human evaluation (coherence, sentiment alignment); automatic sentiment-match rate
- **Latency:** average inference time (analysis & generation)

## Privacy, ethics & limitations

- **Default behavior:** process text locally (no external API calls) unless user explicitly opts in to use remote generation APIs.
- **Explicit consent:** if the app uses a remote service (e.g., OpenAI), present an opt-in toggle and a short explanation of where text is sent.
- **Data storage:** history & exports are local by default; provide a clear delete/export mechanism.
- **Limitations:** models can misinterpret sarcasm, domain-specific phrases, and culturally loaded expressions. Add a short "Limitations" note in the UI.
- **Bias:** document model origin and known biases; allow users to report misclassifications.

## UX & product copy highlights

- **Header:** Hermes — Send. Sense. Shape.
- **Primary CTA:** Analyze sentiment
- **Generator controls:** Sentiment: [Positive / Neutral / Negative] — Length: [Short / Medium / Long] — Variations: [n]
- **Microcopy for confidence:** "Confidence estimates how sure the model is — lower values indicate ambiguity."
- **Privacy note:** "Text is processed locally by default. Toggle 'Use remote generation' to call external APIs."

## Deployment & ops

- **Local dev:** run Streamlit app, pointing to local models or mocked remote API keys
- **Containerize:** provide a Dockerfile for reproducible environments
- **Hosting:** Streamlit Cloud for light demos; use a small VPS or a cloud VM (GPU if you host heavy models)
- **Monitoring:** basic request/latency logging (respect privacy settings)

## Contribution & development guidelines

- Keep wrapper functions consistent: `analyze(text, model)` → returns `{label, score, token_importance, aspects}`
- Keep generation function signature: `generate(prompt, sentiment, length, sampling_params, n)` → returns list of generated texts + metadata
- Document prompt templates and sampling defaults in `docs/prompting.md`
- Add new models via a modular registry (config-driven)

## Example usage flows (conceptual)

### Analyze only

User pastes text → clicks Analyze → Hermes shows label, confidence, top tokens, and aspects.

### Rewrite / Flip

User clicks Generate → chooses Flip sentiment → Negative, length = short, n = 3 → Hermes returns three unique negative rewrites validated by internal sentiment checker.

### Batch & export

Upload CSV of messages → batch analyze → export CSV with labels, scores, and aspect tags.

## Deliverables (for portfolio)

- Live demo link (deployed instance)
- Short demo GIF showcasing Analyze → Generate (Flip sentiment) flow
- README.md (this file)
- `docs/` with evaluation notes and prompt templates
- Short writeup / case study: problem, approach, sample results, limitations

## License

## Contact / Maintainers

- **Project lead:** Xhinvier
- **Repo / issues:** link

# Branding

- **Style:** minimalist, dark-themed
- **Palette:**
  - Jet black: #000000
  - Blackish blue (accent): #0B1F3A
  - Slate gray (secondary): #6B7280
  - Accent mint (success): #1FB67A
  - Alert coral (negative): #FF5A5F
- **Fonts:** Inter (UI), JetBrains Mono
- **Logo Idea:** small anvil + speech bubble outline
