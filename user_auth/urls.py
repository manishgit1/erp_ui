from django.urls import path
from .views import (
    LoginView, RegisterView, Logout,
    SettingsMenuView,
    UserSetupListView, UserSetupListDataView,
    UserSetupCreateView,     UserSetupEditView, UserSetupFindByIdAPIView,
    RoleSetupListView, RoleSetupListDataView,
    RoleSetupCreateView,
    RoleSetupEditView, RoleSetupFindByIdAPIView,
    WorkflowSetupListView, WorkflowSetupListDataView, WorkflowSetupCreateView,
)

urlpatterns = [
    # ── Auth ────────────────────────────────────────────────────────────────
    path('user/login', LoginView.as_view(), name='user-login-create'),
    path('user/register', RegisterView.as_view(), name='user-register'),
    path('user/register/create', RegisterView.as_view(), name='user-register-create'),
    path('', LoginView.as_view(), name='user-login'),
    path('user/logout', Logout.as_view(), name='user-logout'),

    # ── Settings Menu ──────────────────────────────────────────────────────
    path('settings/', SettingsMenuView.as_view(), name='settings-menu'),

    # ── User Setup (API proxy) ────────────────────────────────────────────
    path('user/create', UserSetupCreateView.as_view(), name='user-setup-create'),
    path('user/list', UserSetupListView.as_view(), name='user-setup-list'),
    path('user/lists', UserSetupListDataView.as_view(), name='user-setup-lists'),
    path('user/<str:pk>/findById', UserSetupFindByIdAPIView.as_view(), name='user-setup-find-by-id'),
    path('user/<str:pk>/edit', UserSetupEditView.as_view(), name='user-setup-edit'),

    # ── Role Setup (Pages) ────────────────────────────────────────────────
    path('role/create', RoleSetupCreateView.as_view(), name='role-setup-create'),
    path('role/list', RoleSetupListView.as_view(), name='role-setup-list'),
    path('role/lists', RoleSetupListDataView.as_view(), name='role-setup-lists'),
    path('role/<str:pk>/edit', RoleSetupEditView.as_view(), name='role-setup-edit'),
    path('role/<str:pk>/findById', RoleSetupFindByIdAPIView.as_view(), name='role-setup-find-by-id'),

    # ── Workflow Setup ───────────────────────────────────────────────────
    path('workflow/list', WorkflowSetupListView.as_view(), name='workflow-setup-list'),
    path('workflow/lists', WorkflowSetupListDataView.as_view(), name='workflow-setup-lists'),
    path('workflow/create', WorkflowSetupCreateView.as_view(), name='workflow-setup-create'),
]