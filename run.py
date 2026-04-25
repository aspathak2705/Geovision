from core.pipeline import DEFAULT_T1_PATH, DEFAULT_T2_PATH, run_analysis


def main():
    metrics = run_analysis(DEFAULT_T1_PATH, DEFAULT_T2_PATH)

    print("\nRESULTS")
    print(f"New: {metrics['new']}")
    print(f"Removed: {metrics['removed']}")
    print(f"Unchanged: {metrics['unchanged']}")
    print(f"Change %: {metrics['change_percent']:.2f}%")

    print("\nSystem Completed Successfully")


if __name__ == "__main__":
    main()
