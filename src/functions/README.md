# Functions

## Note

To create this environment, run commands like below.

```bash
cd src/functions
func init --worker-runtime node
func extensions install --package Microsoft.Azure.WebJobs.Extensions.SignalRService --version 1.0.0-preview1-10025
func new --language JavaScript --template "HTTP trigger" --name negotiate

# Get a connection string of SignalR Service
SIGNALR_CONNSTR=$(az signalr key list --resource-group ${RESOURCE_GROUP} --name ${PREFIX}-signalr --query "primaryConnectionString" --output tsv)
```

## References

- [Azure Functions SignalR Service bindings | Microsoft Docs](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-signalr-service)
- [Use the Azure storage emulator for development and testing | Microsoft Docs](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-emulator)