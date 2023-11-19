"""Check configuration."""

import argparse
from bs4 import BeautifulSoup, Tag
from collections import defaultdict
import hashlib
from pathlib import Path
import re
import shortcodes
import yaml

import util
import regex


ARK_FILE = ".ark"
SVG_FONT = "Helvetica:12px"
SVG_FONT_PAT = {
    "font-family": re.compile(r"\bfont-family:\s*(.+?);"),
    "font-size": re.compile(r"\bfont-size:\s*(.+?);"),
}
SVG_MAX_WIDTH = 640


def main():
    """Main driver."""
    args = parse_args()
    config = util.load_config(args.config)
    content = collect_content(config)
    for name, func in globals().items():
        if name.startswith("_lint_"):
            func(args, config, content)


def _lint_bibliography_key_order(args, config, content):
    """Check bibliography file keys for ordering."""
    previous = None
    for key in content["bib"]:
        if (previous is not None) and key <= previous:
            print(f"bibliography key {key} out of order")
        previous = key


def _lint_caption_punctuation(args, config, content):
    """Check punctuation at the ends of captions."""

    def _report(f, c):
        """Is there a problem with this caption?"""
        if c[-1] not in ".?":
            print(f"{filepath} caption '{c}' badly formatted")

    for filepath, doc in content["html"].items():
        for caption in doc.find_all("caption"):
            _report(filepath, caption.string)
        for caption in doc.find_all("figcaption"):
            _report(filepath, caption.string)


def _lint_chapters_again_keys(args, config, content):
    """Check chapters against chapter keys."""
    expected = set(util.source_dirs(args.src, config))
    actual = {str(p) for p in Path(args.src).glob("*") if p.is_dir()}
    report_diff("chapter keys vs. directories", expected, actual)


def _lint_dom_structure(args, config, content):
    """Check DOM structure against spec."""
    seen = {}
    for filepath, doc in content["html"].items():
        seen = collect_dom(seen, doc)
    allowed = yaml.safe_load(Path("lib", config.theme, "dom.yml").read_text())
    diff_dom(seen, allowed)


def _lint_duplicate_files(args, config, content):
    """Check for duplicated files."""
    chapter_order = {slug: i for i, slug in enumerate(config.chapters)}
    arkfiles = content["arkfile"]
    copied = {slug: values.get("copied", []) for slug, values in arkfiles.items()}
    duplicates = find_duplicate_files(config)

    for group in duplicates:
        group = sorted(group, key=lambda filename: chapter_order[filename.parent.name])
        for i, current in list(enumerate(group))[1:]:
            previous = str(group[i - 1])
            slug = str(current.parent.name)
            if previous not in copied[slug]:
                print(f"{current} not listed as duplicate of {previous}")
            else:
                copied[slug].remove(previous)

    for slug, unused in copied.items():
        if unused:
            print(f"{slug}/{ARK_FILE} contains unused {', '.join(sorted(unused))}")


def _lint_inclusions(args, config, content):
    """Check file inclusions."""
    check_inclusions(config, content, "figure")
    check_inclusions(config, content, "table")


def _lint_shortcodes(args, config, content):
    """Check shortcode usage in a single pass."""
    if "bib" not in args.exclude:
        report_diff("bib keys", set(content["b"]), set(content["bib"]))
    report_diff("figure refs", set(content["f"]), set(content["figure"]))
    report_diff("table refs", set(content["t"]), set(content["table"]))


def _lint_single_h1(args, config, content):
    """Check for a single H1 in every file."""
    for filepath, doc in content["html"].items():
        num = len(doc.find_all("h1"))
        if num != 1:
            print(f"{filepath} contains {num} H1 headings")


def _lint_slug_format(args, config, content):
    """Check slugs in headings, figures, and tables."""

    def _check(node, slug, kind):
        """Check format of node's ID."""
        if "id" not in node.attrs:
            print(f"{filepath} {kind} missing 'id'")
        elif not node.attrs["id"].startswith(slug):
            print(f"{filepath} {kind} slug {node.attrs['id']} badly formatted")

    for filepath, doc in content["html"].items():
        slug = filepath.parts[-2]
        for figure in doc.find_all("figure"):
            _check(figure, slug, "figure")
        for table_div in doc.find_all("div", class_="table"):
            _check(table_div, slug, "table div")
        if slug not in util.get_lint(config).get("disable_h2_id", {}):
            for heading in doc.find_all("h2"):
                _check(heading, slug, "H2 heading")


