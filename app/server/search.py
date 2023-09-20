from . import server
from flask import current_app,request
from flask import render_template,jsonify
from flask_login import login_required
from flask_login import current_user
from .. import EsClient


class SearchServiceError(ValueError):
    pass;


@server.route('/search')
@login_required
def search():
    '''
        @search for article
        @area: all user
    '''
    response = {
        'code': 400,
        'result': ''
    }

    query = request.args.get('q','',str);
    if query == '' or not query:
        return response;

    try:
        result = EsClient.search(
            index=current_app.config.get('ELASTICSEARCH_INDEX') or '' ,
            query={
                'regexp': {
                    'context': f'.*{query}.*'
                }
            }
        )
        response['code'] = 200
        response['result'] = result
    except:
        response['result'] = 'error';
        
    
    return response;


@server.route('/<int:userid>/search')
@login_required
def usearch(userid:int):
    '''
        @search for <user> 's article
    '''
    response = {
        'code': 400,
        'result': ''
    }

    print(userid)

    query = request.args.get('q','',str);
    if query == '' or not query:
        return jsonify(response);

    try:
        result = EsClient.search(
            index=current_app.config.get('ELASTICSEARCH_INDEX') or '' ,
            query={
                'regexp': f'.*{query}.*'
            }
        )

        response['code'] = 200
        response['result'] = result
    
    except:
        response['result'] = 'error'
    
    return jsonify(response);


'''
    @ search views with html document
'''
@server.route('/view/search')
@login_required
def searchView():
    data = {}
    return render_template(
        'search/search.html',**data
    )