"""Analyze pollution readings."""

import argparse
import importlib
import json
from pathlib import Path

import plotly.express as px


FIG_SIZE = 600


# [main]
def main():
    """Main driver."""
    args = parse_args()
    config = json.loads(Path(args.plugins).read_text())
    tables = {}
    for plugin_stem, plugin_param in config.items():
        module = importlib.import_module(f"plugin_{plugin_stem}")
        tables[plugin_stem] = module.read_data(plugin_param)
    check(tables)
    _, values = tables.popitem()
    make_figures(args, values["combined"], values["centers"])
# [/main]


# [check]
def check(tables):
    """Check all tables against each other."""
    ref_key = None
    for key in tables:
        if ref_key is None:
            ref_key = key
            continue
        if set(tables[ref_key].keys()) != set(tables[key].keys()):
            print(f"mis-match in provided tables {ref_key} != {key}")
        else:
            for sub_key in tables[ref_key]:
                if len(tables[ref_key][sub_key]) != len(tables[key][sub_key]):
                    print(f"mis-match in {sub_key}: {ref_key} != {key}")
# [/check]


def make_figures(args, combined, centers):
    """Create figures showing calculated results."""
    for i, row in centers.iterrows():
        temp = combined[combined["site"] == row["site"]]
        title = f"{row['site']}: lon={row['lon']:.5f} lat={row['lat']:.5f}"
        fig = px.scatter(
            x=temp["lon"], y=temp["lat"], size=temp["reading"], title=title
        )
        fig.add_vline(x=row["lon"])
        fig.add_hline(y=row["lat"])
        fig.update_layout(width=FIG_SIZE, height=FIG_SIZE)
        if args.figdir:
            fig.write_image(f"{args.figdir}/{row['site']}.svg")
            fig.write_image(f"{args.figdir}/{row['site']}.pdf")
        else:
            fig.show()


# [parse_args]
def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--figdir", type=str, help="output dir")
    parser.add_argument("--plugins", type=str, required=True, help="config")
    return parser.parse_args()
# [/parse_args]


if __name__ == "__main__":
    main()
