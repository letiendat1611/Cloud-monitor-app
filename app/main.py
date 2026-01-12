from fastapi import FastAPI, Depends
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import SubscriptionClient
from app.models import VMResource, Base, engine, SessionLocal
from sqlalchemy.orm import Session

from datetime import datetime

app = FastAPI(title="Simple Azure Monitor")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables on startup (dev only)
Base.metadata.create_all(bind=engine)

@app.get("/vms")
def get_vms(db: Session = Depends(get_db)):
    try:
        credential = DefaultAzureCredential()
        sub_client = SubscriptionClient(credential)
        subscription = next(sub_client.subscriptions.list())
        sub_id = subscription.subscription_id

        compute_client = ComputeManagementClient(credential, sub_id)
        
        vms = []

        for vm in compute_client.virtual_machines.list_all():
            status = "Unknown"
            if vm.instance_view and vm.instance_view.statuses:
                for s in vm.instance_view.statuses:
                    if "PowerState" in s.code:
                        status = s.display_status
                        break
            
            vm_data = {
                "name": vm.name,
                "resource_group": vm.id.split("/")[4],
                "location": vm.location,
                "status": status,
                "size": vm.hardware_profile.vm_size if vm.hardware_profile else "N/A"
            }
            vms.append(vm_data)

            # Save to DB
            db_vm = VMResource(
                name=vm.name,
                resource_group=vm_data["resource_group"],
                location=vm.location,
                status=status,
                size=vm_data["size"],
                fetched_at=datetime.now()
            )
            db.add(db_vm)

        db.commit()  # Save all at once

        return {
            "success": True,
            "subscription_id": sub_id,
            "total_vms": len(vms),
            "vms": vms
        }
    
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}

@app.get("/vms/db")
def get_vms_from_db(db: Session = Depends(get_db)):
    db_vms = db.query(VMResource).all()
    return {
        "total_stored": len(db_vms),
        "vms": [
            {
                "name": vm.name,
                "resource_group": vm.resource_group,
                "location": vm.location,
                "status": vm.status,
                "size": vm.size,
                "fetched_at": vm.fetched_at
            } for vm in db_vms
        ]
    }