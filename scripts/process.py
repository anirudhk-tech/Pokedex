import logging

from processing.graph_builder import build_graph

logging.basicConfig(level=logging.INFO)


def main():
    logging.info("Building graph with data...")
    build_graph()
    logging.info("Graph built successfully.")


if __name__ == "__main__":
    main()
