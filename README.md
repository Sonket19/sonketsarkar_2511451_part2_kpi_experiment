# Part 2: KPI Framework, Business Experiment Analysis & Decision Recommendation

**Assignment:** Final Capstone Project – Business Analytics
**Student:** sonketsarkar
**Student ID:** 2511451
**Part:** 2 of 4

---

## 1. Assignment Title
KPI Framework, Business Experiment Analysis & Decision Recommendation

## 2. Business Problem Summary
A subscription product tested a new onboarding and activation campaign (Treatment) against the existing experience (Control). This analysis defines the KPI framework, runs statistical hypothesis tests on the experiment results, evaluates guardrail metrics, and produces a data-driven decision recommendation.

## 3. Dataset Used
- **Source:** Google Drive (provided by instructor)
- **File:** `campaign_experiment_data.xlsx` placed in `data/` folder
- **Records:** 1408 users (693 Control, 715 Treatment)
- **Key fields:** user_id, signup_date, experiment_group, region, device_type, traffic_source, plan_type, visited_landing_page, started_trial, completed_onboarding, converted_to_paid, revenue_30d, support_tickets_30d, refund_requested, days_to_convert, engagement_score

## 4. Tools Used
- **Python 3.9+**
- **pandas** – data manipulation
- **numpy** – numerical computation
- **scipy.stats** – hypothesis testing
- **openpyxl** – Excel output
- **json** – structured KPI storage

## 5. Steps Performed

| Task | Description |
|------|-------------|
| Task 1 | Understand business problem – subscription onboarding campaign experiment |
| Task 2 | Define North Star Metric – Conversion Rate to Paid |
| Task 3 | Create KPI Tree – hierarchical breakdown from NSM to guardrail metrics |
| Task 4 | Load and prepare experiment data – validate groups and missing values |
| Task 5 | Create experiment summary – per-group descriptive statistics |
| Task 6 | Frame hypotheses – H0 and H1 for conversion rate and revenue |
| Task 7 | Perform A/B hypothesis tests – proportion z-test and Welch t-test |
| Task 8 | Evaluate guardrail metrics – refund rate and support tickets |
| Task 9 | Write recommendation memo – launch, reject, or segment decision |

## 6. Key Outputs

| Output File | Description |
|-------------|-------------|
| `outputs/kpi_tree/north_star_metric.json` | North Star Metric definition |
| `outputs/kpi_tree/kpi_tree.json` | Full KPI tree structure |
| `outputs/experiment_results/experiment_summary.csv` | Per-group descriptive stats |
| `outputs/experiment_results/hypotheses.json` | H0 and H1 definitions |
| `outputs/experiment_results/ab_test_results.json` | Test statistics and p-values |
| `outputs/experiment_results/guardrail_metrics.csv` | Guardrail metric evaluation |
| `outputs/experiment_results/experiment_analysis.xlsx` | Full Excel workbook |
| `outputs/recommendation/recommendation_memo.txt` | Business decision memo |

## 7. Business Insights
- Conversion rate: Control 3.17% vs Treatment 6.99% — a +120% lift (p=0.0006, significant)
- Engagement score significantly higher in Treatment (62.93 vs 57.03, p<0.0001)
- Revenue difference not significant (p=0.9163)
- Guardrail FAILED — support tickets increased significantly in Treatment (0.37 vs 0.22)
- Decision: SEGMENT LAUNCH — significant lift but proceed cautiously due to guardrail concerns

## 8. Assumptions Made
- Two-proportion z-test (one-tailed) used for conversion rate as primary metric
- Welch t-test (two-tailed) used for continuous metrics
- Significance threshold alpha = 0.05
- days_to_convert is NaN for non-converters — treated as expected, not a data error
- Guardrail passes only if Treatment mean is within 10% of Control mean

## 9. Screenshots
Screenshots are in the `screenshots/` folder showing terminal output for each task.

## Folder Structure
## How to Run
```bash
pip install pandas numpy scipy openpyxl
python scripts/kpi_experiment_analysis.py
```
