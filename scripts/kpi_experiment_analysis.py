"""
Part 2: KPI Framework, Business Experiment Analysis & Decision Recommendation
Dataset: campaign_experiment_data.xlsx (1408 rows)
Business context: Subscription product tested new onboarding campaign vs existing.
Student: sonketsarkar | ID: 2511451
"""

import pandas as pd
import numpy as np
import os, json
from scipy import stats
from datetime import datetime

BASE  = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.join(BASE, '..')
DATA  = os.path.join(ROOT, 'data', 'campaign_experiment_data.xlsx')
KPI   = os.path.join(ROOT, 'outputs', 'kpi_tree')
EXP   = os.path.join(ROOT, 'outputs', 'experiment_results')
REC   = os.path.join(ROOT, 'outputs', 'recommendation')
for d in [KPI, EXP, REC]: os.makedirs(d, exist_ok=True)

# ── TASK 1: Business Problem ──────────────────────────────────────────────────
print("=" * 60)
print("Task 1: Business Problem")
print("""
A subscription product ran an A/B experiment testing a new onboarding
and activation campaign (Treatment) against the existing experience (Control).

Key Question: Does the new campaign significantly improve conversion to paid
subscription, revenue, and engagement — without harming guardrail metrics
(refunds, support tickets)?

Decision: Launch, reject, continue testing, or segment launch.
""")

# ── TASK 2: North Star Metric ─────────────────────────────────────────────────
print("Task 2: Define North Star Metric")
nsm = {
    'metric': 'Conversion Rate to Paid (converted_to_paid)',
    'definition': 'Proportion of signed-up users who became paid customers within 30 days',
    'formula': 'converted_to_paid users / total users in group',
    'why': 'Directly measures whether the new onboarding campaign achieves its primary business goal',
    'secondary_metrics': ['revenue_30d', 'engagement_score', 'completed_onboarding'],
    'guardrail_metrics': ['refund_requested', 'support_tickets_30d'],
}
with open(os.path.join(KPI, 'north_star_metric.json'), 'w') as f:
    json.dump(nsm, f, indent=4)
print(f"  North Star: {nsm['metric']}")

# ── TASK 3: KPI Tree ─────────────────────────────────────────────────────────
print("\nTask 3: Create KPI Tree")
kpi_tree = {
    'North_Star': 'Conversion Rate to Paid',
    'L1_KPIs': {
        'Activation_Rate': {
            'formula': 'completed_onboarding / total users',
            'L2': ['visited_landing_page rate', 'started_trial rate']
        },
        'Revenue_Per_User': {
            'formula': 'sum(revenue_30d) / total users',
            'L2': ['days_to_convert', 'plan_type distribution']
        },
        'Engagement_Quality': {
            'formula': 'mean(engagement_score)',
            'L2': ['device_type breakdown', 'traffic_source breakdown']
        },
    },
    'Guardrail_KPIs': {
        'Refund_Rate':        'refund_requested / converted_to_paid',
        'Support_Ticket_Rate':'mean(support_tickets_30d)',
    }
}
with open(os.path.join(KPI, 'kpi_tree.json'), 'w') as f:
    json.dump(kpi_tree, f, indent=4)
print("  KPI tree saved.")

# ── TASK 4: Load & prepare experiment data ────────────────────────────────────
print("\nTask 4: Load and prepare experiment data")
df = pd.read_excel(DATA, sheet_name='experiment_data')
print(f"  Shape: {df.shape}")
print(f"  Groups: {df['experiment_group'].value_counts().to_dict()}")
print(f"  Missing values: {df.isnull().sum()[df.isnull().sum()>0].to_dict()}")

# Clean group labels
df['experiment_group'] = df['experiment_group'].str.strip()

# days_to_convert is NaN for non-converters — correct, keep as-is
# Verify no data issues
assert df['experiment_group'].isin(['Control', 'Treatment']).all(), "Unexpected group labels"
print(f"  Data is clean. Proceeding to analysis.")

ctrl  = df[df['experiment_group'] == 'Control']
treat = df[df['experiment_group'] == 'Treatment']

# ── TASK 5: Experiment Summary ────────────────────────────────────────────────
print("\nTask 5: Experiment Summary")

metrics = ['converted_to_paid', 'revenue_30d', 'engagement_score',
           'completed_onboarding', 'started_trial', 'refund_requested',
           'support_tickets_30d']

