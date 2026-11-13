# HHS Healthcare Breach Analysis

A Python script that analyzes about 8,000 healthcare data breaches reported to the U.S. Department of Health and Human Services (HHS). I built it to learn pandas and matplotlib, and to practice asking business questions about security data: how often breaches happen, how big they get, and where most of the harm comes from.

## Data

Source: the HHS Office for Civil Rights Breach Portal, which lists breaches of unsecured protected health information affecting 500 or more people.

https://ocrportal.hhs.gov/ocr/breach/breach_report.jsf

I exported two tables as CSV files:

* **Archive** (`breaches_archive.csv`): closed cases, 7,361 rows
* **Active investigations** (`breaches_active.csv`): recent cases still open, 724 rows

After combining them and removing 2 exact duplicate rows, the dataset has **8,083 breach reports**.

## What the script does

1. **Loads** both CSV files with `pd.read_csv`
2. **Renames** two columns that exported with garbled Java component names (the HHS site leaks these into the headers, and the hash at the end is different for each export)
3. **Converts** the submission date from text to a real date with `pd.to_datetime`, then pulls out the year with `.dt.year`
4. **Plots** breaches per year for the archive and for the active table separately
5. **Combines** the two tables with `pd.concat` and removes exact duplicate rows with `drop_duplicates`
6. **Plots** breaches per year for the combined data
7. **Summarizes** breach size with `describe`, median, and mean
8. **Groups** breaches by type, by hacking versus other causes, and by whether a vendor was involved, using `groupby` with count, median, and sum
9. **Finds** the 10 largest breaches with `nlargest`
10. **Plots** total people affected by hacking versus other breach types
11. **Counts** breaches per state with `value_counts`

## Charts the script produces

* Breaches per year, archive only
* Breaches per year, active only
* Breaches per year, archive and active combined
* Total individuals affected, hacking versus not hacking

## Findings

**1. Reported breaches grew a lot over time.**
Reports rose from about 200 per year in 2010 to over 700 per year from 2021 to 2024. The archive table alone shows a drop in 2025 and 2026, but that is a data gap. Recent breaches are still in the active investigations table, so both tables are needed for a fair picture. Some of the growth may also reflect more reporting, not only more attacks.

**2. A typical breach is small, but a few are enormous.**
The median breach affected about 4,000 people. The mean is about 137,000, roughly 34 times larger, because a few giant breaches pull it up. The largest, Change Healthcare in 2024, affected 192.7 million people.

**3. Hacking causes most of the harm.**
Hacking and IT incidents were about 60% of breaches but about 91% of all individuals affected.

| | Breaches | Median size | Total affected |
|---|---|---|---|
| Hacking involved | 4,892 | 8,105 | about 1.01 billion |
| Not hacking | 3,190 | 1,866 | about 96 million |

Breach types are stored as comma separated text, so a report can list several types at once. I flagged any report whose type includes the word "Hacking" as a hacking breach, even when it also lists other types.

**4. Vendor breaches are fewer, but their worst cases are far bigger.**
The "Business Associate Present" column says whether a vendor handling data for a provider or insurer was involved in the breach.

| | Breaches | Median size | Total affected |
|---|---|---|---|
| Vendor involved | 2,421 | 4,479 | about 616 million |
| No vendor | 5,661 | 3,861 | about 493 million |

Vendor breaches were about 30% of incidents but about 56% of people affected. The typical sizes are close, so the difference comes from the tail: five incidents (Change Healthcare, Conduent, Welltok, Optum360, and HCA Healthcare) make up nearly half of the vendor total. This is third party risk showing up in the data, since one vendor often holds records for many organizations.

**5. The ten largest breaches**

| Organization | Individuals affected | Year |
|---|---|---|
| Change Healthcare, Inc. | 192,700,000 | 2024 |
| Anthem Inc. | 78,800,000 | 2015 |
| Conduent Business Services LLC | 62,224,658 | 2025 |
| DentaQuest, LLC | 15,000,000 | 2026 |
| Welltok, Inc. | 14,782,887 | 2023 |
| Aflac Incorporated | 13,924,906 | 2025 |
| Kaiser Foundation Health Plan, Inc. | 13,400,000 | 2024 |
| Optum360, LLC | 11,500,000 | 2019 |
| HCA Healthcare | 11,270,000 | 2023 |
| Premera Blue Cross | 11,000,000 | 2015 |

Nine of the ten involved hacking.

**6. Breaches by state follow population.**
The top five states by number of reports are California (791), Texas (659), New York (523), Florida (478), and Illinois (365). Raw counts mostly reflect state size, so a per person comparison would be a fairer next step.

## Limitations

* HHS only lists breaches affecting 500 or more people, so smaller incidents are missing and many reports sit right at 500 or 501.
* Totals count people per report. Someone affected by several breaches is counted more than once, so these are exposures, not unique people.
* One incident can be filed as several reports, so a row count is not always an incident count. I only removed rows that were identical in every column.
* The "Business Associate Present" flag means a vendor was involved in the breach. It does not mean the reporting organization is itself a vendor.
* A few columns have missing values (21 states, 5 entity types, 1 breach type, 1 breach size). Pandas skips these in calculations.

## How to run it

1. Install Python with pandas and matplotlib (I used Spyder through Anaconda)
2. Export the archive and active tables from the HHS portal and save them as `breaches_archive.csv` and `breaches_active.csv` in the same folder as `analysis.py`
3. Check the garbled column names in each file. If they differ from the ones in the script's `rename` steps, update them to match
4. Run `analysis.py`. Results print to the console and the charts appear in the plots pane

## Next steps

* Calculate breaches per million residents by joining state population data
* Match breaches to known vulnerability data from the National Vulnerability Database
* Add a simple risk model that estimates expected loss in dollars
* Turn the repeated cleaning steps for each file into one function

## Tools

Python, pandas, matplotlib
