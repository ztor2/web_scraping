# Youtube Web Scraping
<br>Selenium과 BeautifulSoup를 이용한 유튜브 영상 정보 및 댓글 데이터 수집.

<br>

### 1. 데이터 수집 항목
#### 영상 데이터(vid_data)
- 영상 제목(vid_title)
- 영상 설명(vid_description)
- 게시자 닉네임(vid_creator)
- 조회수(vid_view_count)
- 좋아요/싫어요 수(vid_like(dislike)_count), 
- 영상 게시일(vid_date)
- 댓글 수(vid_total_comment_count)
- 영상 게시 채널 팔로워 수(vid_creator_follower_count)

#### 영상 댓글 데이터(vid_comment_data)
- 영상 댓글 내용(comment_content)
- 댓글 게시자 닉네임(comment_user)
- 댓글 좋아요 수(comment_like_count)
- 댓글 게시일(comment_when)

<br>

### 2. 데이터 수집 및 DB 저장 프로세스 설계
- 데이터 수집은 Selenium, BeautifulSoup 라이브러리를 이용해 수행하며, 마리아(Maria) DB로 구축된 DB에 저장된다.
- 수집할 영상 및 댓글의 수(max_vid_num, max_comment_num)를 지정할 수 있고, 데이터 탐색 중 수집할 데이터 양이 이 수에 다다르면 데이터 탐색이 중지된다. 이를 통해 관련 없거나 불필요하게 많은 수의 데이터 수집을 방지한다.
- 유튜브의 경우 영상 게시일을 기준으로 필터링 검색을 수행할 수 있으므로, 시/일/주/달/연의 5개 기준으로 검색이 가능하도록 한다.
데이터가 중복 수집될 수 있는 가능성을 고려해 DB에 저장 시 중복을 확인하도록 한다. 이 때, 중복이 확인될 경우 새로운 행을 추가하지 않고 기존의 데이터를 업데이트 하는 형태로 데이터를 저장한다.
- 영상 데이터와 함께, 데이터 수집 로그를 함께 저장한다.
- DB는 기본 정보 데이터 테이블와 댓글 데이터 테이블로 구성되며, 각 플랫폼에 채널 번호를 부여해 여러 플랫폼에서 수집한 데이터의 구분이 가능하도록 한다.

### 3. 데이터 수집 예시
