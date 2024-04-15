#!/usr/bin/env python

import json
import sys
import os
from typing import Any


def load_schema(path: str) -> dict[str, Any]:
    with open(path, "r") as input:
        return json.load(input)


def build_property_range(spec: dict[str, Any]) -> str | list[str]:
    t = spec.get("type", None)
    if t is None:
        if "oneOf" in spec:
            return [
                oo["$ref"] for oo in spec["oneOf"]
            ]
        print(f"### {spec=}")
        raise ValueError()

    if t == "boolean":
        return "xsd:boolean"
    if t == "string":
        return "xsd:string"
    if t == "object":
        return "object"
    if t == "integer":
        return "xs:integer"

    print(f"**** {spec=}")
    raise ValueError()


def process_property(property_name: str, spec: dict[str, str], parent: str) -> None:
    objects: list[tuple[str, dict[str, str]]] = []
    refs: list[str] = []

    name = f"{parent}_{property_name}"

    print()
    print(f"### https://fluidos.eu/ontologies/{name}")
    print(f":has{name} rdf:type owl:ObjectProperty ;")

    description = spec.get("description", f"A {property_name} of {parent}")

    r_type = build_property_range(spec)
    if r_type == "object":
        objects.append((name, spec))
        r_type = property_name

    if type(r_type) is list:
        refs = r_type
        r_type = property_name

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
