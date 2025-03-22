# Objaverse


Maybe Useful
1. [PromptTo3D/triposr_copy/objaverse-rendering/](https://github.com/ACROSS-Lab/PromptTo3D/tree/main/triposr_copy/objaverse-rendering)





# Objaverse-XL : A Universe of 10M+ 3D Objects

[Objaverse-XL - Website](https://objaverse.allenai.org/)

[Objaverse 1.0 - Website](https://objaverse.allenai.org/objaverse-1.0)

[Objaverse-XL - Github](https://github.com/allenai/objaverse-xl)

[Objaverse-XL - HuggingFace 🤗](https://huggingface.co/datasets/allenai/objaverse-xl) -

[Objaverse-XL - Colab](https://colab.research.google.com/drive/15XpZMjrHXuky0IgBbXcsUtb_0g-XWYmN?usp=sharing) - objaverse-xl-api-tutorial



## Website

**Scale Comparison** : `Objaverse-XL` is **12x** larger than `Objaverse 1.0` and **100x** larger than `all other 3D datasets combined`.

**Zero123-XL** : Using `Objaverse-XL`, we train `Zero123-XL`, a foundation model for 3D, observing incredible **3D generation abilities**.

**Image-to-3D** : Using `Zero123-XL`, we can perform **single image to 3D generation** using **Dreamfusion**. Implemented in [threestudio](https://github.com/threestudio-project/threestudio#zero-1-to-3-)!

Blender Compatibility : Each `Objaverse-XL` object can be rendered and imported into `Blender`. [Objaverse-XL Rendering Script](https://github.com/allenai/objaverse-xl/tree/main/scripts/rendering)

## Paper







## Code

### Annotations

get all objects as a DataFrame

```python
annotations = oxl.get_annotations(
    download_dir="~/.objaverse"  # default download directory
)
annotations
```
annotations
1. `github.parquet`
2. `thingiverse.parquet`
3. `smithsonian.parquet`
4. `sketchfab.parquet`

## Alignment Fine-tuning Annotations

```python
alignment_annotations = oxl.get_alignment_annotations(
    download_dir="~/.objaverse"  # default download directory
)
alignment_annotations
```

alignment annotations
1. `github/alignment.parquet`
2. `sketchfab/alignment.parquet`


### Download Objects

```python
oxl.download_objects(
    # Base parameters:
    objects: pd.DataFrame,
    download_dir: str = "~/.objaverse",
    processes: Optional[int] = None,  # None => multiprocessing.cpu_count()

    # optional callback functions:
    handle_found_object: Optional[Callable] = None,
    handle_modified_object: Optional[Callable] = None,
    handle_missing_object: Optional[Callable] = None,

    # GitHub specific:
    save_repo_format: Optional[Literal["zip", "tar", "tar.gz", "files"]] = None,
    handle_new_object: Optional[Callable] = None,
)
```
Parameters
1. base parameters
   1. `objects`
      1. a pandas DataFrame the objects to download
      2. Must have columns for the object `"fileIdentifier", "source", "sha256"`
   2. `download_dir` : `"~/.objaverse"`(default)
   3. `processes` : number of processes to use when downloading the objects
      1. If `None`, `multiprocessing.cpu_count()`(the number of CPUs on the machine)
2. optional callback functions
   1. `handle_found_object` : called when an object is successfully found and downloaded
   2. `handle_modified_object` : called when a modified object is found and downloaded
   3. `handle_missing_object` : called when a specified object cannot be found
3. GitHub specific(下载 来源于 Github 的 Objects 时需要，不影响 其他 sources 的 下载)
   1. `save_repo_format` : the format to save the GitHub repository, GitHub objects are not standalone 3D files
      1. If `None`(default), the repository will not be saved
      2. If `"files"` is specified, each file will be saved individually in a standard folder structure
      3. Otherwise, the repository can be saved as a `"zip", "tar", "tar.gz"` file
   2. `handle_new_object`
      1. If `None`, the object will be downloaded, but nothing will be done with it



```python
sampled_df = annotations.groupby('source').apply(lambda x: x.sample(1)).reset_index(drop=True)
# 每种类别挑一个
```




Blender 支持格式
1. glb






