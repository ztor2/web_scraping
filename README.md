# Youtube Web Scraping
<br>Selenium과 BeautifulSoup를 이용한 유튜브 영상 정보 및 댓글 데이터 수집.<br>

최종 코드 테스트: 2021년 10월 29일

<br>

### 연구 배경 및 목적
- 이 저장소의 코드는 중소기업기술정보진흥원 주관의 '2020 기술혁신개발사업'에서 ㈜아이패밀리에스씨 R&D Center와 서울과학기술대학교가 협력 수행 중인 '**화장품 소비자 분석 시스템 프로젝트**'에서 데이터 수집 파트 수행을 위해 작성되었다.
- 이 프로젝트에서는 화장품 리뷰사이트, 블로그, 동영상 플랫폼 등 다양한 플랫폼에서 화장품 관련 데이터를 수집해 활용하는 것을 목표로 하며, 이 저장소의 코드는 그 중 유튜브 플랫폼의 영상 관련 데이터 수집을 수행한다. 

<br>

### 코드 파일 설명
- **ytube.py:** 스크래핑 수행 파일을 위해 실행되는 파일. 데이터를 수집하고, DB에 저장한다.
- **ytube_utils.py:** ytube.py에서 사용되는 함수들이 포함된 파일. 각종 전처리 함수를 포함한다.
- **db_model.py:** 데이터를 DB에 삽입하기 위한 각종 함수들을 포함한다.
- **product_sample.json:** 샘플 영상 정보 데이터 파일.
- **cmt_sample.json:** 샘플 영상 댓글 데이터 파일.
- **sample_data.ipynb:** 샘플 데이터를 dataframe으로 변환해 확인해볼 수 있는 notebook 파일.
<br> 

- 해당 코드는 데이터 스크래핑 후 DB에 데이터를 저장하는 두 단계의 작업을 순차적으로 실행한다.
- 로컬 환경에서는 ytube.py 파일에서 ytube_to_db 함수 실행부분을 비활성화하고 ytube_getdata 에서 출력되는 데이터(vid_data, vid_comment_data)만을 저장함으로써 코드를 테스트할 수 있다.

<br>

### 데이터 수집 항목
#### 영상 데이터(vid_data)
- 영상 제목(vid_title)
- 영상 설명(vid_description)
- 게시자 닉네임(vid_creator)
- 조회수(vid_view_count)
- 좋아요/싫어요 수(vid_like(dislike)_count)
- 영상 게시일(vid_date)
- 댓글 수(vid_total_comment_count)
- 영상 게시 채널 팔로워 수(vid_creator_follower_count)

#### 영상 댓글 데이터(vid_comment_data)
- 영상 댓글 내용(comment_content)
- 댓글 게시자 닉네임(comment_user)
- 댓글 좋아요 수(comment_like_count)
- 댓글 게시일(comment_when)

<br>

### 데이터 수집 및 DB 저장 프로세스 설계
- 데이터 수집은 Selenium, BeautifulSoup 라이브러리를 이용해 수행하며, 마리아(Maria) DB로 구축된 DB에 저장된다.
- 수집할 영상 및 댓글의 수(max_vid_num, max_comment_num)를 지정할 수 있고, scrolling으로 수행되는 데이터 탐색 중 수집할 데이터 양이 입력된 수에 다다르면 데이터 탐색이 중지된다. 이를 통해 키워드와 관련 없는 맥락으로 추천되거나 불필요하게 많은 수의 데이터 수집을 방지한다.
- 유튜브의 경우 영상 게시일을 기준으로 필터링 검색을 수행할 수 있으므로, 시/일/주/달/연의 5개 기준으로 검색이 가능하도록 한다.
- 데이터가 중복 수집될 수 있는 가능성을 고려해 DB에 저장 시 중복을 확인하도록 한다. 이 때, 중복이 확인될 경우 새로운 행을 추가하지 않고 기존의 데이터를 업데이트 하는 형태로 데이터를 저장한다.
- 보다 양질의 데이터를 수집하기 위해, '유료 광고' 오버레이가 표시되는 영상은 데이터 저장 시 제목에 광고 표기가 함께 표시되게 한다. 이를 통해 광고 성격의 데이터를 필터링할 수 있다.
- 영상 데이터와 함께, 데이터 수집 로그를 함께 저장한다.
- DB는 기본 정보 데이터 테이블와 댓글 데이터 테이블로 구성되며, 각 플랫폼에 채널 번호를 부여해 여러 플랫폼에서 수집한 데이터의 구분이 가능하도록 한다.

<br>

### 데이터 수집 예시

<br>

<p align="center"> <img src="https://i.esdrop.com/d/fha5flk1blzo/4HATzSlvil.png" width="50%" align="center"> </p>
<p align="center">  <b> 그림 1. </b> 웹 스크래핑 코드 실행 예시. </p>

<br>

<p align="center"> <img src="https://i.esdrop.com/d/fha5flk1blzo/BqXyvBgJVC.png" width="45%" align="center"> </p>
<p align="center"> <img src="https://i.esdrop.com/d/fha5flk1blzo/TOxq94WQN9.png" width="60%" align="center"> </p>
<p align="center">  <b> 그림 2. </b> 웹 스크래핑을 통해 DB에 수집된 데이터 예시(위: 영상 정보 데이터 테이블, 아래: 영상 댓글 데이터 테이블). </p>
