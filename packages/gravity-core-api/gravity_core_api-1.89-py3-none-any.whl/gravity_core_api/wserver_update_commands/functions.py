""" Содержит функции-обработчики команд и их вспомогательные функции """
import datetime

import wsqluse.wsqluse

from gravity_core_api.wserver_update_commands import settings


def trash_cat_execute(sqlshell, data, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи о категории груза"""
    cat_name = data['cat_name']
    wserver_id = data['wserver_id']
    active = data['active']
    command = "INSERT INTO {} (cat_name, wserver_id, active) values ('{}', {}, {}) " \
              "ON CONFLICT (wserver_id) " \
              "DO UPDATE SET cat_name='{}', active={}"
    command = command.format(settings.trash_cats_tablename, cat_name,
                             wserver_id, active,
                             cat_name, active)
    response = sqlshell.try_execute(command)
    return response


def trash_type_execute(sqlshell, data, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи о категории груза"""
    type_name = data['name']
    wserver_id = data['wserver_id']
    active = data['active']
    wserver_category = data['category']
    command = "INSERT INTO {} (name, wserver_id, active, category) values ('{}', {}, " \
              "{}, (SELECT id FROM {} WHERE wserver_id={})) " \
              "ON CONFLICT (wserver_id) " \
              "DO UPDATE SET name='{}', active={}, category=(SELECT id FROM {} WHERE wserver_id={})"
    command = command.format(settings.trash_types_tablename, type_name,
                             wserver_id,
                             active, settings.trash_cats_tablename,
                             wserver_category,
                             type_name, active, settings.trash_cats_tablename,
                             wserver_category)
    response = sqlshell.try_execute(command)
    return response


def auto_execute(sqlshell, data, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи о машине"""
    car_number = data['car_number']
    rfid = data['rfid']
    active = data['active']
    wserver_id = data['wserver_id']
    auto_id = check_new_auto(sqlshell, car_number)
    ident_id = check_new_identifier(sqlshell, rfid)
    if ident_id:
        detach_ident_from_auto(sqlshell, ident_id)
    else:
        ident_id = create_new_ident(sqlshell, rfid)
    if auto_id:
        update_car(sqlshell, car_number, active)
    else:
        auto_id = create_new_auto(sqlshell, car_number, active)
    create_record_in_send_reports(sqlshell, 6, wserver_id, auto_id)
    fix_ident_to_auto(sqlshell, auto_id, ident_id)

def detach_ident_from_auto(sql_shell, ident_id):
    command = "UPDATE auto SET identifier=null WHERE identifier={}"
    command = command.format(ident_id)
    return sql_shell.try_execute(command)

@wsqluse.wsqluse.tryExecuteStripper
def create_new_auto(sql_shell, car_number, active):
    command = "INSERT INTO auto (car_number, active) VALUES ('{}', {})"
    command = command.format(car_number, active)
    return sql_shell.try_execute(command)


@wsqluse.wsqluse.tryExecuteStripper
def create_new_ident(sqlshell, ident):
    command = "INSERT INTO auto_idents (number, type_id) VALUES ('{}', 2)"
    command = command.format(ident)
    return sqlshell.try_execute(command)


@wsqluse.wsqluse.tryExecuteGetStripper
def check_new_identifier(sql_shell, identifier):
    command = "SELECT id FROM auto_idents WHERE number='{}' and type_id=2"
    command = command.format(identifier)
    return sql_shell.try_execute_get(command)


@wsqluse.wsqluse.tryExecuteGetStripper
def check_new_auto(sql_shell, car_number):
    """ Возвращает True, если организация уже есть в базе"""
    command = "SELECT id from auto WHERE car_number='{}'"
    command = command.format(car_number)
    return sql_shell.try_execute_get(command)


def update_car(sql_shell, car_number, active):
    command = "UPDATE auto SET active={} WHERE car_number='{}'"
    command = command.format(active, car_number)
    sql_shell.try_execute(command)


def fix_ident_to_auto(sql_shell, auto_id, ident_id):
    command = "UPDATE auto SET identifier={} WHERE id={}"
    command = command.format(ident_id, auto_id)
    return sql_shell.try_execute(command)


def clients_execute(sqlshell, data, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи о клиенте"""
    name = data['full_name']
    inn = data['inn']
    kpp = data['kpp']
    active = data['active']
    wserver_id = data['wserver_id']
    client_id = check_new_client(sqlshell, inn)
    if not client_id:
        command = "INSERT INTO clients (name) " \
                  "values ('{}') ".format(name)
        response = sqlshell.try_execute(command)
        client_id = response['info'][0][0]
        create_record_in_send_reports(sqlshell, 5, wserver_id,
                                      client_id)
        command = "INSERT INTO clients_external_info (ex_sys_id, client_id) " \
                  "VALUES (2, {})".format(client_id)
        sqlshell.try_execute(command)
        command = "INSERT INTO clients_juridical_info (client_id, inn, kpp) " \
                  "values ({}, '{}', '{}')".format(client_id, inn, kpp)
        sqlshell.try_execute(command)
        return response
    else:
        return update_client(sqlshell, client_id, inn, kpp, active)


def create_record_in_send_reports(sql_shell, table_id, wserver_id, local_id):
    command = "INSERT INTO ex_sys_data_send_reports (ex_sys_id, local_id, get," \
              "ex_sys_data_id, table_id) VALUES (2, {}, '{}', '{}', {})"
    command = command.format(local_id, datetime.datetime.now(), wserver_id,
                             table_id)
    return sql_shell.try_execute(command)


def update_client(sql_shell, client_id, inn, kpp, active):
    command = "UPDATE clients_juridical_info SET inn='{}', kpp='{}' WHERE client_id={}"
    command = command.format(inn, kpp, client_id)
    response = sql_shell.try_execute(command)
    command = "UPDATE clients SET active={} WHERE id={}".format(active, client_id)
    response = sql_shell.try_execute(command)
    return response

def check_new_client(sql_shell, inn):
    """ Возвращает True, если организация уже есть в базе"""
    command = "SELECT client_id from clients_juridical_info WHERE inn='{}'"
    command = command.format(inn)
    response = sql_shell.try_execute_get(command)
    if response:
        return response[0][0]


def update_route(sqlshell, data, *args, **kwargs):
    """ Обновить маршруты от AR """
    car_number = data['car_number']
    wserver_id = data['id']
    count = data['count']
    active = data['active']
    command = "INSERT INTO {} (car_number, count_expected, wserver_id, active) values ('{}', {}, {}, {}) " \
              "ON CONFLICT (wserver_id) DO UPDATE SET car_number='{}', count_expected={}, active={}"
    command = command.format(settings.routes_tablename, car_number, count,
                             wserver_id, active,
                             car_number, count, active)
    response = sqlshell.try_execute(command)
    # Добавляем в ответ wserver_id, который был при приеме
    response['wserver_id'] = wserver_id
    return response


def update_routes_execute(sqlshell, data, *args, **kwargs):
    all_responses = []
    for route in data:
        response = update_route(sqlshell, route)
        all_responses.append(response)
    return all_responses


def operators_execute(sqlshell, data, *args, **kwargs):
    """ Выполнить данные по созданию/обновлению записи об операторе"""
    username = data['username']
    password = data['password']
    active = data['active']
    command = "INSERT INTO {} (username, password, active) " \
              "values ('{}', '{}', {}) " \
              "ON CONFLICT (username) " \
              "DO UPDATE SET username='{}', password='{}', active={}"
    command = command.format(settings.operators_tablename,
                             username, password,  active,
                             username, password, active)
    response = sqlshell.try_execute(command)
    return response
