class BaseHtmlInfo:

    def create_base_html_info(self):
        base_html_info_info = {
            'tittle': '女優検索サイト',
            'logo_url': 'Todo'
        }
        return base_html_info_info

    def get_base_html(self):
        base_html_info_dict = self.create_base_html_info()

        return base_html_info_dict