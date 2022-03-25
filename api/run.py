from apiv1 import create_app

app = create_app()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="""SMDRM API manager."""
    )
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host IP address. Default is %(default)s."
    )
    parser.add_argument(
        "--port", default=5000, help="Host port. Default is %(default)s."
    )
    parser.add_argument(
        "--debug", action="store_true", default=False,
        help="Enables runtime debug mode to reload app at every file change. Default is %(default)s."
    )
    args = parser.parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)
