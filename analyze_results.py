"""Summarize an executed experiment matrix without inventing results."""
import csv
from src.analysis import summarize_matrix

if __name__ == "__main__":
    with open("results/experiment_matrix.csv", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        for key in ("target_completeness","median","mean","posterior_sd","lower_68","upper_68","lower_95","upper_95","width_68","width_95","pull","missing_host_prior_mass"):
            if key in row:
                row[key] = float(row[key])
        if "host_observed" in row:
            row["host_observed"] = row["host_observed"].lower() == "true"
    summaries = summarize_matrix(rows)
    fields = sorted(summaries[0])
    with open("results/summary_matrix.csv","w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        writer.writerows(summaries)
    print(f"Wrote {len(summaries)} grouped summaries to results/summary_matrix.csv")