def _lint_svg_files(args, config, content):
    """Check style of SVG diagrams."""

    def _bad_font(n):
        return (n.attrs["font-family"] != "Helvetica") or (
            not node.attrs.get("font-size", "").startswith("12")
        )

    sizes = defaultdict(set)
    fontish = []
    for filename in Path(args.src).glob("**/*.svg"):
        doc = BeautifulSoup(filename.read_text(), features="xml").find("svg")
        sizes[get_svg_size(doc)].add(filename)
        fontish.extend(
            (filename, node)
            for node in doc.find_all(lambda x: "font-family" in x.attrs)
        )

    for key in sorted(sizes.keys()):
        if (key[0] != "px") or (key[1] > SVG_MAX_WIDTH):
            print(f"SVG size {key}: {', '.join(sorted(str(s) for s in sizes[key]))}")

    for filename, node in fontish:
        if _bad_font(node):
            print(f"file {filename} has suspicious fonts {node}")
            continue


def _lint_unresolved_markdown_links(args, config, content):
    """Look for Markdown [text][key] links that didn't resolve."""
    pat = re.compile(r"\]\[")
    for filepath, doc in content["html"].items():
        matches = doc.find_all(string=pat)
        matches = [m for m in matches if not in_code(m)]
        if matches:
            matches = "\n".join(f"- {m.parent.sourceline}: {m}" for m in matches)
            print(f"{filepath} contains unresolved link(s):\n{matches}")


def check_inclusions(config, content, kind):
    """Normalize paths of included files."""
    seen = set()
    for entry in content[kind].values():
        slug = entry["filepath"].parent.name
        src = entry["src"]
        original = Path(config.src_dir, slug, src)
        if not original.exists():
            print(f"Bad inclusion: {original} does not exist")
        elif original in seen:
            print(f"Duplicate inclusion: {original}")
        seen.add(original)


def collect_content(config):
    """Collect things to be linted."""

    def _extract_figure(filepath, id_, node):
        img = node.find("img")
        return {
            "filepath": filepath,
            "id": id_,
            "src": None if img is None else img.attrs["src"],
        }

    def _extract_table(filepath, id_, node):
        return {
            "filepath": filepath,
            "id": id_,
            "src": node.attrs.get("data-tbl", None),
        }

    content = {
        "arkfile": collect_ark_files(config),
        "bib": collect_bib_keys(),
        "html": collect_files(config, "html"),
        "src": collect_files(config, "markdown"),
    }
    content |= {
        "figure": collect_ids(content["html"], "figure", _extract_figure),
        "table": collect_ids(content["html"], "table", _extract_table),
        **collect_shortcodes(content),
    }
    return content


def collect_ark_files(config):
    """Collect .ark files in source."""
    result = {}
    for slug in config.chapters:
        filepath = Path(config.src_dir, slug, ARK_FILE)
        if not filepath.exists():
            result[slug] = {}
        else:
            result[slug] = yaml.safe_load(filepath.read_text())
    return result


def collect_bib_keys():
    """Collect bibliography keys from file."""
    content = Path("info", "bibliography.bib").read_text()
    return list(m for m in regex.BIB_KEY.findall(content))


def collect_dom(seen, node):
    """Collect DOM element attributes from given node and its descendents."""

    if not isinstance(node, Tag):
        return seen
    if node.name not in seen:
        seen[node.name] = {}
    for key, value in node.attrs.items():
        if key not in seen[node.name]:
            seen[node.name][key] = set()
        if isinstance(value, str):
            seen[node.name][key].add(value)
        else:
            for v in value:
                seen[node.name][key].add(v)
    for child in node:
        collect_dom(seen, child)

    return seen


