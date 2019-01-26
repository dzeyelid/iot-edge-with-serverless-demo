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

## References

### About copyrights

- [Download Microsoft Azure, Cloud and Enterprise Symbol / Icon Set - Visio stencil, PowerPoint, PNG, SVG from Official Microsoft Download Center](https://www.microsoft.com/en-us/download/details.aspx?id=41937)
- [Trademark rules and brand guidelines - Raspberry Pi](https://www.raspberrypi.org/trademark-rules/)