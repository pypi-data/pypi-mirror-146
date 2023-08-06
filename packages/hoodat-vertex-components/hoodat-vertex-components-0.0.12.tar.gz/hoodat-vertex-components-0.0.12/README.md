# Hoodat Pipeline Components

This repository provides an SDK and a set of components that perform
tasks in hoodat.

It is modelled after this repository of shared components for GCP:
https://github.com/kubeflow/pipelines/tree/google-cloud-pipeline-components-1.0.1/components/google-cloud

## To publish package to pypi:

1. Update the version in `pyproject.toml`

2. Run `poetry publish`:
```
poetry publish --build
```
