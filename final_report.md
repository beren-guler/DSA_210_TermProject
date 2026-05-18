# Final Report: Manhwa Visual Evolution & Success Analysis (2022–2026)

**Author:** Beren Guler  
**Date:** May 2026

---

## 1. Motivation

The manhwa industry has grown into a global phenomenon, with titles distributed through platforms such as Webtoons, Tapas, and catalogued on MyAnimeList (MAL). While narrative quality is widely accepted as the primary driver of a series' success, cover art serves as the first point of audience contact and a key signal of production quality.

This project investigates a deceptively simple question: **can the visual characteristics of a manhwa's cover art — measurable through computer vision — predict its market success?** More specifically, we test whether features such as color complexity, brightness, contrast, and edge detail correlate with MAL scores and popularity rankings.

Beyond the predictive angle, the project captures a longitudinal dimension: by comparing 2022 archive covers (Kaggle) against 2026 live covers (Jikan/MAL), we can measure how cover aesthetics have evolved over four years and whether that evolution is linked to performance.

---

## 2. Data Source

### 2.1 Raw Data Collections

| Source | Year | Platform | Description |
|---|---|---|---|
| Webtoons Dataset — victorsoeiro (Kaggle) | 2022 | Webtoons | Cover image URLs and metadata for manhwa/webtoon titles |
| Tapas Dataset — victorsoeiro (Kaggle) | 2022 | Tapas | Tapas platform title listings and metadata |
| Jikan API (MyAnimeList) | 2026 | MAL | Scores, rankings, popularity, and current cover images |

The 2022 baseline data was sourced from two publicly available Kaggle datasets published by **Victor Soeiro (victorsoeiro)**. These are used strictly for academic research purposes.

### 2.2 Data Collection Pipeline

The data collection process (Notebook `01_data_collection.ipynb`) proceeded in four stages:

1. **Platform Merging:** The two Kaggle datasets (Webtoons: 734 titles; Tapas: 737 titles) were combined using fuzzy string matching (`fuzz.token_sort_ratio`, threshold ≥ 90) to eliminate cross-platform duplicates. The result was a master list of 1,469 unique titles.

2. **API Enrichment via Jikan:** Each title was queried against the Jikan API (the unofficial MyAnimeList API) using a cache-first architecture to minimize redundant requests. A fuzzy confidence threshold of 80% was applied before accepting a match. Rate limiting (1.2-second delays, 30-second cooldown on HTTP 429) ensured ethical scraping. Of the 1,469 titles, **723 were successfully matched** (49.2% success rate); the remaining 746 were either not present in MAL's manhwa database or failed the confidence threshold.

3. **Cover Image Download:** For all 723 matched titles, cover images from both the 2022 (Kaggle CDN) and 2026 (Jikan/MAL) sources were downloaded locally. All 723 titles yielded successful downloads for both time points (100% coverage in the final research dataset).

4. **Top 200 Benchmark Dataset:** An independent dataset of the current Top 200 highest-ranked manhwa on MAL was fetched directly from the Jikan `/top/manga?type=manhwa` endpoint across 8 pages (25 results per page), with covers downloaded separately.

### 2.3 Final Research Dataset

The primary dataset (`data/final_manhwa_research_data.csv`) contains **723 titles** with **23 columns**:

- **Identifiers & MAL Metadata:** `title`, `url_2022`, `url_2026`, `score`, `rank`, `popularity`
- **2022 Visual Features** (extracted via OpenCV): saturation, brightness, contrast RMS, edge density, color entropy
- **2026 Visual Features** (extracted via OpenCV): same five metrics
- **Longitudinal Difference Metrics:** Δ edge, Δ saturation, Δ brightness, Δ entropy (2026 − 2022)
- **Cover Change Flag:** `cover_changed` — True for **714 titles (98.8%)**, indicating nearly universal cover art updates over four years

Of the 723 titles, **556 have valid MAL scores** (mean: 7.12, range: 5.4–9.06). The remaining 167 titles exist in the MAL database but have not accumulated enough user ratings for a published score.

---

## 3. Data Analysis

### 3.1 Visual Feature Extraction (OpenCV)

Five aesthetic metrics were engineered from each cover image using OpenCV (`02_data_analysis.ipynb`):

| Feature | Method | What It Measures |
|---|---|---|
| `saturation_mean` | HSV S-channel mean | Color vibrancy |
| `brightness_mean` | HSV V-channel mean | Tonal lightness |
| `contrast_rms` | Grayscale standard deviation | Light/dark range |
| `edge_density` | Canny edge detection (% edge pixels) | Line complexity / detail |
| `color_entropy` | Grayscale histogram entropy (base-2) | Palette randomness / complexity |

Features were extracted for both the 2022 and 2026 cover versions of each title, yielding a 10-dimensional visual profile per title plus four longitudinal difference metrics.

### 3.2 Exploratory Data Analysis

**Cover Change Detection:** A multi-metric threshold approach was used to flag covers as changed if any of the four difference metrics crossed an empirically determined threshold (Δedge > 0.8%, Δsaturation > 5, Δbrightness > 5, Δentropy > 0.1). 714 out of 723 titles (98.8%) were flagged as changed, confirming near-universal redesign activity across the four-year period.

