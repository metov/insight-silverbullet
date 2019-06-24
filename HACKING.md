# Development guide
## Configurations
Currently, configuration management follows a very KISS approach of using JSON dictionary stored under `/conf`. The more robust way of handling it would be [configparser](https://docs.python.org/3/library/configparser.html), but this is not currently implemented. When dealing with JSON configs, some important things should be kept in mind:

* Do not delete configs or change the schema without checking for breakage in code that relies on them. If you fail to do this, you will likely get a `KeyError` (the configs are dictionaries serialized as JSON).
* Do not break JSON syntax. If in doubt, don't edit by hand - [let Python handle that](https://docs.python.org/3/library/json.html) for you: Open an interactive shell, load the config with `my_dict = json.load(FILE_HANDLE)`, add your keys (eg. `my_dict['new_config'] = new_val`) and then save it again with `json.dump(my_dict, FILE_HANDLE)`.
* When accessing configs in code, always provide default values such as `my_val = configs_dict.get(key_name, default=default_val)`.
* Always back up configs.
* The naming convention is `CONFIG_NAME.json`. The main reason to have multiple files is so that each cluster can have its own dedicated config for configuration that doesn't concern other clusters.

## Running Web UI locally
The Web UI is expected to run on its own AWS node, where it can access the Cassandra cluster through the internal IP. This is easily permitted by AWS security groups. Cassandra is deliberately not made available to public connections for security reasons.

However, developing web apps is easier if they can be run locally. Instead of opening access to Cassandra's public IP, port forwarding can allow the Web UI to tunnel to Cassandra through SSH.

* Port forward to Cassandra's default port: `peg port-forward cassandra-cluster 1 9042:9042`
* In `cassandra.json`, make sure 'cassandra' .

### Pycharm integration
* Open the project in PyCharm. Go to Run -> Edit Configurations.
* Click + icon to add new Python configuration.
* Enter details:
	* Name: web_ui
	* Script path: Point it to your Flask binary, eg. `/usr/bin/flask` (try `where flask` to see where your flask is)
	* Parameters: `run`
	* Environment variables: Add `FLASK_APP=web_ui.py` (remember that environment variables need to be semicolon-separated)
	* Working directory should be the directory that `web_ui.py` is in.
