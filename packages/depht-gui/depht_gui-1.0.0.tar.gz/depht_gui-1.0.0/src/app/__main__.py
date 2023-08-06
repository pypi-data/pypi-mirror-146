"""Run the app."""
import sys

from signal import signal, SIGINT

from app.flask_app import create_app


def exit_handle(sig, frame):
    """Exit when CTRL+C is pressed."""
    sys.exit(0)


def main():
    """Run the app."""
    app = create_app()

    port_range = (50000, 51000)
    for port in range(*port_range):

        signal(SIGINT, exit_handle)

        try:
            app.run(debug=True, port=port)
        except Exception:
            if port == max(port_range) - 1:
                raise RuntimeError(f"All ports in range {port_range} in use")
            # need some way to make sure it doesn't re-run
            continue


if __name__ == "__main__":
    main()
