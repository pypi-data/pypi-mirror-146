# pyBCS

This is a python library to create a BioTuring Compressed Study (`bcs`) file from an AnnData (scanpy) object.

`bcs` files can be imported directly into [BBrowser](https://bioturing.com/bbrowser), a software for single-cell data.

Visit our [github](https://github.com/bioturing/pyBCS) for more detail.

## Installation

```bash
pip install pyBCS-bioturing
```

## Examples

### Create a bcs file from common formats

#### Scanpy
```python
from pyBCS import scanpy2bcs
scanpy2bcs.format_data("/mnt/example/data.h5ad", "/mnt/example/data.bcs",
                        input_format="h5ad", graph_based="louvain")
```

If your data has antibody-derived tags (ADT), you can put ADT expression data in the `obs` as cell metadata with a distinguishable suffix. For example, ADT expression of `CD45` will be `CD45_TotalSeqC`. In such cases, you can declare `cite_seq_suffix` when using `format_data()`:

```python
scanpy2bcs.format_data("/mnt/example/data.h5ad", "/mnt/example/data.bcs",
                       input_format="h5ad", graph_based="louvain", cite_seq_suffix="_TotalSeqC")
```

#### SPRING

```python
from pyBCS import scanpy2bcs
scanpy2bcs.format_data("/mnt/example/spring_study", "/mnt/example/data.bcs",
                        input_format="spring",
                        graph_based="louvain")
```

#### Loom

```python
from pyBCS import scanpy2bcs
scanpy2bcs.format_data("/mnt/example/data.loom", "/mnt/example/data.bcs",
                        input_format="loom",
                        barcode_name="CellID",
                        feature_name="Gene",
                        dimred_keys={"tsne":["tsne1", "tsne2"]})
```

#### Abloom

```python
from pyBCS import scanpy2bcs
scanpy2bcs.format_data("/mnt/example/data.loom", "/mnt/example/data.bcs",
                        input_format="abloom",
                        barcode_name="observation_id",
                        feature_name="accession_id",
                        graph_based="cluster")
```

### Create a folder from OME-TIFF files (Nanostring DSP)

In this example, we use `OME` class from `pyBCS` to load information from OME-TIFF format. An `OME` object requires 2 arguments: (1) an excel that has `SegmentProperties` and `TargetCountMatrix`, (2) a folder that has all the OME-TIFF files for that excel file. After loading data, you can use `.write()` to create a folder that has all the neccessary components for BBrowser.

```python
from pyBCS import OME
ome = OME('path/to/excel_file.xlsx', 'path/to/tif/folder')
ome.write('path/to/output_folder')
```