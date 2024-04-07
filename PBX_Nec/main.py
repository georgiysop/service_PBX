# file connect to ATC

import socket
import time
import os


from helpers.client_request_to_server import *
from helpers.parser_smdr_nec import *
from helpers.parser_string_ring import add_sql_table
from helpers.create_sql_tables import *



def station_nec(ip_adress_station):

    save = []
    check_table()
    client = socket.socket()
    client.connect((ip_adress_station, 60010))
    print('Connect station', ip_adress_station,'...')

    while True:
        time.sleep(1)  # Отправляем запрос на сервер каждую 1 секунду
        
        print('_______________________________________________________________________________________________________________________________________________________________________________ ')
        client.send(request_on_data())
        print('Отправляем данные серверу: ', request_on_data())
        data = client.recv(1024) #получаем строку в байтовом виде (сервер послал ответ на запрос №2)
        data_ascii = data.decode('utf-8',errors='ignore') #преобразуем в строку ASCII
        data_slice = slice_data(data_ascii) #парсим нашу строчку в "нормальный вид" -_-
        #print('Последовательность: ', get_sequnce_data(data_ascii)) #последовательность спарсенная с полученной строчки
        #print('Принимаемые данные от сервера(в Bytes): ', data)
        #print('Принимаемые данные от сервера(в ASCII): ', data_ascii)
        print('Принимаемые данные от сервера(в Normal view): ',  data_slice)

        # Получаем ответ от сервера
        client.send(response_client_from_PBX(get_sequnce_data(data_ascii)))
        client.send(request_monitor())
        print('Отправляем данные подтверждения серверу: ', response_client_from_PBX(get_sequnce_data(data_ascii)))
        print()
        
        # Обрабатываем исключения и добавляем в базу SQL_lite    
        if data != b'\x16300003002\x00':
            if save != data_slice and add_sql_table(data_slice)[5] != '' and add_sql_table(data_slice)[5] != 'Внутренний':
                print('Данные добавленные в базу: ',add_sql_table(data_slice))
                insert_to_table(add_sql_table(data_slice))
                save = data_slice 


if __name__ == "__main__":
    station_nec(os.environ['IP_ADRESS'])
