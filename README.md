# README #

### 개발 개요 ###

대학원 연구 주제인 Thumbnail Visualization 유저스터디를 위해 Amazon Mechanical Turk 를 활용하였습니다.
MTurk 에 사용된 실험 페이지를 구현하였고, 실험 결과는 django의 sqlite3 DB에 저장됩니다. (실제 데이터는 삭제함)
각 실험의 결과 및 통계데이터는 vue.js로 구현된 대시보드를 통해 실시간으로 확인이 가능합니다. 

* 개발 기간 : 2019.2 ~ 2019.6
* 개발 인원 : 2명. 개발 리더 담당
* 사용 스택 : html, Vue.js, python-Django, sqlite3

### 예시 ###
![image](https://user-images.githubusercontent.com/8486747/133775609-5a39ba43-3233-4e06-a066-9cd7916712ec.png)


### 실행 방법 ###
<pre>
<code>
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
</code>
</pre>