**Composite Aesthetic Quality Index (AQI):** The five 2026 visual features were standardized (mean = 0, std = 1) and summed into a single composite AQI score. Titles were then divided into three equal tertiles (Low, Medium, High AQI groups) for group-level comparison.

**Top 200 vs. General Population:** The 723-title dataset was cross-referenced with the independently fetched Top 200 MAL rankings. 67 titles appeared in both datasets, enabling elite-vs-general comparisons across all visual features using KDE plots and statistical tests.

### 3.3 Hypothesis Testing

**Hypothesis:**
- **H₀:** There is no significant correlation between a manhwa's AQI and its market success metrics.
- **H₁:** Manhwas with a High-Energy visual profile — defined by high Color Entropy and optimal Saturation/Contrast balance — achieve significantly higher scores and better popularity ranks.

**ANOVA (Notebook 02):** A one-way ANOVA on MAL scores across the three AQI tertile groups yielded **F-statistic significant at p = 0.0001**, confirming that visual group membership is associated with meaningful score differences. H₀ is rejected.

**Tukey HSD Post-hoc (Notebook 03):** The ANOVA identified that the High AQI group scores significantly higher than the Low group (mean difference = +0.224, p = 0.0004). High vs. Medium did not differ significantly, suggesting the effect is concentrated at the extremes.

**Mann-Whitney U Tests (Notebook 03):** Non-parametric pairwise tests confirmed that Top 200 titles are statistically distinct from the general population on **Color Entropy** (p = 0.009) and near-significantly on Edge Density (p = 0.171). Top 200 titles have on average 5.5% lower Color Entropy and 7.6% lower Edge Density.

### 3.4 Multivariate OLS Regression

An Ordinary Least Squares regression was run with MAL score as the dependent variable and the five 2026 visual features as predictors:

| Feature | Coefficient | p-value | Significant? |
|---|---|---|---|
| Color Entropy | −0.1214 | < 0.0001 | Yes |
| Contrast RMS | +0.0062 | 0.001 | Yes |
| Edge Density | −0.0104 | 0.184 | No |
| Saturation Mean | −0.0004 | 0.601 | No |
| Brightness Mean | +0.0005 | 0.458 | No |

**R² = 0.063** — visual features explain approximately 6.3% of score variance. The model is statistically significant overall (F-statistic p = 1.03e-06).

### 3.5 Spearman Correlation Analysis (Notebook 03)

Non-parametric Spearman correlations between the five visual features and success metrics (score, popularity, rank, Top 200 membership) confirmed:

- **Color Entropy** has the strongest association with score: r = −0.212 (the stronger the color randomness, the lower the score)
- **Contrast RMS** is the only feature with a consistently positive correlation to score: r = +0.084
- Saturation, Brightness, and Edge Density showed weak and mixed associations

### 3.6 K-Means Clustering

The five standardized 2026 features were used to cluster titles into **4 visual style groups** (K-Means, k=4). Tukey HSD on cluster membership vs. score identified one significant pair: Cluster 2 vs. Cluster 3 (mean difference = −0.313, p = 0.0001), confirming that visually distinct style segments do not perform uniformly in the market.

### 3.7 Machine Learning — Random Forest Classifier and Regressor (Notebook 03)

Two tree-based models were trained:

**Classifier (Top 200 vs. General):** A Random Forest Classifier (300 trees, max_depth=6, class_weight='balanced') trained on the five visual features achieved a 5-fold stratified cross-validation **ROC-AUC of 0.5596 ± 0.1242** on the full 723-title dataset. This is above chance but weak, consistent with the low R² from OLS.

**Regressor (Score Prediction):** A Random Forest Regressor trained on the 556-title scored subset produced **feature importance rankings** showing Color Entropy (≈24.9%) and Contrast RMS (≈21.3%) as the two dominant drivers of predicted score — corroborating the OLS findings.

### 3.8 Longitudinal Difference Analysis

All four Δ metrics (change in edge density, saturation, brightness, and entropy from 2022 to 2026) were significantly correlated with MAL score via Spearman correlation:

| Δ Feature | Spearman r | p-value |
|---|---|---|
| Δ Color Entropy | +0.1482 | 0.0005 |
| Δ Edge Density | +0.1252 | 0.0031 |
| Δ Brightness | +0.0951 | 0.0249 |
| Δ Saturation | +0.0898 | 0.0342 |

Titles that increased their visual complexity between 2022 and 2026 tend to have higher scores — an apparent contradiction to the cross-sectional finding that low entropy predicts higher scores. The most likely interpretation is reverse causality: popular titles attract investment in richer, more elaborate cover redesigns, rather than increased complexity causing higher scores.

---

## 4. Findings

### 4.1 The Visual Paradox

The central and most surprising finding of the project is what we term the **Visual Paradox**: contrary to the initial hypothesis that higher visual complexity leads to higher scores, the data reveals the opposite.

