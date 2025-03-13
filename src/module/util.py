import logging
import requests
import time
import pandas as pd


def set_loglevel(level):
    try:

        # ---------------------------------------------------------------------
        # 로그레벨 : DEBUG
        # ---------------------------------------------------------------------
        if level.upper() == 'D':
            logging.basicConfig(
                format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]:%(message)s",
                datefmt="%Y/%m/%d %I:%M:%S %p",
                level=logging.DEBUG
            )
        # ---------------------------------------------------------------------
        # 로그레벨 : ERROR
        # ---------------------------------------------------------------------
        elif level.upper() == 'E':
            logging.basicConfig(
                format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]:%(message)s",
                datefmt="%Y/%m/%d %I:%M:%S %p",
                level=logging.ERROR
            )
        # ---------------------------------------------------------------------
        # 로그레벨 : INFO
        # ---------------------------------------------------------------------
        else:
            # -----------------------------------------------------------------------------
            # 로깅 설정
            # 로그레벨(DEBUG, INFO, WARNING, ERROR, CRITICAL)
            # -----------------------------------------------------------------------------
            logging.basicConfig(
                format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d]:%(message)s",
                datefmt="%Y/%m/%d %I:%M:%S %p",
                level=logging.INFO
            )

    # ----------------------------------------
    # Exception Raise
    # ----------------------------------------
    except Exception as e:
        logging.error("Exception Raised In Setting Log Level!")
        logging.error(e)
        raise


def send_request(type, url, param, header):
    try:

        # 요청 가능회수 확보를 위해 기다리는 시간(초)
        err_sleep_time = 0.3

        # 요청에 대한 응답을 받을 때까지 반복 수행
        while True:

            # 요청 처리
            response = requests.request(type, url, params=param, headers=header)

            # 요청 가능회수 추출
            if "Remaining-Req" in response.headers:

                hearder_info = response.headers["Remaining-Req"]
                start_idx = hearder_info.find("sec=")
                end_idx = len(hearder_info)
                remain_sec = hearder_info[int(start_idx):int(end_idx)].replace("sec=", '')
            else:
                logging.error("헤더 정보 이상")
                logging.error(response.headers)
                break

            # 요청 가능회수가 3개 미만이면 요청 가능회수 확보를 위해 일정시간 대기
            if int(remain_sec) < 3:
                logging.debug("요청 가능회수 한도 도달! 남은횟수:" + str(remain_sec))
                time.sleep(err_sleep_time)

            # 정상 응답
            if response.status_code == 200 or response.status_code == 201:
                break
            # 요청 가능회수 초과인 경우
            elif response.status_code == 429:
                logging.error("요청 가능회수 초과!:" + str(response.status_code))
                time.sleep(err_sleep_time)
            # 그 외 오류
            else:
                logging.error("기타 에러:" + str(response.status_code))
                logging.error(response.status_code)
                logging.error(response)
                break

            # 요청 가능회수 초과 에러 발생시에는 다시 요청
            logging.info("[restRequest] 요청 재처리중...")

        return response

    except Exception as e:
        logging.error("Exception Raised In Sending Request!")
        logging.error(e)
        raise

def dict_list_to_dataframe(data:list):
    sorted_data = sorted(data, key=lambda x: x["timestamp"])
    df = pd.DataFrame(sorted_data)

    df = df.rename(columns={
        "candle_date_time_kst": "Date",
        "opening_price": "Open",
        "high_price": "High",
        "low_price": "Low",
        "trade_price": "Close",
        "candle_acc_trade_volume": "Volume"
    })

    # 🔹 Date 컬럼을 datetime 타입으로 변환 후 인덱스로 설정
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    df = df[~df.index.duplicated(keep='last')]

    return df

