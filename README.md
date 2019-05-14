# QuTePy

A Python package to access data saved by a
[QuteDB](https://github.com/ziotom78/qutedb) instance via its HTTP REST API.

## Installing

QuTePy requires Python 3 and only uses libraries in the standard distribution
(no external dependencies are needed).

You can install and download it by running the following command:

    pip install -e .

## Usage

Once QuTePy is installed, you have to configure it. Run the following command:

    python -c "import qutepy; qutepy.configure()"

A prompt will appear, asking for the URL of the QuteDB database to use. Enter
the basename, e.g., `https://qutedb.server.org`, and press `Enter`. The
configuration will be saved in the file `~/.qutepy`.

Once QuTePy is installed, you can use the `download` function to download tests
and metadata from the server:

```python
import qutepy

metadata = qutepy.download(path="/storage", acquisition="2009-01-01T10:12:34")
```

This example will download the specified acquisition and will save a ZIP file
containing all the data in the directory specified by the parameter `path`. The
return value is a dictionary containing useful metadata. Refer to the
documentation of `qutepy.download` for more information.
