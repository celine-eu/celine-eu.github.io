from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple

from rdflib import Graph, RDF, RDFS, OWL, URIRef


CLASS_TYPES = {OWL.Class, RDFS.Class}
PROPERTY_TYPES = {
    RDF.Property,
    OWL.ObjectProperty,
    OWL.DatatypeProperty,
    OWL.AnnotationProperty,
}


def local_name(uri: URIRef) -> str:
    s = str(uri)
    if "#" in s:
        return s.rsplit("#", 1)[1]
    return s.rsplit("/", 1)[-1]


def get_label(g: Graph, uri: URIRef) -> str | None:
    for o in g.objects(uri, RDFS.label):
        return str(o)
    return None


def get_comment(g: Graph, uri: URIRef) -> str | None:
    for o in g.objects(uri, RDFS.comment):
        return str(o)
    return None


def collect_entities(
    g: Graph,
) -> Tuple[list[URIRef], list[URIRef]]:
    classes: set[URIRef] = set()
    properties: set[URIRef] = set()

    for s, _, o in g.triples((None, RDF.type, None)):
        if not isinstance(s, URIRef):
            continue

        if o in CLASS_TYPES:
            classes.add(s)
        elif o in PROPERTY_TYPES:
            properties.add(s)

    return sorted(classes, key=lambda u: local_name(u).lower()), sorted(
        properties, key=lambda u: local_name(u).lower()
    )


def generate_index(
    ttl_file: Path,
    output_dir: Path,
    namespace: str,
) -> None:
    g = Graph()
    g.parse(ttl_file)

    classes, properties = collect_entities(g)

    lines: list[str] = []

    lines.extend(
        [
            "# CELINE Ontology",
            "",
            "**Namespace**",
            "",
            f"`{namespace}`",
            "",
            "## Classes",
            "",
        ]
    )

    for c in classes:
        ln = local_name(c)
        lines.append(f"- [{ln}](#{ln})")

    if properties:
        lines.extend(["", "## Properties", ""])
        for p in properties:
            ln = local_name(p)
            lines.append(f"- [{ln}](#{ln})")

    lines.append("")

    def render_section(title: str, entities: Iterable[URIRef]) -> None:
        for uri in entities:
            name = local_name(uri)
            label = get_label(g, uri)
            comment = get_comment(g, uri)

            anchor = name
            anchor_lc = name.lower()

            lines.extend(
                [
                    f'<a id="{anchor}"></a>',
                    f'<a id="{anchor_lc}"></a>',
                    f"## {name}",
                    "",
                    f"**IRI** `{uri}`",
                    "",
                ]
            )

            if label:
                lines.extend([f"**Label** {label}", ""])

            if comment:
                lines.extend([f"**Description** {comment}", ""])

    render_section("Classes", classes)
    if properties:
        render_section("Properties", properties)

    output_dir.mkdir(parents=True, exist_ok=True)
    index = output_dir / "index.md"
    index.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print(
            "Usage: generate_ontology_docs.py <ontology.ttl> <output_dir> <namespace>"
        )
        sys.exit(1)

    generate_index(
        ttl_file=Path(sys.argv[1]),
        output_dir=Path(sys.argv[2]),
        namespace=sys.argv[3],
    )
