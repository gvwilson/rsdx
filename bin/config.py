"""Get values from configuration file."""

import argparse
import yaml


def main():
    """Main driver."""
    args = parse_args()
    config = load_config(args.config)
    handlers = {
        name.replace("_get_", ""): func
        for name, func in globals().items()
    }
    handlers[args.get](config)


def _get_keys(config):
    """Get chapter keys."""
    print(" ".join([ch["key"] for ch in config["chapters"]]))


def load_config(filename):
    """Load configuration."""
    with open(filename, "r") as reader:
        return yaml.load(reader, Loader=yaml.FullLoader)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="config file")
    parser.add_argument("--get", type=str, required=True, help="what to get")
    return parser.parse_args()


if __name__ == "__main__":
    main()
