from app import create_app

app = create_app()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Floods API.")
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address.")
    parser.add_argument("--port", default=5000, help="The host port.")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debugging."
    )
    args = parser.parse_args()
    # run app
    app.run(debug=args.debug, host=args.host, port=args.port)
