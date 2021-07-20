# coding=utf-8

import os
from time import sleep, time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer

import addressing_airCondition as ads_ac
import addressing_environment as ads_env

import logging

stamp = '0528'
logging.basicConfig(filename='sensor_log'+stamp+'.log', level=logging.WARNING)  #INFO  DEBUG
log = logging.getLogger()


def ac_modbus2mongodb():
    try:
        t = time()

        DBclient = MongoClient('mongodb://192.168.1.10/',
                               username='sensorManager',
                               password='manage123456',
                               authSource='admin',
                               serverSelectionTimeoutMS=1000)

        # try:  # 数据库连接测试
        #     # The ismaster command is cheap and does not require auth.
        #     DBclient.admin.command('ismaster')
        # except ConnectionFailure as e:  # Exception
        #     DBclient.close()
        #     log.error(e)
        #     # print("Server not available")
        #     return

        db = DBclient['sensor_management']
        collection = db['ac_test_'+stamp]
        logger = db['ac_logger_'+stamp]

        equipments = [{} for i in range(9)]
        for i in range(5):  # 12345总线读数据
            client = ModbusClient(ads_ac.conn[i][0], port=ads_ac.conn[i][1], timeout=3, framer=ModbusFramer)
            bus = ads_ac.buses[i]

            is_connected = client.connect()
            if not is_connected:  # modbus连接失败
                data_db = {'name': 'bus{:0>1d}'.format(i + 1),
                           'err': 'Modbus Connect Failed',
                           'datetime': datetime.now()}
                result = logger.insert_one(data_db)
                client.close()
                sleep(1)
                continue

            sleep(1)
            rr = client.read_coils(ads_ac.rgs_start, ads_ac.len_data, unit=ads_ac.box_ads)
            if hasattr(rr, 'bits'):
                checkout = rr.bits
            else:
                data_db = {'name': 'bus{:0>1d}:'.format(i + 1),
                           'message': rr.message,
                           'err': 'Checkout Failed',
                           'datetime': datetime.now()}
                result = logger.insert_one(data_db)
                checkout = [True for i in range(16)]

            for j in range(len(bus)):
                if checkout[j]:
                    sleep(1)
                    rr = client.read_holding_registers(ads_ac.rgs_start + j * ads_ac.rgs_len, ads_ac.len_data, unit=ads_ac.box_ads)
                    if not hasattr(rr, 'registers'):  # 无返回数据
                        data_db = {
                            'name': 'bus{:0>1d}:'.format(i + 1) + ads_ac.equipment_index[bus[j][0]] + '-' + bus[j][1],
                            'message': rr.message,
                            'err': 'No Data Return',
                            'datetime': datetime.now()}
                        result = logger.insert_one(data_db)
                        continue
                    data_modbus = rr.registers
                    type = data_modbus[0] // 256  # 数据类型
                    if type != bus[j][2]:
                        data_db = {
                            'name': 'bus{:0>1d}:'.format(i + 1) + ads_ac.equipment_index[bus[j][0]] + '-' + bus[j][1],
                            'data': data_modbus,
                            'err': 'Wrong Type Index: Should be 0x{:0X}, but accepted 0x{:0X}'.format(bus[j][2],
                                                                                                      type),
                            'datetime': datetime.now()}
                        result = logger.insert_one(data_db)
                        continue
                    pos = data_modbus[0] % 16  # 小数位数
                    sign_n = data_modbus[0] % 256 - pos  ## 有无符号
                    if sign_n == 0x80:
                        sign = True  # 有符号
                    elif sign_n == 0x00:
                        sign = False  # 无符号
                    else:
                        data_db = {
                            'name': 'bus{:0>1d}:'.format(i + 1) + ads_ac.equipment_index[bus[j][0]] + '-' + bus[j][1],
                            'data': data_modbus,
                            'err': 'Wrong Sign Index: Should be 0x{:0X} or 0x{:0X}, but accepted 0x{:0X}'.format(
                                0x80, 0x00, sign_n),
                            'datetime': datetime.now()}
                        result = logger.insert_one(data_db)
                        continue
                    data_origin = data_modbus[1]
                    if sign and data_origin >= 32767:
                        data = -(65536 - data_origin) / (10 ** pos)
                    else:
                        data = data_origin / (10 ** pos)
                    equipments[bus[j][0]][bus[j][1]] = data

                else:
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads_ac.equipment_index[bus[j][0]] + '-' + bus[j][1],
                               'data': checkout,
                               'err': 'The Sensor Is Outline',
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
            client.close()

        for i in range(5, 9):  # 6789总线读数据
            client = ModbusClient(ads_ac.conn[i][0], port=ads_ac.conn[i][1], timeout=3, framer=ModbusFramer)
            bus = ads_ac.buses[i]

            is_connected = client.connect()
            if not is_connected:  # modbus连接失败
                data_db = {'name': 'bus{:0>1d}'.format(i + 1),
                           'err': 'Modbus Connect Failed',
                           'datetime': datetime.now()}
                result = logger.insert_one(data_db)
                client.close()
                sleep(1)
                continue

            sleep(1)
            rr = client.read_holding_registers(ads_ac.rgs_start, ads_ac.len_data, unit=ads_ac.box_ads)
            if not hasattr(rr, 'registers'):  # 无返回数据
                data_db = {'name': 'bus{:0>1d}:'.format(i + 1),
                           'message': rr.message,
                           'err': 'No Data Return',
                           'datetime': datetime.now()}
                result = logger.insert_one(data_db)
                continue
            data_modbus = rr.registers
            for j in range(len(bus)):
                type = data_modbus[2 * j] // 4096  # 数据类型 C0
                if type != 12:
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads_ac.equipment_index[bus[j][0]] + '-' + bus[j][1],
                               'data': data_modbus,
                               'err': 'Wrong Type Index: Should be 0xC0, but accepted 0x{:0X}'.format(type),
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue
                pos = data_modbus[0] % 256  # 小数位数
                data_origin = data_modbus[2 * j + 1] / (10 ** pos)
                inf0 = ads_ac.i2v[0][0]
                sup0 = ads_ac.i2v[0][1]
                inf1 = ads_ac.i2v[bus[j][2]][0]
                sup1 = ads_ac.i2v[bus[j][2]][1]
                if inf0 <= data_origin <= sup0:
                    data = (data_origin - inf0) / (sup0 - inf0) * (sup1 - inf1) + inf1
                else:
                    data_db = {'name': 'bus{:0>1d}:'.format(i + 1) + ads_ac.equipment_index[bus[j][0]] + '-' + bus[j][1],
                               'data': data_modbus,
                               'err': 'Wrong Value Range: Should be 4~20, but accepted {:0X}'.format(data_origin),
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue
                equipments[bus[j][0]][bus[j][1]] = data
            client.close()

        # for eqt in range(9):  # 9个设备写入数据库
        #     data_db = {'name': ads_ac.equipment_index[eqt],
        #                'data': equipments[eqt],
        #                'datetime': datetime.now()}
        #     result = collection.insert_one(data_db)
        data_db = []
        for eqt in range(9):  # 9个设备写入数据库
            data_db.append({'name': ads_ac.equipment_index[eqt],
                            'data': equipments[eqt],
                            'datetime': datetime.now()})
        result = collection.insert_many(data_db)

        # meter
        client = ModbusClient(ads_ac.conn[9][0], port=ads_ac.conn[9][1], timeout=3, framer=ModbusFramer)
        bus = ads_ac.bus_meter
        is_connected = client.connect()
        if is_connected:  # modbus连接失败
            data = {}
            for i in range(len(bus)):
                sleep(1)
                rr = client.read_holding_registers(bus[i][1], bus[i][2], unit=ads_ac.box_ads)
                if not hasattr(rr, 'registers'):  # 无返回数据
                    data_db = {'name': 'meter',
                               'message': rr.message,
                               'err': 'No Data Return',
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue
                data_modbus = rr.registers
                value = 0
                for j in range(bus[i][2]):
                    value += data_modbus[j] * 0x10000 ** (bus[i][2] - j - 1)
                data[bus[i][0]] = value
            client.close()
            data_db = {'name': 'meter',
                       'data': data,
                       'datetime': datetime.now()}
            result = collection.insert_one(data_db)
        else:
            data_db = {'name': 'bus_meter',
                       'err': 'Modbus Connect Failed',
                       'datetime': datetime.now()}
            result = logger.insert_one(data_db)
            client.close()
            sleep(1)

        # host
        client = ModbusClient(ads_ac.conn[10][0], port=ads_ac.conn[10][1], timeout=3, framer=ModbusFramer)
        bus = ads_ac.bus_host
        is_connected = client.connect()
        if is_connected:  # modbus连接失败
            data = {}
            for i in range(len(bus)):
                sleep(1)
                rr = client.read_holding_registers(bus[i][1], bus[i][2], unit=ads_ac.box_ads)
                if not hasattr(rr, 'registers'):  # 无返回数据
                    data_db = {'name': 'host',
                               'message': rr.message,
                               'err': 'No Data Return',
                               'datetime': datetime.now()}
                    result = logger.insert_one(data_db)
                    continue
                data_modbus = rr.registers
                data[bus[i][0]] = data_modbus
            client.close()
            # data_db = {'name': 'meter',
            #            'data': data,
            #            'datetime': datetime.now()}
            data['name'] = 'host'
            data['datetime'] = datetime.now()
            result = collection.insert_one(data)
        else:
            data_db = {'name': 'bus_host',
                       'err': 'Modbus Connect Failed',
                       'datetime': datetime.now()}
            result = logger.insert_one(data_db)
            client.close()
            sleep(1)

    except ConnectionFailure as e:
        log.error(e)
    except Exception as e:
        # log.exception(e)
        # client.close()
        # DBclient.close()
        log.error(e)
        return
    finally:
        DBclient.close()
        # log.info('Time Consuming: ' + str(time() - t))

def env_modbus2mongodb():
    try:
        t = time()

        DBclient = MongoClient('mongodb://192.168.1.10/',
                               username='sensorManager',
                               password='manage123456',
                               authSource='admin',
                               serverSelectionTimeoutMS=1000)

        # try:  # test db connect
        #     # The ismaster command is cheap and does not require auth.
        #     DBclient.admin.command('ismaster')
        # except ConnectionFailure as e:  # Exception
        #     DBclient.close()
        #     log.error(e)
        #     # print("Server not available")
        #     return

        db = DBclient['sensor_management']
        collection = db['env_test_'+stamp]

        for bus in range(1, 12):
            client = ModbusClient(ads_env.conn[bus - 1][0], port=ads_env.conn[bus - 1][1], timeout=3, framer=ModbusFramer)

            is_connected = client.connect()
            if not is_connected:  # modbus connect fail
                data_db = {'name': '{:0>2d}xxxx'.format(bus),
                           'err': 'Modbus Connect Failed',
                           'datetime': datetime.now()}
                result = collection.insert_one(data_db)
                client.close()
                sleep(1)
                continue

            for box in range(ads_env.busBox[bus - 1], ads_env.busBox[bus]):  # box index (begin from 0)
                sleep(1)
                rr = client.read_holding_registers(ads_env.rgs, ads_env.len_data, unit=box + 1)
                if not hasattr(rr, 'registers'):  # no data return
                    data_db = {'name': '{:0>2d}{:0>2d}xx'.format(bus, box + 1),
                               'message': rr.message,
                               'err': 'No Data Return',
                               'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                    continue
                data_modbus = rr.registers

                err_d = True
                for k in range(112):
                    if (data_modbus[k] != 0):
                        err_d = False
                        break
                    pass
                if err_d:
                    data_db = {'name': '{:0>2d}{:0>2d}xx'.format(bus, box + 1),
                               'data': data_modbus,
                               'err': 'All Null',
                               'datetime': datetime.now()}
                    result = collection.insert_one(data_db)
                else:
                    for i in range(ads_env.box_num[box][0]):  # 二合一编号（0开始）
                        pos_two = ads_env.two_start + ads_env.two_len * i
                        # print('two', data_modbus[pos_two + ads_env.pos_name], (box+1) * 256 + i+1)
                        if data_modbus[pos_two + ads_env.pos_name] == (box + 1) * 256 + ads_env.two_start + i + 1:
                            data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads_env.two_start + i + 1),
                                       'two_in_one': {
                                           ads_env.two_type[j]: data_modbus[pos_two + ads_env.pos_data + j] * ads_env.two_carry[j]
                                           for j in range(2)},
                                       'datetime': datetime.now()}
                        else:
                            data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads_env.two_start + i + 1),
                                       'data': data_modbus,
                                       'err': 'Unexpected Data Received',
                                       'datetime': datetime.now()}
                        result = collection.insert_one(data_db)
                    for i in range(ads_env.box_num[box][1]):  # 六合一编号
                        pos_six = ads_env.six_start * ads_env.two_len + ads_env.six_len * i
                        if data_modbus[pos_six + ads_env.pos_name] == (
                                box + 1) * 256 + ads_env.six_start + i + ads_env.six_bios + 1:
                            data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads_env.six_start + i + 1),
                                       'six_in_one': {
                                           ads_env.six_type[j]: data_modbus[pos_six + ads_env.pos_data + j] * ads_env.six_carry[j]
                                           for j in range(6)},
                                       'datetime': datetime.now()}
                        else:
                            data_db = {'name': '{:0>2d}{:0>2d}{:0>2d}'.format(bus, box + 1, ads_env.six_start + i + 1),
                                       'data': data_modbus,
                                       'err': 'Unexpected Data Received',
                                       'datetime': datetime.now()}
                        result = collection.insert_one(data_db)
            client.close()
    except ConnectionFailure as e:
        log.error(e)
    except Exception as e:
        log.error(e)
        return
    finally:
        DBclient.close()
        # log.info('Time Consuming: ' + str(time() - t))

