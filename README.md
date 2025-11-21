# Gemini Geometry ReAct Agent

Jednoduchý AI agent implementujúci architektúru **ReAct (Reason and Act)** pomocou modelu Google Gemini. Agent dokáže používať nástroje na vykonávanie matematických výpočtov (konkrétne výpočet euklidovskej vzdialenosti bodov v 2D priestore).

## 📋 Funkcionalita

* **Model:** Google Gemini 2.5 Flash
* **Nástroj:** `calculate_distance` (vlastná Python funkcia pre výpočet vzdialenosti)
* **Logika:** Agent analyzuje otázku, rozhodne sa použiť nástroj, vykoná výpočet a sformuluje finálnu odpoveď.

## 🚀 Inštalácia a Spustenie

Tento projekt vyžaduje Python 3.10 alebo novší.

### 1. Príprava prostredia

Vytvorte si virtuálne prostredie a nainštalujte závislosti:

```bash
# Vytvorenie venv
python -m venv .venv

# Aktivácia (Windows)
.venv\Scripts\activate

# Aktivácia (macOS/Linux)
source .venv/bin/activate

# Inštalácia knižníc
pip install -r requirements.txt