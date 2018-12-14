import os, sys, pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

RESULT_DIR = "./"

def main(start_page, end_page, key):

    '''
    start_page (int) : １〜
    key (str) : 検索文字列
    
    >>> main(start_page=1, end_page=20, key="久保利明")

    保存されるデータ : 各棋譜データ（辞書）の入ったリスト
    各棋譜データは以下のような形式。
    {
        'info': {
            '先手': '久保利明',
            '場所': '関西将棋会館',
            '後手': '渡辺明',
            '戦型': '先手四間飛車',
            '手合割': '平手',
            '持ち時間': '4時間',
            '棋戦': '棋聖戦',
            '棋戦詳細': '棋聖戦',
            '消費時間': '',
            '開始日時': '2010-03-01 09:00:00'
        },
        'kifu': ['+7776FU', '-3334FU', ... ]
    }

    '''

    # ブラウザを開く。
    driver = webdriver.Chrome()
    # TOP画面を開く。
    driver.get("https://shogidb2.com/")

    name = key

    # 検索窓
    elem_serach = driver.find_element_by_name("q")
    elem_serach.send_keys(name)
    # 検索
    search_button = driver.find_element_by_class_name("input-group-append")
    search_button.click()


    result = []

    no_more_page = False
    page_number = start_page - 1
    kifu_list_page = None

    while True:
        sleep(0.5)
        
        if kifu_list_page is not None:
            driver.get(kifu_list_page)
            
        sleep(0.5)

        if no_more_page:
            break

        page_number += 1
        print("page number : {}".format(str(page_number)))
        if page_number == end_page + 1:
            break


        def find_the_pagenation():

            while True:
        
                # ページネーション
                def find_the_pagenation_in_this_page():

                    pagenations = driver.find_elements_by_class_name("page-item")
                    pagenations = pagenations[:int(len(pagenations)/2)]
                    for pagenation in pagenations:
                        pagenation_link = pagenation.find_element_by_tag_name("a")
                        if pagenation_link.text == str(page_number):
                            href = pagenation_link.get_attribute("href")
            #                 pagenation_link.click()
                            driver.get(href)
                            
                            return True

                    return False

                found = find_the_pagenation_in_this_page()

                if found:
                    break

                else:
                    link_arial_next = driver.find_elements_by_class_name("page-link")[-1]
                    # 「>」ボタンをクリック
                    href_arial_next = link_arial_next.get_attribute("href")
                    driver.get(href_arial_next)

        find_the_pagenation()

        kifu_list_page = driver.current_url

        # 各ページ
        i = 0

        print("page number : ")
        print(page_number)

        while True:

            # 各棋譜をみる
            sleep(1)
            print(i)

            contents = driver.find_element_by_class_name("list-group")
            all_kifu_link = contents.find_elements_by_class_name("list-group-item")
            if i == len(all_kifu_link):
                if len(all_kifu_link) < 20:
                    no_more_page = True
                break
            all_kifu_link[i].click()
            i += 1

            # 対局情報を取得
            rows = driver.find_elements_by_tag_name("tr")
            info = {}
            # info = []
            for row in rows:
                abouts = row.find_elements_by_tag_name("th")
                if len(abouts) > 0:
                    about_text = abouts[0].text
                    val = row.find_element_by_tag_name("td")
                    val_text = val.text
                    info[str(about_text)] = val_text
                    # info.append((about_text, val_text))

            print(info)

    #         print(info)

            # 棋譜モーダルを開く
            csa_modal_buttom = driver.find_element_by_id("csa-export")
            csa_modal_buttom.click()
            sleep(1)
            # 棋譜を取得
            modal_field = driver.find_element_by_class_name("control-group")
            modal_textarea = modal_field.find_element_by_tag_name("textarea")
            csa_text = modal_textarea.text

            # csaから指し手を取り出す
            hands = []  # hands = [] になることがある（棋譜がない）
            for csa_row in csa_text.split("\n"):
                if len(str(csa_row)) > 0:
                    if (csa_row[0] == "+") or (csa_row[0] == "-"):
                        if csa_row != "+":
                            hands.append(csa_row)

            result_thie_war = {"info" : info, "kifu" : hands}
            result.append(result_thie_war)

            # 棋譜一覧に戻る
            driver.back()

        print(len(result))
        
    with open(os.path.join(RESULT_DIR, "四間飛車_1to10.pickle"), mode="wb") as f:
        pickle.dump(result, f)
        
if __name__ == "__main__":

    main(start_page=1, end_page=10, key="四間飛車")