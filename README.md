# Zeitreihenanalyse Reuss in Andermatt – CAMELS-CH

## Fragestellung

Ziel dieses Projekts ist es, **den Wasserstand der Reuss bei Andermatt im Rahmen einer Zeitreihenanalyse vorherzusagen**. Die Analyse basiert auf den hydrometeorologischen Zeitreihen und statischen Einzugsgebietsmerkmalen aus dem CAMELS-CH Datensatz ([zenodo.org/records/15025258](https://zenodo.org/records/15025258)).

Wir wollen herausfinden, welche meteorologischen Faktoren und vergangene Wasserstände besonders relevant für die Prognose sind und wie genau sich der Wasserstand modellieren lässt.

### Leitfragen

- Wie gut ist der Wasserstand der Reuss in Andermatt explizit aus den beobachteten Zeitreihendaten vorhersagbar?
- Welche Faktoren (z. B. Niederschlag, Temperatur) sind die wichtigsten Einflussgrößen?
- Welche statistischen Verfahren eignen sich für die Prognose im hydrologischen Kontext?

## Datenbasis

- **CAMELS-CH Datensatz**: Enthält tägliche Zeitreihen zu Abfluss, Wasserstand, Niederschlag, Temperatur und weitere meteorologische sowie statische Einzugsgebietsvariablen für 331 Einzugsgebiete in der Schweiz (und angrenzende Regionen).
- **Untersuchungsgebiet Reuss (Andermatt)**: Auswahl und Analyse der Zeitreihen speziell für das Einzugsgebiet an der Reuss bei Andermatt.


## Zielsetzung

- Entwicklung eines Vorhersagemodells für den Wasserstand der Reuss in Andermatt
- Ableitung hydrologisch relevanter Einflussgrössen
- Dokumentation der Analyseschritte und Ergebnisse

## Installation und Anforderungen

- Python 3.10+ empfohlen
- Installiere Abhängigkeiten (siehe `requirements.txt`):

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Bei Problemen mit `pyextremes` kann es nötig sein, zusätzliche Systembibliotheken oder eine neuere/weniger neue Version zu installieren.

## Projektstruktur (Kurzüberblick)

- `data/` – Eingelesene und vorbereitete Datensätze (timeseries, prediction, usw.)
- `notebooks/` – Jupyter Notebooks mit Arbeitsschritten:
  - `1_data_selection.ipynb` – Datenimport und Auswahl
  - `2_zerlegung.ipynb` – Zerlegung in Trend / Saison / Residuen
  - `2.1_monthly_data.ipynb` – Monatsaggregation und Zusatzanalysen
  - `3_analyse.ipynb` – Explorative Analyse und Feature-Auswahl
  - `4_vorhersage.ipynb` – Modellierung, Vorhersage und Extremwert-Analyse
- `requirements.txt` – Python-Abhängigkeiten

## Schnellstart (Notebooks lokal ausführen)

1. Virtuelle Umgebung aktivieren und Abhängigkeiten installieren (siehe oben).
2. Jupyter starten:

```powershell
jupyter lab
```

3. Öffne `notebooks/4_vorhersage.ipynb` und führe die Zellen schrittweise aus. Achte auf Zellen mit EVA/`pyextremes` (Extremwert-Analyse) – hier können Versionsabhängigkeiten Warnungen erzeugen.

## Hinweise zur Extremwert-Analyse (EVA)

- In den Notebooks wird sowohl die Block-Maxima (BM) Methode als auch POT (Peaks Over Threshold) verwendet.
- Für POT ist die Generalized Pareto Distribution (`genpareto`) nach dem Pickands–Balkema–de Haan-Theorem zu bevorzugen; bei Problemen fällt das Notebook auf `genextreme` zurück.
- Bei stark korrelierten oder getaggten Extremwerten ist ein Declustering-Schritt nötig; die verwendete `pyextremes`-Version bestimmt, ob das automatisch unterstützt wird.

## Verwendete Methoden in den Notebooks

Kurzüberblick über die wichtigsten Methodiken, die in den Notebooks zur Zeitreihenanalyse angewendet werden:

- Allgemeine Datenvorverarbeitung:
  - Datumsparsing und `DatetimeIndex`-Setzung (`pd.to_datetime`, `set_index('date')`).
  - Frequenzanpassung (`asfreq('D')`), `dropna()` und einfache Imputations-/Filter-Schritte.
  - Resampling/Aggregation (z. B. Monatsaggregation in `2.1_monthly_data.ipynb`).

- Zerlegung (Notebooks `2_zerlegung.ipynb`, `2.1_monthly_data.ipynb`):
  - Zerlegung der Zeitreihe in Trend / Saisonalität / Residuen (z. B. additive Zerlegung / STL-Ansatz).
  - Erstellung saisonaler Lookup-Tabellen (durchschnittliche Saisonalität pro Tag des Jahres).

- Explorative Analyse (`3_analyse.ipynb`):
  - Visualisierung der Zeitreihen (Trend, Season, Residuen), Autokorrelationen (ACF/PACF), Heatmaps und Korrelationsmatrizen.
  - Prüfung auf fehlende Werte, Deskriptive Statistiken und einfache Feature-Auswahl.

- Modellierung und Vorhersage (`4_vorhersage.ipynb`):
  - Trendmodellierung: Lineare Regression auf Zeit (z. B. Tage seit Start) mit `sklearn.linear_model.LinearRegression`.
  - Saisonalität: Periodische Regressionsansätze (Polynom auf `day_of_year`) oder Lookup-basierte Saisonalität.
  - Residuenmodellierung: AR(p)-Modelle mit `statsmodels.tsa.ar_model.AutoReg` (Lag-Auswahl mittels ACF/PACF), manuelle rolling-/iterative Vorhersagen.
  - Zusammensetzung der Vorhersage: Addition von Trend + Saisonalität + Residuen-Reconstruction.
  - Machine-Learning-Modelle: `RandomForestRegressor` zur Vorhersage des Wasserstands aus anderen Variablen (Feature-Importances zur Interpretation).

- Extremwert-Analyse (EVA):
  - Block-Maxima (BM) Methode und Peaks-Over-Threshold (POT) mit dem `pyextremes`-Paket.
  - POT-Fit standardmäßig mit der Generalized Pareto Distribution (`genpareto` / GPD); diagnostische QQ-/Diagnostic-Plots, Return-Period-Analysen.
  - Declustering/Threshold-Auswahl und Vergleich BM vs POT als Best-Practice-Schritte.

- Evaluation:
  - Fehlerkennzahlen: MAE, RMSE, R²; grafische Vergleiche Original vs. Forecast.

Die Notebooks enthalten konkrete Implementierungen und Beispiele zu diesen Punkten; bei Bedarf kann ich einzelne Methoden in separaten, kommentierten Zellen ausführlicher dokumentieren.

## Branching Workflow

Wir verwenden **GitHub Flow**:

- `main` — stabiler Branch, immer lauffähig. Direkte Commits sind gesperrt.
- `feature/<name>` — ein Branch pro Feature oder Notebook-Abschnitt (z. B. `feature/vorhersage-model`)
- `fix/<name>` — für Bugfixes

**Ablauf:**
1. `git checkout -b feature/dein-feature`
2. Lokal entwickeln und committen
3. Branch pushen und Pull Request auf GitHub öffnen
4. Mindestens ein Teammitglied reviewed und approved
5. Merge in `main` via PR

**Beispiele für Branch-Namen:**
- `feature/extremwert-analyse`
- `feature/random-forest-tuning`
- `fix/requirements-pyextremes`

## Code Review Checkliste (Pull Requests)

Vor dem Approven eines PRs prüfen:
- [ ] Code besteht ruff-Check (keine Style-Fehler)
- [ ] Alle Unit Tests laufen durch
- [ ] Neue Funktionalität hat mindestens einen Unit Test
- [ ] Keine hardcodierten Dateipfade — relative Pfade vom Repo-Root
- [ ] Notebooks vor dem Commit geleert (`Kernel → Restart & Clear Output`)
- [ ] `requirements.txt` aktualisiert falls neue Packages hinzugefügt

## CI/CD Pipeline

Bei jedem Push und Pull Request läuft automatisch via GitHub Actions:

1. **Lint** — `ruff check tests/` prüft Python Code Style
2. **Unit Tests** — `pytest tests/ -v` führt alle Tests aus
3. **Artefakte** — Testergebnisse werden als `test-results.xml` gespeichert

Status kann unter dem **Actions** Tab auf GitHub eingesehen werden.

## Datenversionierung (DVC)

Die rohen Wasserstands-Daten (`data/wasserstand/`) sind zu gross für Git und werden mit **DVC** versioniert.

Daten herunterladen nach dem Klonen:
```bash
pip install dvc
dvc pull
```