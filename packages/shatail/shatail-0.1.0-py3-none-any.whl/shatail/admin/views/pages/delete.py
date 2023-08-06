from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _

from shatail import hooks
from shatail.actions.delete_page import DeletePageAction
from shatail.admin import messages
from shatail.admin.views.pages.utils import get_valid_next_url_from_request
from shatail.models import Page


def delete(request, page_id):
    page = get_object_or_404(Page, id=page_id).specific
    if not page.permissions_for_user(request.user).can_delete():
        raise PermissionDenied

    with transaction.atomic():
        for fn in hooks.get_hooks("before_delete_page"):
            result = fn(request, page)
            if hasattr(result, "status_code"):
                return result

        next_url = get_valid_next_url_from_request(request)

        if request.method == "POST":
            parent_id = page.get_parent().id
            action = DeletePageAction(page, user=request.user)
            # Permission checks are done above, so skip them in execute.
            action.execute(skip_permission_checks=True)

            messages.success(
                request, _("Page '{0}' deleted.").format(page.get_admin_display_title())
            )

            for fn in hooks.get_hooks("after_delete_page"):
                result = fn(request, page)
                if hasattr(result, "status_code"):
                    return result

            if next_url:
                return redirect(next_url)
            return redirect("shatailadmin_explore", parent_id)

    return TemplateResponse(
        request,
        "shatailadmin/pages/confirm_delete.html",
        {
            "page": page,
            "descendant_count": page.get_descendant_count(),
            "next": next_url,
        },
    )
