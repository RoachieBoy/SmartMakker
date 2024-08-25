import argparse
import json
import os

from data_collector.data_io.input_config_parser import load_parse_input_config
from data_collector.backends.collector_pipeline import build_pipeline, run_pipeline
from data_collector.data_io.data_writer import save_to_csv


def main():
    parser = argparse.ArgumentParser(prog="data_scraper", description="CLI lyrics scraper system")
    run_configuration = None

    parser.add_argument(
        "-o",
        "--output",
        help="Specify the output folder path for the scraped lyrics"
    )
    parser.add_argument(
        "-c",
        "--config_path",
        help="Specify the path to the configuration file you want to use for the scraper"
    )

    args = parser.parse_args()

    if args.output:
        print("Output folder: " + args.output)

    if args.config_path:
        config_path = args.config_path

        if not os.path.exists(config_path):
            print("Error: Config file does not exist at the specified path.")

        if not config_path.endswith(".json"):
            print("Error: Config file is not a JSON file.")

        try:
            run_configuration = load_parse_input_config(config_path)
        except json.JSONDecodeError:
            print("Error: Config file is not valid JSON.")

        print("Config file path: " + config_path)

    build_pipeline(run_configuration)

    text_container = run_pipeline()

    save_to_csv(text_container, f"{args.output}/lyrics.csv")


if __name__ == "__main__":
    main()
