# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:53:02 2026

@author: dom
"""

import pandas as pd
import matplotlib.pyplot as plt



##Archive Plot

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df_archive = pd.read_csv("breaches_archive.csv")

df_archive = df_archive.rename(columns={
    "javax.faces.component.UIPanel@a66c37a": "Organization",
    "javax.faces.component.UIPanel@4381c6fb": "Business Associate Present",
    
    })




df_archive["Breach Submission Date"] = pd.to_datetime(df_archive["Breach Submission Date"], format="%m/%d/%Y")
df_archive["Year"] = df_archive["Breach Submission Date"].dt.year

counts_archive = df_archive["Year"].value_counts().sort_index()
plt.figure()
counts_archive.plot(kind="bar")
plt.title("HHS Reported Breaches per Year (Archive)")
plt.xlabel("Year")
plt.ylabel("Number of Breaches")
plt.tight_layout()
plt.show()


"""
print(df_archive.shape)
print(df_archive.columns)
"""

##Active Plot




pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df_active = pd.read_csv("breaches_active.csv")

df_active = df_active.rename(columns={
    "javax.faces.component.UIPanel@52242a69": "Organization",
    "javax.faces.component.UIPanel@1a2dcbb4": "Business Associate Present",
})





df_active["Breach Submission Date"] = pd.to_datetime(df_active["Breach Submission Date"], format="%m/%d/%Y")
df_active["Year"] = df_active["Breach Submission Date"].dt.year

counts_active = df_active["Year"].value_counts().sort_index()
plt.figure()
counts_active.plot(kind="bar")
plt.title("HHS Reported Breaches per Year (Active)")
plt.xlabel("Year")
plt.ylabel("Number of Breaches")
plt.tight_layout()
plt.show()


"""
print(df_active.shape)
print(df_active.columns)
"""

##Delete duplicates
df_dupe = pd.concat([df_archive, df_active], ignore_index=True)
df_dupe = df_dupe.drop_duplicates()
print(df_dupe.shape)

df = df_dupe


counts_all = df["Year"].value_counts().sort_index()
plt.figure()
counts_all.plot(kind="bar")
plt.title("HHS Reported Breaches per Year (Archive + Active)")
plt.xlabel("Year")
plt.ylabel("Number of Breaches")
plt.tight_layout()
plt.show()

print(df["Individuals Affected"].describe())
print("Median:", df["Individuals Affected"].median())
print("Mean:", df["Individuals Affected"].mean())


print(df.groupby("Type of Breach")["Individuals Affected"].agg(["count", "median", "sum"]))


df["Hacking"] = df["Type of Breach"].str.contains("Hacking", na=False)
print(df.groupby("Hacking")["Individuals Affected"].agg(["count", "median", "sum"]))



print(df.groupby("Business Associate Present")["Individuals Affected"].agg(["count", "median", "sum"]))

top10 = df.nlargest(10, "Individuals Affected")[["Organization", "Individuals Affected", "Business Associate Present", "Type of Breach", "Year"]]
print(top10)


hack_totals = df.groupby("Hacking")["Individuals Affected"].sum() / 1_000_000
plt.figure()
hack_totals.plot(kind="bar")
plt.xticks([0, 1], ["Not hacking", "Hacking"], rotation=0)
plt.title("Total Individuals Affected by Breach Type")
plt.ylabel("People Affected (millions)")
plt.tight_layout()
plt.show()


top10States = (df["State"].value_counts().head(10))
print(top10States)



##Check for duplicates


##dupes = df.duplicated(subset=["Organization", "Breach Submission Date", "Individuals Affected"]).sum()
##print("Possible duplicate rows:", dupes)
##dupe_rows = df[df.duplicated(subset=["Organization", "Breach Submission Date", "Individuals Affected"], keep=False)]
##print(dupe_rows.sort_values("Organization"))
##print(dupe_rows[["Organization", "Breach Submission Date", "Individuals Affected", "Type of Breach"]].sort_values("Organization"))
