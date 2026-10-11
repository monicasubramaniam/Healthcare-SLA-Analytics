import pandas as pd
df=pd.read_csv("healthcare_ticket_sla_raw.csv")
print(df.head())
print(df.shape)
print(df.columns)

print(df.info())
print(df.isnull().sum())

print(df["Team"].unique())
print(df["Issue_Type"].unique())
print(df["Priority"].unique())
print(df["Channel"].unique())
print(df["SLA_Status"].unique())
print(df["Escalated"].unique())

df["Team"]=df["Team"].str.strip()
print(df["Team"].unique())

df["Priority"]=df["Priority"].str.title()
print(df["Priority"].unique())

df["Channel"]=df["Channel"].str.title()
print(df["Channel"].unique())

df["Channel"]=df["Channel"].fillna("Unknown")
df["Root_Cause"]=df["Root_Cause"].fillna("unknown")
print(df.isnull().sum())

df["Created_Date"]=pd.to_datetime(df["Created_Date"], dayfirst=True)
df["Resvoled_Date"]=pd.to_datetime(df["Resolved_Date"], dayfirst=True)
print(df[["Created_Date", "Resolved_Date"]].dtypes)

df["Resolved_Date"]=pd.to_datetime(df["Resolved_Date"], dayfirst=True)
print(df[["Created_Date", "Resolved_Date"]].dtypes)

print("Duplicate Ticket IDs:",df["Ticket_ID"].duplicated().sum())

duplicates=df[df["Ticket_ID"].duplicated(keep=False)]
print(duplicates.sort_values("Ticket_ID").head(20))
print("Exact duplicate rows:", df.duplicated().sum())



df=df.drop_duplicates()
print("Shape after removing duplicates:", df.shape)
print("Duplicates rows remaining:", df.duplicated().sum())

df=df.rename(columns={"Resvoled_Date": "Resolved_Date"})
print(df.shape)
print(df.columns.tolist())

print(df["Resolved_Date"].iloc[:,0].equals(df["Resolved_Date"].iloc[:,1]))
df["Resolved_Date"]

df=df.loc[:,~df.columns.duplicated()]
print(df.shape)
print(df.columns.tolist())

print(df["SLA_Target_Hours"].describe())

print("Negative SLA target Hours:",
      (df["SLA_Target_Hours"] < 0).sum())

print(df[df["SLA_Target_Hours"] < 0])

print(df.loc[df["SLA_Target_Hours"] < 0,
             ["Ticket_ID", "Team", "Issue_Type", "Priority",
              "SLA_Target_Hours", "Resolution_Time_Hours",
              "SLA_Status", "Root_Cause", "Escalated"]])
print(df[df["Team"] == "Member Services"]["SLA_Target_Hours"].value_counts().sort_index())

print(df.loc[df["Ticket_ID"] == "TKT10601",
             ["Ticket_ID", "Team", "Issue_Type", "Priority",
              "SLA_Target_Hours", "Resolution_Time_Hours",
              "SLA_Status"]])

print("\nSimilar tickets:")
print(
    df[
        (df["Team"] == "Member Services") &
        (df["Issue_Type"] == df.loc[df["Ticket_ID"] == "TKT10601", "Issue_Type"].iloc[0]) &
        (df["Priority"] == df.loc[df["Ticket_ID"] == "TKT10601", "Priority"].iloc[0])
    ][["Issue_Type", "Priority", "SLA_Target_Hours", "SLA_Status"]]
    .value_counts()
)
print(
    df.groupby("SLA_Status")["Resolution_Time_Hours"]
      .agg(["count", "min", "max", "mean"])
)

print("Negative Resolution Time:",
      (df["Resolution_Time_Hours"] < 0).sum())

