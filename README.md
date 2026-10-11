# Healthcare-SLA-Analytics
Healthcare ticket analysis using Python, Pandas, and Power BI to evaluate SLA compliance, escalations, and support performance.

## Project Overview

An end-to-end data analytics project focused on healthcare support tickets, Service Level Agreement (SLA) compliance, resolution performance, escalations, and root-cause analysis. Built using Python, Pandas, and Power BI to identify operational bottlenecks and support data-driven decision-making.

## Dashboard Preview

<img width="605" height="338" alt="dashboard" src="https://github.com/user-attachments/assets/6eeae7cc-ec29-4490-9438-753bfb53a140" />


## Business Problem

Healthcare support teams handle tickets across Enrollment, Eligibility, Claims, Provider Support, and Member Services. Meeting SLA targets is essential to resolve issues quickly and deliver effective service.

This project investigates three key business questions:

1. What percentage of support tickets meet or breach their SLA targets?
2. Which ticket priorities and operational patterns are associated with higher breach rates?
3. What are the main reported causes of SLA breaches, and where can processes improve?

## Dataset

- **Source:** Synthetic dataset generated with ChatGPT for learning and portfolio purposes.
- **Records analyzed:** 49,999 valid tickets after cleaning.
- **Date range:** January 2025 - October 2026.
- **Key fields:** Ticket priority, support team, root cause, escalation status, resolution time, customer satisfaction score, and SLA status.

The dataset represents simulated healthcare support operations and is not presented as real patient or customer data.

## Tools & Technologies

- **Python:** Data inspection and analysis.
- **Pandas:** Data cleaning, transformation, filtering, and exploratory data analysis.
- **Power BI:** Interactive dashboard development and KPI visualization.
- **Excel:** Supporting data review, if applicable.

## Project Objectives

- Measure SLA compliance and breach rates.
- Analyze ticket resolution times and escalation patterns.
- Identify operational factors associated with SLA breaches.
- Compare SLA performance across ticket priorities, teams, and root causes.
- Build a dashboard that communicates key findings and supports business decisions.

## Project Workflow

1. **Data inspection:** Loaded the dataset into Python using Pandas and reviewed its structure and data quality.
2. **Data cleaning:** Prepared the dataset for analysis and checked record validity. Specific cleaning operations should be documented according to the steps actually performed.
3. **Exploratory data analysis:** Examined ticket patterns across priority, support team, root cause, escalation status, and time.
4. **KPI calculation:** Analyzed SLA compliance, SLA breach rate, average resolution time, and average customer satisfaction.
5. **Performance analysis:** Compared breach rates across relevant operational categories to identify areas requiring attention.
6. **Dashboard development:** Built a Power BI dashboard featuring KPI cards and visualizations for SLA performance, priorities, teams, root causes, monthly trends, and escalation status.

## Key Performance Indicators

| Metric | Reported Value |
|---|---:|
| Total valid tickets | 49,999 |
| SLA compliance rate | 91.61% |
| SLA breach rate | 8.39% |
| Average resolution time | 19.89 hours |
| Average customer satisfaction | 3.74 |


## Key Findings

- **Critical-priority tickets:** The reported SLA breach rate is 95.33%, substantially higher than the reported 10.14% for High-priority tickets.
- **Escalation patterns:** Escalated tickets have a reported breach rate of 44.09%, compared with 2.96% for non-escalated tickets.
- **Root causes:** Process Delay and Customer Response Delay have reported breach rates of 15.01% and 10.97%, respectively.
- **Team performance:** The analysis indicates that breach rates across the five support teams are relatively close to the overall rate.
- **Root-cause data quality:** Some breached tickets have an Unknown root cause, highlighting an opportunity to improve issue classification and reporting.

These findings describe patterns in the synthetic dataset and should not be interpreted as actual healthcare industry benchmarks.

## Business Recommendations

Based on the reported findings, the following actions could help improve operational performance:

1. **Review Critical-ticket handling:** Investigate routing, prioritization, staffing, and escalation procedures for Critical-priority tickets.
2. **Reduce process delays:** Map ticket handoffs and identify stages where requests remain pending.
3. **Improve customer follow-ups:** Use reminders and structured follow-up procedures when tickets are awaiting customer information.
4. **Review escalation workflows:** Investigate why escalated tickets are associated with higher breach rates and identify opportunities for earlier intervention.
5. **Strengthen root-cause classification:** Encourage consistent root-cause tagging for breached tickets to improve future analysis.
6. **Monitor performance regularly:** Track SLA compliance and breach rates over time to evaluate whether corrective actions are effective.

## Power BI Dashboard

The dashboard provides a consolidated view of healthcare support ticket performance through KPI cards and visualizations covering:

- SLA breach rate by priority.
- SLA breach rate by support team.
- SLA breach rate by root cause.
- Monthly SLA breach trends.
- SLA status distribution.
- SLA breach rate by escalation status.

The dashboard is designed to help users identify performance gaps, compare operational categories, and focus attention on areas that may require improvement.

## Repository Files

| File | Description |
|---|---|
| `healthcare_SLA_analysis.py` | Python script for data inspection and analysis |
| `healthcare_ticket_sla_raw.csv` | Synthetic dataset used for the analysis |
| `dashboard.png` | Power BI dashboard screenshot displayed in this README |
| `Healthcare Ticket SLA Performance.pbix` | Power BI report file, if uploaded |


## Author

**Monica Subramaniam**

[LinkedIn Profile](https://www.linkedin.com/in/monica-subramaniam-2a3006398)

**Project focus:** Data Analytics | Python | Pandas | Power BI | SLA Performance Analysis
