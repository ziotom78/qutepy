# -*- encoding: utf-8 -*-

import json
import urllib.request as request
from os.path import expanduser, join

DEFAULT_CONFIGURATION_FILE_NAME = join(expanduser("~"), ".qutepy")
SERVER_NAME = None
version = "0.0.1"


def __interactive_configure():
    global SERVER_NAME

    while True:
        SERVER_NAME = input("Enter the base URL of the QuteDB database to use: ")
        print(
            'The name of the server is "{}". Is this ok? [Y/N] '.format(SERVER_NAME),
            end="",
        )
        while True:
            answer = input("").upper()
            if answer in ["Y", "N"]:
                break

        if answer == "Y":
            break


def configure(
    configuration_file_name=DEFAULT_CONFIGURATION_FILE_NAME, interactive=True
):
    """Configure QuTePy

    This function prompts a few questions to the user in order to properly
    configure QuTePy. At the moment, the function asks for the URL of the
    QuteDB server and stores it in a file under the user's home directory.

    If `configuration_file_name` is specified, a different configuration
    file will be accessed.
    
    If `interactive` is False and the function is struck somewhere, it will
    fail instead of prompting the user.
    """

    global SERVER_NAME

    try:
        with open(configuration_file_name) as inpf:
            SERVER_NAME = inpf.readline().strip()

        if not interactive:
            return

        print(
            'The QuteDB URL is "{}". Do you want to change it? [Y/N] '.format(
                SERVER_NAME
            ),
            end="",
        )

        while True:
            answer = input("").upper()
            if answer in ["Y", "N"]:
                break

        if answer == "Y":
            __interactive_configure()
    except FileNotFoundError:
        if interactive:
            __interactive_configure()

    with open(configuration_file_name, "wt") as outf:
        outf.write(SERVER_NAME)


def download(path, acquisition, verbose=False):
    """Download one or more acquisitions from a Qubic test database.

    Connect to QuteDB and download the list of acquisitions specified by the
    argument `acquisitions`. For each acquisition, both the metadata and a ZIP
    file bundling all the FITS files acquired by QubicStudio are downloaded. The
    metadata are returned by the function, and the ZIP file is saved in the
    directory `path`.

    The parameter `acquisition` can be either a string identifying an
    acquisition, like "2019-01-02T11:23:54", or a list of strings of the same
    type. In the second case, all the acquisitions will be downloaded in the
    same order.

    The return value is either a dictionary, if `acquisition` refers to one
    acquisition, or a list of dictionaries.

    If `qutepy.configure` was not called properly, this function will complain
    and return `None`.
    """

    global SERVER_NAME

    if not SERVER_NAME:
        configure(interactive=False)
        if not SERVER_NAME:
            print("Use qutepy.configure() to properly configure the server")
            return

    if type(acquisition) is list:
        result = []
        for cur_acq in acquisition:
            result.append(download(path, cur_acq))

        return result

    if verbose:
        print('Downloading acquisition "{}"'.format(acquisition))

    metadata_url = request.urljoin(SERVER_NAME, "api/v1/acquisitions/" + acquisition)
    req = request.urlopen(metadata_url)
    metadata = json.loads(req.read().decode("utf-8"))
    archive_url = request.urljoin(
        SERVER_NAME, "api/v1/acquisitions/" + acquisition + "/archive"
    )

    req = request.urlopen(archive_url)
    datafile = req.read()
    output_file_name = join(path, metadata["directory_name"] + ".zip")
    with open(output_file_name, "wb") as outf:
        outf.write(datafile)

    if verbose:
        print('File "{}" written to disk'.format(output_file_name))

    metadata["output_file_name"] = output_file_name
    return metadata

