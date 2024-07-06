import datetime
import urllib.request
from tqdm import tqdm

#Caso fosse salvar no HDFS direto - mas n consegui processar o R de lá, então vou mover no final da transformacaoS
    # from hdfs import InsecureClient
    # from urllib.request import urlopen
    #client = KerberosClient('http://localhost:9870')
    #client = InsecureClient('http://localhost:9870',user='Daniel')

    # def get_data_uf_ano_mes(uf, ano, mes, path):
    #     url = f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/RD{uf}{ano}{mes}.dbc"
        
    #     hdfs_path = f"/DataSus/rd/dbc/landing/RD{uf}{ano}{mes}.dbc"

    #     with urlopen(url) as response:
    #         content = response.read()
    #         with client.write(hdfs_path,overwrite=True) as writer:
    #             writer.write(content)

def get_data_uf_ano_mes(uf, ano, mes, path):
    url = f"ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/RD{uf}{ano}{mes}.dbc"
    
    file_path = f"{path}/RD{uf}{ano}{mes}.dbc"
    try:
        resp = urllib.request.urlretrieve(url, file_path)
    except:
        print(f"Não foi possivel coletar o arquivo: RD{uf}{ano}{mes}.dbc")
def get_data_uf(uf, datas, path):
    print(uf)

    for i in tqdm(datas):
        ano, mes, dia = i.split("-")
        ano = ano[-2:]
        get_data_uf_ano_mes(uf, ano, mes, path)

def date_range(start, stop, monthly=False):
    dt_start = datetime.datetime.strptime(start, '%Y-%m-%d')
    dt_stop = datetime.datetime.strptime(stop, '%Y-%m-%d')
    dates =[]

    while dt_start <= dt_stop:
        dates.append(dt_start.strftime("%Y-%m-%d"))
        dt_start += datetime.timedelta(days=1)

    if monthly:
        return [i for i in dates if i.endswith("01")]
    
    return dates