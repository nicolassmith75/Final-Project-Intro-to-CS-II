#Grabbed imports and main() from a previous assignment
import sys
from PyQt6.QtWidgets import QApplication
from logic import Logic


def main():
    """
    Starts the Voting App
    """
    app = QApplication(sys.argv)
    window = Logic()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
