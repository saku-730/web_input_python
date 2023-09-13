from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time


def book(number, passcode, day, lesson, club):
    options = webdriver.EdgeOptions()
    # options.add_argument(' headless')

    print("connectiong to remote browser...")
    driver = webdriver.Edge(options=options)

    # コナミのログイン画面を開く。
    driver.get("https://member.konamisportsclub.jp/login.php")
    print(driver.current_url)

    # 会員番号とパスワードの入力
    user_number = driver.find_element(by=By.XPATH, value='//*[@id="username"]')
    user_number.send_keys(number)

    password = driver.find_element(by=By.XPATH, value='//*[@id="password"]')
    password.send_keys(passcode)

    # ログイン
    login_button = driver.find_element(by=By.XPATH, value='//*[@id="btnSubmit"]')
    login_button.click()

    print(driver.current_url)

    # 予約
    studio_book_button = driver.find_element(
        by=By.XPATH, value='//*[@id="main"]/div[2]/div/div/ul/li[4]/a'
    )
    studio_book_button.click()
    studio_book_button = driver.find_element(
        by=By.XPATH,
        value='//*[@id="main"]/div[2]/div/div/ul/li[4]/div/div/div/ul/li[1]/a',
    )
    studio_book_button.click()  # タイムテーブルから予約に移動
    print(driver.current_url)

    place_list = driver.find_element(
        By.XPATH,
        value='//*[@id="pageAccess"]/div[1]/main/div/section/div[1]/div/div[2]/div/span/label/select',
    )
    place = Select(place_list)
    select_place = "コナミスポーツクラブ " + club

    place.select_by_visible_text(select_place)  # 施設の選択

    lesson = '"' + lesson + '")]'
    lesson_XPATH = '//*[@id="js-studioreserve-body"]/*[contains(., ' + lesson
    for i in range(20):
        try:
            day_select = driver.find_element(By.PARTIAL_LINK_TEXT, value=day)
            day_select.click()  # 日付選択

            lesson_slect = driver.find_elements(By.XPATH, value=lesson_XPATH)  # プログラム選択
            for element in lesson_slect:
                if element.is_displayed():
                    lesson_slect1 = element
            print(lesson_slect1.is_enabled())
            lesson_slect1.click()
        except Exception:
            print(Exception)
            time.sleep(0.5)
            driver.refresh()  # ページ更新
        else:
            break

    confirm = driver.find_element(
        By.XPATH, value='//*[@id="js-modal-program-reserve-button"]/button'
    )

    confirm.click()
    print(driver.current_url)

    consent = driver.find_element(By.XPATH, value='//*[@id="detailArea"]/div[5]/label')
    consent.click()
    print(driver.current_url)
    consent = driver.find_element(By.XPATH, value='//*[@id="next"]')
    consent.click()
    print(driver.current_url)
    consent = driver.find_element(By.XPATH, value='//*[@id="complete"]')
    consent.click()
    print(driver.current_url)

    # x. ブラウザを終了する
    driver.quit()
