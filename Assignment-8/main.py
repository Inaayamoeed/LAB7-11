from app.data.schema import create_tables
from services.user_migration import migrate_users_from_file
from app.services.load_csv import (
    load_cyber_incidents,
    load_datasets_metadata,
    load_it_tickets,
)
from app.data.reports import (
    get_all_cyber_incidents,
    get_high_severity_incidents,
    get_open_it_tickets,
    get_large_datasets,
)


def main():
    print("Creating tables...")
    create_tables()

    print("\nMigrating users...")
    migrate_users_from_file()

    print("\nLoading CSV files...")
    load_cyber_incidents()
    load_datasets_metadata()
    load_it_tickets()

    print("\nAll data imported successfully!")

    print("\n--- REPORTS / QUERIES ---")

    print("\nAll cyber incidents:")
    print(get_all_cyber_incidents())

    print("\nHigh or critical severity incidents:")
    print(get_high_severity_incidents())

    print("\nOpen IT tickets:")
    print(get_open_it_tickets())

    print("\nLarge datasets (size > 2000):")
    print(get_large_datasets(2000))


if __name__ == "__main__":
    main()
