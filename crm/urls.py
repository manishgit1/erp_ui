from django.urls import path
from crm import views

urlpatterns = [
   path('leadQuotation/create', views.LeadQuotationCreateView.as_view(), name='lead-quotation-create'),
   path('leadQuotation/list', views.LeadQuotationListView.as_view(), name='lead-quotation-list'),
   path('leadQuotation/lists', views.LeadQuotationListDataView.as_view(), name='lead-quotation-lists'),
   path('leadQuotation/emiSchedule', views.LeadQuotationEMIScheduleView.as_view(), name='lead-quotation-emi-schedule'),

   path('inquiryFollowUp/list', views.InquiryFollowUpListView.as_view(), name='inquiry-follow-up-list'),
   path('inquiryFollowUp/lists', views.InquiryFollowUpListDataView.as_view(), name='inquiry-follow-up-lists'),

   path('documentUpload/create', views.DocumentUploadCreateView.as_view(), name='document-upload-create'),
   path('documentUpload/upload', views.DocumentUploadUploadView.as_view(), name='document-upload'),

   path('documentApproval/list',views.DocumentApprovalListView.as_view(), name='document-approval-list'),
   path('documentApproval/lists',views.DocumentApprovalListDataView.as_view(), name='document-approval-lists'),
   
   path('approvedDocuments/list',views.ApprovedDocumentsListView.as_view(), name='approved-document-list'),
   path('approvedDocuments/lists',views.ApprovedDocumentsListDataView.as_view(), name='approved-document-lists'),

   path('printModalSearch/search',views.PrintModalSearchListDataView.as_view(), name='print-modal-search'),

   path('documentApproval/rejectApprove/create',views.DocumentApprovalApproveRejectDocumentsView.as_view(), name='document-approval-reject-approve'),
]