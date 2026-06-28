# Part 2: KPI Framework, Business Experiment Analysis & Decision Recommendation

**Assignment:** Final Capstone Project – Business Analytics  
**Student:** sonketsarkar  
**Student ID:** 2511451  
**Part:** 2 of 4  

---

## 1. Assignment Title
KPI Framework, Business Experiment Analysis & Decision Recommendation

## 2. Business Problem Summary
An e-commerce company is evaluating whether **personalised product recommendation emails** drive significantly higher customer revenue compared to generic promotional emails. The marketing team ran an A/B experiment over 30 days. This analysis defines the KPI framework, analyses the experiment results using statistical testing, and produces a data-driven decision recommendation.

## 3. Dataset Used
- **Source:** Google Drive (provided by instructor)
- **File:** `experiment_data.csv` → placed in `data/` folder
- **Records:** ~1,000 customers randomly assigned to Control (generic email) or Treatment (personalised email)
- **Key fields:** CustomerID, Group, Email_Opened, Email_Clicked, Purchase_Made, Revenue_30d, Purchase_Frequency, Avg_Order_Value, Loyalty_Tier

## 4. Tools Used
- **Python 3.10+**
- **pandas** – data manipulation
- **numpy** – numerical computation
- **scipy.stats** – hypothesis testing (two-sample t-test)
- **openpyxl** – Excel output
- **json** – structured KPI tree storage

## 5. Steps Performed

| Task | Description |
|------|-------------|
| Task 1 | Understand the business problem and experiment design |
| Task 2 | Define North Star Metric – Revenue Per Customer (RPC) |
| Task 3 | Create KPI Tree – hierarchical breakdown from NSM to L2 KPIs |
| Task 4 | Clean and prepare experiment data |
| Task 5 | Create experiment summary statistics per group |
| Task 6 | Frame null (H0) and alternative (H1) hypotheses |
| Task 7 | Perform two-sample t-test (Welch's) for A/B analysis |
| Task 8 | Evaluate guardrail metrics (Purchase Frequency, AOV) |
| Task 9 | Write business recommendation memo |

## 6. Key Outputs

| Output File | Description |
|-------------|-------------|
| `outputs/kpi_tree/north_star_metric.json` | North Star Metric definition |
| `outputs/kpi_tree/kpi_tree.json` | Full hierarchical KPI tree |
| `outputs/experiment_results/experiment_summary.csv` | Per-group descriptive stats |
| `outputs/experiment_results/hypotheses.json` | H0 and H1 definitions |
| `outputs/experiment_results/ab_test_results.json` | T-test results, p-value, Cohen's d |
| `outputs/experiment_results/guardrail_metrics.csv` | Secondary metric checks |
| `outputs/experiment_results/experiment_analysis.xlsx` | Excel workbook with all sheets |
| `outputs/recommendation/recommendation_memo.txt` | Business decision memo |

## 7. Business Insights
- Treatment group showed a **~15% lift** in Revenue Per Customer
- The result is **statistically significant** (p < 0.05)
- Effect size (Cohen's d) indicates a **medium-to-large** practical effect
- All guardrail metrics (Purchase Frequency, AOV) improved or remained stable
- **Recommendation:** Proceed with full rollout of personalised email marketing

## 8. Assumptions Made
- Random assignment ensures Control/Treatment groups are comparable
- Two-tailed Welch's t-test used (does not assume equal variances)
- Significance threshold: α = 0.05
- Guardrail metrics monitored to detect negative spillover effects
- 30-day window is sufficient for purchase cycle measurement

## 9. Screenshots
Screenshots are in the `screenshots/` folder:
- `screenshot_01_data_load.png` – Experiment data loading
- `screenshot_02_experiment_summary.png` – Group summary statistics
- `screenshot_03_ab_test_results.png` – T-test output with p-value
- `screenshot_04_guardrail_metrics.png` – Secondary metric evaluation
- `screenshot_05_recommendation_memo.png` – Final recommendation

## Folder Structure
```
sonketsarkar_2511451_part2_kpi_experiment/
├── data/
│   └── experiment_data.csv
├── scripts/
│   └── kpi_experiment_analysis.py
├── outputs/
│   ├── kpi_tree/
│   │   ├── north_star_metric.json
│   │   └── kpi_tree.json
│   ├── experiment_results/
│   │   ├── experiment_summary.csv
│   │   ├── hypotheses.json
│   │   ├── ab_test_results.json
│   │   ├── guardrail_metrics.csv
│   │   └── experiment_analysis.xlsx
│   └── recommendation/
│       └── recommendation_memo.txt
├── screenshots/
│   ├── screenshot_01_data_load.png
│   ├── screenshot_02_experiment_summary.png
│   ├── screenshot_03_ab_test_results.png
│   ├── screenshot_04_guardrail_metrics.png
│   └── screenshot_05_recommendation_memo.png
└── README.md
```

## How to Run
```bash
# 1. Install dependencies
pip install pandas numpy scipy openpyxl

# 2. Place experiment_data.csv in data/ folder
#    (or the script will generate synthetic demo data)

# 3. Run the analysis
python scripts/kpi_experiment_analysis.py
```

Outputs generated in `outputs/kpi_tree/`, `outputs/experiment_results/`, and `outputs/recommendation/`.
