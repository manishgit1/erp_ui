from django.urls import path
from loan import views
urlpatterns = [
    path('loanRequest/create', views.LoanRequestCreateView.as_view(), name='loan-request-create'),
    path('loanRequest/list', views.LoanRequestListView.as_view(), name='loan-request-list'),
    path('loanRequest/lists', views.LoanRequestListJsonView.as_view(), name='loan-request-lists'),
    path('loanRequest/<str:pk>/findById', views.LoanRequestDataByIdView.as_view(), name='loan-request-data-by-id'),
    path('loanRequest/pending/lists', views.PendingLoansDataView.as_view(), name='loan-request-pending-lists'),
    path('loanRequest/reverted/lists', views.RevertedLoansDataView.as_view(), name='loan-request-reverted-lists'),
    path('loanRequest/rejected/lists', views.RejectedLoansDataView.as_view(), name='loan-request-rejected-lists'),
    path('loanRequest/approved/lists', views.ApprovedLoansDataView.as_view(), name='loan-request-approved-lists'),
    path('loanRequest/disbursed/lists', views.DisbursedLoansDataView.as_view(), name='loan-request-disbursed-lists'),
    path('loanRequest/approve', views.LoanRequestApproveView.as_view(), name='loan-request-approve'),
    path('loanRequest/reject', views.LoanRequestRejectView.as_view(), name='loan-request-reject'),
    path('loanRequest/revert', views.LoanRequestRevertView.as_view(), name='loan-request-revert'),
    path('loanRequest/<str:pk>/timeline', views.LoanRequestTimelineDataView.as_view(), name='loan-request-timeline'),
    path('loanRequest/disburse', views.LoanRequestDisburseView.as_view(), name='loan-request-disburse'),
    path('loanReport/view', views.LoanReportsView.as_view(), name='loan-report-view'),
    path('loanReport/lists', views.LoanReportsDataView.as_view(), name='loan-report-lists'),
]