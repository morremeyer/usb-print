# usb-print

This python script checks a remote WebDav instance at a specific path and sends files to configured cups daemon to print.
It checks the WebDav server every 15 seconds and sends all found files to cups. Afterwards, it moves them to another folder.

Just plug your printer and follow the usage instructions below!

**Note: Currently, this script always uses the first printer on the CUPS server.**

## Usage

You need to set the following environment variables:

* `USB_PRINT_CUPS_HOST`: The host or IP of the CUPS server. Defaults to `localhost`.
* `USB_PRINT_CUPS_PORT`: The port on which the CUPS server listens. Defaults to `631`.
* `USB_PRINT_URL`: The URL of your WebDAV server, e.g. "https://dav.example.com"
* `USB_PRINT_USER`: The user to login with = "printer"
* `USB_PRINT_PASSWORD`: The password for the user
* `USB_PRINT_DIRECTORY`: The directory to use for printing. On Nextcloud, if the user the directory belongs to is `printer` and the directory is `printer/print`, this looks like `/remote.php/dav/files/printer/printer/print/`
* `USB_PRINT_ARCHIVE_DIRECTORY`: Where to archive printed files. See `USB_PRINT_DIRECTORY`.

### Locally

You need to have `libcups2-dev` installed (Debian/Ubuntu, on other OS. the package name might be different).

```sh
# Set up a virtual environment to not pollute your system python
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Set the required environment variables
export USB_PRINT_URL=https://nextcloud.example.com
export USB_PRINT_USER=printer
export USB_PRINT_PASSWORD=VerySecurePassword
export USB_PRINT_DIRECTORY=/remote.php/dav/files/printer/printer/print/
export USB_PRINT_ARCHIVE_DIRECTORY=/remote.php/dav/files/printer/printer/print-archive/

# Run the script
python src/print.py
```

## Development environment

You need to have `libcups2-dev` installed on Debian/Ubuntu:

```sh
sudo apt-get install libcups2-dev
```

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

pre-commit install --hook-type pre-commit
```
