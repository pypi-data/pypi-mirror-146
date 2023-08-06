==========
gocd-tools
==========

A tool for automating the configuration of a `GoCD <https://www.gocd.org>`_ server.

It achieves this by utilizing the published `GoCD API <https://api.gocd.org/current/#introduction>`_ specification.

---------------
Getting Started
---------------

Before the ``gocd-tool`` can be used, it has to be built and installed.
To accomplish this, use the following make workflow.

To build the image, simply use make in the root of the repo directory::

    $ make
    python3 -m venv venv
    venv/bin/python -m pip install --upgrade pip setuptools wheel
    ...
    => exporting to image                                                                                                                          0.1s
    => => exporting layers                                                                                                                         0.1s
    => => writing image sha256:ca6354050605d70eba222536fb2155ae75db734e1191020d68a42742f9e658a9                                                    0.0s
    => => naming to docker.io/ucphhpc/gocd-tools:edge                                                                                              0.0s

    $ make install
    /Library/Developer/CommandLineTools/usr/bin/make install-dep
    venv/bin/pip install -r requirements.txt
    Requirement already satisfied: requests in ./venv/lib/python3.10/site-packages (from -r requirements.txt (line 1)) (2.27.1)
    ...
    Successfully built gocd-tools
    Installing collected packages: gocd-tools
    Attempting uninstall: gocd-tools
        Found existing installation: gocd-tools 0.0.1a3
        Uninstalling gocd-tools-0.0.1a3:
        Successfully uninstalled gocd-tools-0.0.1a3
    Successfully installed gocd-tools-0.0.1a3

-------
Support
-------

Currently, the tool supports configuring the follow aspects.

    * `Artifacts Config <https://api.gocd.org/current/#artifacts-config>`_
    * `Cluster Profiles <https://api.gocd.org/current/#cluster-profiles>`_
    * `Config Repo <https://api.gocd.org/current/#config-repo>`_
    * `Elastic Agent Profiles <https://api.gocd.org/current/#elastic-agent-profiles>`_
    * `Pipeline Group Config <https://api.gocd.org/current/#pipeline-group-config>`_
    * `Roles <https://api.gocd.org/current/#roles>`_
    * `Secret Configs <https://api.gocd.org/current/#secret-configs>`_
    * `Template Config <https://api.gocd.org/current/#template-config>`_

-------------
Configuration
-------------

The ``gocd-tools`` configures the targeted GoCD server via YAML config files.

These configuration files are by default expected to be located in the current user's ``~/.gocd-tools/config`` directory.


    -rw-r--r--   1 user  staff    100 13 Apr 14:38 artifacts_config.yml
    -rw-r--r--   1 user  staff    328 13 Apr 14:38 cluster_profiles.yml
    -rw-r--r--   1 user  staff   1595 13 Apr 14:38 elastic_agent_profiles.yml
    -rw-r--r--   1 user  staff    438 13 Apr 14:38 pipeline_group_configs.yml
    -rw-r--r--   1 user  staff   5141 13 Apr 14:38 repositories.yml
    -rw-r--r--   1 user  staff    237 13 Apr 14:38 roles.yml
    -rw-r--r--   1 user  staff   1107 13 Apr 14:38 secret_managers.yml
    -rw-r--r--   1 user  staff  18267 13 Apr 14:38 templates.yml

To specify which server should be configured, and how the tool should authenticate against that server the tool currently relies on environment variables.
Namely the ``GOCD_BASE_URL`` and the ``GOCD_AUTH_TOKEN`` environment variables.

Therefore they should be set in the current shell before the targeted server is attempted to be configured::

    export GOCD_BASE_URL=https://url-to-the-gocd-server
    export GOCD_AUTH_TOKEN=`Your Personal Access Token <https://docs.gocd.org/current/configuration/access_tokens.html>`_

-----
Usage
-----

After installation and the required configuration, the tool can be used by calling the `gocd-tools` command::

    $ gocd-tools -h
    usage: gocd-tools [-h] {setup} ...

    options:
    -h, --help  show this help message and exit

    COMMAND:
    {setup}

Thereby, the supported commands can be discovered through the defined CLI, for example::

    $ gocd-tools setup -h
    usage: gocd-tools setup [-h] {secrets,server} ...

    options:
    -h, --help        show this help message and exit

    COMMAND:
    {secrets,server}


    $ gocd-tools setup server -h
    usage: gocd-tools setup server [-h] {init,configure,cleanup} ...

    options:
    -h, --help            show this help message and exit

    COMMAND:
    {init,configure,cleanup}


For instance, to configure and subsequent cleanup a server, the following commands should be used::

    $ gocd-tools setup server init
    Init server: https://url-to-the-gocd-server
    Failed to find: 401:{
    "message": "You are not authenticated!"
    }
    {
        "msg": "The Authorization config for: https://ci.erda.dk was completed",
        "status": "success"
    }

    $ gocd-tools setup server configure
    Authenticate
    Setup Roles
    Failed to find: 404:{"message":"Role with name \u0027manager\u0027 was not found!"}
    Creating: manager
    ...
    {
        "msg": "Succesfully configured the https://url-to-the-gocd-server endpoint",
        "status": "success"
    }

    $ gocd-tools setup server cleanup
    Authenticate
    Delete Config Repositories
    ...
    Delete Roles
    Removing: manager
    {
        "msg": "Succesfully finished the cleanup of endpoint: https://url-to-the-gocd-server",
        "status": "success"
    }

