import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel
from config_data.config import load_config
import logging
import uvicorn


class UserData(BaseModel):
    GUID: str
    Timestamp: str
    OuterIP: str
    NgToken: str


logger = logging.getLogger(__name__)


def main():
    connection = None
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')
    config = load_config()
    app = FastAPI(title='user_checker')

    try:
        #Подключение к базе данных
        connection = psycopg2.connect(host=config.host,
                                      user=config.user,
                                      password=config.password,
                                      database=config.db_name,
                                      )
        logger.info('PostgreSQL connection opened')

        #Инструкция для создания БД
        with open('create_table.txt') as file:
            create_table_text = file.read()

        #Создание БД
        with connection.cursor() as cursor:
            cursor.execute(create_table_text)
            logger.info('New table was created')
            connection.commit()

        #Пост запрос к базе и ответом
        @app.post("/checkuser")
        def check_query(user_info: UserData):
            guid = user_info.GUID
            time = user_info.Timestamp
            out_ip = user_info.OuterIP
            token = user_info.NgToken
            with connection.cursor() as cursor:
                cursor.execute(f'''SELECT OuterIP, NgToken
                                FROM UserLogs
                                WHERE GUID = '{guid}' ''')
                info = cursor.fetchone()
            if info:
                new_ip, new_token = info[0], info[1]
                if new_ip == out_ip and token == new_token:
                    return {'status':200,'user_status':'correct user' }
                else:
                    logger.warning('SUSPICIOUS ACTIVITY!')
                    return {'status':200,'user_status':'Additional verification required!' }
            else:
                return {'status':200,'user_status':'new user!' }


        uvicorn.run(app, host=config.host, port=8000)


    except Exception:
        logger.exception('Error while working with PostgreSQL')
    finally:
        if connection:
            connection.close()
            logger.info('PostgreSQL connection closed')


if __name__ == "__main__":
    main()



#{"GUID":"guid-001", "Timestamp":"2024-08-20 08:30:00", "OuterIP":"192.168.0.1", "NgToken":"token-001"}
#{"GUID":"guid-009", "Timestamp":"2024-08-20 08:30:00", "OuterIP":"192.168.0.1", "NgToken":"token-009"}
