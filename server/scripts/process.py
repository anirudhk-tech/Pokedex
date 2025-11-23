import logging

from processing.graph_builder import build_graph_and_export_to_csv_and_json

logging.basicConfig(level=logging.INFO)


def main():
    logging.info("Building graph with data...")
    build_graph_and_export_to_csv_and_json()
    logging.info("Graph built and exported to CSV and JSON successfully.")


if __name__ == "__main__":
    main()
