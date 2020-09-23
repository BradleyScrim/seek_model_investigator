from typing import Tuple

DOMAIN_TO_CHECK = "//fairdomhub.org"

MIME_TYPES_YES: Tuple = ("application/sbml+xml",)
MIME_TYPES_MAYBE: Tuple = ("application/xml",
                           "text/xml",)
MIME_TYPES_NO: Tuple = ("namespace",
                        "application/gzip",
                        "application/json",
                        "application/mathematica",
                        "application/matlab",
                        "application/octet-stream",
                        "application/pdf",
                        "application/x-compressed-tar",
                        "application/x-rar",
                        "application/x-ruby",
                        "application/x-tar",
                        "application/xhtml+xml",
                        "application/zip",
                        "image/png",
                        "text/html",
                        "text/plain",
                        "text/x-python",
                        "text/x-uuencode",
                        "text/nlogo",)
