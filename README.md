# Inservency

**IMPORTANT:** Inservency is currently pre-alpha release, with work starting at the very end of May 2021. It is not yet fully functional. This repository is only public to provide an up-to-date example of my Python programming for potential employers.
When Inservency is ready to be used, this message will be removed and a release will be created.

## What is Inservency?
Inservency is a dedicated graphical server management application for Insurgency: Sandstorm with a focus on small private servers. It features both Windows and Linux versions (macOS is not supported by the I:S binaries).

## Features
 - An easy to use map cycle creator and manager
 - Server settings saved persistently
 - Automatic update handling and server binary installation
 - A GUI for ease of use
 - Many more planned!

## For Developers
Inservency depends on the free version of `fbs`, so the Python version is restricted to <=3.6.

### Installation

1. Ensure you have Python 3.6 downloaded.
2. Clone the code: `git clone git@github.com:nstgeorge/Inservency.git`
3. `cd Inservency`
4. Create a venv: `python3 -m venv ./venv`
5. Install dependencies: `pip install -r requirements.txt`
6. (Optional): If using PyCharm (highly recommended), `src/main/python` should be marked as a sources folder automatically. If it isn't, do that now.

### Running the Project

As mentioned before, this project depends on `fbs`, which will handle packaging and installation in the future. For now, you can run the project using the command `fbs run`. If using PyCharm, there may be a run config called "FBS Run" which will run this command, but if it's not created, the following steps will create it:

1. Create a new run configuration.
2. Select "Shell Script" as the configuration type.
3. Change the "Execute" option to "Script text."
4. Set the script text to `fbs run`
