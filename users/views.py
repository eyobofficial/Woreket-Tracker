from collections import namedtuple

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from shared.constants import ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF, \
    ROLE_SUPPLIER
from purchases.models import Supplier

from .forms import UserForm
from .mixins import BaseUserEditView


User = get_user_model()


class UserListView(BaseUserEditView, ListView):
    template_name = 'users/user_list.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        role = self.request.GET.get('role')
        search_query = self.request.GET.get('search')

        if status is not None:
            qs = qs.filter(status=status)

        if role is not None:
            qs = qs.filter(groups__name=role)

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
        admin_list = self.queryset.filter(groups__name=ROLE_ADMIN)
        management_list = self.queryset.filter(groups__name=ROLE_MANAGEMENT)
        staff_list = self.queryset.filter(groups__name=ROLE_STAFF)
        supplier_list = self.queryset.filter(groups__name=ROLE_SUPPLIER)

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


class UserDetailView(BaseUserEditView, DetailView):
    template_name = 'users/modals/user_detail.html'

    def get_context_data(self, **kwargs):
        kwargs.update(ROLE_SUPPLIER=ROLE_SUPPLIER)
        return super().get_context_data(**kwargs)


class UserUpdateView(BaseUserEditView, UpdateView):
    template_name = 'users/modals/user_form.html'
    form_class = UserForm
    success_url = reverse_lazy('users:user-list')

    def get_context_data(self, **kwargs):
        kwargs.update(role_supplier=Group.objects.get(name=ROLE_SUPPLIER))
        return super().get_context_data(**kwargs)


class UserActivateView(BaseUserEditView, UpdateView):
    template_name = 'users/modals/user_activate.html'
    fields = ('status', )
    success_url = reverse_lazy('users:user-list')


class UserDeactivateView(BaseUserEditView, UpdateView):
    template_name = 'users/modals/user_deactivate.html'
    fields = ('status', )
    success_url = reverse_lazy('users:user-list')
