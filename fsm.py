from os import times_result
from transitions.extensions import GraphMachine
from linebot import LineBotApi, WebhookParser
from utils import send_multi_image,send_text_message, send_carousel_message, send_button_message, send_image_message,send_button_carousel,send_image_and_text_message
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction,CarouselColumn
from bs4 import BeautifulSoup
import requests


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_intro(self, event):
        text = event.message.text
        return (text.lower() == '介紹' or text.lower() == 'back')

    def on_enter_intro(self, event):
        title = '介紹'
        text = '請選擇你想知道的資訊'
        btn = [
            MessageTemplateAction(
                label = '簡介',
                text ='簡介'
            ),
            MessageTemplateAction(
                label = '特色',
                text = '特色'
            ),
            MessageTemplateAction(
                label = '新手',
                text ='新手'
            ),
        ]
        url = 'https://cdn2.ettoday.net/images/4215/4215808.jpg'
        send_button_message(event.reply_token, title, text, btn, url)


    def is_going_to_summary(self, event):
        text = event.message.text
        if text == '簡介':
            return True
        return False

    def on_enter_summary(self, event):
        send_text_message(event.reply_token, '《傳說對決》是一款多人在線戰術競技遊戲，又稱為MOBA遊戲以第三人稱視角進行。 玩家需要選擇一位「英雄」進行操控，並且這些英雄各自都有不同的技能。 英雄初始等級1級，透過玩家對線（擊殺小兵），擊殺敵人、野怪以進行招式升級也可以在裝備商店購買適當的裝備讓自己的角色變強。')

    def is_going_to_feature(self, event):
        text = event.message.text
        if text == '特色':
            return True
        return False

    def on_enter_feature(self, event):

        url1 = 'https://moba.garena.tw/img/page/synopsis_banner_2.jpg'
        url2 = 'https://moba.garena.tw/img/page/synopsis_banner_3.jpg'
        url3 = 'https://moba.garena.tw/img/page/synopsis_banner_4.jpg'
        url4 = 'https://moba.garena.tw/img/page/synopsis_banner_5.jpg'

        send_multi_image(event.reply_token,url1,url2,url3,url4)    

    def is_going_to_newbie(self, event):
        text = event.message.text
        return (text.lower() == '新手' or text.lower() == 'back')

    def on_enter_newbie(self, event):
        title = '新手'
        text = '請選擇你想知道的資訊'
        btn = [
            MessageTemplateAction(
                label = '容易上手英雄',
                text ='容易上手英雄'
            ),
            MessageTemplateAction(
                label = '英雄定位',
                text = '英雄定位'
            ),
            MessageTemplateAction(
                label = 'back',
                text = 'back'
            ),
        ]
        url = 'https://cdn2.ettoday.net/images/4215/4215808.jpg'
        send_button_message(event.reply_token, title, text, btn, url)          

    def is_going_to_easy_hero(self, event):
        text = event.message.text
        return text.lower() == "容易上手英雄"

    def on_enter_easy_hero(self, event):
        img_list = ['https://www.newton.com.tw/img/a/020/83ea2970271171c6e04c89835b72.jpg',
        'https://dlgarenanow-a.akamaihd.net/mgames/kgtw/Official%20website/2020/957x483/28h2-1.jpg',
        'https://i.ytimg.com/vi/foVKuvlmVy8/maxresdefault.jpg',
        'https://cdngarenanow-a.akamaihd.net/mgames/kgcenter/tw/client/GameData/Hero/12/skin/20170824061122-6447.jpg',
        'https://cdngarenanow-a.akamaihd.net/mgames/kgcenter/tw/client/GameData/Hero/3/20191208084826-1471.jpg']

        text_list = ['薩尼','歐米茄','趙雲','凡恩','薇菈',]
        lable_list = ['薩尼','歐米茄','趙雲','凡恩','薇菈',]


        col = []
        for i in range(5):
            c = ImageCarouselColumn(
                image_url = img_list[i],
                #image_url = 'http://i1.hdslb.com/bfs/archive/3a6365877cbcef1d87922a77ced328749e353565.jpg',
                action = MessageTemplateAction(
                    label = lable_list[i],
                    text = text_list[i]
                )
            )
            col.append(c)
        send_carousel_message(event.reply_token, col)    



    def is_going_to_location(self, event):
        text = event.message.text
        return (text.lower() == "英雄定位" or text.lower() == "back")

    def on_enter_location(self, event):
        col=[
            CarouselColumn(
                thumbnail_image_url='https://cdn2.ettoday.net/images/4215/4215808.jpg',
                title='英雄定位',
                text='選擇位置查看詳細資訊',
                actions=[
                    MessageTemplateAction(
                        label = '坦克',
                        text ='坦克'
                    ),
                    MessageTemplateAction(
                        label = '戰士',
                        text ='戰士'
                    ),
                    MessageTemplateAction(
                        label = '刺客',
                        text ='刺客'
                    ),                    
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://cdn2.ettoday.net/images/4215/4215808.jpg',
                title='英雄定位',
                text='選擇位置查看詳細資訊',
                actions=[
                    MessageTemplateAction(
                        label = '法師',
                        text ='法師'
                    ),
                    MessageTemplateAction(
                        label = '射手',
                        text = '射手'                        

                    ),
                    MessageTemplateAction(
                        label = '輔助',
                        text ='輔助'
                    ),                    
                
                ]
            ),
        ]     
        send_button_carousel(event.reply_token, col)

    def is_going_to_show_easy_hero(self, event):
        global part
        text = event.message.text
        if text == '薩尼' or text == '歐米茄' or text == '趙雲' or text == '凡恩' or text == '薇菈':
            part = text
            return True
        return False

    def on_enter_show_easy_hero(self, event):
        global part
        if part == '薩尼':
            url = 'https://i.ytimg.com/vi/gt7Z1GNOoBc/maxresdefault.jpg'
            text = '薩尼是近戰坦克英雄，第一招與第二招帶來的控制效果可以保護我方輸出，確保進攻時能更輕易破壞敵隊的陣型。超高防禦能力讓薩尼如同戰場上橫衝直撞的坦克車，推薦給喜歡帶領團隊作戰的挑戰者使用。 第一招「無畏衝鋒」是非常霸道的控制技能，能強制將目標從原本的位置推開很長一段距離。當兩軍交手時，進行衝鋒將敵方坦克推至後排位置，讓對手聚集在一起再使用第二招「聖劍裁決」控制所有敵人，然後配合我方法師進行輸出；在混戰時，也可以先使用聖劍裁決控制敵方後排英雄，再使用「無畏衝鋒」將其推向我軍攻擊範圍，與隊友一起秒殺重點敵人。 薩尼的被動「光明庇護」擁有強大的恢復能力，而且自身最大生命越高，能恢復的血量也就越多，因此推薦全防禦的出裝方向，讓薩尼在砲火中能撐住最長的時間，多次施放「無畏衝鋒」給予敵方巨大的壓力。'
        elif part == '歐米茄':
            url = 'https://dlgarenanow-a.akamaihd.net/mgames/kgtw/Official%20website/2020/957x483/28h2-1.jpg'
            text = '歐米茄是近戰坦克英雄，第一招可高速移動並於戰場最前線衝鋒，吸引敵方的砲火。適時使用第一招與第二招的雙重控制，可有效限制敵方走位並保護我方英雄，幫助隊友創造良好的輸出時機。歐米茄技能操作簡單又強力，推薦給立誓守護隊友的挑戰者使用。 第一招「等離子場」擁有多個效果，可以同時增加移動速度並獲得等離子護盾，而且下一次的普攻還可以擊飛敵人，簡直是三個願望一次滿足。配合第二招「衝擊盾」的暈眩控制，不論用來開戰或保護隊友都十分出色。 歐米茄的大招「暴走鑽頭」非常引人注目，大範圍的旋轉能給予敵方壓力以掩護隊友輸出。推薦歐米茄往全防禦的方向出裝，坦住所有傷害。只要歐米茄不倒下，我方攻擊角色便能安心的盡情輸出。'
        elif part == '趙雲':
            url = 'https://cdngarenanow-a.akamaihd.net/mgames/kgcenter/tw/client/GameData/Hero/11/20191208072831-8250.jpg'
            text = '趙雲是個近戰戰士英雄，被動「龍騎」能讓攻擊力隨擊殺或助攻持續成長。趙雲前中期可以盡量與敵方碰撞，一旦人頭陸續進帳，就會擁有非常強悍的後期能力，不論面對輸出角或坦克都能輕鬆收割，推薦給嚮往拯救世界的挑戰者使用。 第一招「龍血啟動」能增加攻擊速度與移動速度並移除控制效果，是非常適合追擊的優秀技能。大招「龍王之怒」讓普攻帶有真實傷害，敵人血量越多打得越痛，是趙雲能輕鬆刺穿坦克的關鍵。 趙雲推薦購買一至兩件輸出裝後開始撐防禦，因為「龍騎」的疊加效果相當於多穿了一件攻擊裝備，因此增加防禦並提高續戰力讓趙雲更能貼著敵人瘋狂輸出。 趙雲進攻時可優先施放「龍王之怒」，並補上第二招「狂熱」持續緩速敵人，當敵人使用控制技能時利用「龍血啟動」解除控制並快速貼近，一口氣在「龍王之怒」的持續時間內打出突破天際的傷害瞬殺敵人。'
        elif part == '凡恩':
            url = 'https://cdngarenanow-a.akamaihd.net/mgames/kgcenter/tw/client/GameData/Hero/12/skin/20190117014909-1681.jpg'
            text = '凡恩是個遠程射手英雄，被動「神秘力量」讓第三次普攻附帶隨機的獵魔飛鏢，搭配第二招「送葬詛咒」的單體暈眩，給予凡恩強大的控制能力，推薦給享受風騷拉打的挑戰者使用。 凡恩的技能傷害會隨物理攻擊力增加而提高，但實際上卻是造成魔法傷害，因此可利用這點突破敵人的防禦，由於能同時造成物理與魔法兩種傷害，敵人將更難防守住凡恩的攻擊。 凡恩推薦購買增加攻擊力與攻擊速度的裝備，擔當團隊中重要的火力來源。一個好的射手要隨時留意自身走位，保持在安全的位置對敵人輸出，若有人接近就利用暈眩與普攻壓低敵方血量，最後近身施放大招「水銀彈幕」，多發水銀子彈同時擊中敵人，會獲得意想不到的超高傷害。'
        elif part == '薇菈':
            url = 'https://cdngarenanow-a.akamaihd.net/mgames/kgcenter/tw/client/GameData/Hero/3/20191208084826-1471.jpg'
            text = '薇菈是個遠程法師英雄，第一招「夜魅鬼蝠」的攻擊範圍很廣，可以在遠方不斷的騷擾敵人。交手過程中只要先壓低敵方的血量，就可以趁對方走位失誤時，接上一套技能輕鬆收割人頭，推薦給喜愛秒殺敵人的挑戰者使用。 薇菈的血量與機動性都不佳，平時就要保持好與敵人的距離，若不幸被敵人貼身，可先施放第二招「色誘之術」控制住敵人後趕緊逃離。 薇菈推薦購買冷卻縮減與提高魔法攻擊的裝備，堆疊高魔攻後搭配被動「蠱惑」降低敵人魔防，讓薇菈擁有一套秒殺薄皮目標的破壞力。 大招「地獄魔靈」若五隻蝙蝠皆攻擊同一個敵人，累積傷害會特別的高，鎖定血量不多的落單對手，連續施放「色誘之術」、「夜魅鬼蝠」與「地獄魔靈」，敵人將被瞬間擊潰，毫無抵抗機會。'
        send_image_and_text_message(event.reply_token, url,text)
    
    def back_show_easy_hero(self, event):
        text = event.message.text
        return text.lower() == "back"

    def is_going_to_show_location(self, event):
        global part
        text = event.message.text        
        if text == '坦克' or text == '戰士' or text == '刺客' or text == '法師' or text == '射手' or text == '輔助':
            part = text
            return True
        return False

    def on_enter_show_location(self, event):
        title = '英雄定位'
        text = '請選擇你想知道的資訊'
        btn = [
            MessageTemplateAction(
                label = '位置介紹',
                text ='位置介紹'
            ),
            MessageTemplateAction(
                label = '攻略影片',
                text = '攻略影片'
            ),
            MessageTemplateAction(
                label = '英雄',
                text ='英雄'
            ),
        ]
        if part == '坦克':
            url = 'https://moba.garena.tw/img/page/locate_pic-01.jpg'
        elif part == '戰士':
            url = 'https://moba.garena.tw/img/page/locate_pic-02.jpg'
        elif part == '刺客':
            url = 'https://moba.garena.tw/img/page/locate_pic-03.jpg'
        elif part == '法師':
            url = 'https://moba.garena.tw/img/page/locate_pic-04.jpg'
        elif part == '射手':
            url = 'https://moba.garena.tw/img/page/locate_pic-05.jpg'
        elif part == '輔助':
            url = 'https://moba.garena.tw/img/page/locate_pic-06.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_get_location(self, event):
        text = event.message.text
        global location
        if text == '位置介紹' or text == '攻略影片' or text == '英雄':
            location = text
            return True
        return False

    def on_enter_get_location(self, event):
        global location
        global part
        if location == '位置介紹':
            if part == '坦克':
                url = 'https://moba.garena.tw/img/page/locate_pic-01.jpg'
                text = '因為具有高血量與防禦力的特性，因此常被稱為「肉盾」。在多人對戰模式中通常可獨自防守一路，因為就算被偷襲，死亡率相對其他定位的角色也較低。坦克在會戰時負責衝入敵方陣形開戰，以吸收大量傷害讓我方攻擊角色安心輸出為目標。坦克的出裝以增加血量為主，但若敵方陣營主力為魔法攻擊角色，須另外搭配魔法防禦裝備；反之若敵方主力為物理攻擊，則以物理防禦為主要出裝方向。'
            elif part == '戰士':
                url = 'https://moba.garena.tw/img/page/locate_pic-02.jpg'
                text = '戰士為近戰物理輸出角色，通常血量與防禦力僅次於坦克，且具有一定的攻擊力，可以作為隊伍中的副坦與次要輸出角色。戰士前期同樣適合獨自防守一路，而在會戰時等坦克開戰後，可以直攻對方後排輸出角色，以擾亂敵方陣型。出裝方向可以選擇全物理攻擊裝備，或嘗試混合防禦裝成為一個副坦，可說是玩法相當多變的一個定位。'
            elif part == '刺客':
                url = 'https://moba.garena.tw/img/page/locate_pic-03.jpg'
                text = '刺客是非常需要走位技巧與地圖觀念的突襲型角色，通常技能帶有「位移」的特性，因此很適合遊走各路進行偷襲。因為血量與防禦力較低，遊戲前期需與隊友良好搭配，以擊殺盡可能多的小兵或英雄，並趕緊購買輸出裝備以快速壯大。遊戲中後期，刺客的進場時機與走位技巧將是每一場會戰勝敗的關鍵，因此必須瞄準對方威脅性高的角色，盡快將其擊殺。若狀況許可，刺客也可以前往無人防守的路線，靠強大的攻擊能力迅速拿下防禦塔以破壞敵方陣線。'
            elif part == '法師':
                url = 'https://moba.garena.tw/img/page/locate_pic-04.jpg'
                text = '法師具有強大的魔法攻擊能力，能製造大範圍傷害並具備控場能力，能暈眩或冰凍敵人並予以擊殺。因為皮薄血少的關係，前期必須靠著技能快速清理兵線以取得經濟優勢，並購買以魔法傷害為主的裝備。團戰中法師扮演控制敵方動向的角色，可藉由大範圍的魔法對多數敵人造成重大傷害。法師是強而有力的輸出角色，但因為防禦力非常薄弱，必須謹慎走位以免瞬間陣亡。'
            elif part == '射手':
                url = 'https://moba.garena.tw/img/page/locate_pic-05.jpg'
                text = '與法師同樣具備強大的輸出能力，不同的是射手屬於物理輸出角色。前期同樣因為生存能力較低，必須與隊友妥善搭配才能穩定在線上發展。中期就可以開始發揮強大的攻擊能力，以本身具有的遠距離輸出優勢在敵人靠近之前就削減對方大量血量，以製造會戰優勢。出裝方向以提高物理攻擊力與穿透力為主。若整體戰局不利我方，可適時搭配防禦裝來提高自身存活率，並抓緊機會扭轉形勢。'
            elif part == '輔助':
                url = 'https://moba.garena.tw/img/page/locate_pic-06.jpg'
                text = '輔助在遊戲中是一個相當獨特的定位。輔助角的攻擊能力不強，但技能效果具有牽制敵方、提高我方能力等特性，可以說是前中後期都不可或缺的重要角色。由於缺乏攻擊手段，前期必須跟隊友同行，以各項輔助技能協助隊友取得擊殺數優勢。出裝以防禦裝、回血或回魔裝為主，提高自身生存力與續戰力的同時，也代表能持續在戰場上幫助隊友。'
            send_image_and_text_message(event.reply_token, url,text)
        elif location == '攻略影片':
            if part == '坦克':
           
                url_list = ['https://www.youtube.com/watch?v=PLOux5n1r00','https://www.youtube.com/watch?v=tvoGCp8c7p0','https://www.youtube.com/watch?v=aq-6mtCvDpo','https://www.youtube.com/watch?v=2Eq_i6zWaKk']
                img_list = ['https://img.ttshow.tw/images/media/frontcover/2020/07/31/746-1.jpg','https://cdngarenanow-a.akamaihd.net/mgames/kgcenter/tw/client/GameData/Hero/1/skin/20161005043601-7809.jpg','https://i.ytimg.com/vi/1dKPJ3OP43g/hqdefault.jpg','https://s.newtalk.tw/album/news/106/5a23eeb679c23.jpg']
                lable_list = ['免費最強100%勝率','牛魔王硬到有點扯！','極限三連殺碰到對手','坦克出全攻擊裝這麼恐怖']
                col = []
                for i in range(4):
                    c = ImageCarouselColumn(
                        image_url = img_list[i],
                        action = URITemplateAction(
                            label = lable_list[i],
                            uri = url_list[i]
                        )
                    )
                    col.append(c)
                                  
            elif part == '戰士':
                url_list = ['https://www.youtube.com/watch?v=yDF2A-tyzL0','https://www.youtube.com/watch?v=bA8p2-TXiI4','https://www.youtube.com/watch?v=AnelXyx6jbs','https://www.youtube.com/watch?v=yyUOgLyUTV8']
                img_list = ['https://i.imgur.com/NiuwTNd.jpg','https://i.imgur.com/KO56v6O.jpg','https://dlgarenanow-a.akamaihd.net/mgames/kgtw/Official%20website/2020/news/1202SAOxAOVnews03.jpg','https://cdngarenanow-a.akamaihd.net/mgames/kgcenter/tw/client/GameData/Hero/84/skin/20190402110308-7194.jpg']
                lable_list = ['５個當前版本最強凱撒路','戰士META根本打不死','近距離最強戰士','埃羅｜超狂戰士']
                col = []
                for i in range(4):
                    c = ImageCarouselColumn(
                        image_url = img_list[i],
                        action = URITemplateAction(
                            label = lable_list[i],
                            uri = url_list[i]
                        )
                    )
                    col.append(c)
            elif part == '刺客':
                url_list = ['https://www.youtube.com/watch?v=kUpYdoo4e3c','https://www.youtube.com/watch?v=aZaUXDhCd4k','https://www.youtube.com/watch?v=7CiaO7mnxyY','https://www.youtube.com/watch?v=5m1GklWFvHQ']
                img_list = ['https://i.ytimg.com/vi/kUpYdoo4e3c/maxresdefault.jpg','https://dlgarenanow-a.akamaihd.net/mgames/kgtw/Official%20website/2021/957x483/02082021LNYnews02.jpg',
                'https://cdngarenanow-a.akamaihd.net/mgames/kgcenter/tw/client/GameData/Hero/16/skin/20210504052418-1020.jpg','https://image.garena.tw/images/moba/%E6%95%99%E5%AD%B8/%E6%94%BB%E7%95%A5%E7%B6%B2/1117%E5%A5%8E%E5%80%AB.jpg']
                lable_list = ['傳說對決最強刺客','十大高人氣戰士刺客','最靈活的刺客打野','誰才是隱形刺客之王']
                col = []
                for i in range(4):
                    c = ImageCarouselColumn(
                        image_url = img_list[i],
                        action = URITemplateAction(
                            label = lable_list[i],
                            uri = url_list[i]
                        )
                    )
                    col.append(c)
            elif part == '法師':
                url_list = ['https://www.youtube.com/watch?v=HCOy3GSIFYE','https://www.youtube.com/watch?v=FMJPSklGHqM','https://www.youtube.com/watch?v=geBafqr_8Ys','https://www.youtube.com/watch?v=i9B0U-DNXHA']
                img_list = ['https://images.newtalk.tw/resize_action2/600/album/news/116/5a8f7488a0e47.JPG','https://i.ytimg.com/vi/FMJPSklGHqM/maxresdefault.jpg',
                'https://cdn-www.bluestacks.com/bs-images/aov-top-5-mid-lane-mages-tw-3.jpg','https://img.league-funny.com/imgur/155586670244.jpg']
                lable_list = ['中路最強法師保證沒對手','高手最愛用的強勢中路法師','傳說對決最強中路法王','最神中路教學']
                col = []
                for i in range(4):
                    c = ImageCarouselColumn(
                        image_url = img_list[i],
                        action = URITemplateAction(
                            label = lable_list[i],
                            uri = url_list[i]
                        )
                    )
                    col.append(c)
            elif part == '射手':
                url_list = ['https://www.youtube.com/watch?v=31jhGb8Nmvw','https://www.youtube.com/watch?v=PfuOZfkvjsQ','https://www.youtube.com/watch?v=23RNCOWBUm4','https://www.youtube.com/watch?v=dyXT9hA_TI0']
                img_list = ['https://i.ytimg.com/vi/xudl4MC48_8/maxresdefault.jpg','https://truth.bahamut.com.tw/s01/201808/d8a61f2ab2f3051f06dd2e3788d8cfd1.JPG',
                'https://triplep01.files.wordpress.com/2020/08/screenshot_20200822-191451.jpg','https://i.imgur.com/5oj7Nwf.jpg']
                lable_list = ['魔龍路射手選角觀念','最詳細的魔龍路大補包','AIC世界賽熱門射手','射手必備的上分意識']
                col = []
                for i in range(4):
                    c = ImageCarouselColumn(
                        image_url = img_list[i],
                        action = URITemplateAction(
                            label = lable_list[i],
                            uri = url_list[i]
                        )
                    )
                    col.append(c)                
            elif part == '輔助':
                url_list = ['https://www.youtube.com/watch?v=3e-1FFuGLYk','https://www.youtube.com/watch?v=PJCR1C62p_Y','https://www.youtube.com/watch?v=CWVqhmc633I','https://www.youtube.com/watch?v=Av7O62lClo8']
                img_list = ['https://i.imgur.com/ifPZb6J.jpg','https://truth.bahamut.com.tw/s01/201806/e09c8771bef9eede9a5878e8d577f64e.JPG',
                'https://i.ytimg.com/vi/LNhQe7Tr7DE/maxresdefault.jpg','https://truth.bahamut.com.tw/s01/201806/5f10d48effc13072e5d52569171d6837.JPG']
                lable_list = ['輔助型中路起飛','流行輔助全收錄','學會這隻最強輔助神角！','輔助五大錯誤！']
                col = []
                col.clear()
                for i in range(4):
                    c = ImageCarouselColumn(
                        image_url = img_list[i],
                        action = URITemplateAction(
                            label = lable_list[i],
                            uri = url_list[i]
                        )
                    )
                    col.append(c)  
            send_carousel_message(event.reply_token, col)
          
        elif location == '英雄':
            if part == '坦克':
                url = 'https://i.imgur.com/PC4Nvig.jpg'
                send_image_message(event.reply_token, url)
            elif part == '戰士':
                url = 'https://i.imgur.com/9t2oNO8.jpg'
                send_image_message(event.reply_token, url)     
            elif part == '刺客':
                url = 'https://i.imgur.com/D4Nohjs.jpg'
                send_image_message(event.reply_token, url)    
            elif part == '法師':
                url = 'https://i.imgur.com/WxpTxko.jpg'
                send_image_message(event.reply_token, url)    
            elif part == '射手':
                url = 'https://i.imgur.com/S1tYoaE.jpg'
                send_image_message(event.reply_token, url) 
            elif part == '輔助':
                url = 'https://i.imgur.com/UHgiwEP.jpg'
                send_image_message(event.reply_token, url)                                                                         

    def back_show_location(self, event):
        text = event.message.text
        return text.lower() == "back"
                


 
    def is_going_to_hero(self, event):
        text = event.message.text
        return text.lower() == "英雄"

    def on_enter_hero(self, event):        
        title = '英雄'
        text = '請選擇你想知道的資訊'
        btn = [
            MessageTemplateAction(
                label = '周免英雄free',
                text ='周免英雄free'
            ),
            MessageTemplateAction(
                label = '英雄介紹',
                text = '英雄介紹'
            ),

        ]
        url = 'https://cdn2.ettoday.net/images/4215/4215808.jpg'
        send_button_message(event.reply_token, title, text, btn, url)   

 
    def is_going_to_free(self, event):
        text = event.message.text
        return text.lower() == "周免英雄free"   
    def on_enter_free(self, event):
        response = requests.get(f"https://moba.garena.tw/")
        soup = BeautifulSoup(response.text, "lxml")
        results = soup.find_all("img", {"class": "index-freeheros__item-img"}, limit=6)
        img_list = [result.get("src") for result in results]
        for i in range(5):
            print(img_list[i])      
        response = requests.get(f"https://moba.garena.tw/")
        soup = BeautifulSoup(response.text, "lxml")
        results = soup.find_all("a", {"class": "index-freeheros__item-link"}, limit=6)
        url_list = [result.get("href") for result in results]    
        col = []
        col.clear()
        for i in range(6):
            c = ImageCarouselColumn(
                image_url = 'https:' + img_list[i],
                action = URITemplateAction(
                    label ='點擊查看英雄詳細資訊',
                    uri = url_list[i]
                )
            )
            col.append(c)  
        send_carousel_message(event.reply_token, col)

    def is_going_to_hero_intro(self, event):
        text = event.message.text
        return text.lower() == "英雄介紹"   
    def on_enter_hero_intro(self, event):
        send_text_message(event.reply_token, '請輸入數字1~103')

    def is_going_to_show_hero_intro(self, event):
        global num
        text = event.message.text
        if text.lower().isnumeric():
            num = text
            return True  
        return False
    
    def on_enter_show_hero_intro(self, event):
        global num
        response = requests.get(f"https://moba.garena.tw/game/hero/" + num)
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.select('div.h_i_t_name')
        story = soup.select('div.h_story h4')
        #img = soup.select('div.h_i_pic')
        #results = soup.find_all("img", {"class": "div.h_info"}, limit=1)
        img = soup.select("img", {"class": "div.h_i_pic"})


        text = name[0].text + '\n' + story[0].text
        url = 'https:' + img[1]["src"]
        print(url)
        

        send_image_and_text_message(event.reply_token, url,text)

    def back_hero(self, event):
        text = event.message.text
        return text.lower() == "back"     
    def back_hero_intro(self, event):
        text = event.message.text
        return text.lower() == "back"                  
    
    def is_going_to_test1(self, event):
        text = event.message.text
        return text.lower() == "檢測適合位置"   
    def on_enter_test1(self, event):
        global medium
        global warrior
        global shoot
        global support
        global jungle
        medium = 0
        warrior = 0
        shoot = 0
        support = 0
        jungle = 0
        title = '第1題'
        text = '你是一個善於指揮大局的人嗎?'
        btn = [
            MessageTemplateAction(
                label = '是，我時常引導大家',
                text = '是，我時常引導大家'
            ),
            MessageTemplateAction(
                label = '偶爾，視情況而決定',
                text = '偶爾，視情況而決定'
            ),
            MessageTemplateAction(
                label = '否，我習慣跟隨他人的指揮',
                text = '否，我習慣跟隨他人的指揮'
            ),            

        ]
        url = 'https://cdn2.ettoday.net/images/4215/4215808.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_test2(self, event):
        global medium
        global warrior
        global shoot
        global support
        global jungle        
        text = event.message.text
        if text == '是，我時常引導大家':
            jungle = jungle + 1
            return True
        elif text == '偶爾，視情況而決定':
            medium = medium + 1
            warrior = warrior + 1
            return True   
        elif text == '否，我習慣跟隨他人的指揮':
            support = support + 1
            shoot = shoot + 1
            return True         
        return False 
    def on_enter_test2(self, event):
        title = '第2題'
        text = '當面對強勁的敵人時，你會迎上去嗎?'
        btn = [
            MessageTemplateAction(
                label = '會，不打怎麼知道打不打得過呢',
                text = '會，不打怎麼知道打不打得過呢'
            ),
            MessageTemplateAction(
                label = '偶爾，會先觀察隊友和敵人位置',
                text = '偶爾，會先觀察隊友和敵人位置'
            ),
            MessageTemplateAction(
                label = '先躲躲，等我變更強再說',
                text = '先躲躲，等我變更強再說'
            ),            

        ]
        url = 'https://cdn2.ettoday.net/images/4215/4215808.jpg'
        send_button_message(event.reply_token, title, text, btn, url)                 
    
    def is_going_to_test3(self, event):
        global medium
        global warrior
        global shoot
        global support
        global jungle        
        text = event.message.text
        if text == '會，不打怎麼知道打不打得過呢':
            warrior = warrior + 1            
            return True
        elif text == '偶爾，會先觀察隊友和敵人位置':
            medium = medium + 1
            jungle = jungle + 1
            return True   
        elif text == '先躲躲，等我變更強再說':
            support = support + 1
            shoot = shoot + 1
            return True         
        return False 
    def on_enter_test3(self, event):
        title = '第3題'
        text = '當團戰快要輸時你會怎麼做?'
        btn = [
            MessageTemplateAction(
                label = '不能丟下隊友，拚到底',
                text = '不能丟下隊友，拚到底'
            ),
            MessageTemplateAction(
                label = '自己不死的前提，隊友能幫就幫',
                text = '自己不死的前提，隊友能幫就幫'
            ),
            MessageTemplateAction(
                label = '趕緊撤退，留得青山在',
                text = '趕緊撤退，留得青山在'
            ),            

        ]
        url = 'https://cdn2.ettoday.net/images/4215/4215808.jpg'
        send_button_message(event.reply_token, title, text, btn, url)  

    def is_going_to_test4(self, event):
        global medium
        global warrior
        global shoot
        global support
        global jungle        
        text = event.message.text
        if text == '不能丟下隊友，拚到底':
            warrior = warrior + 1
            support = support + 1            
            return True
        elif text == '自己不死的前提，隊友能幫就幫':
            medium = medium + 1
            
            return True   
        elif text == '趕緊撤退，留得青山在':
            jungle = jungle + 1
            shoot = shoot + 1
            return True         
        return False 
    def on_enter_test4(self, event):

        title = '第4題'
        text = '你更在意整體還是自己'
        btn = [
            MessageTemplateAction(
                label = '團隊贏了就好，自己無所謂',
                text = '團隊贏了就好，自己無所謂'
            ),
            MessageTemplateAction(
                label = '雖然要贏，但自己也不能太差',
                text = '雖然要贏，但自己也不能太差'
            ),
            MessageTemplateAction(
                label = '自己夠帥夠秀最重要',
                text = '自己夠帥夠秀最重要'
            ),            

        ]
        url = 'https://cdn2.ettoday.net/images/4215/4215808.jpg'
        send_button_message(event.reply_token, title, text, btn, url)  
    
    def is_going_to_test5(self, event):
        global medium
        global warrior
        global shoot
        global support
        global jungle        
        text = event.message.text
        if text == '團隊贏了就好，自己無所謂':            
            support = support + 1            
            return True
        elif text == '雖然要贏，但自己也不能太差':
            medium = medium + 1
            shoot = shoot + 1            
            return True   
        elif text == '自己夠帥夠秀最重要':
            jungle = jungle + 1            
            warrior = warrior + 1
            return True         
        return False 
    def on_enter_test5(self, event):

        title = '第5題'
        text = '你是一個直覺很準的人嗎'
        btn = [
            MessageTemplateAction(
                label = '是',
                text = '是'
            ),
            MessageTemplateAction(
                label = '普通',
                text = '普通'
            ),
            MessageTemplateAction(
                label = '否',
                text = '否'
            ),            

        ]
        url = 'https://cdn2.ettoday.net/images/4215/4215808.jpg'
        send_button_message(event.reply_token, title, text, btn, url)  

    def is_going_to_test6(self, event):
        global medium
        global warrior
        global shoot
        global support
        global jungle        
        text = event.message.text
        if text == '是':            
            support = support + 1
            shoot = shoot + 1
            jungle = jungle + 1                    
            return True
        elif text == '普通':
            medium = medium + 1                    
            return True   
        elif text == '否':                
            warrior = warrior + 1
            return True         
        return False 
    
    def on_enter_test6(self, event):

        title = '第6題'
        text = '你是一個反應反射很快的人嗎'
        btn = [
            MessageTemplateAction(
                label = '是',
                text = '是'
            ),
            MessageTemplateAction(
                label = '普通',
                text = '普通'
            ),
            MessageTemplateAction(
                label = '否',
                text = '否'
            ),            

        ]
        url = 'https://cdn2.ettoday.net/images/4215/4215808.jpg'
        send_button_message(event.reply_token, title, text, btn, url)

    def is_going_to_result(self, event):
        global medium
        global warrior
        global shoot
        global support
        global jungle       
        text = event.message.text
        if text == '是':            
            support = support + 1
            shoot = shoot + 1
            jungle = jungle + 1                    
            return True
        elif text == '普通':
            medium = medium + 1                    
            return True   
        elif text == '否':                
            warrior = warrior + 1
            return True         
        return False 
    
    def on_enter_result(self, event):
        if support >= medium and support >= jungle and support >= warrior and support >= shoot:
            url = 'https://moba.garena.tw/img/page/locate_pic-06.jpg'
            text = '你最適合的位置是輔助！輔助在遊戲中是一個相當獨特的定位。輔助角的攻擊能力不強，但技能效果具有牽制敵方、提高我方能力等特性，可以說是前中後期都不可或缺的重要角色！'
            send_image_and_text_message(event.reply_token, url,text)
        elif medium >= support and medium >= jungle and medium >= shoot and medium >= warrior:
            url = 'https://moba.garena.tw/img/page/locate_pic-04.jpg'
            text = '你最適合的位置是中路！中路通常以法師為主，單人一路，法師的優勢在於強大的技能輸出，眼觀四路，可以視情況去支援任何人！'
            send_image_and_text_message(event.reply_token, url,text)            
        elif jungle >= support and jungle >= medium and jungle >= shoot and jungle >= warrior:
            url = 'https://moba.garena.tw/img/page/locate_pic-03.jpg'
            text = '你最適合的位置是打野！打野非常需要走位技巧與地圖觀念，你的頭腦是最清楚，靈敏的，神出鬼沒給對手壓力，也是遊戲中帶風向的重要角色！'
            send_image_and_text_message(event.reply_token, url,text)
        elif warrior >= support and warrior >= medium and warrior >= shoot and warrior >= jungle:
            url = 'https://moba.garena.tw/img/page/locate_pic-02.jpg'
            text = '你最適合的位置是凱撒路！凱薩路的對線能力，單殺能力都強，是個容易單機的位置，讓你可以專心的跟你的對手周旋。屢敗屢戰，越挫越勇，就是最勇猛的莫得感情的戰士！'
            send_image_and_text_message(event.reply_token, url,text)
        elif shoot >= support and shoot >= medium and shoot >= warrior and shoot >= jungle:
            url = 'https://moba.garena.tw/img/page/locate_pic-05.jpg'
            text = '你最適合的位置是魔龍路！魔龍路以射手為主，與法師同樣具備強大的輸出能力，不同的是射手屬於物理輸出角色。前期同樣因為生存能力較低，需要穩穩地發展自己的實力，成長起來後就是人見人怕的殺人機器！'
            send_image_and_text_message(event.reply_token, url,text)                                  


    def is_going_to_user(self, event):
        text = event.message.text
        return text.lower() == "restart"   
    def on_enter_user(self, event):
        send_text_message(event.reply_token,'你好，我是你的傳說小助理，請輸入你想知道的資訊\n' + 
        '輸入『介紹』可查看遊戲相關介紹\n' + '輸入『英雄』可查看英雄相關資訊\n' + '輸入『檢測適合位置』可檢測你適合玩的位置\n' + 
        '隨時輸入『back』可以回到上一頁\n隨時輸入『restart』可以從頭開始。' )            