# usb-print

## Usage

You need to set the following environment variables:

* `USB_PRINT_URL`: The URL of your WebDAV server, e.g. "https://dav.example.com"
* `USB_PRINT_USER`: The user to login with = "printer"
* `USB_PRINT_PASSWORD`: The password for the user
* `USB_PRINT_DIRECTORY`: The directory to use for printing. On Nextcloud, if the user the directory belongs to is `printer` and the directory is `printer/print`, this looks like `/remote.php/dav/files/printer/printer/print/`
* `USB_PRINT_ARCHIVE_DIRECTORY`: Where to archive printed files. See `USB_PRINT_DIRECTORY`.

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
