# usb-print

## Usage

You need to set the following environment variables:

* `USB_PRINT_URL`: The URL of your WebDAV server, e.g. "https://dav.example.com"
* `USB_PRINT_USER`: The user to login with = "printer"
* `USB_PRINT_PASSWORD`: The password for the user
* `USB_PRINT_DIRECTORY`: The directory to use for printing. On Nextcloud, if the user the directory belongs to is `printer` and the directory is `printer/print`, this looks like `/remote.php/dav/files/printer/printer/print/`
* `USB_PRINT_ARCHIVE_DIRECTORY`: Where to archive printed files. See `USB_PRINT_DIRECTORY`.

Configure your docker-compose.yml as follows:

```yaml
# You MUST use 2.4 as 3.x+ do not support device_cgroup_rules
version: '2.4'

services:
  print:
    image: registry.git.mor.re/tools/usb-print:latest
    restart: unless-stopped
    container_name: print
    volumes:
      # Persist cups configuration - you don’t want to add your printer on each reboot, do you?
      - cups-config:/etc/cups
      # Mount the USB bus so that the printer can be turned off and on again. It will get a new mount point,
      # so just mounting the path where it currently sits won’t work
      - /dev/bus/usb:/dev/bus/usb

    # This allows your container to read and write to all devices from all cgroups.
    # It’s to broad, but I couldn’t be bothered to narrow it down for now
    device_cgroup_rules:
      - 'a *:* rwm'
    environment:
      - USB_PRINT_URL=https://nextcloud.example.com
      - USB_PRINT_USER=printer
      - USB_PRINT_PASSWORD=VerySecurePassword
      - USB_PRINT_DIRECTORY=/remote.php/dav/files/printer/printer/print/
      - USB_PRINT_ARCHIVE_DIRECTORY=/remote.php/dav/files/printer/printer/print-archive/

volumes:
  cups-config: {}
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
