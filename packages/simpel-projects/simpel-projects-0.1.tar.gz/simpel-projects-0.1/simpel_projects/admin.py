from django.apps import apps
from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.contenttypes.models import ContentType
from django.forms import modelform_factory
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportMixin
from polymorphic.admin import (
    PolymorphicChildModelAdmin, PolymorphicInlineSupportMixin, PolymorphicParentModelAdmin, StackedPolymorphicInline,
)
from simpel_actions.admin import AdminActivityMixin
from simpel_admin.base import AdminPrintViewMixin, ModelAdminMixin
from simpel_contacts.admin import DeliverableAddressInline

from .backends import convert_salesorder
from .helpers import get_deliverable_childs_models, get_task_childs_models, get_workorder_childs_models
from .models import CancelationDeliverable, Deliverable, DocumentDeliverable, FinalDocument, Task, WorkOrder
from .settings import projects_settings


class TaskPolymorphicInline(StackedPolymorphicInline):
    model = Task

    def get_child_models(self):
        """
        Register child model using defaults from settings
        """
        # Get deliverable child models map from hooks
        child_models = get_task_childs_models()
        child_models += [Task]
        return child_models

    def get_child_inline_classes(self):
        child_models = self.get_child_models()
        child_inlines = []
        for child in child_models:
            class_name = child.__class__.__name__
            props = {"model": child}
            parent_class = (StackedPolymorphicInline.Child,)
            inline_class = type("%sInline" % class_name, parent_class, props)
            child_inlines.append(inline_class)
        return child_inlines

    def get_child_inline_instances(self):
        instances = []
        for ChildInlineType in self.get_child_inline_classes():
            instances.append(ChildInlineType(parent_inline=self))
        return instances


class WorkOrderAdminBase(
    PolymorphicInlineSupportMixin,
    ImportExportMixin,
    AdminPrintViewMixin,
    AdminActivityMixin,
    ModelAdminMixin,
):
    change_list_template = "admin/simpel_projects/workorder_changelist.html"
    inlines = [TaskPolymorphicInline]
    # autocomplete_fields = ["customer"]
    readonly_fields = ["status", "group"]
    search_fields = ["inner_id", "title", "reference_id"]
    actions = [
        "validate_action",
        "complete_action",
    ]
    list_filter = ["status"]
    date_hierarchy = "created_at"
    list_display = [
        "inner_id",
        "reference_id",
        "progress",
        "status",
        "object_buttons",
    ]

    def has_change_permission(self, request, obj=None):
        default = super().has_change_permission(request, obj)
        if obj:
            return obj.is_editable and default
        else:
            return default

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["customer", "reference_type", "reference_id"]
        return super().get_readonly_fields(request, obj)


class PolymorphicWorkOrderAdmin(WorkOrderAdminBase, PolymorphicParentModelAdmin):
    child_models = [WorkOrder]
    parent_include = True

    def get_child_models(self):
        """
        Register child model using defaults from settings

        """
        super_child_models = super().get_child_models()
        child_models = list(super_child_models).copy()
        # Get deliverable child models map from hooks
        child_models = get_workorder_childs_models()

        if len(child_models) == 0:
            child_models = [WorkOrder]
        if self.parent_include and WorkOrder not in child_models:
            child_models += [WorkOrder]
        return child_models

    def convert(self, request):
        """Crate Work Order from Sales Order"""
        if not self.has_add_permission(request):
            messages.error(request, _("You don't have create work order permission!"))
            return redirect(self.get_changelist_url())
        template_name = "admin/simpel_projects/workorder_convert_form.html"
        reference_type = None
        model_name = request.GET.get("ref_type", None)
        if model_name is not None:
            try:
                reference_type = ContentType.objects.get_for_model(apps.get_model(model_name))
            except Exception as err:
                messages.error(request, err)
                return redirect(self.get_changelist_url())
        form_class = modelform_factory(self.model, fields=["reference_type", "reference_id"])
        context = {
            **self.admin_site.each_context(request),
            "title": _("Create Work Order"),
            "cancel_url": self.get_changelist_url(),
        }
        if request.method == "POST":
            form = form_class(request.POST)
            if form.is_valid():
                try:
                    reference = form.instance.reference
                    workorder = convert_salesorder(request, reference)
                    msg = _("Create workorder %s for order %s.") % (workorder, reference)
                    messages.success(request, msg)
                    return redirect(reverse(admin_urlname(workorder._meta, "inspect"), args=(workorder.id,)))
                except Exception as err:
                    messages.error(request, err)
                    return redirect(self.get_inspect_url(workorder.id))
            else:
                context["form"] = form
                return render(request, template_name, context)
        else:
            reference_id = request.GET.get("ref_id", None)
            form = form_class(initial={"reference_type": reference_type, "reference_id": reference_id})
            context["form"] = form
            return render(request, template_name, context)

    def get_urls(self):
        urls = [
            path(
                "convert/",
                self.admin_site.admin_view(self.convert),
                name="%s_%s_convert" % (self.opts.app_label, self.opts.model_name),
            ),
        ]
        urls += super().get_urls()
        return urls


