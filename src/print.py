import logging
import sys
from os import getenv, remove
from time import sleep

import cups

from webdav import Client

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

if __name__ == "__main__":
    """Print documents from a WebDav server

    1. Checks the WebDAV server URL specified for new files
    2. Downloads them to /tmp
    3. Prints them
    4. Deletes them locally
    5. Moves them to another folder on the WebDAV server
    """

    logging.info("Starting usb-print")

    URL = getenv("USB_PRINT_URL")
    USER = getenv("USB_PRINT_USER")
    PASSWORD = getenv("USB_PRINT_PASSWORD")
    DIRECTORY = getenv("USB_PRINT_DIRECTORY")
    ARCHIVE_DIRECTORY = getenv("USB_PRINT_ARCHIVE_DIRECTORY")

    logging.info(
        f"Directory '{URL}{DIRECTORY}' will be checked with user '{USER}' for new files to print."
        f"Archive directory is '{URL}{ARCHIVE_DIRECTORY}'"
    )

    # WebDAV client
    client = Client(URL, USER, PASSWORD)

    # Connect to cups
    conn = cups.Connection()

    # We assume to only have one printer, so get its name (which is the key in the dict)
    printers = conn.getPrinters()
    if len(printers) == 0:
        logging.error("No printers found, exiting")
        sys.exit(1)

    printer = list(printers.keys())[0]
    logging.info(f"Using printer {printer}")

    while True:  # Yeah, I know, busy wating loops yaddah yaddah
        # We just authenticate every time to avoid authentication issues
        client.authenticate()

        # Get list of all files
        profind = client.propfind(DIRECTORY)
        paths = [
            f["href"]
            for f in profind.getchildren()
            if not str(f["href"]).endswith(DIRECTORY)
        ]

        if len(paths) == 0:
            logging.debug("No files to print, going back to sleep")

        # Loop over file names, download, print, delete, move remotely
        for path in paths:
            logging.debug(f"Downloading {path}")
            download = client.get(path)

            if download:
                file_name = str(path).split("/")[-1]
                target_path = f"/tmp/{file_name}"

                logging.debug(f"Writing {path} to {target_path}")

                with open(target_path, "wb") as f:
                    f.write(download)

                # Print the file
                logging.info(f"Printing {file_name}")
                conn.printFile(printer, target_path, file_name, {})

                # Cleanup
                logging.debug(f"Removing {target_path}")
                remove(target_path)

                logging.debug(
                    f"Moving {path} to archive at {ARCHIVE_DIRECTORY}{file_name}"
                )
                client.move(path, f"{ARCHIVE_DIRECTORY}{file_name}", True)

            else:
                logging.error(f"Couldn’t download {path}")

        # And now we wait for a moment
        sleep(15)
