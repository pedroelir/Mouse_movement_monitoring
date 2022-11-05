"""Modue that loops monitoring the position of the mouse (runs MouseApp)."""
from KMI.apps.mouse_app import MouseApp
from KMI.utils.logger_conf import create_logger


def main() -> None:
    """Run Main function."""
    create_logger()
    mapp = MouseApp()
    mapp.run()


if __name__ == "__main__":
    main()
