from utils.environment_check import check_environment, format_environment_report


def main():
    report = check_environment()
    print(format_environment_report(report))

    if not report["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