print(
    df.loc[df["Resolution_Time_Hours"] < 0,
           ["Ticket_ID", "Created_Date", "Resolved_Date",
            "Team", "Issue_Type", "Priority",
            "SLA_Target_Hours", "Resolution_Time_Hours",
            "SLA_Status"]]
)
print(
    df.loc[df["Ticket_ID"] == "TKT10801",
           ["Ticket_ID", "Created_Date", "Resolved_Date",
            "SLA_Target_Hours", "Resolution_Time_Hours",
            "SLA_Status"]]
)
ticket = df[df["Ticket_ID"] == "TKT10801"]

print("Created Date:", ticket["Created_Date"].iloc[0])
print("Resolved Date:", ticket["Resolved_Date"].iloc[0])
print("Recorded Resolution Time:",
      ticket["Resolution_Time_Hours"].iloc[0])
df["Calculated_Resolution_Hours"] = (
    df["Resolved_Date"] - df["Created_Date"]
).dt.total_seconds() / 3600

print(
    df[["Created_Date", "Resolved_Date",
        "Resolution_Time_Hours",
        "Calculated_Resolution_Hours"]].head()
)

df["Resolution_Time_Difference"] = (
    df["Resolution_Time_Hours"]
    - df["Calculated_Resolution_Hours"]
)

print(
    df["Resolution_Time_Difference"].describe()
)
mismatches = df[
    df["Resolution_Time_Difference"].abs() > 0.1
]

print("Number of mismatches:", len(mismatches))

print(
    mismatches[
        ["Ticket_ID",
         "Created_Date",
         "Resolved_Date",
         "Resolution_Time_Hours",
         "Calculated_Resolution_Hours",
         "Resolution_Time_Difference"]
    ]
)

df.loc[df["Ticket_ID"] == "TKT10801",
       "Resolution_Time_Hours"] = df.loc[
           df["Ticket_ID"] == "TKT10801",
           "Calculated_Resolution_Hours"
       ]

print(
    df.loc[df["Ticket_ID"] == "TKT10801",
           ["Ticket_ID",
            "Resolution_Time_Hours",
            "Calculated_Resolution_Hours"]]
)

print(
    "Negative Resolution Time remaining:",
    (df["Resolution_Time_Hours"] < 0).sum()
)

print("SLA Target <= 0:",
      (df["SLA_Target_Hours"] <= 0).sum())

print(
    df[df["SLA_Target_Hours"] <= 0]
    [["Ticket_ID", "Team", "Issue_Type", "Priority",
      "SLA_Target_Hours", "Resolution_Time_Hours",
      "SLA_Status"]]
)

df["SLA_Target_Data_Quality"] = "Valid"

df.loc[
    df["SLA_Target_Hours"] <= 0,
    "SLA_Target_Data_Quality"
] = "Invalid"

print(df["SLA_Target_Data_Quality"].value_counts())

print(
    df.loc[
        df["SLA_Target_Data_Quality"] == "Invalid",
        ["Ticket_ID", "SLA_Target_Hours", "SLA_Target_Data_Quality"]
    ]
)

date_issues = df[
    df["Resolved_Date"] < df["Created_Date"]
]

print("Resolved before Created:", len(date_issues))

print(
    date_issues[
        ["Ticket_ID", "Created_Date", "Resolved_Date"]
    ]
)

df["Calculated_SLA_Status"] = "Met"

df.loc[
    df["Resolution_Time_Hours"] > df["SLA_Target_Hours"],
    "Calculated_SLA_Status"
] = "Breached"

print(
    pd.crosstab(
        df["SLA_Status"],
        df["Calculated_SLA_Status"]
    )
)
sla_mismatches = df[
    df["SLA_Status"] != df["Calculated_SLA_Status"]
]

print("SLA Status mismatches:", len(sla_mismatches))

print(
    sla_mismatches[
        ["Ticket_ID",
         "Team",
         "Issue_Type",
         "Priority",
         "SLA_Target_Hours",
         "Resolution_Time_Hours",
         "SLA_Status",
         "Calculated_SLA_Status"]
    ]
)

