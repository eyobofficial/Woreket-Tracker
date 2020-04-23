from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.generic import ListView, DetailView

from shared.constants import ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF, \
    ROLE_SUPPLIER
from .mixins import BaseUsersView


User = get_user_model()


class UserListView(BaseUsersView, ListView):
    template_name = 'users/user_list.html'
    model = User
    queryset = User.objects.filter(is_superuser=False, is_active=True)
    paginate_by = 10
    access_roles = [ROLE_ADMIN]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(pk=self.request.user.pk)

        status = self.request.GET.get('status')
        role = self.request.GET.get('role')
        search_query = self.request.GET.get('search')

        if status is not None:
            qs = qs.filter(status=status)

        if role is not None:
            qs = qs.filter(role__name=role)

        if search_query is not None:
            search_query = search_query.strip()
            qs = self.get_search_result(search_query)

        return qs.order_by('status')

    def get_context_data(self, **kwargs):
        # status
        status = self.request.GET.get('status')
        all_count = self.queryset.count()
        pending_list = self.queryset.filter(status=User.PENDING)
        active_list = self.queryset.filter(status=User.ACTIVE)
        disabled_list = self.queryset.filter(status=User.DISABLED)

        # Role
        role = self.request.GET.get('role')
        admin_list = self.queryset.filter(role__name=ROLE_ADMIN)
        management_list = self.queryset.filter(role__name=ROLE_MANAGEMENT)
        staff_list = self.queryset.filter(role__name=ROLE_STAFF)
        supplier_list = self.queryset.filter(role__name=ROLE_SUPPLIER)

        kwargs.update({
            # Status
            'selected_status': status,
            'all_count': all_count,
            'pending_count': pending_list.count(),
            'active_count': active_list.count(),
            'disabled_count': disabled_list.count(),

            # Status Constants
            'PENDING': User.PENDING,
            'ACTIVE': User.ACTIVE,
            'DISABLED': User.DISABLED,

            # Role
            'selected_role': role,
            'admin_count': admin_list.count(),
            'management_count': management_list.count(),
            'staff_count': staff_list.count(),
            'supplier_count': supplier_list.count(),

            # Role Constants
            'ROLE_ADMIN': ROLE_ADMIN,
            'ROLE_MANAGEMENT': ROLE_MANAGEMENT,
            'ROLE_STAFF': ROLE_STAFF,
            'ROLE_SUPPLIER': ROLE_SUPPLIER
        })
        return super().get_context_data(**kwargs)

    def get_search_result(self, query):
        """Returns a user queryset using search query."""
        search_qs = self.queryset.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
        return search_qs


class UserDetailView(BaseUsersView, DetailView):
    template_name = 'users/modals/user_detail.html'
    model = User
    queryset = User.objects.filter(is_active=True, is_superuser=False)
    access_roles = [ROLE_ADMIN]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(pk=self.request.user.pk)
        return qs

    def get_context_data(self, **kwargs):
        kwargs.update(ROLE_SUPPLIER=ROLE_SUPPLIER)
        return super().get_context_data(**kwargs)