class DeliverablePolymorphicInline(StackedPolymorphicInline):
    model = Deliverable

    def has_change_permission(self, request, obj=None):
        if obj and obj.workorder.status == WorkOrder.VALID and not obj.progress_complete:
            return super().has_change_permission(request, obj)
        else:
            False

    def get_child_models(self):
        """
        Register child model using defaults from settings
        """
        # Get deliverable child models map from hooks
        child_models = get_deliverable_childs_models()
        if len(child_models) == 0:
            child_models = [Deliverable, CancelationDeliverable]
        return child_models

    def get_child_inline_classes(self):
        child_models = self.get_child_models()
        child_inlines = []
        for child in child_models:
            class_name = child.__class__.__name__
            props = {"model": child, "fields": child.formset_fields}
            parent_class = (StackedPolymorphicInline.Child,)
            inline_class = type("%sInline" % class_name, parent_class, props)
            child_inlines.append(inline_class)
        return child_inlines

    def get_child_inline_instances(self):
        instances = []
        for ChildInlineType in self.get_child_inline_classes():
            instances.append(ChildInlineType(parent_inline=self))
        return instances


class TaskAdmin(PolymorphicInlineSupportMixin, ModelAdminMixin):
    search_fields = [
        "inner_id",
        "reference_id",
        "workorder__inner_id",
        "workorder__reference_id",
    ]
    list_display = [
        "inner_id",
        "name",
        "reference",
        "quantity",
        "completes",
        "progress",
    ]
    fields = [
        "position",
        "workorder",
        "reference_id",
        "start_at",
        "end_at",
        "quantity",
    ]

    readonly_fields = fields
    inlines = [DeliverableAddressInline, DeliverablePolymorphicInline]

    # def has_change_permission(self, request, obj=None):
    #     if obj and obj.workorder.status == WorkOrder.VALID and not obj.progress_complete:
    #         return super().has_change_permission(request, obj)
    #     else:
    #         False


class DeliverableAdminBase(ModelAdminMixin):
    search_fields = ["inner_id", "customer__name", "order_item__inner_id"]
    list_display = ["inner_id", "name", "customer"]
    autocomplete_fields = ["task"]
    inspect_template = "admin/simpel_projects/deliverable_inspect.html"


class DeliverableAdmin(DeliverableAdminBase, PolymorphicParentModelAdmin):
    child_models = [CancelationDeliverable, DocumentDeliverable]
    list_display = ["inner_id", "task", "customer", "created_at"]

    def get_child_models(self):
        """
        Register child model using defaults from settings

        """
        super_child_models = super().get_child_models()
        child_models = list(super_child_models).copy()
        # Get deliverable child models map from hooks
        child_models = get_deliverable_childs_models()
        if len(child_models) == 0:
            child_models = [Deliverable, CancelationDeliverable]
        return child_models


class DeliverableChildAdmin(DeliverableAdminBase, PolymorphicChildModelAdmin):
    show_in_index = True


class CancelationDeliverableAdmin(DeliverableChildAdmin):
    list_display = ["inner_id", "customer", "created_at"]


class DocumentDeliverableAdmin(DeliverableChildAdmin):
    list_display = ["inner_id", "customer", "created_at"]


class FinalDocumentAdmin(AdminPrintViewMixin, AdminActivityMixin, ModelAdminMixin):
    print_template = "admin/finaldocument_print.html"
    list_filter = ["status"]
    search_fields = ["inner_id", "workorder__inner_id", "workorder__cunstomer__name"]
    readonly_fields = ["workorder", "user"]
    actions = ["mark_as_complete"]

    def has_add_permission(self, request):
        return False

    def mark_as_complete(self, request, queryset):
        try:
            for obj in queryset:
                obj.complete(request)
            if obj.status == obj.PROCESSED:
                messages.success(request, _("%s complete.") % obj)
        except PermissionError as err:
            messages.error(request, err)


admin.site.register(WorkOrder, projects_settings.WORKORDER_ADMIN)
admin.site.register(Task, projects_settings.TASK_ADMIN)
admin.site.register(Deliverable, projects_settings.DELIVERABLE_ADMIN)
admin.site.register(CancelationDeliverable, projects_settings.CANCELATION_DELIVERABLE_ADMIN)
admin.site.register(DocumentDeliverable, projects_settings.DOCUMENT_DELIVERABLE_ADMIN)
admin.site.register(FinalDocument, projects_settings.FINAL_DOCUMENT_ADMIN)
