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

@app.route('/like_matjip', methods=["POST"])
def like_matjip():
    # 즐겨찾기 like 를 저장하는 db 기능 만들기
    title_receive = request.form['title_give']
    address_receive = request.form['address_give']
    action_receive = request.form['action_give'] #좋아하기 버튼을 눌렀는지, 좋아하기 해제 버튼을 눌렀는지에 대한 액션 구분
    
    if action_receive == 'like':
        db.matjips.update_one({'title' : title_receive, 'address' : address_receive}, {'$set' : {'liked' : True}})  # 앞에는 {업데이트할 대상을 매칭하는 조건}, {'$set' : ~~} 는 해당 조건이면 이걸로 업데이트
    else : 
        db.matjips.update_one({'title' : title_receive, 'address' : address_receive}, {'$unset' : {'liked' : False}}) # 이건 action 상태가 like 가 아니면 liked 를 지워주기 , '$unset' 은 업데이트가 아닌, 필드 삭제하는 업데이트다. '$unset' 뒤에 삭제할는 필드 : '', 'false', 'true' 뭐를 넣던 간에 상관 없음. 
    return jsonify({'result' : 'success'}) 

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)