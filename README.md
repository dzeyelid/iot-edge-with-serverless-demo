# [WIP] IoT Edge with serverless application demonstration

## Purpose

This project purpose is to make a demonstration that is a combination of Azure IoT Edge and serverless architecture like Azure Functions, Azure SignalR Service and static website hosting feature in Azure Storage.

## Overview

![Overall design figure](./docs/images/20190126_watch-iot-edge-online_design-overall.png)

### Technical components

| Components | Description |
|------------|-------------|
| Azure IoT Hub and IoT Edge | Implement module that run on device and manage device status as twins |
| Azure Functions | Relay message from IoT Hub to SignalR Service |
| Azure SignalR Service | Send real-time trigger to a static web application |
| Azure Storage | Host a static web application |
| Azure DevOps | Manage tasks and perform CI/CD |

## Deployment

To deploy and provision resources use Azure CLI. If you do not have it, prepare the environment.

- [Overview of the Azure CLI \| Microsoft Docs](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)

Then make your `.env` file with copying `.env.sample`, rename it to `.env` and update for your environment.

```bash
# Load .env
source .env

# Login to your Azure account
az login

# Create a resource group
az group create \
    --name ${RESOURCE_GROUP} \
    --location ${LOCATION}

# Deploy resources with ARM template
az group deployment create \
  --resource-group ${RESOURCE_GROUP} \
  --template-file src/arm-template/template.json \
  --parameters @src/arm-template/parameters.json

# Provision Storage Accounts to enable static website hosting
az extension add --name storage-preview
STORAGE_NAME=$(az storage account list \
    --resource-group ${RESOURCE_GROUP} \
    --query "[0].name" \
    --output tsv)

az storage blob service-properties update \
    --account-name ${STORAGE_NAME} \
    --static-website \
    --index-document index.html

# Provision each resources

# Hold project root path
PROJECT_ROOT=$(pwd)

# Deploy static web application
cd src/static-web-app
yarn build
az storage blob upload-batch \
    --source dist \
    --destination \$web \
    --account-name ${STORAGE_NAME}

# Show the url of static web application
az storage account show \
    --name ${STORAGE_NAME} \
    --resource-group ${RESOURCE_GROUP} \
    --query "primaryEndpoints.web" \
    --output tsv

# Return to project root directory
cd ${PROJECT_ROOT}
```

## References

### About copyrights

- [Download Microsoft Azure, Cloud and Enterprise Symbol / Icon Set - Visio stencil, PowerPoint, PNG, SVG from Official Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=41937)
- [Trademark rules and brand guidelines - Raspberry Pi](https://www.raspberrypi.org/trademark-rules/)