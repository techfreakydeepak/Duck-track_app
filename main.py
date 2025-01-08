import os
import signal
import sys
import traceback

from PyQt6.QtWidgets import QApplication

from ducktrack import MainInterface
from ducktrack.recorder import Recorder  # Ensure Recorder is imported if used in MainInterface


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    interface = MainInterface(app)
    interface.show()

    # Fetch OBS password from environment variable or use a default value
    obs_password = os.getenv("OBS_PASSWORD", "JQd0VScSsBXpzd3T")
    interface.obs_password = obs_password  # Pass the password to the MainInterface for later use

    # Override the default exception hook to handle errors gracefully
    original_excepthook = sys.excepthook

    def handle_exception(exc_type, exc_value, exc_traceback):
        # Log the exception details
        print("Exception type:", exc_type)
        print("Exception value:", exc_value)

        trace_details = traceback.format_exception(exc_type, exc_value, exc_traceback)
        trace_string = "".join(trace_details)

        print("Exception traceback:", trace_string)

        # Display the error message using the interface
        message = f"An error occurred!\n\n{exc_value}\n\n{trace_string}"
        interface.display_error_message(message)

        # Call the original excepthook to handle logging or other processes
        original_excepthook(exc_type, exc_value, exc_traceback)

    sys.excepthook = handle_exception

    # Start the Qt application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
