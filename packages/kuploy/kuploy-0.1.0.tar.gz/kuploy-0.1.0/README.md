# Kuploy - a handy helm3 deployment tool

Kuploy is a wrapper around helm that adds a lot of convenient features. It allows to store everything that is needed to deploy to kubernetes in one place.

## Features

* store chart names and versions along with values into yaml files and deploy from this files
* Verify that the correct kubeconfig is active
* Auto-Select a kube config for a deployment
* Simple and secure secret management
* Install docker secrets before installing a chart
* Apply k8s yamls before/after a chart is installed
* Use local charts and charts from repositories
* Automatically add and refresh chart repositories
* Point to the correct location in a chart in case of an error

## Usage

Deploy all charts from a yaml:

`kuploy mystack.yaml`

## Secret handling

Kuploy creates an AES master key that is stored as secret in kubernetes. Whenever a secret is encrypted or decrypted, the master key is queried from kubernetes. That means that every user with access to a particular kubernetes context is able to encrypt and decrypt secrets.

### Initialize the master key

Create an AES masterkey to encrypt secrets:

`kuploy secrets --context testcluster --init-masterkey`

This allows to create a new master key or to restore a previously generated one. A new master key should be backed up on a secure location (e.g. a password database).

### Encrypt a secret

`kuploy secrets --context testcluster --encrypt`

Queries for a secret and encrypts it. Instead of a secret, a number can be entered to create a random secret and encrypt it.

A secret looks like `<SECRET>+GO41xBf2X7dHtjTk+OTQ7g=`. It can be used as value in a deployment yaml and will be decrypted during deployment.

## Yaml format

```
context: testcluster

charts:
  - name: victoria-metrics-k8s-stack
    namespace: monitoring
    chart:
      repo: https://victoriametrics.github.io/helm-charts/
      name: victoria-metrics-k8s-stack
      version: 0.6.1
    values:
      grafana:
        enabled: false
```

## 