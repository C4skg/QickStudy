from . import server
from ..config import Config

from flask import current_app,request
from flask import render_template
from elasticsearch import Elasticsearch

client = Elasticsearch(
    [Config.ELASTICSEARCH_HOST],
    http_auth=(Config.ELASTICSEARCH_USER,Config.ELASTICSEARCH_PASSWORD),
    sniff_on_start=False,
    sniff_on_connection_fail=False,
    sniffer_timeout=None
)

class EsBasic:
    index = 'Qick_index'

@current_app.cli.command()
def create_index():
    client.indices.create(index=EsBasic.index)

@server.route('/search',methods=['POST'])
def search():
    '''
        @search for user
        @search for article
        @search for all infos
    '''

    pass;


@server.route('/<user>/search',methods=['POST'])
def usearch():
    '''
        @search for <user> 's info
    ''' 
    pass;


'''
@methods exports
'''
def add_document():
    pass