#!/usr/bin/env python3

"""Générateur de service AVAHI pour Freebox en mode bridge

Lit les informations depuis http://mafreebox.freebox.fr/api_version
Crée un fichier utilisable comme service avahi.

Permet d’utiliser Freebox Compagnon avec une Freebox en mode Bridge :
    https://dev.freebox.fr/bugs/task/22301
"""

import argparse
import sys
import logging
import logging.handlers
import os
import urllib.request, json

logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])

class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass


def parse_args(args=sys.argv[1:]):
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter)
    parser.add_argument("output_file", help="Write to")
    g = parser.add_mutually_exclusive_group()
    g.add_argument("--debug", "-d", action="store_true",
        default=False,
        help="enable debugging")
    g.add_argument("--silent", "-s", action="store_true",
        default=False,
        help="don't log to console")

    return parser.parse_args(args)

def setup_logging(options):
    """Configure logging."""
    root = logging.getLogger("")
    root.setLevel(logging.WARNING)
    logger.setLevel(options.debug and logging.DEBUG or logging.INFO)
    if not options.silent:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(
            "%(levelname)s[%(name)s] %(message)s"))
        root.addHandler(ch)

def get_fbx_params(api_url):
    """Read parms from Freebox API url
    Returns an array of strings"""
    with urllib.request.urlopen(api_url) as url:
        data = json.loads(url.read().decode())
    logger.debug("Downloaded content: {}".format(data))
    params=[]
    for param, value in data.items():
        params.append("{}={}".format(param,value))
    logger.debug("Array of params: {}".format(params))
    return params

def write_to_service_file(file_name,params):
    """Write Avahi service file"""
    with open(file_name,'w') as output:
        output.write("""<service-group>
        <name replace-wildcards="yes">Freebox Server</name>
        <service protocol="ipv4">
                <type>_fbx-api._tcp</type>
                <port>80</port>
                <host-name>mafreebox.freebox.fr</host-name>
""")
        for param in params:
            output.write("                <txt-record>{}</txt-record>\n".format(param))
        output.write("""        </service>
</service-group>""")

if __name__ == "__main__":
    options = parse_args()
    setup_logging(options)

    try:
        logger.debug("Parameters: {}".format(options.output_file))
        fbx_params = get_fbx_params("http://mafreebox.freebox.fr/api_version")
        write_to_service_file(options.output_file,fbx_params)

    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)