def collect_files(config, which):
    """Read text of source and output files."""

    def _same(x):
        return x

    def _parse(x):
        return BeautifulSoup(x, "html.parser")

    if which == "markdown":
        root_dir = config.src_dir
        filename = "index.md"
        transform = _same
    elif which == "html":
        root_dir = config.out_dir
        filename = "index.html"
        transform = _parse
    else:
        util.fail(f"unknown file type in collector {which}")

    paths = [
        Path(root_dir, filename),
        *[Path(root_dir, slug, filename) for slug in config.chapters],
    ]
    return {p: transform(p.read_text()) for p in paths}


def collect_ids(htmls, kind, extract=None):
    """Collect all IDs of a certain kind."""
    seen = {}
    for filepath, doc in htmls.items():
        nodes = doc.find_all(kind)
        for node in nodes:
            if node.has_attr("class") and "no-id" in node["class"]:
                continue
            if "id" not in node.attrs:
                print(f"{filepath}: {kind} node missing ID")
                continue
            id_ = node.attrs["id"]
            seen[id_] = None if extract is None else extract(filepath, id_, node)
    return seen


def collect_shortcodes(content):
    """Gather information from shortcodes for checking."""

    def _collect(extra, kind, pargs, kwargs, multiple):
        length = (len(pargs) > 0) if multiple else (len(pargs) == 1)
        util.require(
            length and (not kwargs),
            f"Bad '{kind}' shortcode with {pargs} and {kwargs} in {extra['filename']}",
        )
        extra[kind].update(pargs)

    def collect_b(pargs, kwargs, extra):
        _collect(extra, "b", pargs, kwargs, True)

    def collect_f(pargs, kwargs, extra):
        _collect(extra, "f", pargs, kwargs, False)

    def collect_t(pargs, kwargs, extra):
        _collect(extra, "t", pargs, kwargs, False)

    parser = shortcodes.Parser(inherit_globals=False, ignore_unknown=True)
    parser.register(collect_b, "b")
    parser.register(collect_f, "f")
    parser.register(collect_t, "t")

    collected = {
        "b": set(),
        "f": set(),
        "t": set(),
    }
    for filename in content["src"]:
        collected["filename"] = filename
        try:
            parser.parse(Path(filename).read_text(), collected)
        except shortcodes.ShortcodeSyntaxError as exc:
            util.fail(f"%b shortcode parsing error in {filename}: {exc}")

    return collected


def diff_dom(actual, expected):
    """Show difference between two summaries of DOM structures."""
    for name in sorted(actual):
        if name not in expected:
            print(f"DOM {name} seen but not expected")
            continue
        for attr in sorted(actual[name]):
            if attr not in expected[name]:
                print(f"DOM {name}.{attr} seen but not expected")
                continue
            if expected[name][attr] == "*":
                continue
            for value in sorted(actual[name][attr]):
                if value not in expected[name][attr]:
                    print(f"DOM {name}.{attr} == '{value}' seen but not expected")


def find_duplicate_files(config):
    """Group files by duplicate hashes."""
    groups = defaultdict(set)
    for slug in config.chapters:
        for path in Path(config.src_dir, slug).glob("*"):
            if (
                (not path.is_file())
                or str(path).endswith("~")
                or str(path).startswith(".")
            ):
                continue
            hash_code = hashlib.sha256(path.read_bytes()).hexdigest()
            groups[hash_code].add(path)
    return [group for group in groups.values() if len(group) > 1]


def get_svg_size(svg):
    """Get width and height of SVG document."""
    result = (svg.attrs["width"], svg.attrs["height"])
    if result[0].endswith("px"):
        result = ("px", int(result[0][:-2]), int(result[1][:-2]))
    elif result[0].endswith("pt"):
        result = ("pt", int(result[0][:-2]), int(result[1][:-2]))
    else:
        result = ("raw", int(result[0]), int(result[1]))
    return result


def in_code(node):
    """Is this DOM node inside a code element?"""
    return any(p.tag == "code" for p in node.parents)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True, help="config file")
    parser.add_argument("--exclude", nargs="+", default=[], help="tests to exclude")
    parser.add_argument("--src", type=str, required=True, help="source directory")
    return parser.parse_args()


def report_diff(title, expected, actual):
    """Report mis-matches."""
    if diff := expected - actual:
        print(f"{title} missing: {', '.join(sorted(diff))}")
    if diff := actual - expected:
        print(f"{title} extra: {', '.join(sorted(diff))}")


if __name__ == "__main__":
    main()
