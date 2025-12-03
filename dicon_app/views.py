
from django.views.generic import ListView, DetailView, CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy # リダイレクト先を指定するためにインポート
from .models import Customer
from .forms import CustomerForm # 作成したフォームをインポート
from django.contrib.auth.mixins import LoginRequiredMixin # 11/26インポート
from django.db.models import Q # 12/3インポート

# ---------1126入力→作成したすべてのCBV５つにLoginRequiredMixin, を追加（先に書くのが慣例）
  
# 顧客一覧を表示するビュー（ListViewを継承）   
class CustomerListView(LoginRequiredMixin, ListView):
    
    model = Customer # 1. どのモデルのデータを取得するか
    template_name = 'dicon_app/customer_list.html' # 2. どのテンプレートファイルを使うか
    context_object_name = 'customers' # 3. テンプレート内で使う変数名（指定なしは'object_list'になる）
    paginate_by = 10# おまけ: 1ページに表示する件数（ページネーション）

    # おまけ: 並び順の指定（会社名順）
    #queryset = Customer.objects.all().order_by('company_name')

    # # このメソッドをオーバーライド（追記）
    # def get_queryset(self): # ログインしているユーザー(self.request.user)が担当する
    #     return Customer.objects.filter(user=self.request.user).order_by('company_name') # 顧客データのみを会社（名）で取得する
    # 1203修正のためコメアウト

    def get_queryset(self):
        #1. まず、基本となる「自分の担当顧客」を取得（第５回目の内容）
        queryset = Customer.objects.filter(user=self.request.user).order_by('company_name')

        #2. GETパラメータから　'query'（検索キーワード）を取得
        query = self.request.GET.get('query')

        #3. キーワードが存在する場合のみ絞り込みを行う
        if query:
            # Qオブジェクトを使って「OR条件」を構築
            # icontains は　「大文字小文字を区別しない部分一致」
            queryset = queryset.filter(
                Q(company_name__icontains=query) |
                Q(contact_name__icontains=query) |
                Q(email__icontains=query)
            ) 
        return queryset
    
    # ▼検索キーワードをテンプレートに返すための設定（UX向上）
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # テンプレートの value="{{ query }}" にわたす値を設定
        context['query'] = self.request.GET.get('query', '')
        return context
    
# 顧客詳細ページ用のビュー
class CustomerDetailView(LoginRequiredMixin, DetailView):
    
    # 顧客詳細を表示するビュー（DetailViewを継承）
    
    # 1. どのモデルのデータを取得するか
    model = Customer
    # 2. どのテンプレートファイルを使うか
    template_name = 'dicon_app/customer_detail.html'
    # 3. テンプレート内で使う変数名（指定しない場合、 'object' または 'customer' になる）
    context_object_name = 'customer'
# ---------1119入力
# 11/26：各メソッドをオーバーライド（追記）
    # このメソッドをオーバーライド（追記）
    def get_queryset(self):
        # 自分が担当のデータのみを対象とする
        return Customer.objects.filter(user=self.request.user)

# 顧客の新規登録ビュー
class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'dicon_app/customer_form.html' # 新規も更新も同じテンプレートを使い回す
    success_url = reverse_lazy('customer_list') # 成功したら一覧ページにリダイレクト

        # このメソッドをオーバーライド（11/26追記）
    def form_valid(self, form):
        # フォームが保存される直前に、担当営業（user）フィールドに
        # 現在ログインしているユーザー(self.request.user)をセットする
        form.instance.user = self.request.user

                # 親クラス（CreateView）のform_validを呼び出し、保存処理を続行
        return super().form_valid(form) 

# 顧客の更新ビュー
class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'dicon_app/customer_form.html' # 新規も更新も同じテンプレートを使い回す
    success_url = reverse_lazy('customer_list') # 成功したら一覧ページにリダイレクト
    # <int:pk> で渡されたIDの顧客データを自動でフォームにセットしてくれる

    # このメソッドをオーバーライド（11/26追記）
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'dicon_app/customer_confirm_delete.html' # 削除確認用の専用テンプレート
    success_url = reverse_lazy('customer_list') # 成功したら一覧ページにリダイレクト

    # このメソッドをオーバーライド（11/16追記）
    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)