valid_sla = df[
    df["SLA_Target_Data_Quality"] == "Valid"
]

print(
    pd.crosstab(
        valid_sla["SLA_Status"],
        valid_sla["Calculated_SLA_Status"]
    )
)

print("Team:")
print(df["Team"].value_counts())

print("\nPriority:")
print(df["Priority"].value_counts())

print("\nChannel:")
print(df["Channel"].value_counts())

print("\nSLA Status:")
print(df["SLA_Status"].value_counts())

print("\nEscalated:")
print(df["Escalated"].value_counts())

print("SLA Target Hours:")
print(df["SLA_Target_Hours"].describe())

print("\nResolution Time Hours:")
print(df["Resolution_Time_Hours"].describe())

print("\nCustomer Satisfaction:")
print(df["Customer_Satisfaction"].describe())

print("Root Cause:")
print(df["Root_Cause"].value_counts())

df["Root_Cause"] = df["Root_Cause"].str.title()
print(df["Root_Cause"].value_counts())

valid_sla = df[
    df["SLA_Target_Data_Quality"] == "Valid"
]

total_tickets = len(valid_sla)

met_tickets = (
    valid_sla["SLA_Status"] == "Met"
).sum()

breached_tickets = (
    valid_sla["SLA_Status"] == "Breached"
).sum()

sla_compliance_rate = (
    met_tickets / total_tickets
) * 100

sla_breach_rate = (
    breached_tickets / total_tickets
) * 100

print("Total Valid Tickets:", total_tickets)
print("SLA Met:", met_tickets)
print("SLA Breached:", breached_tickets)
print("SLA Compliance Rate:", round(sla_compliance_rate, 2), "%")
print("SLA Breach Rate:", round(sla_breach_rate, 2), "%")

