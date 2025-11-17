from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import re
import os

# -----------------------------
# 크롬 드라이버 설정
# -----------------------------
driver_path = "C:/Users/tlsgo/Downloads/chromedriver-win64 (1)/chromedriver-win64/chromedriver.exe"

service = Service(driver_path)
driver = webdriver.Chrome(service=service)
# -----------------------------
# 스크래핑 대상 URL 리스트
# -----------------------------
urls = {
    "남현": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EB%82%A8%ED%98%84%EB%8F%99-350&salesType=officetel%2Cone_room%2Ctwo_room&tradeType=borrow",
    "청룡": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%B2%AD%EB%A3%A1%EB%8F%99-346&salesType=officetel%2Cone_room%2Ctwo_room&tradeType=borrow",
    "성현": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%84%B1%ED%98%84%EB%8F%99-343&salesType=officetel%2Cone_room%2Ctwo_room&tradeType=borrow",
    "조원": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%A1%B0%EC%9B%90%EB%8F%99-357&salesType=officetel%2Cone_room%2Ctwo_room&tradeType=borrow",
    "미성": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EB%AF%B8%EC%84%B1%EB%8F%99-360&salesType=officetel%2Cone_room%2Ctwo_room&tradeType=borrow",
    "서림": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%84%9C%EB%A6%BC%EB%8F%99-353&salesType=officetel%2Cone_room%2Ctwo_room&tradeType=borrow",
    "보라매": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EB%B3%B4%EB%9D%BC%EB%A7%A4%EB%8F%99-341&salesType=officetel%2Cone_room%2Ctwo_room&tradeType=borrow",
    "신림": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%8B%A0%EB%A6%BC%EB%8F%99-355&salesType=officetel%2Ctwo_room%2Cone_room&tradeType=borrow",
    "봉천": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EB%B4%89%EC%B2%9C%EB%8F%99-6058&salesType=officetel%2Ctwo_room%2Cone_room&tradeType=borrow",
    "대학": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EB%8C%80%ED%95%99%EB%8F%99-358&salesType=officetel%2Ctwo_room%2Cone_room&tradeType=borrow",
    "낙성대": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EB%82%99%EC%84%B1%EB%8C%80%EB%8F%99-345&salesType=one_room%2Ctwo_room%2Cofficetel&tradeType=borrow",
    "난곡": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EB%82%9C%EA%B3%A1%EB%8F%99-361&salesType=officetel%2Ctwo_room%2Cone_room&tradeType=borrow",
    "은천": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%9D%80%EC%B2%9C%EB%8F%99-347&salesType=officetel%2Ctwo_room%2Cone_room&tradeType=borrow",
    "행운": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%ED%96%89%EC%9A%B4%EB%8F%99-344&salesType=officetel%2Ctwo_room%2Cone_room&tradeType=borrow",
    "인헌": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%9D%B8%ED%97%8C%EB%8F%99-349&salesType=officetel%2Ctwo_room%2Cone_room&tradeType=borrow",
    "신사": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%8B%A0%EC%82%AC%EB%8F%99-354&salesType=one_room%2Ctwo_room%2Cofficetel&tradeType=borrow",
    "서원": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%84%9C%EC%9B%90%EB%8F%99-351&salesType=one_room%2Ctwo_room%2Cofficetel&tradeType=borrow",
    "삼성": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%82%BC%EC%84%B1%EB%8F%99-359&salesType=one_room%2Ctwo_room%2Cofficetel&tradeType=borrow",
    "난향": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EB%82%9C%ED%96%A5%EB%8F%99-356&salesType=one_room%2Ctwo_room%2Cofficetel&tradeType=borrow",
    "중앙": "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%A4%91%EC%95%99%EB%8F%99-348&salesType=one_room%2Ctwo_room%2Cofficetel&tradeType=borrow",
    "신원":  "https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%8B%A0%EC%9B%90%EB%8F%99-352&salesType=one_room%2Ctwo_room%2Cofficetel&tradeType=borrow",
    "청림":"https://www.daangn.com/kr/realty/?areaViewType=p&in=%EC%B2%AD%EB%A6%BC%EB%8F%99-342&salesType=one_room%2Ctwo_room%2Cofficetel&tradeType=borrow"
}


