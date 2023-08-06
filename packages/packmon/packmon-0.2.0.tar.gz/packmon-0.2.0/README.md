packmon is a cli tool to monitor aging packages in order to see if somes become obsolete
or updates are availables.


# Philosophy

As a simple monitoring tool, packmon is pure-python in order to simplify its use.


# Usage

1. Install packmon globally on your system
2. Use it to detect obsolescence and vulnerabilities in any of your project (virtual
    environment or not)


## Example

System level :

    pip install packmon

Then :

    packmon myproject/requirements.txt
    pip freeze |packmon
    curl -s https://raw.githubusercontent.com/AFPy/Potodo/master/requirements.txt |packmon

Result :

