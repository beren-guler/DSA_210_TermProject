# Manhwa Visual Evolution & Success Analysis (2022-2026)

A Data Science project exploring the relationship between **visual art characteristics** (extracted via Computer Vision) and the **market success** (Scores & Popularity) of Manhwa titles.

## 📌 Project Overview
This project investigates whether a Manhwa’s cover art—specifically its color profile, complexity, and contrast—can predict its success on platforms like MyAnimeList (MAL). We leverage data from 2022 (Kaggle) and 2026 (Jikan API/MAL) to analyze visual shifts and aesthetic trends.

## 🛠️ Tech Stack
* **Data Collection:** Kaggle (2022 baseline — Webtoons & Tapas datasets by victorsoeiro), Jikan API (MAL), Python `requests`, JSON processing.
* **Image Processing:** `OpenCV` (Feature extraction: Saturation, Brightness, Contrast, Edge Density, Color Entropy).
* **Data Analysis:** `pandas`, `numpy`, `scipy` (Hypothesis Testing).
* **Visualization:** `matplotlib`, `seaborn` (KDE Plots, Box Plots, Regression Plots).
* **Machine Learning:** `scikit-learn` (K-Means Clustering, Random Forest), `statsmodels` (Multivariate OLS Regression).

## 📊 Key Research Findings
Contrary to the initial hypothesis that "more detail = more success," our statistical models revealed a **"Visual Paradox"**:
* **Color Cohesion over Complexity:** High **Color Entropy** (too many random colors) negatively correlates with scores ($p < 0.0001$). Successful titles favor refined, cohesive palettes.
* **The Contrast Factor:** **Contrast RMS** is a significant positive predictor. Sharpness and visual punch are more valued than sheer detail.
* **Industry Standards:** Top 200 titles show a much more concentrated "Aesthetic Index," suggesting that elite studios follow specific visual "Golden Ratios."

## 🔬 Methodology & Machine Learning
### 1. Feature Extraction (Computer Vision)
We used OpenCV to analyze cover images and calculate:
* **Edge Density:** Amount of visual detail/line work.
* **Color Entropy:** Complexity of the color distribution.
* **Contrast & Brightness:** Lighting and tonal range.

### 2. Statistical Testing
* **ANOVA ($p=0.0001$):** Confirmed significant differences in MAL score across visual style groups (Low / Medium / High AQI).
* **Tukey HSD Post-hoc:** Identified that the High AQI group scores significantly higher than the Low group (Δ=+0.224, $p=0.0004$); High vs. Medium did not differ.
* **Mann-Whitney U:** Non-parametric test confirming Top 200 titles are statistically distinct on Color Entropy ($p=0.009$) — no normality assumption required.
* **Spearman Correlation:** Non-parametric correlation between all visual features and success metrics (score, popularity, rank, Top 200 membership).
* **Multivariate OLS Regression:** Quantified the impact of each visual metric on MAL scores ($R^2 = 0.063$).

### 3. Machine Learning (Ensemble)
* **Random Forest Classifier** (300 trees, `class_weight='balanced'`, 80/20 stratified split + 5-fold Stratified K-Fold CV): Predicts Top 200 membership from visual features. ROC-AUC: 0.5596 ± 0.1242.
* **Random Forest Regressor** (300 trees): Predicts MAL score; **Feature Importance** reveals Color Entropy (24.9%) and Contrast RMS (21.3%) as dominant predictors.
* **K-Means Clustering:** Segmented the dataset into 4 distinct visual style groups; Tukey HSD confirmed Cluster 2 vs. 3 differs significantly ($p=0.0001$).

## 📂 Dataset

