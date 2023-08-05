Pro Custodibus Agent
====================

[Pro Custodibus](https://www.procustodibus.com/) is a service that makes [WireGuard](https://www.wireguard.com/) VPNs easy to deploy and manage. You run the Pro Custodibus agent on your own internal hosts, and the agent monitors and synchronizes your hosts' WireGuard settings with the remote Pro Custodibus service.


Installing
----------

Requires python 3.6 or newer and libsodium. Installer script can install requirements, plus the agent itself, on most linuxes. Install from source like the following:
```
./install.sh --install
```

Or run it like the following to see more options:
```
./install.sh --help
```

See the [Installer Documentation](https://docs.procustodibus.com/guide/agents/install/) for full details.


Development
-----------

### Set up dev env

1. Create a virtualenv with [pyenv](https://github.com/pyenv/pyenv):
```
pyenv virtualenv 3.6.13 procustodibus-agent
```

2. Activate the virtualenv:
```
pyenv local procustodibus-agent 3.6.13 3.7.10 3.8.8 3.9.2
```

3. Install tox:
```
pip install tox
```

4. Install pre-commit and pre-push hooks:
```
tox -e pre-commit install
tox -e pre-commit install -- -t pre-push
```

### Dev tasks

List all tox tasks you can run:
```
tox -av
```

Run unit tests in watch mode:
```
tox -e watch
```

Run all (docker-based) installer tests:
```
docker-compose -f test_install/docker-compose.yml build --pull
tox -e py36 test_install
```

Manually run pre-push hook on all version-controlled files:
```
tox -e pre-commit run -- -a --hook-stage push
```


Resources
---------

* Home page: https://www.procustodibus.com/
* Documentation: https://docs.procustodibus.com/guide/agents/run/
* Changelog: https://docs.procustodibus.com/guide/agents/download/#changelog
* Issue tracker: https://todo.sr.ht/~arx10/procustodibus-agent
* Source code: https://git.sr.ht/~arx10/procustodibus-agent


License
-------

[The MIT License](https://git.sr.ht/~arx10/procustodibus-agent/tree/main/LICENSE)
