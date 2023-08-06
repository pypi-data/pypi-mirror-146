# JS Runner
Run JavaScript From Python.

# Installing

```
pip3 install py_js_runner
```

# How To Use

## Note

py_js_runner Uses Node.JS To Run JavaScript Code.

So Make Sure Node.JS Is Installed.

## JavaScript
```python
import py_js_runner

# Check If Node.JS Is Installed.

py_js_runner.javascript().check_node() # Gives Error If Not Installed.

# Run JavaScript

py_js_runner.javascript().run("""
// Some JavaScript Comments.
// Blah Blah
// Print Someting
console.log('hello from javascript with python!');

// Some More JavaScript Comments.
// Blah Blah""")
```

# NPM
```python
import py_js_runner

# Check If NPM Is Installed.

py_js_runner.npm().check_npm() # Gives Error If Not Installed.

# Command Line Arguments For NPM

# This Line Will Execute: npm help
py_js_runner.npm().npm_cli("help")

# Check If A NPM Package.
print(py_js_runner.npm().check_if_npm_package()) # Returns Boolean.

# You Can Also Specify Directory To Check If A NPM Package.
print(py_js_runner.npm().check_if_npm_package("./somedirectory"))

# Create NPM Package
py_js_runner.npm().init_npm_package("MY_HELPFUL_PACKAGE_NAME")

# Default Parameters:
# license: str = "MIT"
# author: str = ""
# description: str = ""
# version: str = "1.0.0"
# main: str = "index.js"
# npm_package_path: str = "./"

# Install Packages
py_js_runner.npm().install_packages("nodemon vite")

# Run: npm install
py_js_runner.npm().install()

# Uninstall Packages
py_js_runner.npm().uninstall("nodemon vite")

# Remove NPM Package.
py_js_runner.npm().remove_npm_package() # You Can Specify Path.
```