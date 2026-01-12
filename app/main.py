from fastapi import FastAPI
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import SubscriptionClient

app = FastAPI(title="Simple Azure Monitor")

@app.get("/vms")
def get_vms():
    try:
        credential = DefaultAzureCredential()
        sub_client = SubscriptionClient(credential)
        subscription = next(sub_client.subscriptions.list())
        sub_id = subscription.subscription_id

        compute_client = ComputeManagementClient(credential, sub_id)
        
        vms = []
        for vm in compute_client.virtual_machines.list(resource_group_name='MonitorApp'):
            status = "Unknown"
            if vm.instance_view and vm.instance_view.statuses:
                # Find the power state
                for s in vm.instance_view.statuses:
                    if "PowerState" in s.code:
                        status = s.display_status
                        break
            
            vms.append({
                "name": vm.name,
                "resource_group": vm.id.split("/")[4],
                "location": vm.location,
                "status": status,
                "size": vm.hardware_profile.vm_size if vm.hardware_profile else "N/A"
            })
        
        return {
            "success": True,
            "subscription_id": sub_id,
            "total_vms": len(vms),
            "vms": vms
        }
    
    except Exception as e:
        return {"success": False, "error": str(e)}