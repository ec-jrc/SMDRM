import json
import libdrm.datamodels
import libdrm.nicelogging


def iter_from_json_file(path):
    with open(path) as _file:
        for json_line in _file:
            yield json.loads(json_line)


def iter_lines_to_parse(lines):
    for line in lines:
        if "tweet" in line:
            # internal data holding the raw tweet inside "tweet" field
            line = line["tweet"]
        yield {key: value for key, value in line.items() if key in required_fields}


def save(path, parsed_lines):
    console.info("parsing {}".format(path))
    path = path.replace(".json", "_parsed.json")
    with open(path, mode="w") as out:
        for line in parsed_lines:
            console.debug(line)
            out.write(json.dumps(line)+"\n")
    console.info("saved to {}".format(path))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Parse file content to comply to SMDRM data model."
    )
    parser.add_argument("-p", "--path", required=True, help="The full path to the file to parse.")
    parser.add_argument("-d", "--debug", action="store_true", default=False, help="Enables debugging.")
    args = parser.parse_args()

    level = "info" if not args.debug else "debug"
    console = libdrm.nicelogging.console_logger("file_parser", level=level.upper())
    # the required fields to filter parsed lines against
    required_fields = libdrm.datamodels.disaster.DisasterModel.get_required_fields()
    # make parsing pipeline
    parsing_pipeline = iter_lines_to_parse(iter_from_json_file(args.path))
    # save to new file (*_parsed.*) in the same directory
    save(args.path, parsing_pipeline)