### Sources
| Source | Year | Description |
|--------|------|-------------|
| [Webtoons Dataset – victorsoeiro (Kaggle)](https://www.kaggle.com/datasets/victorsoeiro/webtoons-dataset) | 2022 | Cover image URLs and metadata for manhwa/webtoon titles |
| [Tapas Dataset – victorsoeiro (Kaggle)](https://www.kaggle.com/datasets/victorsoeiro/tapas-webtoons) | 2022 | Tapas platform title listings and metadata |
| Jikan API (MyAnimeList) | 2026 | Updated scores, rankings, popularity, and current cover images |

### Data Attribution
The 2022 baseline data used in this project comes from two Kaggle datasets published by **[Victor Soeiro (victorsoeiro)](https://www.kaggle.com/victorsoeiro)**:

- **Webtoons Dataset** — [kaggle.com/datasets/victorsoeiro/webtoons-dataset](https://www.kaggle.com/datasets/victorsoeiro/webtoons-dataset)
  Used for Webtoon platform 2022 cover image archive and manhwa metadata baseline (`data/webtoon_data.csv`).
- **Tapas × Webtoons Dataset** — [kaggle.com/datasets/victorsoeiro/tapas-webtoons](https://www.kaggle.com/datasets/victorsoeiro/tapas-webtoons)
  Used for Tapas platform 2022 cover image archive and manhwa metadata baseline (`data/tapas_data.csv`).

All credit for the original 2022 data collection goes to the dataset author. These datasets are used here strictly for academic research purposes.

### Main Research Dataset (`data/final_manhwa_research_data.csv`)
The primary dataset contains **723 manhwa titles** matched across both time periods, with **23 columns** covering:

- **Identifiers & Metadata:** `title`, `url_2022`, `url_2026`, `score`, `rank`, `popularity`
- **2022 Visual Features** (extracted via OpenCV from Kaggle covers):
  - `v2022_saturation_mean`, `v2022_brightness_mean`, `v2022_contrast_rms`, `v2022_edge_density`, `v2022_color_entropy`
- **2026 Visual Features** (extracted via OpenCV from MAL/Jikan covers):
  - `v2026_saturation_mean`, `v2026_brightness_mean`, `v2026_contrast_rms`, `v2026_edge_density`, `v2026_color_entropy`
- **Longitudinal Difference Metrics:** `diff_edge`, `diff_sat`, `diff_bright`, `diff_entropy` (2026 − 2022 changes)
- **Cover Change Flag:** `cover_changed` — `True` for 714 titles (~98.8%) whose cover art changed between 2022 and 2026

Of the 723 titles, **556** have valid MAL scores (mean: **7.12**, range: 5.4–9.06).

### Top 200 Elite Dataset (`data/top_200_research/json/top_200_metadata.json`)
A separate curated set of the **top 200 highest-ranked manhwa** on MAL (as of 2026), used as a benchmark group in the analysis. Contains `title`, `rank`, `popularity`, `score`, and `cover_url`.

### Supplementary Data
- `data/webtoon_data.csv` — Additional Webtoon platform listings
- `data/tapas_data.csv` — Additional Tapas platform listings
- `data/broken_links_2022.csv` — Titles excluded due to invalid 2022 image URLs
- `data/missing_from_jikan.csv` — Titles not found in the 2026 Jikan API lookup

## 📁 File Structure
* `01_data_collection.ipynb`: API calls, fuzzy matching, data merging, and cover image downloading.
* `02_data_analysis.ipynb`: EDA, feature engineering (AQI composite), ANOVA, OLS regression, K-Means clustering, and hypothesis testing.
* `03_machine_learning.ipynb`: Random Forest Classifier & Regressor, Spearman correlation heatmap, Mann-Whitney U tests, Tukey HSD post-hoc analysis, feature importance, and longitudinal diff analysis.
* `data/`: Contains raw JSONs, processed CSVs, and image metadata.
* `requirements.txt`: List of necessary Python libraries.

## 🤖 AI Collaboration & Methodology

### 1. Conceptual Framework & Hypothesis Design
* **Consultancy:** AI was used to brainstorm and refine the "Visual Paradox" hypothesis, moving from simple correlations to complex multivariate models.
* **Metric Selection:** Claude provided guidance on which OpenCV metrics (Entropy, RMS Contrast, etc.) would be most relevant for a longitudinal study on manhwa aesthetics.

### 2. Code Architecture & Technical Implementation
* **OpenCV Integration:** Guidance was provided on the mathematical implementation of image processing filters (e.g., Canny edge detection for density, Laplacian for contrast).
* **Library Integration:** Technical support for environment management (`venv`) and library installations (`scikit-learn`, `statsmodels`).

### 3. Code Quality
* **Refactoring:** AI was used to optimize Python code, ensuring adherence to PEP 8 standards.

## 🚀 Getting Started

To run this project locally, follow these steps to set up your environment:

### 1. Clone the repository
```bash
git clone https://github.com/beren-guler/DSA_210_TermProject.git
cd DSA_210_TermProject
```
### 2.Set up a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```
### 3. Install Dependencies

```bash 
pip install -r requirements.txt
```

## ⚠️ Limitations
* **Dataset Coverage:** Only 723 of 1,469 combined Kaggle titles (49.2%) were successfully matched to the Jikan API; the remaining 746 are excluded, creating potential platform and genre bias toward Korean manhwa with global fanbases.
* **Low Explained Variance:** Visual features account for only ~6.3% of score variance (OLS R²=0.063, RF ROC-AUC≈0.56). Cover art is a signal, not a determinant — narrative quality, fandom, and platform algorithms dominate.
* **Class Imbalance:** Only 67 of 723 titles (9.3%) are in the Top 200. Despite `class_weight='balanced'`, the classifier achieved near-zero recall for the Top 200 class on the test set.
* **Temporal Confound:** The 2022→2026 Δ metrics capture net cumulative change, not discrete redesign events. The positive correlation between Δ entropy and score likely reflects reverse causality (popular titles attract richer redesigns), not causation.
* **URL Decay:** 2022 cover URLs are hosted on third-party CDNs (Webtoons, Tapas) and may break over time, making reproducibility dependent on locally cached images.
* **Fuzzy Matching Confidence:** The 80% similarity threshold for Jikan API matching may introduce false positives or miss valid titles due to transliteration differences.

## 👨‍💻 Author
**Beren Guler** *Data Science & Analysis Project - 2026*