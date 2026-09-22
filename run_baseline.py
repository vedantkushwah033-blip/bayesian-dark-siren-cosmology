"""Run the baseline calibration experiment."""
from src.experiments import run_repeated

if __name__ == "__main__":
    result=run_repeated(n_runs=100, completeness=1.0, missingness="complete", host_generation="uniform")
    print(result)
