from django.urls import path
from .views import CustomerListView, CustomerDetailView # 作成したCBVをインポート

urlpatterns = [
    # 顧客一覧ページ
    # path('', ...)はプロジェクトのurls.pyから引き継いだルートURLを指す
    path('', CustomerListView.as_view(), name='customer_list'),
    
    # 顧客詳細ページ
    # <int:pk> はURLの一部（顧客のID）を変数として受け取るという意味
    # 例: /customer/1/, /customer/2/
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
]