# -----------------------------
# 정제 함수
# -----------------------------
def clean_text(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    text = re.sub(r'[\U00010000-\U0010FFFF]', '', text)
    return text.strip()


# -----------------------------
# 1. 기존 CSV 불러오기
# -----------------------------
output_file = "daangn_list.csv"
new_file = "new_identifiers.csv"

if os.path.exists(output_file):
    combined_df = pd.read_csv(output_file, dtype=str)
    existing_ids = set(combined_df["identifier"].dropna())
    print(f"[INFO] 기존 CSV 불러오기 완료, 현재 행 수: {len(combined_df)}")
else:
    combined_df = pd.DataFrame(columns=["area", "identifier", "description", "image_count", "image"])
    existing_ids = set()
    print(f"[INFO] 기존 CSV 없음, 신규 생성 예정")

new_records = []  # 이번 스케줄에서 신규 매물만 담을 리스트

# -----------------------------
# URL 반복 처리
# -----------------------------
MAX_RETRY = 3  # 최대 재시도 횟수

for area, url in urls.items():
    print(f"\n[INFO] {area} 페이지 스크래핑 중...")

    success = False
    for attempt in range(1, MAX_RETRY + 1):
        try:
            if attempt == 1:
                driver.get(url)
            else:
                driver.refresh()

            time.sleep(5)  # 페이지 로딩 대기

            soup = BeautifulSoup(driver.page_source, "html.parser")
            scripts = soup.find_all("script", type="application/ld+json")

            # JSON 데이터 파싱
            json_data_list = []
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get("@type") == "ItemList":
                        json_data_list.extend(data.get("itemListElement", []))
                except:
                    continue

            if len(json_data_list) == 0:
                raise ValueError("매물 데이터 없음")

            print(f"[INFO] {area} 추출 매물 수: {len(json_data_list)}개")
            success = True
            break

        except Exception as e:
            print(f"[WARN] {area} 로드 실패 ({attempt}/{MAX_RETRY})회차: {e}")
            if attempt < MAX_RETRY:
                print("[INFO] 3초 후 재시도 (새로고침)...")
                time.sleep(3)
            else:
                print(f"[ERROR] {area} 페이지 로드 실패, 스킵 처리.")
                json_data_list = []
                break

    # 실패 시 다음 지역으로
    if not success:
        continue

    # -----------------------------
    # 데이터 정제
    # -----------------------------

    results = []
    for i, item in enumerate(json_data_list):
        try:
            unit = item.get("item", {})
            description = clean_text(unit.get("description", ""))
            identifier = unit.get("identifier", "")
            images = unit.get("image", [])

            if not identifier:  # identifier 없으면 스킵
                continue

            image_url = ""
            image_count = 0
            if isinstance(images, list) and len(images) > 0:
                image_url = "|".join(images)
                image_count = len(images)

            results.append({
                "area": area,
                "identifier": identifier,
                "description": description,
                "image_count": image_count,
                "image": image_url
            })
        except Exception as e:
            print(f"[WARN] {area} 매물 {i} 추출 오류: {e}")

    temp_df = pd.DataFrame(results)

    # -----------------------------
    # 신규 매물 판별 및 병합
    # -----------------------------

    if "identifier" in temp_df.columns and len(temp_df) > 0:
        temp_df_new = temp_df[~temp_df["identifier"].isin(existing_ids)]
    else:
        temp_df_new = pd.DataFrame(columns=combined_df.columns)  # 빈 DF로 대체

    print(f"[INFO] {area} 신규 매물 {len(temp_df_new)}건 발견")

    if len(temp_df_new) > 0:
        new_records.append(temp_df_new)  

    combined_df = pd.concat([combined_df, temp_df_new], ignore_index=True)
    existing_ids.update(temp_df_new["identifier"].tolist())


# -----------------------------
# 5. CSV 저장
# -----------------------------
# 전체 누적 저장
combined_df.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"[INFO] 누적 CSV 저장 완료 ({len(combined_df)}행)")

# 신규 매물만 별도 저장
if len(new_records) > 0:
    new_df = pd.concat(new_records, ignore_index=True)
    if len(new_df) > 0:
        new_df.to_csv(new_file, index=False, encoding="utf-8-sig")
        print(f"[INFO] 신규 매물 CSV 저장 완료 ({len(new_df)}행): {new_file}")
    else:
        print("[INFO] 이번 실행에서 신규 매물 없음.")
else:
    print("[INFO] 신규 데이터 없음 (new_records 비어 있음)")

# -----------------------------
# 종료
# -----------------------------
driver.quit()
print("[INFO] 크롬 드라이버 종료 완료")