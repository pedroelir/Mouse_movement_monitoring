"""Modue that loops monitoring the position of the mouse (runs MouseApp)."""
from KMI.apps.mouse_app import MouseApp


def main() -> None:
    """Run Main function."""
    mapp = MouseApp()
    mapp.run()


if __name__ == "__main__":
    main()
