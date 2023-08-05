from actstream import action
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from simpel_contacts.models import DeliverableAddress

from .models import Task, WorkOrder


def convert_salesorder(request, reference):
    # Check if sales order valid to process
    with transaction.atomic():
        workorder = WorkOrder(
            user=request.user,
            group=reference.group,
            customer=reference.customer,
            reference=reference,
            title=_("%s Work Order for %s") % (reference.group, reference),
            content=reference.note,
        )
        workorder.save()

        # Add work order task
        for item in reference.items.filter(product__group=reference.group):
            task = Task(
                workorder=workorder,
                name=item.name,
                reference=item,
                quantity=item.quantity,
                note=item.note,
            )
            task.save()
            # Add deliverable Information
            deliverable_info = getattr(item, "deliverable_informations", None)
            if deliverable_info is not None:
                try:
                    delinfo = deliverable_info.first() or reference.customer.address
                    delinfo_dict = delinfo.to_dict()
                    delinfo_dict.pop("address_type", None)
                    delinfo_dict.pop("primary", None)
                    if delinfo_dict.get("phone_number", None):
                        phone = reference.customer.contacts.first()
                        delinfo_dict["phone_number"] = None if phone is None else phone.contact
                    task_delinfo = DeliverableAddress(content=task, **delinfo_dict)
                    task_delinfo.save()
                except Exception as err:
                    print(err)
        action.send(
            request.user,
            verb="create %s" % workorder._meta.verbose_name,
            action_object=workorder,
            target=reference,
        )
        return workorder
