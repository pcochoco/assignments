### 프로젝트 개요
파이썬 퀴즈 게임

### 퀴즈 주제와 선정 이유
파이썬 복습 

### 실행 방법

``` python main.py ```


- 프로그램 실행 시 메뉴에서 번호를 선택
- 결정에 따라 퀴즈 출제/등록/목록/점수 확인/종료 화면 출력

### 기능 목록

- 퀴즈 풀기
- 퀴즈 추가
- 퀴즈 목록 확인
- 최고 점수 확인
- 프로그램 종료
- state.json 자동 저장 / 불러오기
- 잘못된 입력 처리
- 파일 손상 시 기본 퀴즈 데이터 복구
- Ctrl+C, EOFError 발생 시 안전 종료

### 파일 구조
- main.py: 프로그램 시작 파일
- quiz.py: 개별 퀴즈를 표현하는 Quiz 클래스
- quiz_game.py: 게임 전체를 관리하는 QuizGame 클래스
- state.json: 퀴즈 데이터와 최고 점수를 저장하는 파일
- README.md: 프로젝트 설명 문서
- .gitignore: Git 추적 제외 파일 설정

데이터는 프로젝트 루트의 state.json에 UTF-8 인코딩으로 저장하고 불러온다.

최소 10개 이상의 의미 있는 커밋이 존재한다.
최소 1회 이상의 브랜치 생성 및 병합(checkout, merge) 기록이 있다.
clone과 pull을 각각 1회 이상 사용한 기록이 있다.

### 데이터 파일(state.json 경로, 역할, 스키마)
- 경로 : 루트
- 점수, 데이터 저장
- 스키마
```
{
    "quizzes": [
        {
            "question": "Python의 창시자는 누구인가요?",
            "choices": ["Guido", "Linus", "Bjarne", "James"],
            "answer": 1
        }
    ],
    "best_score": 3
}
```
- quizzes: 퀴즈 목록
- question: 문제
- choices: 4개의 선택지
- answer: 정답 번호(1~4)
- best_score: 최고 정답 수


