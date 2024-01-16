from utils.management import create_superuser


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2 and sys.argv[1] != create_superuser:
        print("Usage: python manage.py createsuperuser")
        sys.exit(1)
    create_superuser.manage_create_superuser()
