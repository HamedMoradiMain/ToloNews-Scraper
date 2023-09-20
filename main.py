import requests
from configparser import ConfigParser
import mysql.connector
class telegramBot:
    def send_message(self,image,des):
        config_object = ConfigParser()
        with open("config.ini","r") as file_object:
            config_object.read_file(file_object)
            token=config_object.get("api","bot_token")
            chat_id = config_object.get("api","chat_id")
        url = f"https://api.telegram.org/bot{token}/sendPhoto"
        payload = {
        "chat_id": chat_id,
        "photo": image,
        "caption": des,
        "disable_notification": False,
        "reply_to_message_id": None}
        headers = {
        "accept": "application/json",
        "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
        "content-type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
    def run(self):
        try:
            connection = mysql.connector.connect(host='localhost',
                                         database='news',
                                         user='root',
                                         password='')
            sql_select_Query = "select * from latest"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            # get all records
            records = cursor.fetchall()
            for row in records:
                if len(row[2]) > 3:
                    news_image_url = "https://tolonews.com"+row[2].replace("[",'').replace(']','').replace("'",'')
                else:
                    news_image_url = 'https://yt3.googleusercontent.com/KWO2AbFNmJ37cgI52cquwrNXr365EdJMsJEicm-bzK_litK8Ak0m9vBrDYE4zx5L10lHmF2E9-o=s900-c-k-c0x00ffffff-no-rj'
                news_title = row[1].replace("/n","").replace("[",'').replace("]",'').replace("'",'').strip()[2:-2]
                news_url = row[3]
                news_description = row[4]
                des = news_title 
                self.send_message(news_image_url,des)   
        except mysql.connector.Error as e:
                print("Error reading data from MySQL table", e)
        finally:
            if connection.is_connected():
                connection.close()
                cursor.close()
        print("MySQL connection is closed")

if __name__ == "__main__":
    obj = telegramBot()
    text = "Hello!"
    obj.run()