- **Color Entropy is a negative predictor of success.** Titles with a high number of random, disorganized colors in their cover art tend to score *lower* on MAL (r = −0.212, p < 0.0001; OLS coefficient = −0.1214). Top 200 elite titles exhibit on average 5.5% lower Color Entropy than the general population (p = 0.009). Successful titles favor **refined, cohesive color palettes** over visual noise.

- **Contrast RMS is a positive predictor.** Sharp, high-contrast cover art is the only visual feature consistently associated with *higher* scores (OLS coefficient = +0.0062, p = 0.001). High contrast is linked to perceived professional polish and strong visual impact.

- **Edge Density (detail) does not significantly predict success.** More intricate line art does not translate to better market performance once other features are controlled for.

### 4.2 Industry Visual Standards

Top 200 titles show a more concentrated Aesthetic Quality Index distribution compared to the general population (confirmed via KDE plots and violin plots), suggesting the existence of implicit "visual golden ratios" adopted by elite studios — high contrast, cohesive palettes, moderate complexity.

### 4.3 Predictive Power of Cover Art

Visual features account for approximately **6.3% of score variance** (OLS R² = 0.063). This is a statistically significant but practically modest effect. The Random Forest Classifier achieves ROC-AUC ≈ 0.56, confirming that cover art alone cannot reliably classify a title as Top 200 quality. Narrative quality, fandom dynamics, genre trends, and platform algorithms account for the remaining variance.

### 4.4 Near-Universal Cover Art Evolution

98.8% of titles in the dataset changed their cover art between 2022 and 2026, indicating that cover redesign is a standard industry practice — not an exception. Titles that updated toward higher complexity scores also tended to have higher MAL scores, likely because commercial success enables investment in higher-quality cover redesigns.

### 4.5 Hypothesis Verdict

- **H₀ is rejected:** Multiple converging tests (ANOVA, Tukey HSD, Mann-Whitney U, Spearman correlations) confirm that visual features are significantly associated with market performance.
- **H₁ is partially rejected:** The hypothesis correctly predicted the importance of Saturation/Contrast balance, but incorrectly predicted the direction of Color Entropy's effect. High entropy *hurts* scores, not helps them.

---

## 5. Limitations and Future Work

### 5.1 Limitations

**Dataset Coverage:** Only 723 of 1,469 combined Kaggle titles (49.2%) could be matched to the Jikan API, and only 556 of those have MAL scores. Titles that are not present on MAL (many western Tapas webcomics, for example) are systematically excluded, creating potential platform and genre bias toward Korean manhwa with global fanbases.

**Cross-Platform URL Decay:** The 2022 cover URLs from Kaggle are hosted on third-party CDNs (Webtoons, Tapas). While all 723 URLs resolved at the time of download, these links are fragile and may break over time, making reproducibility dependent on the locally cached images.

**Temporal Confound in Longitudinal Analysis:** The 2022 covers reflect the state of the series at a single point during its early life, while the 2026 covers reflect potentially multiple redesigns. The longitudinal Δ metrics therefore capture the net cumulative change, not discrete redesign events.

**Low Explained Variance:** The OLS R² of 0.063 and RF ROC-AUC of ~0.56 confirm that cover art is a weak predictor of success. The model cannot be used for reliable recommendation or quality screening; it identifies tendencies, not rules.

**Fuzzy Matching Confidence:** The 80% similarity threshold used for Jikan API matching may introduce some false positives (incorrectly matched titles with similar names) or false negatives (valid titles rejected due to transliteration differences). Manual validation of a random sample was not performed.

**Class Imbalance:** Only 67 of 723 titles (9.3%) are in the Top 200, creating a heavily imbalanced classification problem. Despite `class_weight='balanced'`, the classifier achieved near-zero recall for the Top 200 class on the test set.

### 5.2 Future Work

**Richer Feature Engineering:** The current five OpenCV metrics capture low-level pixel statistics. Future work could incorporate deep learning-based features (e.g., CNN embeddings from a pre-trained ResNet or CLIP) to capture semantic and compositional elements — character placement, background complexity, typography style — that human viewers respond to intuitively but that raw pixel statistics miss.

**Genre-Stratified Analysis:** Aesthetic preferences likely differ significantly by genre (e.g., fantasy vs. romance vs. horror). Running the same analysis within genre subgroups could reveal genre-specific visual formulas rather than a single universal optimum.

**Platform-Specific Modeling:** This project aggregates across Webtoons and Tapas, which have different demographic audiences. Platform-stratified models could determine whether the Visual Paradox holds equally across both, or whether one platform rewards higher-entropy designs.

**Granular Temporal Tracking:** Rather than comparing two snapshots (2022 vs. 2026), future work could track covers at quarterly intervals to model the exact timing of redesigns relative to score trajectory — testing whether redesigns precede or follow score inflection points.

**Multimodal Success Prediction:** Combining visual features with textual features (synopsis sentiment, genre tags, author history) and social features (update frequency, community engagement) in a unified model would likely yield much higher predictive power than visual features alone.

**Reader Perception Study:** A survey-based study asking readers to rate covers on subjective qualities (professionalism, appeal, genre clarity) and correlating those ratings with the objective OpenCV metrics would help validate whether the measured features actually align with how humans perceive cover quality.
