from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Customer,Activity

class CustomerModelTests(TestCase):
    """
    CustomerModelに関するテスト
    """

    def test_is_empty(self):
        """初期状態ではデータが0件であること"""
        saved_customers = Customer.objects.all()
        self.assertEqual(saved_customers.count(), 0)

    def test_create_customer(self):
        """顧客データを1件作成し、正しく保管されるか"""
        # 1. データを作成・保存
        customer = Customer.objects.create(
            company_name ="テスト株式会社",
            contact_name ="テスト　太郎",
            email ="test@example.com"
        )

        # 2. データベースから全件取得
        saved_customers = Customer.objects.all()

        # 3.　検証(Assertion)
        self.assertEqual(saved_customers.count(), 1)# 件数は1件か？
        self.assertEqual(saved_customers[0].company_name, "テスト株式会社" )# 会社名は合っているか？



class CustomerViewTests(TestCase):
    """
    View（画面表示）に関するテスト
    """

    def setUp(self):
        """
        各テストメソッドの実行前に呼ばれる前準備
        ユーザーを作成し、顧客データも1件作っておく
        """
        # テスト用ユーザーを作成
        self.user = User.objects.create_user(username='testuser', password='password')

        # このユーザーが担当する、、、
        self.customer = Customer.objects.create(
            company_name= "自分の担当顧客",
            contact_name= "担当者A",
            email= "a@example.com",
            user=self.user #重要：　illustratorのユーザーに紐づける
        )

        # 別のユーザーを作成（権限確認用）
        self.other_user = User.objects.create_user(username='otheruser', password='password')

    def test_login_required(self):
        """ログインしていない場合"""
        # ログインせずに
        response = self.client.get(reverse('customer_list'))

        # 302
        self.assertEqual(response.status_code, 302)

        # リダイレクト先がログインページ
        self.assertIn('/accounts/login/',response.url)

    def test_logged_in_users_can_see_list(self):
        """ログインユーザーは自分の担当顧客を見られるか"""
        # 1.ログインする
        self.client.force_login(self.user)

        # 2.一覧ページに
        response = self.client.get(reverse('customer_list'))

        # 3.正常に表示される
        self.assertEqual(response.status_code, 200)

        # 4.画面に自分の担当顧客
        self.assertContains(response, "自分の担当顧客")

    def test_cannot_see_others_data(self):
        """ログインユーザーは自分の担当顧客を見られるか"""
        # 1.別のユーザーでログインする　他人のが見えない
        self.client.force_login(self.other_user)

        # 2.一覧ページにアクセス
        response = self.client.get(reverse('customer_list'))

        # 3.200
        self.assertEqual(response.status_code, 200)

        # 4.表示されない
        self.assertNotContains(response, "自分の担当顧客")
        
