# Sleep & Lifestyle Analysis

End-to-End-Data-Science-Projekt zur Analyse von Schlafqualität, Stresslevel und Lebensstilfaktoren. Das Projekt umfasst explorative Datenanalyse, Feature Engineering, Clustering, prädiktive Modellierung, Hypothesenprüfung sowie ein interaktives Dash-Dashboard.

## Projektueberblick

Das Projekt untersucht, wie Lebensstil-, Verhaltens- und physiologische Faktoren mit Schlafqualität und Stressniveau zusammenhängen. Dafür wurde ein vollständiger analytischer Workflow von der Rohdatenaufbereitung bis zur interaktiven Ergebnisdarstellung umgesetzt.

Die Analyse ist in drei aufeinander aufbauenden Jupyter Notebooks strukturiert:

| Notebook | Fokus |
|---|---|
| [`01-EDA-Hypothesenentwicklung.ipynb`](notebooks/01-EDA-Hypothesenentwicklung.ipynb) | Datenverständnis, Datenqualität, EDA und Hypothesenentwicklung |
| [`02-Feature-Engineering-Clustering-Modeling-MapReduce.ipynb`](notebooks/02-Feature-Engineering-Clustering-Modeling-MapReduce.ipynb) | Feature Engineering, Clustering, Regression und Klassifikation |
| [`03-Evaluation-Hypothesenprüfung-Dash-Deployment.ipynb`](notebooks/03-Evaluation-Hypothesenprüfung-Dash-Deployment.ipynb) | Modellevaluation, Feature Importance, Hypothesenprüfung und Dash-Deployment |

## Zielstellung

Zentrale Fragestellung des Projekts ist:

> Welche Lebensstil- und Gesundheitsfaktoren beeinflussen Schlafqualität und Stressniveau — und wie zuverlässig lassen sich diese Zielgrößen vorhersagen?

Konkrete Projektziele:

- Datenstruktur, Datenqualität und Zusammenhänge systematisch untersuchen
- Hypothesen zu Schlaf, Stress, Aktivität, Ernährung und physiologischer Belastung ableiten
- Homogene Lifestyle-Typen durch Clustering identifizieren
- Schlafqualität regressionsbasiert vorhersagen
- Hohes Stressniveau klassifikationsbasiert erkennen
- Die wichtigsten Einflussfaktoren interpretierbar aufbereiten
- Ergebnisse in einem interaktiven Dashboard zugänglich machen

## Datensatz

Verwendet wird der Datensatz **Sleep Health and Lifestyle**. Die Rohdaten liegen unter `data/sleep-health-lifestyle.csv`, der bereinigte und für die Modellierung verwendete Datensatz unter `data/data_clean.csv`.

Der bereinigte Datensatz enthält:

- **2.000 Beobachtungen**
- **15 Variablen**
- **10 numerische** und **5 kategoriale Merkmale**
- **0 fehlende Werte**
- **0 Duplikate**

Enthalten sind unter anderem Alter, Geschlecht, Familienstand, Rauchstatus, Alkoholkonsum, Zuckeraufnahme, körperliche Aktivität, tägliche Schritte, Stresslevel, Schlafdauer, Schlafqualität, Herzfrequenz, BMI-Kategorie sowie Health-Risk-Indikatoren.

## Projektstruktur

```text
sleep-lifestyle-analysis/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── sleep-health-lifestyle.csv
│   ├── data_clean.csv
│   ├── cluster_data.csv
│   ├── cluster_summary.csv
│   ├── regression_results.csv
│   ├── classification_results.csv
│   ├── model_performance_summary.csv
│   ├── cv_scores_regression.csv
│   ├── cv_scores_classification.csv
│   └── feature_importance_rf.csv
├── notebooks/
│   ├── 01-EDA-Hypothesenentwicklung.ipynb
│   ├── 02-Feature-Engineering-Clustering-Modeling-MapReduce.ipynb
│   └── 03-Evaluation-Hypothesenprüfung-Dash-Deployment.ipynb
└── outputs/
    └── figures/
```

