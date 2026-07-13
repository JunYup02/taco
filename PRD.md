# PRD: Second-Hand Marketplace Scam Detector

## Problem & Goal

Generative AI has made second-hand marketplace scams more convincing (fake listings, stolen photos, scripted seller replies), and buyers still fall for them. Goal: let a buyer paste a listing and get an instant, evidence-backed fraud risk score before they contact the seller or pay.

## Target User (Persona)

"Cautious Buyer" — an individual (B2C) shopping on second-hand marketplaces (e.g., Carousell, Facebook Marketplace, Craigslist) for higher-value items (electronics, tickets, designer goods). Not a fraud expert; wants a fast yes/no signal, not a research project.

## Value — Why Ours

- Two **independent models** — a listing-text model and a seller-data model — cross-check each other, reducing false positives/negatives that a single-signal checker would miss.
- Shows *why* a listing is risky (quantified basis from both models), not just a score — builds trust and helps users learn.
- Gets smarter over time via user-submitted fraud reports, unlike static rule-based checkers.

## Must-Have Features

1. **Listing text analysis model** — paste a listing (text/URL); an NLP model trained on scam-listing patterns (pricing, phrasing, images, urgency cues) outputs a scam probability for the post itself.
2. **Seller data analysis model** — pull the seller's profile/history (account age, reviews, transaction patterns) and run a separate model to output a scammer-likelihood score for the seller.
3. **Combined verdict engine** — merges the two independent model outputs into one final fraud score/verdict, with a quantified, human-readable basis drawn from both models (e.g., "72% risk — listing model: price 40% below market + urgency language; seller model: account created 3 days ago, no review history").
4. **User-reported fraud feedback loop** — users submit confirmed scam cases; reports feed back as training data into both the listing and seller models.

## User Stories

- As a buyer, I paste a listing so the listing model can flag scam patterns in the post's text/images before I message the seller.
- As a buyer, I look up the seller so the seller model can score them independently of the listing itself.
- As a buyer, I see one combined verdict with reasons from both models so I can decide quickly without cross-checking myself.
- As a buyer, I report a confirmed scam so both underlying models improve for future users.

## Out of Scope (for v1)

- Browser extension / auto-scan while browsing marketplaces
- In-app messaging or transaction/escrow features
- Multi-language support beyond launch market
- Marketplace/seller partnerships or API integrations for verified badges
- Mobile app (web only for v1)
- Team/B2B or enterprise dashboards