def power_modbus2mongodb():
    try:
        t = time()

        DBclient = MongoClient('mongodb://192.168.1.10/',
                               username='sensorManager',
                               password='manage123456',
                               authSource='admin',
                               serverSelectionTimeoutMS=1000)

        # try:  # 数据库连接测试
        #     # The ismaster command is cheap and does not require auth.
        #     DBclient.admin.command('ismaster')
        # except ConnectionFailure as e:  # Exception
        #     DBclient.close()
        #     log.error(e)
        #     # print("Server not available")
        #     return

        db = DBclient['sensor_management']
        # collection = db['air_condition']
        collection = db['power_test_'+stamp]

        name = ['room1', 'room2', 'room4']
        gateway = [24, 48, 87]
        register = [0x2000, 0x4000]
        length = [18, 2]

        var_n = [
            [
                ['voltage', 0],
                ['electric_current', 2],
                ['instant_total_active_power', 4],
                ['instant_useless_total_power', 6],
                ['instant_apparent_total_power', 8],
                ['power_factor_total', 10],
                ['grid_frequency', 14],
            ],
            [
                ['total_active_energy', 0]
            ]
        ]

        client = ModbusClient('192.168.1.146', port=12345, timeout=3, framer=ModbusFramer)
        is_connected = client.connect()
        if is_connected:  # modbus connect fail
            for i in range(3):
                data = {}
                for j in range(2):
                    sleep(1)
                    rr = client.read_holding_registers(register[j], length[j], unit=gateway[i])
                    if hasattr(rr, 'registers'):
                        # data_modbus = {}
                        for v in var_n[j]:

                            # IEEE-754 hex to float
                            B = '{:0>16b}{:0>16b}'.format(rr.registers[v[1]], rr.registers[v[1] + 1])
                            s = int(B[0])
                            e = int(B[1:9], 2) - 127
                            M = B[9:32]
                            if e > 0:
                                Mi = int('1' + M[0:e], 2)
                                Mf = M[e:23]
                            elif e == 0:
                                Mi = 1.0
                                Mf = M
                            else:
                                Mi = 0.0
                                Mf = '1' + M
                                for k in range(-e - 1):
                                    Mf = '0' + Mf
                            xm = 0.0
                            for k in range(len(Mf)):
                                xm += int(Mf[k]) / 2 ** (k + 1)
                            x = (-1) ** s * (Mi + xm)

                            data[v[0]] = x
                    else:  # no data return
                        data['0x{:4x}'.format(register[j])] = 'No Data Return'
                data_db = {'name': name[i],
                           'data': data,
                           'datetime': datetime.now()}
                result = collection.insert_one(data_db)

        else:
            data_db = {'name': 'power',
                       'err': 'Modbus Connect Failed',
                       'datetime': datetime.now()}
            result = collection.insert_one(data_db)
        client.close()
    except ConnectionFailure as e:
        log.error(e)
    except Exception as e:
        # log.exception(e)
        # client.close()
        # DBclient.close()
        log.error(e)
        return
    finally:
        DBclient.close()
        # log.info('Time Consuming: ' + str(time() - t))

def sensor_manage():
    ac_modbus2mongodb()
    env_modbus2mongodb()
    power_modbus2mongodb()


if __name__ == '__main__':

    job_defaults = {
        'coalesce': True,
        'misfire_grace_time': 120,
        'max_instances': 2
    }
    trigger = OrTrigger([CronTrigger(minute=i) for i in range(0, 60, 5)])
    scheduler = BackgroundScheduler(job_defaults=job_defaults)  # jobstores=jobstores
    # scheduler.add_job(env_modbus2mongodb_next, 'interval', seconds=300, id='env_bus2db',
    #                   replace_existing=True)
    scheduler.add_job(sensor_manage, trigger=trigger, id='env_bus2db',
                      replace_existing=True)  # , jobstore='mongo'
    scheduler.start()
    log.info('Start Time: ' + str(datetime.now()))
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            sleep(10)
    # except (KeyboardInterrupt, SystemExit):
    except Exception as e:
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
        log.error(e)
        log.info('End Time: ' + str(datetime.now()))
