import contextlib
import datetime
import json


class Meta:
    Title = 'title'
    Artist = 'artist'
    Year = 'year'
    Comment = 'comment'


class WeSing:
    def __init__(self, src):
        self._src = src
        self._data = None

    def get_meta(self):
        meta = {}
        try:
            data = self._extract_data()
            detail = data['detail']
        except KeyError:
            pass
        else:
            song_name = detail.get('song_name')
            if song_name:
                meta[Meta.Title] = song_name

            author = detail.get('nick')
            if author:
                meta[Meta.Artist] = author

            ctime = detail.get('ctime')
            with contextlib.suppress(Exception):
                year = datetime.date.fromtimestamp(ctime).year
                meta[Meta.Year] = str(year)

            content = detail.get('content')
            if content:
                meta[Meta.Comment] = content

        return meta

    def get_cover(self):
        data = self._extract_data()
        return data['detail']['cover']

    def get_music_url(self):
        try:
            return self._extract_data()['detail']['playurl']
        except KeyError:
            return

    def _extract_data(self):
        """
        {"shareid":"rz0rtglrkEYIpla3","isPcQQMusic":false,"nohref":false,"detail":{"activity_id":0,"avatar":"http://p.qpic.cn/wsinghead/2100829728/2100829728/100","client_key":"","comment_num":0,"content":"","cover":"https://y.gtimg.cn/music/photo_new/T002R500x500M000004GArUe26PXvZ.jpg?max_age=2592000","ctime":1508461315,"f_lat":"0","f_lon":"00","fb_cover":"https://y.gtimg.cn/music/photo_new/T002R300x300M000004GArUe26PXvZ.jpg?max_age=2592000","file_mid":"002NaDd93srdHz","flower_num":0,"gift_num":0,"hc_avatar":"","hc_level":0,"hc_nick":"","hc_second_sing_count":0,"hc_ugcid_half":"","hc_uid":"669c9982242a368b3d4a","iHasCp":0,"is_anonymous":0,"is_segment":0,"kg_nick":"Wilson","ksong_mid":"003BRxnX4bD3fu","lSongMask":0,"level":3,"mapAuth":{"0":""},"nick":"Wilson","play_num":8,"playurl":"http://ws.stream.kg.qq.com/szkge/4c8a1b1fdb3df38dc25b71b4512552977b7ff5c9?ftnrkey=c47cae3aaaf226cd3a140b6b592ad425c1dd02b25fe64372939d7ba7dd3ab53b556f0ecece6e51ede3aae4adada9b6e86d0fd5e425de2e81c6d1fa437d7efa38&vkey=E781387579518871F86F53D047694DC4508CCFD4D9EACAD8FB7270324FF66F464524EE16EB757F91D8E756D785BC1F1EFADC376CAAA2ED305A7D597DBCA05E58559D9142BCCF7F4D1972D27595C6D8BB2DEA60F6FD516E60&fname=82_afe744ec35033fc6567e47ef80f9fafc5981b0ac.48.m4a&fromtag=1000&sdtfrom=v1000","playurl_video":"","poi_id":"","score":2774,"scoreRank":6,"segment_end":200451,"segment_start":0,"sentence_count":28,"singer_mid":"004WgCsE3KBddt","singer_name":"陈粒","song_name":"易燃易爆炸","tail_name":"iPhone 5","total":4294967295,"ugc_id":"","ugc_mask":0,"ugctype":0,"uid":"609c9d852d2f3e8c3646","comments":[],"flower":[],"photos":[]},"lyric":null,"bullet":null,"share":{"title":"易燃易爆炸","link":"https://wesingapp.com/play?s=rz0rtglrkEYIpla3&lang=en","content":"Wilson that you sing 易燃易爆炸 is great. Listen to it (from WeSing, download it immediately)( WeSing, a social KTV community https://c.y.qq.com/r/8zQU )","img_url":"https://y.gtimg.cn/music/photo_new/T002R300x300M000004GArUe26PXvZ.jpg?max_age=2592000"},"langType":"en","lang":{"bullet":"Bullet screen","scan_follow":"Scan to follow me","introduce":"In WeSing, you can view song details and interact","alert_title":"Bullet screen title","close":"Close","qrcode":"QR code","share_tit_s":" that you sing ","share_tit_e":" is great. Listen to it (from WeSing, download it immediately)","seo_tit_s":" has recorded the song, ","seo_tit_e":", on WeSing. Download the application now to compete with your friends for the championship!","view_detail":"View song details","view_more_comment":"View more comments","send_flower":"Send flowers to the publisher","share_to":"Shared to: ","qzone":"QZone","weibo":"Sina Weibo","wechat_scan":"Scan with WeChat and share it on Moments","qiangshafa":"You've only got one chance to get the sofa","gift_rank":"Gift ranking","no_data_hint":"The song does not exist or has been removed","share_intro":"WeSing, a social KTV community","musicerr_hint":"Play errors. Refresh to rfeplay","open":"Open","download":"Download","use_browser":"Open this page with the browser to use the function","yesterday":"Yesterday","today":"Today","comments":"Comments","singer_count":" Users Sung","want_sing":"Go to Sing","open_see_more":"Open sing this song","download_see_more":"Download sing this song","open_see_more_comment":"Open view more comments","download_see_more_comment":"Download view more comments","more_songs":"More Songs","want_your_comment":"Your comment","send_comment":"Send","register_flower":"Received 10 flowers for join WeSing","give_flower":"You could send some flowers to your friends!","recieve_flower":"Receive","comment_success":"Success","download_see_friends_comment":"Download view your friends reply!","dowload_now":"Download now","none_flower":"No flowers","download_get_flower":"Download get more flowers!","follow":"follow","retry":"Server error, please try later.","confirm":"OK","comment_max_length":"Comments can not exceed 140 characters.","login":"Login information is invalid, please login"},"wxlogined":false,"code":"","rawCode":0,"rawMessage":"commlogin fail uin error.","isMV":false}
        """
        if not self._data:
            _1 = self._src[self._src.index('window.__DATA__'):]
            _2 = _1[:_1.index('</script>')]
            json_str = _2[_2.find('{'):_2.rfind('}') + 1]
            self._data = json.loads(json_str)

        return self._data
