from django.views.generic import TemplateView
from django.shortcuts import render
from .actressSrch import SearchActress
from .base import BaseHtmlInfo
import cgi

class TopView(TemplateView):
    """
    :tittle TOPページVIew
    :Note   TOPページ作成用のView情報を作成する
    """

    # 表示テンプレートページ
    template_name = 'top.html'

    def get_context_data(self, **kwargs):
        """
        コンテキストデータ取得
        :Override
        :param kwargs:
        :return: コンテキスト
        """

        # ベース情報を取得
        base_info = BaseHtmlInfo()
        base_html_info =  base_info.get_base_html()

        # コンテキスト情報を取得
        context = super().get_context_data(**kwargs)
        # コンテキスト情報を設定
        context['base'] = base_html_info
        return context


def search_action_and_send_list(request):
    """
    検索処理
    :Note  POST情報からAPIをキックし、検索結果を取得する。
           一覧ページに繊維させる。

    :param request:
    :return: コンテキスト
    """
    template_name = 'list.html'

    # ベース情報を取得
    base_info = BaseHtmlInfo()
    base_html_info = base_info.get_base_html()

    # コンテキスト情報を生成
    context = {'base': base_html_info}

    if request.method == 'POST':
        sa = SearchActress()
        search_actress = sa.search_actress(request)

        # 検索結果をコンテキストに展開
        for key, value in search_actress.items():
            context.setdefault(key, value)

    return render(request, template_name, context)