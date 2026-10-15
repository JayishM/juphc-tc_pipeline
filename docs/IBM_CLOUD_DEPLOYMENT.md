# IBM Cloud Container Registry (ICR) Deployment Guide

This guide details the procedure for authenticating with IBM Cloud, preparing your Container Registry namespace, and tagging and pushing the Tax Calculator Docker image.

---

## 1. Prerequisites

Before pushing images to IBM Cloud Container Registry, make sure you have:
1. An active **IBM Cloud Account** ([cloud.ibm.com](https://cloud.ibm.com)).
2. **IBM Cloud CLI (`ibmcloud`)** installed on your workstation.
3. The **Container Registry plugin (`container-registry`)** installed.
4. **Docker** installed and running locally.

---

## 2. Configuration Placeholders Reference

The commands in this guide use the following standardized placeholders. Replace them with your account details:

| Placeholder | Description | Example Value |
|---|---|---|
| `<REGION>` | IBM Cloud target region | `us-south` or `eu-de` |
| `<REGISTRY_HOST>` | IBM Cloud Container Registry endpoint | `us.icr.io` (for us-south) or `de.icr.io` (for eu-de) |
| `<RESOURCE_GROUP>` | IBM Cloud target resource group | `default` |
| `<NAMESPACE>` | Your unique ICR namespace | `sn-labs-yourname` |
| `<IMAGE_NAME>` | Application image name | `tax-calculator` |
| `<IMAGE_TAG>` | Image tag or version identifier | `v1` or `latest` |
| `<API_KEY>` | IBM Cloud IAM API Key | `abC123...XYZ` |

---

## 3. Step-by-Step Execution Workflow

### Step 1: Install IBM Cloud CLI & Plugins

If not already installed on your workstation:

```bash
# macOS (via Homebrew)
brew install ibmcloud

# Or standalone curl installer (Linux / macOS):
curl -fsSL https://clis.cloud.ibm.com/install/osx | sh

# Install Container Registry CLI plugin
ibmcloud plugin install container-registry -r 'IBM Cloud'

# Install Code Engine CLI plugin (for deployment)
ibmcloud plugin install code-engine -r 'IBM Cloud'
```

---

### Step 2: Authenticate with IBM Cloud

Log in using an API key or interactive browser session:

```bash
# Log in using an API Key (recommended for automated/scripted environments)
ibmcloud login --apikey <API_KEY> -r <REGION> -g <RESOURCE_GROUP>

# Interactive login (if working in local desktop terminal)
ibmcloud login -r <REGION> -g <RESOURCE_GROUP>
```

Verify your targeted environment:
```bash
ibmcloud target
```

---

### Step 3: Configure Container Registry Region & Namespace

Set the Container Registry region:

```bash
# Example for us-south: us.icr.io
ibmcloud cr region-set <REGION>
```

Check existing namespaces or create a new dedicated namespace:

```bash
# List existing namespaces
ibmcloud cr namespaces

# Create a new namespace (must be globally unique within the region)
ibmcloud cr namespace-add <NAMESPACE>
```

Verify namespace creation:
```bash
ibmcloud cr namespace-list
```

---

### Step 4: Authenticate Docker with IBM Cloud Container Registry

Authenticate your local Docker daemon to IBM Cloud Container Registry using the CLI helper:

```bash
ibmcloud cr login
```

Expected output:
```text
Authenticating with '<REGISTRY_HOST>'...
SUCCESS: Logged in to '<REGISTRY_HOST>'.
```

---

### Step 5: Tag the Local Docker Image

Tag your local `tax-calculator` image to target your private ICR repository:

```bash
# Tag as version 1 (matches course rubrics)
docker tag <IMAGE_NAME>:latest <REGISTRY_HOST>/<NAMESPACE>/<IMAGE_NAME>:v1

# Also tag as latest for continuous delivery
docker tag <IMAGE_NAME>:latest <REGISTRY_HOST>/<NAMESPACE>/<IMAGE_NAME>:latest
```

Verify the tagged images locally:
```bash
docker images | grep <IMAGE_NAME>
```

---

### Step 6: Push the Image to IBM Cloud Container Registry

Push the tagged container image to ICR:

```bash
docker push <REGISTRY_HOST>/<NAMESPACE>/<IMAGE_NAME>:v1
```

To push the `latest` tag:
```bash
docker push <REGISTRY_HOST>/<NAMESPACE>/<IMAGE_NAME>:latest
```

---

### Step 7: Verify Image in IBM Cloud Container Registry

Verify that the image layers were successfully uploaded and scanned by IBM Cloud Vulnerability Advisor:

```bash
# List all images in your namespace
ibmcloud cr images --restrict <NAMESPACE>

# Inspect vulnerability report
ibmcloud cr va <REGISTRY_HOST>/<NAMESPACE>/<IMAGE_NAME>:v1
```

Expected output format:
```text
Listing images...

Repository                                   Tag   Digest         Namespace     Created        Size     Security status
us.icr.io/<NAMESPACE>/tax-calculator         v1    4a8b7c6d5e4f   <NAMESPACE>   1 minute ago   23.4MB   No Issues
us.icr.io/<NAMESPACE>/tax-calculator         latest 4a8b7c6d5e4f  <NAMESPACE>   1 minute ago   23.4MB   No Issues
```

---

## 4. Troubleshooting Registry Operations

### Error: `unauthorized: authentication required`
- **Fix**: Run `ibmcloud cr login` again. If on a remote machine without Docker daemon socket permissions, generate an ICR IAM token and execute:
  ```bash
  docker login -u iamapikey -p <API_KEY> <REGISTRY_HOST>
  ```

### Error: `The namespace '<NAMESPACE>' does not exist`
- **Fix**: Confirm namespace existence with `ibmcloud cr namespaces` and verify you have targeted the same region (`ibmcloud cr region`).

### Error: `Quota exceeded for repository storage`
- **Fix**: Check ICR quota with `ibmcloud cr plan` and clean up unused images with `ibmcloud cr image-rm <IMAGE_URL>`.
