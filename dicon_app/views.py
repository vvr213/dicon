from django.views.generic import ListView, DetailView
from .models import Customer

# 顧客一覧ページ用のビュー
class CustomerListView(ListView):
    """
    顧客一覧を表示するビュー（ListViewを継承）
    """
    # 1. どのモデルのデータを取得するか
    model = Customer
    # 2. どのテンプレートファイルを使うか
    template_name = 'dicon_app/customer_list.html'
    # 3. テンプレート内で使う変数名（指定しない場合、 'object_list' になる）
    context_object_name = 'customers'
    # おまけ: 1ページに表示する件数（ページネーション）
    paginate_by = 10
    # おまけ: 並び順の指定（会社名順）
    queryset = Customer.objects.all().order_by('company_name')

# 顧客詳細ページ用のビュー
class CustomerDetailView(DetailView):
    """
    顧客詳細を表示するビュー（DetailViewを継承）
    """
    # 1. どのモデルのデータを取得するか
    model = Customer
    # 2. どのテンプレートファイルを使うか
    template_name = 'dicon_app/customer_detail.html'
    # 3. テンプレート内で使う変数名（指定しない場合、 'object' または 'customer' になる）
    context_object_name = 'customer'