import json
import pandas as pd
import requests
import time
import sqlite
import re
import os
path = os.getcwd()

def get_block(address):
    api_response = requests.get('https://blockchain.info/rawblock/' + address + "?json").content
    data = json.loads(api_response)
    dataframe = pd.DataFrame.from_dict(data, orient="index")
    dataframe = dataframe.applymap(str)
    dataframe.columns = ['Value']
    print(dataframe)
    return dataframe


def get_transaction(address):
    api_response = requests.get('https://blockchain.info/rawtx/' + address + "?json").content
    data = json.loads(api_response)
    dataframe = pd.DataFrame.from_dict(data, orient="index")
    dataframe = dataframe.applymap(str)
    dataframe.columns = ['Value']
    print(dataframe)
    return dataframe

def get_address(address):
    api_response = requests.get('https://blockchain.info/rawaddr/' + address + "?json").content
    data = json.loads(api_response)
    dataframe = pd.DataFrame.from_dict(data, orient="index")
    dataframe = dataframe.applymap(str)
    dataframe.columns = ['Value']
    print(dataframe)
    return dataframe


# FOR LABELS AND SAVING TO DB
def gettxdetails(dataframe):
    inputs = dataframe.iat[14, 0]
    inputs = inputs[1:-1]
    inputs = inputs.split(',')
    inputaddr = list(filter(lambda x: 'addr' in x, inputs))
    inputvals = list(filter(lambda x: 'value' in x, inputs))

    outputs = dataframe.iat[15, 0]
    outputs = outputs[1:-1]
    outputs = outputs.split(',')
    outputvals = list(filter(lambda x: 'value' in x, outputs))
    outputaddr = list(filter(lambda x: 'addr' in x, outputs))

    inpAddrList = []
    for i in inputaddr:
        string = re.sub(r"[^a-zA-Z0-9]", "", i)
        string = string.replace('addr', '')
        inpAddrList.append(string)

    inpValList = []
    for i in inputvals:
        string = re.sub(r"[^a-zA-Z0-9]", "", i)
        string = string.replace('value', '')
        inpValList.append(string)

    outpAddrList = []
    for i in outputaddr:
        string = re.sub(r"[^a-zA-Z0-9]", "", i)
        string = string.replace('addr', '')
        outpAddrList.append(string)

    outpValList = []
    for i in outputvals:
        string = re.sub(r"[^a-zA-Z0-9]", "", i)
        string = string.replace('value', '')
        outpValList.append(string)

    total = 0
    for i in outpValList:
        total = total + int(i)

    total = total / 100000000
    total = ('%.8f' % total)
    txtime = gettxtime(dataframe)
    graphlist = [total, txtime]
    df = pd.DataFrame(graphlist)
    df = df.T
    df.columns = ['Amount', 'Time']
    return df, inpAddrList, inpValList, outpAddrList, outpValList


def graphblock():
    df = sqlite.get_block_graph_data()
    bIndex = df['block_index'].tolist()
    time_list = df['time'].tolist()
    sorted_time_list = []
    for i in time_list:
        epochtime = int(i)
        txtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epochtime))
        sorted_time_list.append(txtime)
    TXnum_list = df['n_tx'].tolist()
    data2 = {"BlockIndex": bIndex, "Date": sorted_time_list, "NumberofTx": TXnum_list}
    df2 = pd.DataFrame.from_dict(data2)
    df2 = df2.astype({'BlockIndex': 'int', 'NumberofTx': 'int'})
    df2['Date'] = pd.to_datetime(df2['Date'])
    df2.sort_values(by='Date', inplace=True)

    return df2

def graphtx():
    df = sqlite.get_tx_graph_data()
    total_List = df['Amount'].tolist()
    total_List = [float(x) for x in total_List]
    time_List = df['Time'].tolist()

    data2 = {"Date": time_List, "Amount": total_List}
    df2 = pd.DataFrame.from_dict(data2)

    df2 = df2.astype({'Amount': 'float'})
    df2['Date'] = pd.to_datetime(df2['Date'])
    df2.sort_values(by='Date', inplace=True)

    return df2


def graphaddr():
    df = sqlite.get_address_graph_data()
    addresslist = df['address'].tolist()
    sentlist = df['total_sent'].tolist()
    sentlist = list(map(int, sentlist))
    receivedlist = df['total_received'].tolist()
    receivedlist = list(map(int, receivedlist))
    txsTotalList = df['n_tx'].tolist()
    BTCSentList = []
    BTCReceivedList = []
    for i in sentlist:
        string = valuetoBTC(i)
        BTCSentList.append(string)
    for i in receivedlist:
        string = valuetoBTC(i)
        BTCReceivedList.append(string)

    data2 = {"Address": addresslist, "Sent": BTCSentList, "Received": BTCReceivedList}
    df2 = pd.DataFrame.from_dict(data2)
    df2.set_index('Address')

    df2 = df2.astype({"Sent": 'float', 'Received': 'float'})

    return df2


def valuetoBTC(strValue):
    value = int(strValue)
    value = value / 100000000
    btc = ('%.8f' % value)
    return btc


def gettxtime(dataframe):
    epochtime = int(dataframe.iat[11, 0])
    txtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epochtime))
    return txtime


def latestblock():
    response_API = requests.get('https://blockchain.info/latestblock/')
    data = response_API.text
    parse_json = json.loads(data)
    json_object = json.dumps(parse_json, indent=0)