rows = []
for m in metrics:
    for grp, sub in [('Control', ctrl), ('Treatment', treat)]:
        rows.append({
            'Metric': m, 'Group': grp, 'N': len(sub),
            'Mean': round(sub[m].mean(), 4),
            'Sum': round(sub[m].sum(), 2),
            'Std': round(sub[m].std(), 4),
        })
summary_df = pd.DataFrame(rows)
summary_df.to_csv(os.path.join(EXP, 'experiment_summary.csv'), index=False)
print(summary_df[summary_df['Metric'].isin(['converted_to_paid','revenue_30d','refund_requested'])].to_string(index=False))

# ── TASK 6: Hypotheses ───────────────────────────────────────────────────────
print("\nTask 6: Frame Hypotheses")
hypotheses = {
    'Primary': {
        'H0': 'Conversion rate to paid is the same in Control and Treatment groups.',
        'H1': 'Treatment group has a higher conversion rate to paid than Control.',
        'test': 'Two-proportion z-test (one-tailed)',
        'alpha': 0.05,
    },
    'Secondary_Revenue': {
        'H0': 'Mean revenue_30d is equal across groups.',
        'H1': 'Treatment group generates higher mean revenue_30d.',
        'test': "Welch's t-test (two-tailed)",
        'alpha': 0.05,
    }
}
with open(os.path.join(EXP, 'hypotheses.json'), 'w') as f:
    json.dump(hypotheses, f, indent=4)
print("  Hypotheses documented.")

# ── TASK 7: A/B Hypothesis Tests ─────────────────────────────────────────────
print("\nTask 7: Perform Hypothesis Tests")

# Primary: conversion rate (proportion test)
c_conv  = ctrl['converted_to_paid'].sum()
t_conv  = treat['converted_to_paid'].sum()
c_n     = len(ctrl)
t_n     = len(treat)
c_rate  = c_conv / c_n
t_rate  = t_conv / t_n
p_pool  = (c_conv + t_conv) / (c_n + t_n)
se      = np.sqrt(p_pool * (1 - p_pool) * (1/c_n + 1/t_n))
z_stat  = (t_rate - c_rate) / se
p_val_conv = 1 - stats.norm.cdf(z_stat)   # one-tailed

# Secondary: revenue t-test
t_stat_rev, p_val_rev = stats.ttest_ind(
    treat['revenue_30d'].dropna(), ctrl['revenue_30d'].dropna(), equal_var=False
)

# Engagement
t_stat_eng, p_val_eng = stats.ttest_ind(
    treat['engagement_score'].dropna(), ctrl['engagement_score'].dropna(), equal_var=False
)

ab_results = {
    'Conversion_Rate': {
        'Control_Rate':   round(c_rate, 4),
        'Treatment_Rate': round(t_rate, 4),
        'Absolute_Lift':  round(t_rate - c_rate, 4),
        'Relative_Lift_%': round((t_rate - c_rate) / c_rate * 100, 2),
        'Z_Statistic':    round(z_stat, 4),
        'P_Value':        round(p_val_conv, 6),
        'Significant_at_0.05': bool(p_val_conv < 0.05),
    },
    'Revenue_30d': {
        'Control_Mean':   round(ctrl['revenue_30d'].mean(), 4),
        'Treatment_Mean': round(treat['revenue_30d'].mean(), 4),
        'T_Statistic':    round(t_stat_rev, 4),
        'P_Value':        round(p_val_rev, 6),
        'Significant_at_0.05': bool(p_val_rev < 0.05),
    },
    'Engagement_Score': {
        'Control_Mean':   round(ctrl['engagement_score'].mean(), 4),
        'Treatment_Mean': round(treat['engagement_score'].mean(), 4),
        'T_Statistic':    round(t_stat_eng, 4),
        'P_Value':        round(p_val_eng, 6),
        'Significant_at_0.05': bool(p_val_eng < 0.05),
    }
}
with open(os.path.join(EXP, 'ab_test_results.json'), 'w') as f:
    json.dump(ab_results, f, indent=4)
print(f"  Conversion: Control={c_rate:.2%}, Treatment={t_rate:.2%}, p={p_val_conv:.4f}, Sig={p_val_conv<0.05}")
print(f"  Revenue:    Control=${ctrl['revenue_30d'].mean():.2f}, Treatment=${treat['revenue_30d'].mean():.2f}, p={p_val_rev:.4f}")
print(f"  Engagement: Control={ctrl['engagement_score'].mean():.2f}, Treatment={treat['engagement_score'].mean():.2f}, p={p_val_eng:.4f}")

