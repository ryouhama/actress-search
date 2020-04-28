import json
import requests
from .model.ActressDto import Actress


class SearchActress:

    request_base_url = 'https://api.dmm.com/affiliate/v3/ActressSearch'
    api_id = '0bd369rbPG9mapQSmh7k'
    affiliate_id = 'katopanapp-990'

    def get_init_search_cnd(self):
        # 検索条件
        search_cnd = {
            'initial': None,
            'actress_id': None,
            'keyword': None,
            'gte_bust': None,
            'lte_bust': None,
            'gte_waist': None,
            'lte_waist': None,
            'gte_hip': None,
            'lte_hip': None,
            'gte_height': None,
            'lte_height': None,
            'gte_birshday': None,
            'lte_birthday': None,
            'hits': None,
            'offset': None,
            'sort': None,
            'output': None,
            'callback': None
        }
        return search_cnd


    def create_search_cnd(self, request):

        search_cnd = self.get_init_search_cnd()

        # 取得件数設定
        search_cnd['hits'] = '10'

        # かんたん検索用設定
        if request.POST.get('Easy-App', '0') == '1':

            # キーワード設定
            search_cnd['keyword'] = request.POST.get('kwd', None)

            # バスト設定
            bst = request.POST.get('bst', 'None')
            if 'S' == bst:
                search_cnd['lte_bust'] = '60'
            elif 'M' == bst:
                search_cnd['gte_bust'] = '61'
                search_cnd['lte_bust'] = '90'
            elif 'L' == bst:
                search_cnd['gte_bust'] = '91'

            # 体型設定
            bdy = request.POST.get('bdy', None)
            if 'S' == bdy:
                search_cnd['lte_waist'] = '60'
                search_cnd['lte_hip'] = '60'
                search_cnd['lte_height'] = '145'
            elif 'M' == bdy:
                search_cnd['gte_waist'] = '61'
                search_cnd['gte_hip'] = '61'
                search_cnd['gte_height'] = '146'
                search_cnd['lte_waist'] = '80'
                search_cnd['lte_hip'] = '80'
                search_cnd['lte_height'] = '165'

            elif 'L' == bdy:
                search_cnd['gte_waist'] = '81'
                search_cnd['gte_hip'] = '81'
                search_cnd['gte_height'] = '166'

        # ソート順を指定
        search_cnd['id'] = 'id'

        return search_cnd


    def create_api_url(self, search_cnd):

        # アフェリエイトIDを追加
        api_url = self.request_base_url + '?api_id=' + self.api_id + '&affiliate_id=' +self.affiliate_id

        # 検索条件をURLに展開
        if search_cnd:
            for key, value in search_cnd.items():
                if key and value:
                    search_parameter  = '&' + key + '=' + value
                    api_url = api_url + search_parameter

        # 展開後のURLを返却
        return api_url


    def search_actress(self, request):

        # 検索条件を生成
        search_cnd = self.create_search_cnd(request)

        # API用のURLを生成
        api_url = self.create_api_url(search_cnd)

        response = requests.get(api_url)

        # レスポンスからJSONデータ取得
        json_data = response.json()

        # JSONから検索結果を取得
        json_result = json_data['result']

        # ステータス確認
        if json_result['status'] != '200':
            print('ステータスエラー')
            return None

        # 女優情報を取得
        hit_cnt = json_result['result_count']

        search_result_actress_list = []
        for i in range(hit_cnt):

            # キー値一覧を取得
            json_key_list = []
            for json_key in json_result['actress'][i]:
                json_key_list.append(json_key)

            json_imageUrl_small = None
            json_imageUrl_large = '/static/img/no_img.png'
            if 'imageURL' in json_key_list:
                json_imageUrl_small = json_result['actress'][i]['imageURL']['small']
                json_imageUrl_large = json_result['actress'][i]['imageURL']['large']

            json_listURL_digital = None
            json_listURL_monthly = None
            json_listURL_ppm = None
            json_listURL_mono = None
            json_listURL_rental = None
            if 'listURL' in json_key_list:
                json_listURL_digital = json_result['actress'][i]['listURL']['digital'],
                json_listURL_monthly = json_result['actress'][i]['listURL']['monthly'],
                json_listURL_ppm = json_result['actress'][i]['listURL']['ppm'],
                json_listURL_mono = json_result['actress'][i]['listURL']['mono'],
                json_listURL_rental = json_result['actress'][i]['listURL']['rental']

            # 女優情報を生成
            dto = Actress(id = json_result['actress'][i]['id'],
                          name = json_result['actress'][i]['name'] if 'name' in json_key_list else None,
                          ruby = json_result['actress'][i]['ruby'] if 'ruby' in json_key_list else None,
                          bust = json_result['actress'][i]['bust'] if 'bust' in json_key_list else None,
                          waist = json_result['actress'][i]['waist'] if 'waist' in json_key_list else None,
                          hip = json_result['actress'][i]['hip'] if 'hip' in json_key_list else None,
                          height = json_result['actress'][i]['height'] if 'height' in json_key_list else None,
                          birthday = json_result['actress'][i]['birthday'] if 'birthday' in json_key_list else None,
                          blood_type = json_result['actress'][i]['blood_type'] if 'blood_type' in json_key_list else None,
                          hobby = json_result['actress'][i]['hobby'] if 'hobby' in json_key_list else None,
                          prefectures = json_result['actress'][i]['prefectures'] if 'prefectures' in json_key_list else None,
                          imageURL_small = json_imageUrl_small,
                          imageURL_large = json_imageUrl_large,
                          listURL_digital = json_listURL_digital,
                          listURL_monthly = json_listURL_monthly,
                          listURL_ppm = json_listURL_ppm,
                          listURL_mono = json_listURL_mono,
                          listURL_rental = json_listURL_rental
                          )

            search_result_actress_list.append(dto)

        # 表示用情報をマップに設定
        search_result_map = {'result_count': hit_cnt,
                             'actress_list': search_result_actress_list}

        return search_result_map