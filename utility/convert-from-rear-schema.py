#!/usr/bin/env python

import json
import sys
import os
from typing import Any


def load_schema(path: str) -> dict[str, Any]:
    try:
        with open(path, "r") as input:
            return json.load(input)
    except FileNotFoundError:
        blocks = path.split("/")
        return load_schema("/".join(blocks[:-2] + ["flavor-types"] + blocks[-2:]))


def build_property_range(spec: dict[str, Any]) -> tuple[str | list[str], bool]:
    t = spec.get("type", None)
    if t is None:
        if "oneOf" in spec:
            try:
                return [
                    oo["$ref"] for oo in spec["oneOf"]
                ], True
            except KeyError:
                pass
        print(f"### {spec=}")
        raise ValueError()

    if t == "boolean":
        return "xsd:boolean", True
    if t == "string":
        return "xsd:string", True
    if t == "object":
        return "object", True
    if t == "integer":
        return "xs:integer", True

    if t == "array":
        if "items" not in spec:
            return "owl:Thing", False

        item_type = spec["items"]["type"]
        if item_type == "boolean":
            return "xsd:boolean", False
        if item_type == "string":
            return "xsd:string", False
        if item_type == "integer":
            return "xs:integer", False

    print(f"**** {spec=}")
    raise ValueError()


def process_property(property_name: str, spec: dict[str, str], parent: str) -> None:
    objects: list[tuple[str, dict[str, str]]] = []
    refs: list[str] = []

    name = f"{parent}_{property_name}"

    print()

    description = spec.get("description", f"A {property_name} of {parent}")

    r_type, is_functional = build_property_range(spec)
    if r_type == "object":
        objects.append((name, spec))
        r_type = property_name

    if type(r_type) is list:
        refs = r_type
        r_type = property_name

    print(f"### https://fluidos.eu/ontologies/{name}")

    if is_functional:
        print(f":has{name} rdf:type owl:FunctionalProperty ;")
    else:
        print(f":has{name} rdf:type owl:ObjectProperty ;")
    print(f"\t rdfs:comment \"{description}\"@en ;")
    print(f"\t rdfs:domain :{parent} ;")
    print(f"\t rdfs:range {r_type} ;")
    print(f"\t rdf:label \"{property_name}\"@en .")
    print()

    for (obj_name, spec) in objects:
        process_object(obj_name, spec, parent=None, desc=None)

    for ref in refs:
        process_schema(os.path.join(sys.argv[1], ref), f":{property_name}")


def process_object(object_name: str, spec: dict[str, Any], parent: str | None, desc: str | None) -> None:  # -> list[tuple[str, dict[str, Any], str]]:
    print(f"###  https://fluidos.eu/ontologies/{object_name}")
    print(f":{object_name} rdf:type {parent} ;")
    if desc is None:
        if "description" in spec:
            desc = str(spec["description"])
        else:
            desc = "Missing description"

    print(f"\trdfs:comment \"{desc}\"@en . ")

    schema_properties: dict[str, dict[str, Any]] = spec["properties"]

    properties_to_process = []

    for property_name, property_spec in schema_properties.items():
        properties_to_process.append((property_name, property_spec))
        # n = f"{object_name}_{property_name}"
        # print(f"\t :has{property_name} :{n}")

    print()

    for property_name, property_spec in properties_to_process:
        process_property(property_name, property_spec, object_name)

    pass


def process_schema(file: str, base_type: str | None) -> int:
    schema = load_schema(file)

    type_name = schema["title"]

    process_object(type_name, schema, base_type, "")

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing parameter: REAR-data-model schema folder")
        sys.exit(-1)
    basedir = sys.argv[1]
    raise SystemExit(process_schema(os.path.join(basedir, "flavor.json"), "owl:Class"))
