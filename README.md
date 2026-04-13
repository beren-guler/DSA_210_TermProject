# Manhwa Visual Evolution & Success Analysis (2022-2026)

A Data Science project exploring the relationship between **visual art characteristics** (extracted via Computer Vision) and the **market success** (Scores & Popularity) of Manhwa titles.

## 📌 Project Overview
This project investigates whether a Manhwa’s cover art—specifically its color profile, complexity, and contrast—can predict its success on platforms like MyAnimeList (MAL). We leverage data from 2022 (Kaggle) and 2026 (Jikan API/MAL) to analyze visual shifts and aesthetic trends.

## 🛠️ Tech Stack
* **Data Collection:** Jikan API (MAL), Python `requests`, JSON processing.
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
* **ANOVA ($p=0.0001$):** Confirmed significant differences between visual style groups.
* **Multivariate Regression:** Quantified the impact of each visual metric on MAL scores ($R^2 = 0.063$).

### 3. Clustering & Importance
* **K-Means Clustering:** Segmented the dataset into 4 distinct "Visual Styles."
* **Random Forest Regressor:** Determined **Feature Importance** to identify which artistic traits are the strongest predictors of success.

## 📁 File Structure
* `01_data_collection.ipynb`: API calls, Data merging, and Image processing.
* `02_data_analysis.ipynb`: EDA, Hypothesis testing, and ML modeling.
* `data/`: Contains raw JSONs, processed CSVs, and image metadata.
* `requirements.txt`: List of necessary Python libraries.

## 🤖 AI Collaboration & Methodology
This project was developed with the strategic support of **Gemini (AI)**, acting as a technical consultant and data science architect. The collaboration was structured around the following pillars:

### 1. Conceptual Framework & Hypothesis Design
* **Consultancy:** AI was used to brainstorm and refine the "Visual Paradox" hypothesis, moving from simple correlations to complex multivariate models.
* **Metric Selection:** Gemini provided guidance on which OpenCV metrics (Entropy, RMS Contrast, etc.) would be most relevant for a longitudinal study on manhwa aesthetics.

### 2. Code Architecture & Technical Implementation
* **OpenCV Integration:** Guidance was provided on the mathematical implementation of image processing filters (e.g., Canny edge detection for density, Laplacian for contrast).
* **Library Integration:** Technical support for environment management (`venv`) and library installations (`scikit-learn`, `statsmodels`).

### 3. Statistical Analysis & Interpretation
* **Model Selection:** AI advised on the use of **Random Forest Regressors** for feature importance and **OLS Regression** for statistical significance.


### 4. Code Quality & Best Practices
* **Refactoring:** AI was used to optimize Python code, ensuring adherence to PEP 8 standards and professional documentation (English comments and Markdown structure).
* **Troubleshooting:** Real-time debugging support for data merging issues.

## 🚀 Getting Started

To run this project locally, follow these steps to set up your environment:

### 1. Clone the repository
```bash
git clone [https://github.com/beren-guler/DSA_210_TermProject.git]
cd [DSA_210_TermProject]
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
* **Platform Sync:** MAL covers may not always reflect the absolute latest art update.
* **Sample Bias:** Focuses on titles available in both 2022 and 2026 datasets.

## 👨‍💻 Author
**Beren Guler** *Data Science & Analysis Project - 2026*