## Installation

Voraussetzungen:

- Python 3.10 oder höher
- Jupyter Notebook oder JupyterLab

Repository klonen und virtuelle Umgebung einrichten:

```bash
git clone [https://github.com/](https://github.com/novoigt/sleep-lifestyle-analysis.git)

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

Jupyter starten:

```bash
jupyter lab
```

## Nutzung

Die Notebooks sollten in dieser Reihenfolge ausgeführt werden:

1. `01-EDA-Hypothesenentwicklung.ipynb`  
   Datenqualität, Verteilungen, Korrelationen und erste Hypothesen.

2. `02-Feature-Engineering-Clustering-Modeling-MapReduce.ipynb`  
   Feature Engineering, Multikollinearitätsprüfung, PCA, K-Means-Clustering sowie Regressions- und Klassifikationsmodelle.

3. `03-Evaluation-Hypothesenprüfung-Dash-Deployment.ipynb`  
   Modellvergleich, Cross Validation, Feature Importance, Hypothesenprüfung und Dashboard.

## Methodik

Die Analyse folgt einem reproduzierbaren Data-Science-Workflow:

1. **Datenverständnis und Datenqualität**  
   Prüfung von Datentypen, fehlenden Werten, Duplikaten, Konsistenz und Ausreißern.

2. **Explorative Datenanalyse**  
   Deskriptive Statistik, Verteilungsanalysen, Korrelationsanalysen und visuelle Untersuchung von Zusammenhängen zwischen Schlaf, Stress, Aktivität, Ernährung und physiologischen Indikatoren.

3. **Feature Engineering**  
   Ableitung modellrelevanter Merkmale, unter anderem:
   - `shortSleep`: Indikator für kurze Schlafdauer
   - `lifestyleRisk`: aggregierter Lebensstil-Risikoindikator
   - `stressSleepMismatch`: Diskrepanz zwischen Stresslevel und Schlafqualität

4. **Multikollinearitätsprüfung und Dimensionsreduktion**  
   Einsatz von VIF zur Identifikation redundanter Merkmale sowie PCA zur Strukturanalyse.

5. **Clustering**  
   K-Means-Clustering auf standardisierten Merkmalen zur Identifikation von Lifestyle-Typen. Die Clusterzahl wurde anhand von Silhouette Score und inhaltlicher Interpretierbarkeit bewertet.

6. **Prädiktive Modellierung**  
   - **Regression:** Vorhersage der Schlafqualität  
   - **Klassifikation:** Identifikation eines hohen Stresslevels  

   Eingesetzte Modellfamilien sind lineare Modelle sowie Random-Forest-Modelle. Die Modelle wurden per Train-Test-Split und Cross Validation bewertet.

7. **Evaluation und Interpretation**  
   Vergleich der Modellperformance, Analyse der Feature Importance sowie inhaltliche Einordnung der Ergebnisse.

## Zentrale Ergebnisse

- Die Datenbasis nach Bereinigung umfasst 2.000 vollständige Beobachtungen ohne fehlende Werte und Duplikate.
- Schlafqualität und Stressniveau lassen sich durch Lebensstil-, Verhaltens- und physiologische Merkmale modellieren.
- Das Random-Forest-Modell liefert für die Vorhersage der Schlafqualität die stärkste Performance und ermöglicht zusätzlich eine interpretierbare Feature-Importance-Analyse.
- Die Clusteranalyse identifiziert vier unterscheidbare Lifestyle-Typen mit unterschiedlichen Profilen hinsichtlich Aktivität, Schlaf, Stress und Risikofaktoren.
- Die wichtigsten Einflussfaktoren für die Schlafqualität sind in `data/feature_importance_rf.csv` dokumentiert.

| Aufgabe | Modell | Kennzahl | Ergebnis |
|---|---|---:|---:|
| Schlafqualität vorhersagen | Bestes Regressionsmodell | R² | `[WERT]` |
| Schlafqualität vorhersagen | Bestes Regressionsmodell | RMSE | `[WERT]` |
| Schlafqualität vorhersagen | Bestes Regressionsmodell | MAE | `[WERT]` |
| Hohen Stress klassifizieren | Bestes Klassifikationsmodell | Accuracy | `[WERT]` |
| Hohen Stress klassifizieren | Bestes Klassifikationsmodell | F1-Score | `[WERT]` |
| Hohen Stress klassifizieren | Bestes Klassifikationsmodell | ROC-AUC | `[WERT]` |

## Hypothesenpruefung

Die in der EDA formulierten Hypothesen wurden im dritten Notebook anhand der Modell- und Clusterergebnisse geprüft. Untersucht wurden insbesondere:

- Zusammenhänge zwischen Schlafdauer, BMI, körperlicher Aktivität und Stresslevel
- Unterschiede der identifizierten Lifestyle-Cluster hinsichtlich Schlafqualität und Stress
- Der Einfluss zentraler Verhaltens- und physiologischer Faktoren auf die Zielgrößen
- Die Eignung der Modelle zur zuverlässigen Vorhersage von Schlafqualität beziehungsweise hohem Stress

Die detaillierte Prüfung inklusive Visualisierungen befindet sich in  
[`03-Evaluation-Hypothesenprüfung-Dash-Deployment.ipynb`](notebooks/03-Evaluation-Hypothesenprüfung-Dash-Deployment.ipynb).

## Dashboard

Das dritte Notebook enthält die Aufbereitung der Ergebnisse für ein interaktives Dashboard. Es ermöglicht die explorative Betrachtung von:

- Modellperformance und Modellvergleich
- Feature Importance der Schlafqualitätsvorhersage
- Clusterprofilen und Lifestyle-Typen
- Zusammenhängen zwischen Stress, Schlafdauer und Schlafqualität

Lokale Ausführung:

```bash
python app.py
```

Anschließend ist das Dashboard im Browser unter folgender Adresse verfügbar:

```text
http://127.0.0.1:8050/
```

## Limitationen

- Der Datensatz ist beobachtungsbezogen und erlaubt keine kausalen Aussagen.
- Die Stichprobe umfasst 2.000 Personen und ist möglicherweise nicht repräsentativ für die Allgemeinbevölkerung.
- Selbstberichtete Variablen wie Stresslevel und Schlafqualität können Verzerrungen enthalten.
- Die Cluster sind datengetriebene Segmente und keine klinisch validierten Personengruppen.
- Die Modellgüte ist kontextabhängig und sollte vor einem produktiven Einsatz mit externen Daten validiert werden.

## Ausblick

Mögliche Weiterentwicklungen:

- Einsatz von Gradient-Boosting-Modellen wie XGBoost oder LightGBM
- Hyperparameter-Optimierung per Grid Search oder Optuna
- SHAP-basierte Modellinterpretation
- Zeitreihenanalyse bei Verfügbarkeit longitudinaler Schlafdaten
- Automatisierte Pipeline mit Prefect, Airflow oder GitHub Actions
- Deployment des Dashboards über Render, Hugging Face Spaces oder eine Cloud-Plattform

## Technologien

- **Python**
- **Pandas** und **NumPy** für Datenverarbeitung
- **Matplotlib**, **Seaborn** und **Plotly** für Visualisierung
- **scikit-learn** für Preprocessing, PCA, Clustering, Regression, Klassifikation und Evaluation
- **Statsmodels** für statistische Diagnostik und VIF
- **Jupyter Notebook** für reproduzierbare Analyse
- **Dash** für das interaktive Dashboard

## Autor

**Norbert Voigt**  
Data Analytics / Data Science  

## Lizenz

Dieses Projekt steht unter der [MIT License](LICENSE).