team_sla = (
    valid_sla
    .groupby("Team")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

team_sla["Total_Tickets"] = (
    team_sla["Met"] + team_sla["Breached"]
)

team_sla["Breach_Rate"] = (
    team_sla["Breached"]
    / team_sla["Total_Tickets"]
) * 100

team_sla = team_sla.sort_values(
    "Breach_Rate",
    ascending=False
)
print(team_sla)

priority_sla = (
    valid_sla
    .groupby("Priority")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

priority_sla["Total_Tickets"] = (
    priority_sla["Met"] + priority_sla["Breached"]
)

priority_sla["Breach_Rate"] = (
    priority_sla["Breached"]
    / priority_sla["Total_Tickets"]
) * 100

priority_sla = priority_sla.sort_values(
    "Breach_Rate",
    ascending=False
)

print(priority_sla)

issue_sla = (
    valid_sla
    .groupby("Issue_Type")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

issue_sla["Total_Tickets"] = (
    issue_sla["Met"] + issue_sla["Breached"]
)

issue_sla["Breach_Rate"] = (
    issue_sla["Breached"]
    / issue_sla["Total_Tickets"]
) * 100

issue_sla = issue_sla.sort_values(
    "Breach_Rate",
    ascending=False
)

print(issue_sla)

channel_sla = (
    valid_sla
    .groupby("Channel")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

channel_sla["Total_Tickets"] = (
    channel_sla["Met"] + channel_sla["Breached"]
)

channel_sla["Breach_Rate"] = (
    channel_sla["Breached"]
    / channel_sla["Total_Tickets"]
) * 100

channel_sla = channel_sla.sort_values(
    "Breach_Rate",
    ascending=False
)

print(channel_sla)

escalation_sla = (
    valid_sla
    .groupby("Escalated")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

escalation_sla["Total_Tickets"] = (
    escalation_sla["Met"] + escalation_sla["Breached"]
)

escalation_sla["Breach_Rate"] = (
    escalation_sla["Breached"]
    / escalation_sla["Total_Tickets"]
) * 100

print(escalation_sla)

root_cause_sla = (
    valid_sla
    .groupby("Root_Cause")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

root_cause_sla["Total_Tickets"] = (
    root_cause_sla["Met"] + root_cause_sla["Breached"]
)

root_cause_sla["Breach_Rate"] = (
    root_cause_sla["Breached"]
    / root_cause_sla["Total_Tickets"]
) * 100

root_cause_sla = root_cause_sla.sort_values(
    "Breach_Rate",
    ascending=False
)

print(root_cause_sla)

satisfaction_sla = (
    valid_sla
    .groupby("SLA_Status")["Customer_Satisfaction"]
    .agg(
        Average_Satisfaction="mean",
        Median_Satisfaction="median",
        Count="count"
    )
)

print("\n========== KPI 8: CUSTOMER SATISFACTION VS SLA ==========")
print(satisfaction_sla)

agent_performance = (
    valid_sla
    .groupby("Agent_ID")
    .agg(
        Total_Tickets=("Ticket_ID", "count"),
        Breached_Tickets=(
            "SLA_Status",
            lambda x: (x == "Breached").sum()
        ),
        Average_Resolution_Hours=(
            "Resolution_Time_Hours",
            "mean"
        ),
        Average_Satisfaction=(
            "Customer_Satisfaction",
            "mean"
        )
    )
)

agent_performance["Breach_Rate"] = (
    agent_performance["Breached_Tickets"]
    / agent_performance["Total_Tickets"]
) * 100

agent_performance = agent_performance.sort_values(
    "Breach_Rate",
    ascending=False
)

print("\n========== KPI 9: AGENT PERFORMANCE ==========")
print(agent_performance)

account_performance = (
    valid_sla
    .groupby("Account")
    .agg(
        Total_Tickets=("Ticket_ID", "count"),
        Breached_Tickets=(
            "SLA_Status",
            lambda x: (x == "Breached").sum()
        ),
        Average_Resolution_Hours=(
            "Resolution_Time_Hours",
            "mean"
        ),
        Average_Satisfaction=(
            "Customer_Satisfaction",
            "mean"
        )
    )
)

account_performance["Breach_Rate"] = (
    account_performance["Breached_Tickets"]
    / account_performance["Total_Tickets"]
) * 100

account_performance = account_performance.sort_values(
    "Breach_Rate",
    ascending=False
)

print("\n========== KPI 10: ACCOUNT PERFORMANCE ==========")
print(account_performance)

valid_sla["Month"] = valid_sla["Created_Date"].dt.to_period("M")

monthly_sla = (
    valid_sla.groupby("Month")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

monthly_sla["Total_Tickets"] = (
    monthly_sla["Met"] + monthly_sla["Breached"]
)

monthly_sla["Breach_Rate"] = (
    monthly_sla["Breached"]
    / monthly_sla["Total_Tickets"]
) * 100

monthly_sla["Compliance_Rate"] = (
    monthly_sla["Met"]
    / monthly_sla["Total_Tickets"]
) * 100

print("\n========== KPI 11: MONTHLY SLA TREND ==========")
print(monthly_sla)

priority_escalation = (
    valid_sla
    .groupby(["Priority", "Escalated"])["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

priority_escalation["Total_Tickets"] = (
    priority_escalation["Met"]
    + priority_escalation["Breached"]
)

priority_escalation["Breach_Rate"] = (
    priority_escalation["Breached"]
    / priority_escalation["Total_Tickets"]
) * 100

priority_escalation = priority_escalation.sort_values(
    "Breach_Rate",
    ascending=False
)

print("\n========== KPI 12: PRIORITY + ESCALATION ==========")
print(priority_escalation)

critical_issue = (
    valid_sla[valid_sla["Priority"] == "Critical"]
    .groupby("Issue_Type")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

critical_issue["Total_Tickets"] = (
    critical_issue["Met"] +
    critical_issue["Breached"]
)

critical_issue["Breach_Rate"] = (
    critical_issue["Breached"] /
    critical_issue["Total_Tickets"]
) * 100

critical_issue = critical_issue.sort_values(
    "Breach_Rate",
    ascending=False
)

print("\n========== CRITICAL TICKETS BY ISSUE TYPE ==========")
print(critical_issue)

priority_resolution = (
    valid_sla.groupby("Priority")
    .agg(
        Total_Tickets=("Ticket_ID", "count"),
        Average_SLA_Target_Hours=("SLA_Target_Hours", "mean"),
        Average_Resolution_Hours=("Resolution_Time_Hours", "mean"),
        Median_SLA_Target_Hours=("SLA_Target_Hours", "median"),
        Median_Resolution_Hours=("Resolution_Time_Hours", "median"),
        Breached_Tickets=("SLA_Status", lambda x: (x == "Breached").sum())
    )
)

priority_resolution["Breach_Rate"] = (
    priority_resolution["Breached_Tickets"]
    / priority_resolution["Total_Tickets"]
) * 100

print("\n========== PRIORITY: SLA TARGET VS RESOLUTION ==========")
print(priority_resolution.sort_values("Breach_Rate", ascending=False))

print(priority_resolution.to_string())

critical_escalation = (
    valid_sla[valid_sla["Priority"] == "Critical"]
    .groupby("Escalated")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

critical_escalation["Total_Tickets"] = (
    critical_escalation["Met"] +
    critical_escalation["Breached"]
)

critical_escalation["Breach_Rate"] = (
    critical_escalation["Breached"]
    / critical_escalation["Total_Tickets"]
) * 100

print("\n========== CRITICAL TICKETS: ESCALATION ANALYSIS ==========")
print(critical_escalation)

critical_root_cause = (
    valid_sla[valid_sla["Priority"] == "Critical"]
    .groupby("Root_Cause")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

critical_root_cause["Total_Tickets"] = (
    critical_root_cause["Met"] +
    critical_root_cause["Breached"]
)

critical_root_cause["Breach_Rate"] = (
    critical_root_cause["Breached"]
    / critical_root_cause["Total_Tickets"]
) * 100

critical_root_cause = critical_root_cause.sort_values(
    "Breach_Rate",
    ascending=False
)

print("\n========== CRITICAL TICKETS: ROOT CAUSE ANALYSIS ==========")
print(critical_root_cause)

critical_team = (
    valid_sla[valid_sla["Priority"] == "Critical"]
    .groupby("Team")
    .agg(
        Total_Tickets=("Ticket_ID", "count"),
        Average_SLA_Target_Hours=("SLA_Target_Hours", "mean"),
        Average_Resolution_Hours=("Resolution_Time_Hours", "mean"),
        Breached_Tickets=("SLA_Status", lambda x: (x == "Breached").sum())
    )
)

critical_team["Breach_Rate"] = (
    critical_team["Breached_Tickets"]
    / critical_team["Total_Tickets"]
) * 100

critical_team = critical_team.sort_values(
    "Breach_Rate",
    ascending=False
)

print("\n========== CRITICAL TICKETS: TEAM ANALYSIS ==========")
print(critical_team)

escalated_root_cause = (
    valid_sla[valid_sla["Escalated"] == "Yes"]
    .groupby("Root_Cause")["SLA_Status"]
    .value_counts()
    .unstack(fill_value=0)
)

escalated_root_cause["Total_Tickets"] = (
    escalated_root_cause["Met"] +
    escalated_root_cause["Breached"]
)

escalated_root_cause["Breach_Rate"] = (
    escalated_root_cause["Breached"]
    / escalated_root_cause["Total_Tickets"]
) * 100

escalated_root_cause = escalated_root_cause.sort_values(
    "Breach_Rate",
    ascending=False
)

print("\n========== ESCALATED TICKETS: ROOT CAUSE ANALYSIS ==========")
print(escalated_root_cause.to_string())

df.to_csv("healthcare_ticket_sla_cleaned.csv", index=False)
print("Cleaned CSV saved successfully!")
