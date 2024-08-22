## 목적
* LMS 메시지 송신 시 080 번호로 수신 거부를 하면 080 업체에서 API 로 전달함.
* 메세지를 받으면 DB에 적재하여 마케팅 팀에 전달

* API 규격
<pre><code>
 curl -X POST http://127.0.0.1:5000/add_user \
      -H "Content-Type: application/json" \
      -d '{"id": "user123", "phone": "010-1234-5678"}'
</code></pre>

* mysql테이블세팅
  <pre><code>
    CREATE TABLE users (
    id VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    PRIMARY KEY (id)
    );
</code></pre>
<hr/>