# ── TASK 8: Guardrail Metrics ─────────────────────────────────────────────────
print("\nTask 8: Evaluate Guardrail Metrics")
guardrails = []
for metric in ['refund_requested', 'support_tickets_30d']:
    t_s, p_s = stats.ttest_ind(treat[metric], ctrl[metric], equal_var=False)
    guardrails.append({
        'Metric': metric,
        'Control_Mean':   round(ctrl[metric].mean(), 4),
        'Treatment_Mean': round(treat[metric].mean(), 4),
        'P_Value':        round(p_s, 4),
        'Significant':    bool(p_s < 0.05),
        'Direction':      'Up' if treat[metric].mean() > ctrl[metric].mean() else 'Down',
        'Guardrail_Pass': treat[metric].mean() <= ctrl[metric].mean() * 1.10,
    })
gdf = pd.DataFrame(guardrails)
gdf.to_csv(os.path.join(EXP, 'guardrail_metrics.csv'), index=False)
print(gdf.to_string(index=False))

# ── TASK 9: Recommendation Memo ──────────────────────────────────────────────
print("\nTask 9: Write Recommendation Memo")
sig = ab_results['Conversion_Rate']['Significant_at_0.05']
lift = ab_results['Conversion_Rate']['Relative_Lift_%']
all_guardrails_pass = all(g['Guardrail_Pass'] for g in guardrails)

if sig and all_guardrails_pass:
    decision = "LAUNCH – Roll out new campaign to all users."
elif sig and not all_guardrails_pass:
    decision = "SEGMENT LAUNCH – Significant lift but guardrail concern. Launch to low-risk segments only."
elif not sig:
    decision = "REJECT / CONTINUE TESTING – Insufficient evidence of improvement."

memo = f"""
============================================================
BUSINESS RECOMMENDATION MEMO
============================================================
Date    : {datetime.now().strftime('%Y-%m-%d')}
Subject : A/B Experiment – New Onboarding Campaign Decision
Analyst : sonketsarkar (2511451)

EXPERIMENT DESIGN
  Control   : {c_n} users | Existing onboarding experience
  Treatment : {t_n} users | New campaign experience

PRIMARY METRIC – CONVERSION TO PAID
  Control Rate   : {c_rate:.2%}
  Treatment Rate : {t_rate:.2%}
  Relative Lift  : {lift:+.2f}%
  P-value (z)    : {p_val_conv:.4f}
  Significant    : {'Yes ✅' if sig else 'No ❌'} (α = 0.05)

SECONDARY METRICS
  Revenue 30d  – Control: ${ctrl['revenue_30d'].mean():.2f} | Treatment: ${treat['revenue_30d'].mean():.2f} | p={p_val_rev:.4f}
  Engagement   – Control: {ctrl['engagement_score'].mean():.2f} | Treatment: {treat['engagement_score'].mean():.2f} | p={p_val_eng:.4f}

GUARDRAIL METRICS
  Refund Rate        – Control: {ctrl['refund_requested'].mean():.2%} | Treatment: {treat['refund_requested'].mean():.2%} | Pass: {guardrails[0]['Guardrail_Pass']}
  Support Tickets    – Control: {ctrl['support_tickets_30d'].mean():.2f} | Treatment: {treat['support_tickets_30d'].mean():.2f} | Pass: {guardrails[1]['Guardrail_Pass']}

DECISION: {decision}

RATIONALE
  {'The new campaign delivers a statistically significant improvement in conversion rate' if sig else 'The observed difference is not statistically significant.'}
  {'All guardrail metrics remain within acceptable range.' if all_guardrails_pass else 'Guardrail concern detected — proceed with caution.'}

NEXT STEPS
  1. {'Full rollout with weekly monitoring for 90 days.' if sig else 'Redesign campaign elements and re-test with larger sample.'}
  2. Segment analysis by device_type and traffic_source to optimise targeting.
  3. Monitor days_to_convert trend post-launch.
============================================================
"""
with open(os.path.join(REC, 'recommendation_memo.txt'), 'w') as f:
    f.write(memo)
print(memo)

# Excel output
with pd.ExcelWriter(os.path.join(EXP, 'experiment_analysis.xlsx'), engine='openpyxl') as w:
    df.to_excel(w, sheet_name='Experiment_Data', index=False)
    summary_df.to_excel(w, sheet_name='Summary', index=False)
    gdf.to_excel(w, sheet_name='Guardrail_Metrics', index=False)
print("✅ Part 2 complete!")
