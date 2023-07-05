#!/usr/bin/env python3

import os
import sys
from dataclasses import dataclass
from typing import Optional


def extract_resources() -> list[tuple]:
    with os.popen("kubectl api-resources") as stream:
        output = stream.readlines()

    resources = []

    for resource in output[1:]:
        parts = resource.strip().split()

        resources.append(tuple(parts))

    return resources


def print_prehamble(base_uri: str, onto_version: str = "0.0.2") -> None:
    print(f'''
@prefix : <{base_uri}> .
@prefix dc: <http://purl.org/dc/elements/1.1> .
@prefix net: <http://www.w3.org/2007/uwa/context/network.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix hardware: <http://www.w3.org/2007/uwa/context/hardware.owl#> .
@prefix oboInOwl: <http://www.geneontology.org/formats/oboInOwl#> .
@base <{base_uri}> .

<https://fluidos.eu/ontologies> rdf:type owl:Ontology ;
                                 owl:versionIRI <{base_uri}/{onto_version}> ;
                                 <http://purl.org/dc/elements/1.1/creator> "IBM Research Europe" ;
                                 <http://purl.org/dc/elements/1.1/publisher> "IBM Research Europe" ,
                                                                             "This ontology describes a schema for specifying resource and functional element requirements and offering within the FLUIDOS Horizon Europe project" ;
                                 dcterms:created "2023-03-22"^^xsd:date ,
                                                 "FLUIDOS Resource and Functional Requirements Ontology" ;
                                 owl:versionInfo "{onto_version}" .

 ''')


def process_documentation(data):
    fields = []

    fields_position = data.find("FIELDS:\n")
    if len(data.strip()) and -1 != fields_position:
        for field_description in data[fields_position + len("FIELDS:\n"):].rstrip().split("\n\n"):
            lines = field_description.strip().split('\n')
            fields.append(tuple(lines[0].split()))

    return fields


def extract_object_properties(obj_name: str) -> tuple[list[tuple], Optional[list[tuple]]]:
    with os.popen(f"kubectl explain {obj_name}.spec") as stream:
        specs_data = stream.read()

    specs_field = process_documentation(specs_data)

    with os.popen(f"kubectl explain {obj_name}") as stream:
        obj_data = stream.read()

    obj_fields = process_documentation(obj_data)

    return (obj_fields, specs_field)


def build_property_name(resource_name: str, property_name: str) -> str:
    return f"{resource_name}_{property_name}"


def build_property_range(property_spec: list[tuple]) -> tuple[str, bool]:
    codomain = property_spec[1]

    if codomain == '<boolean>':
        return 'xsd:boolean', True
    if codomain == '<integer>':
        return 'xsd:integer', True
    if codomain == '<string>':
        return 'xsd:string', True

    if codomain.startswith('<[]'):
        codomain_type = codomain[3:-1]
        if codomain_type == 'string':
            return 'xsd:string', False
        return f":{codomain_type}", False

    if codomain.startswith('<map[string][]string'):
        return 'xsd:string', False
    if codomain.startswith('<map[string]string>'):
        return 'xsd:string', False
    if codomain.startswith('<map[string]'):
        return f':{codomain[len("<map[string]"):-1]}', False

    return f':{codomain[1:-1]}', True


def create_base_uri() -> str:
    return "https://fluidos.eu/ontologies/kubernetes/"


def main() -> int:
    base_uri = create_base_uri()

    # all resources
    print_prehamble(base_uri)

    for resource in extract_resources():
        obj_properties, obj_spec = extract_object_properties(resource[0])

        print()
        print()
        print(f"### {base_uri}{resource[-1]}")
        print(f":{resource[-1]} rdf:type owl:Class ;")
        print(f"\t rdf:subClassOf :KubernetesComponent ;")
        print(f"\t rdf:label \"{resource[-1]}\"@en ;")
        print(f"\t :apiVersion \"{resource[2]}\" ;")
        if obj_spec:
            print(f"\t :hasSpec :{resource[-1]}Spec ;")
        print(f"\t :isNameSpaced :{resource[3]} .")

        for obj_property in obj_properties:
            property_name = build_property_name(resource[0], obj_property[0])
            r_type, is_functional = build_property_range(obj_property)
            print()
            print(f'### {base_uri}#{property_name}')
            if is_functional:
                print(f':{property_name} rdf:type owl:FunctionalProperty ;')
            else:
                print(f':{property_name} rdf:type owl:ObjectProperty ;')
            print(f'\t rdfs:domain :{resource[-1]} ;')
            print(f'\t rdfs:range {r_type} ;')
            print(f'\t rdf:label "{property_name}"@en .')

        print()
        print()
        print(f"### {base_uri}{resource[-1]}Spec")
        print(f":{resource[-1]}Spec rdf:type owl:Class ;")
        print(f"\t rdf:subClassOf :KubernetesComponentSpec ;")
        print(f"\t rdf:label \"{resource[-1]}Spec\"@en ;")
        print(f"\t :apiVersion \"{resource[2]}\" ;")
        print(f"\t :isNameSpaced :{resource[3]} .")

        for obj_property in obj_spec:
            property_name = build_property_name(resource[0]+"Spec", obj_property[0])
            r_type, is_functional = build_property_range(obj_property)
            if r_type == ':string':
                raise Exception(f"{r_type}, {obj_property}")
            print()
            print(f'### {base_uri}#{property_name}')
            if is_functional:
                print(f':{property_name} rdf:type owl:FunctionalProperty ;')
            else:
                print(f':{property_name} rdf:type owl:ObjectProperty ;')
            print(f'\t rdfs:domain :{resource[-1]}Spec ;')
            print(f'\t rdfs:range {r_type} ;')
            print(f'\t rdf:label "{property_name}"@en .')


if __name__ == "__main__":
    raise SystemExit(main())

