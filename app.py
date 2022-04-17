from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('15.164.250.227', 27017, username="test", password="test")
db = client.dbsparta_plus_week3


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/matjip', methods=["GET"])
def get_matjip():
    # 맛집 목록을 반환하는 API
    # 1 단계 : 데이터베이스에서 맛집 목록을 꺼내와야 한다.
    matjip_list = list(db.matjips.find({}, {'_id' : False}))
    # 2 단계 : 그걸 클라이언트에 돌려준다.
    return jsonify({'result': 'success', 'matjip_list': matjip_list})

@app.route('/api/save_bookmark', methods=["POST"])
def save_bookmark():
    bookmark_receive = request.form['bookmark_give']
    title_receive = request.form['index_give']
    doc = {
        'bookmark_status' : bookmark_receive
    }
    db.matjips.update({'title' : title_receive}, {'$set': {doc}})
    return jsonify({'result' : 'success', 'msg' : '북마크 저장완료'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)