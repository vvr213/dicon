
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy # リダイレクト先を指定するためにインポート
from .models import Customer
from .forms import CustomerForm # 作成したフォームをインポート
# ---------1119入力ここから（上記一部除く）
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
# ---------1119入力ここまで
# 顧客の新規登録ビュー
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'dicon_app/customer_form.html' # 新規も更新も同じテンプレートを使い回す
    success_url = reverse_lazy('customer_list') # 成功したら一覧ページにリダイレクト

# 顧客の更新ビュー
class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'dicon_app/customer_form.html' # 新規も更新も同じテンプレートを使い回す
    success_url = reverse_lazy('customer_list') # 成功したら一覧ページにリダイレクト
    # <int:pk> で渡されたIDの顧客データを自動でフォームにセットしてくれる

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'dicon_app/customer_confirm_delete.html' # 削除確認用の専用テンプレート
    success_url = reverse_lazy('customer_list') # 成功したら一覧ページにリダイレクト