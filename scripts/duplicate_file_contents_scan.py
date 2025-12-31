#!/usr/bin/env python3
import sys
from llm_context.toolbelt import run_from_wrapper

if __name__ == "__main__":
    run_from_wrapper("duplicate-file-contents-scan", sys.argv[1:])
