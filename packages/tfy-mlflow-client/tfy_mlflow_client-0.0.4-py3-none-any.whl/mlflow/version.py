# Copyright 2018 Databricks, Inc.
import re

VERSION = "0.0.4"


def is_release_version():
    return bool(re.match(r"^\d+\.\d+\.\d+$", VERSION))
