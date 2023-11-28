"""Make README.md file from content."""

import argparse
import frontmatter
from pathlib import Path
import yaml
import util


def main():
    """Main driver."""
    args = parse_args()
    config = util.load_config(args.config)
    content = util.collect_files(config, "markdown")
    with open(args.outfile, "w") as writer:
        print(f"# {config.title}", file=writer)

        for path, chapter in list(content.items())[1:]:
            slug = Path(path).parent.stem
            doc = frontmatter.loads(chapter)
            if "tag" not in doc:
                continue
            print(
                f"""\n<h2 id="{config.slug}-{slug}">{doc["title"]}</h2>""", file=writer
            )
            print(f'*{doc["tag"]}*', file=writer)
            for point in doc["syllabus"]:
                print(f"- {point}", file=writer)

        print("\n", file=writer)
        with open(args.links) as reader:
            links = yaml.safe_load(reader)
            for lnk in links:
                print(f'[{lnk["key"]}]: {lnk["url"]}', file=writer)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="config file")
    parser.add_argument("--links", type=str, required=True, help="links file")
    parser.add_argument("--outfile", type=str, required=True, help="output file")
    return parser.parse_args()


if __name__ == "__main__":
    main()
