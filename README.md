python_memory_module_import
===========================

Python Memory Module Loader

This library give a way to import a module or package from memory

Usage
-----

The two main functions are get_modules_meta_paths and get_module_meta_path.
The first one iterates over an iterable (containing tuples as wanted by get_module_meta_path), calls the other one and yields results.

The second one takes a tuple of 2 elements:

(FORMAT, CONTENT)

CONTENT is a Base64 encoded string representing a zip, tar, tar.gz, tar.bz2 or python file

FORMAT can be one of: 'zip', 'tar', 'tar:gz', 'tar:bz' or string.
    if the last option is given the CONTENT will be treated as plain python file and the FORMAT string will be used as module name

The return value is a Finder that needs to be appended to sys.meta_path

Examples
--------

The examples folder contains a module where 2 modules are defined as variables:

MODULE_COLORIZE: 'tar:gz'

A_MODULE_MYTEST: 'testmodule'

For an usage example look at the __main__ section of the memory_module_loader.py file
