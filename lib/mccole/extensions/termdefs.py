"""Show terms defined in chapter."""

import ark
import ibis

from glossary import glossary_ref
import util


@ibis.filters.register("termdefs")
def termdefs(node):
    """Construct list of defined terms."""
    if (not node.slug) or (node.slug not in ark.site.config["chapters"]):
        return ""
    keys = ark.site.config["_terms_"].get(node.slug, None)
    if not keys:
        return ""
    lang = ark.site.config["lang"]
    glossary = {g["key"]: g for g in util.load_glossary()}
    terms = [glossary_ref([key, glossary[key][lang]["term"]], {}, node) for key in sorted(keys)]
    terms = ", ".join(terms)
    return f'<p class="terms">{util.kind('defined')}: \n{terms}\n</p>'
