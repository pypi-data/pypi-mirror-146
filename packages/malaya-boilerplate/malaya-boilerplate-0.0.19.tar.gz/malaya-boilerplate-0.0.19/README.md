<p align="center">
    <a href="#readme">
        <img alt="logo" width="40%" src="malaya-boilerplate.png">
    </a>
</p>
<p align="center">
    <a href="https://pypi.python.org/pypi/malaya-boilerplate"><img alt="Pypi version" src="https://badge.fury.io/py/malaya-boilerplate.svg"></a>
    <a href="https://pypi.python.org/pypi/malaya-boilerplate"><img alt="Python3 version" src="https://img.shields.io/pypi/pyversions/malaya-boilerplate.svg"></a>
    <a href="https://discord.gg/aNzbnRqt3A"><img alt="discord" src="https://img.shields.io/badge/discord%20server-malaya-rgb(118,138,212).svg"></a>
</p>

---

**malaya-boilerplate**, Tensorflow freeze graph optimization and boilerplates to share among Malaya projects.

## Table of contents

  * [malaya_boilerplate.frozen_graph](#malaya_boilerplate_frozen_graph)
  * [malaya_boilerplate.utils](#malaya_boilerplate_utils)
  
### malaya_boilerplate.frozen_graph

#### malaya_boilerplate.frozen_graph.load_graph

```python
def load_graph(package, frozen_graph_filename, **kwargs):
    """
    Load frozen graph from a checkpoint.

    Parameters
    ----------
    frozen_graph_filename: str
    use_tensorrt: bool, optional (default=False)
        Use TensorRT.
    tensorrt_precision_mode: str, optional (default='FP32')
        TensorRT precision mode, only supported one of ['FP32', 'FP16', 'INT8'].
        if device is not a gpu, `load_graph` will throw an error.
    precision_mode: str, optional (default='FP32')
        change precision frozen graph, only supported one of ['BFLOAT16', 'FP16', 'FP32', 'FP64'].
    auto_gpu: bool, optional (default=True)
        if installed gpu version, will automatically allocate a model to a gpu with the most empty memory.
    t5_graph: bool, optional (default=False)
        if True, will replace static shape to dynamic shape for first element in batch.
        This should do for T5 models only.
    glowtts_graph: bool, optional (default=False)
        if True, will have some extra condition for glowTTS models.
    glowtts_multispeaker_graph: bool, optional (default=False)
        if True, will have some extra condition for glowTTS Multispeaker models.
    device: str, optional (default='CPU:0')
        device to use for specific model, read more at https://www.tensorflow.org/guide/gpu

    Returns
    -------
    result : tensorflow.Graph
    """
```

#### malaya_boilerplate.frozen_graph.generate_session

```python
def generate_session(graph, **kwargs):
    """
    Load session for a Tensorflow graph.

    Parameters
    ----------
    graph: tensorflow.Graph
    gpu_limit: float, optional (default = 0.999)
        limit percentage to use a gpu memory.

    Returns
    -------
    result : tensorflow.Session
    """
```

### malaya_boilerplate.utils

#### malaya_boilerplate.utils.available_device

```python
def available_device(refresh = False):
    """
    Get list of devices and memory limit from `tensorflow.python.client.device_lib.list_local_devices()`.

    Returns
    -------
    result : List[str]
    """
```

#### malaya_boilerplate.utils.available_gpu

```python
def available_gpu(refresh = False):
    """
    Get list of GPUs and memory limit from `tensorflow.python.client.device_lib.list_local_devices()`.

    Returns
    -------
    result : List[str]
    """
```

#### malaya_boilerplate.utils.print_cache

```python
def print_cache(package, location=None):
    """
    Print cached data, this will print entire cache folder if let location = None.

    Parameters
    ----------
    location : str, (default=None)
        if location is None, will print entire cache directory.

    """
```

#### malaya_boilerplate.utils.delete_cache

```python
def delete_cache(package, location):
    """
    Remove selected cached data, please run print_cache() to get path.

    Parameters
    ----------
    location : str

    Returns
    -------
    result : boolean
    """
```

#### malaya_boilerplate.utils.delete_all_cache

```python
def delete_all_cache(package):
    """
    Remove cached data, this will delete entire cache folder.
    """
```

#### malaya_boilerplate.utils.close_session

```python
def close_session(model):
    """
    Close session from a model to prevent any out-of-memory or segmentation fault issues.

    Parameters
    ----------
    model : malaya object.

    Returns
    -------
    result : boolean
    """
```