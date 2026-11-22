# Manhwa Cover Art & Reader Reception (2022–2026)

A data science project asking a reader's question: **is there anything measurable about a manhwa's cover art that relates to how well the title is received?** I extracted simple visual features from 723 manhwa covers with OpenCV and tested how they relate to MyAnimeList (MAL) scores, popularity and Top 200 membership.

**Short answer:** a few visual features are *statistically significantly* but only *weakly* associated with scores. Covers with a more concentrated tonal distribution (lower histogram entropy) and higher contrast tend to score slightly higher, and visual complexity does not help. Together, cover features explain only about 6% of score variance, so cover art is at most a small signal next to story, fandom and platform effects. The results are correlational and do not establish cause and effect (see Limitations).

## 📌 Research Questions
1. Do visual features of cover art (tonal entropy, contrast, saturation, brightness, edge density) relate to MAL score and popularity?
2. Do Top 200 titles look visually different from the rest?
3. How did covers change between 2022 and 2026, and is that change related to score?

## 📊 Key Findings
| Finding | Evidence | Strength |
|---|---|---|
| Higher **tonal entropy** goes with lower scores | OLS coef = −0.121, p < 0.0001; Spearman r = −0.21 | Significant, weak |
| Higher **RMS contrast** goes with higher scores, holding other features constant | OLS coef = +0.006, p = 0.001; Spearman r = +0.08 | Significant, very weak |
| Top 200 titles have lower tonal entropy | Mann-Whitney U, p = 0.009 (−5.5%) | Significant, small difference |
| Saturation, brightness, edge density | OLS p > 0.18 | No clear relationship |
| All five features together | OLS R² = 0.063 | Explain ~6% of score variance |
| Predicting Top 200 membership from cover features | Random Forest ROC-AUC = 0.56 ± 0.12; recall for Top 200 ≈ 0 | Close to chance |

The direction of the effect went *against* my initial hypothesis that more visually complex, "high-energy" covers would perform better. Simpler, more tonally concentrated covers tended to score slightly higher.

## ⚠️ Limitations
* **Weak effects:** Visual features explain only ~6.3% of score variance (OLS R² = 0.063), and the classifier is close to chance (ROC-AUC ≈ 0.56). Statistical significance here reflects sample size, not a large effect.
* **Correlation, not causation:** Popular titles may get redesigned covers (reverse causality). The positive correlation between 2022→2026 visual change and score most likely reflects this, not covers driving success.
* **"Color entropy" is grayscale entropy:** The entropy feature is computed on the grayscale histogram, so it measures *tonal* spread, not color palette diversity. A true color-palette measure (e.g. entropy over a hue or quantized RGB histogram) would be a better test of the "cohesive palette" interpretation.
* **Composite index:** The "Aesthetic Index" sums five standardized features with equal weights, even though they relate to score in opposite directions (entropy −, contrast +). The tertile ANOVA on this index (p = 0.0001; Low index group scored ~0.22 higher than High, Tukey p = 0.0004) is therefore hard to interpret, and the per-feature OLS results are the more meaningful ones.
* **Dataset coverage:** Only 723 of 1,469 combined Kaggle titles (49.2%) were matched to the Jikan API, biasing the sample towards manhwa with global fanbases. 556 have MAL scores.
* **Class imbalance:** Only 67 of 723 titles (9.3%) are in the Top 200; despite `class_weight='balanced'`, the classifier never predicted the Top 200 class on the test set.
* **Fuzzy matching:** The 80% similarity threshold may introduce false matches or miss titles with different transliterations.
* **URL decay:** 2022 cover URLs are on third-party CDNs and may break, so reproducibility depends on cached images.

## 🔬 Methodology
### 1. Data
| Source | Year | Description |
|---|---|---|
| [Webtoons Dataset – victorsoeiro (Kaggle)](https://www.kaggle.com/datasets/victorsoeiro/webtoons-dataset) | 2022 | Cover image URLs and metadata |
| [Tapas Dataset – victorsoeiro (Kaggle)](https://www.kaggle.com/datasets/victorsoeiro/tapas-webtoons) | 2022 | Tapas title listings and metadata |
| Jikan API (MyAnimeList) | 2026 | Scores, rankings, popularity and current cover images |

The two Kaggle datasets were merged with fuzzy matching (1,469 unique titles) and enriched through the Jikan API with a cache-first, rate-limited client, giving **723 matched titles** with covers from both 2022 and 2026.

### 2. Visual Features (OpenCV)
| Feature | Computation | What it captures |
|---|---|---|
| `saturation_mean` | Mean of HSV S-channel | Color vibrancy |
| `brightness_mean` | Mean of HSV V-channel | Overall lightness |
| `contrast_rms` | Standard deviation of grayscale intensities | Light/dark spread |
| `edge_density` | % of pixels detected by Canny (after Gaussian blur) | Line work / detail |
| `color_entropy` | Shannon entropy (base 2) of the 256-bin grayscale histogram | Tonal spread (not hue diversity) |

### 3. Analysis
* **OLS regression** of MAL score on the five 2026 features (n = 556).
* **Spearman correlations** between features and score, popularity, rank and Top 200 membership.
* **Mann-Whitney U** tests comparing Top 200 vs. other titles on each feature.
* **K-Means (k = 4)** on standardized features to find visual style groups, followed by Tukey HSD on score (one significant pair: clusters 2 vs. 3, p = 0.0001).
* **Random Forest** classifier (Top 200 membership) and regressor (score), 300 trees, stratified 5-fold CV.
* **Longitudinal comparison** of 2022 vs. 2026 features (98.8% of covers changed).

## 📁 File Structure
* `01_data_collection.ipynb`: API calls, fuzzy matching, data merging, cover downloads and feature extraction.
* `02_data_analysis.ipynb`: EDA, composite index, ANOVA, OLS regression, K-Means clustering.
* `03_machine_learning.ipynb`: Random Forest models, Spearman correlations, Mann-Whitney U, Tukey HSD, feature importance and longitudinal analysis.
* `final_report.md`: Full write-up.
* `data/`: Raw JSONs, processed CSVs and image metadata.
* `requirements.txt`: Python dependencies.

## 🛠️ Tech Stack
Python · `requests` · `thefuzz` · OpenCV · pandas · NumPy · SciPy · statsmodels · scikit-learn · matplotlib · seaborn

## 🤖 AI Use
I used AI assistants (Claude) during this project for brainstorming the hypothesis, suggesting candidate OpenCV metrics, explaining image-processing and statistical methods, debugging and refactoring code. The research question and the choice of data sources are my own.

## 🚀 Getting Started
```bash
git clone https://github.com/beren-guler/DSA_210_TermProject.git
cd DSA_210_TermProject
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📚 Data Attribution
The 2022 baseline data comes from two Kaggle datasets by **[Victor Soeiro](https://www.kaggle.com/victorsoeiro)**: the [Webtoons Dataset](https://www.kaggle.com/datasets/victorsoeiro/webtoons-dataset) and the [Tapas × Webtoons Dataset](https://www.kaggle.com/datasets/victorsoeiro/tapas-webtoons). All credit for the original data collection goes to the dataset author; the data is used here for academic purposes only.

## Author
**Beren Güler**, DSA 210 Introduction to Data Science term project, Sabancı University, 2026
