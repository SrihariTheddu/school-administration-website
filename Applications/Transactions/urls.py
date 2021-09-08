from django.urls import path

from Applications.Transactions.views import (
        PaymentFormView,
        TransactionOnSuccessView,
        TransactionOnFailureView,
        TransactionDetailView,
        FeePaymentCardView,
        FeeStructureView,
        TransactionIndexView
        )
app_name = 'Transactions'

urlpatterns = [


path('Transactions/fee-structure/all/',FeeStructureView.as_view(),name='FeeStructurePage'),

path('Transactions/payment/<slug:pk>/details/',FeePaymentCardView.as_view(),name='FeePaymentCardPage'),


path('Transactions/payment/<slug:pk>/success/',TransactionOnSuccessView.as_view(),name='PaymentOnSuccessPage'),

path('Transactions/payment/<slug:pk>/failure/',TransactionOnFailureView.as_view(),name='PaymentOnFailurePage'),

path('Transactions/payment/<slug:pk>/details/',TransactionDetailView.as_view(),name='TransactionDetailPage'),

path('Transactions/',TransactionIndexView.as_view(),name='TransactionIndexPage'),
]
