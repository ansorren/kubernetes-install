Kubernetes the hard way

required tools:

- cfssl, cfssljson

- python-netaddr

- python-openshift

* build cni plugins *

Build CNI plugins

go get github.com/containernetworking/plugins

./build_linux.sh

set cni_plugins_location variable to point to bin dir
