# FLUIDOS resource definition ontology

[![format](https://img.shields.io/badge/Ontology_Format-TTL-blue)](https://pages.github.com/fluidos-project/fluidos-ontology/ontology.ttl)
[![specification](https://img.shields.io/badge/Ontology_Specification-Docs-yellow)](https://pages.github.com/fluidos-project/fluidos-ontology/ontology-specification/)
[![visualize](https://img.shields.io/badge/Visualize-WebVOWL-blue)](https://github.com/fluidos-project/fluidos-ontology/webvowl/index.html#)
[![license](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![user guide](https://img.shields.io/badge/User_Guide-Docs-yellow)](https://pages.github.com/fluidos-project/fluidos-ontology/)

The ontology developed within the scope of the FLUIDOS project is an ontology that aims to represent and link together information about resources and services offered and accessed within a Kubernetes-based Cloud-to-Edge.
This work is motivated by the need to better, and formally, define and understand the resources offered within the continuum, their utilization from other actors, and their relationship with the underlining kubernetes infrastructure.

The ontology can be used to generate resources and intent-centered knowledge graphs (i.e. instances of the ontology) and support analytics and other inference tasks in the scope of Cloud Continuum.

## Quick links

- [User Guide and Examples](https://pages.github.com/fluidos-project/fluidos-ontology/)
- [Visualize with WebVOWL](https://pages.github.com/fluidos-project/fluidos-ontology/ontology-specification/webvowl/index.html#)
- [Ontology Specification](https://pages.github.com/fluidos-project/fluidos-ontology/ontology-specification/)
- [How to Contribute](CONTRIBUTING.md)
- [Github repository](https://github.com/fluidos-project/fluidos-ontology)

## Getting started

The FLUIDOS ontology comprises of two ontology definition.
The first one, called [kubernetes](ontology/kubernetes.ttl), describes resource model and it is automatically generated from the API exposed by Kubernetes.
The tooling for the generation is available [here](utility/build_k8s_ttl.py).
The second ontology properly characterizes the cloud continuum according to FLUIDOS terminology, and its interconnection with its counterparts in the Kubernetes world.
Refer to the FLUIDOS protocol specifications [Docs](https://github.com/fluidos-project/Docs/) for additional information.

## Help and Support

Please feel free to reach out to one of the maintainers listed in the [MAINTAINERS.md](MAINTAINERS.md) page.

## Contributing

We are always looking for help and support to continue to develop this project. Please see our [guidance](CONTRIBUTING.md) for details on how to contribute.

## Citing this Project

If you use the FLUIDOS Ontology or code, please consider citing:

```bib
@software{ontology,
    author = {FLUIDOS Team},
    month = {4},
    title = {{FLUIDOS Ontology}},
    url = {https://github.com/fludios-project/fluidos-ontology},
    version = {main},
    year = {2023}
}
```

## License

The FLUIDOS Ontology project is under the Apache 2.0 license. Please [see details here](LICENSE).
