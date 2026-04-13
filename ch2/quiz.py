from __future__ import annotations
#Quiz, list[Quiz] 같은 타입 표기를 더 안전하고 편하게 쓰려고 넣은 것
#타입 힌트를 나중에 평가하게 하는 설정
#파이썬이 함수 선언에 적힌 타입들을 즉시 실제 객체로 해석하지 않고 문자열처럼 미뤄서 처리
#함수 본문 ex) return Quiz(...)와 달리 함수 정의를 읽는 시점에 처리될 수 있는 정보
#class 이름 Quiz를 아직 참조할 수 없는 시점에 해석하게 되면 문제가 되는 것
#type hint : 변수, 값이 어떤 자료형인지 사람이랑 도구에게 알려주는 표시(매개인자 옆의 자료형 표시)
#ex) data: dict 의 경우 실제 변수 data 가 dict 자료형인게 아니라 dict로 쓰기 위해 만드는 변수임을 의미 

#class Quiz:
    # @classmethod
    # def from_dict(cls, data: dict) -> Quiz:
    #     ...


class Quiz:
    #__init__ : 생성자, self : 메서드 호출한 객체
    def __init__(self, question: str, choices: list[str], answer: int) -> None: #반환 x
        #question, choices 공백 제거
        self.question = question.strip() 
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    #number can be int or None, default is None
    def display(self, number: int | None = None) -> None:
        print("-" * 40)
        if number is not None:
            #formatted string literal(f-string) : %s와 같은 식의 형식 지정자 생략
            print(f"[문제 {number}]")
        print(self.question)
        print()

        #enumerate : list into list of index, value ex) [(0, "a"), ...]
        for idx, choice in enumerate(self.choices, start=1):
            print(f"{idx}. {choice}") 
        print()

    def is_correct(self, user_answer: int) -> bool:
        return user_answer == self.answer

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod #객체 생성용의 static method (python에서 일반적 static method는 @staticmethod) -> dictionary data 로 quiz 생성
    def from_dict(cls, data: dict) -> "Quiz":
        #data dictionary key에 대한 value or default 값
        question = data.get("question", "").strip()
        choices = data.get("choices", [])
        answer = data.get("answer", 0)

        #question is str type(or str의 하위 타입)
        if not isinstance(question, str) or not question:
            raise ValueError("유효하지 않은 question 데이터입니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("choices는 4개의 항목을 가진 리스트여야 합니다.")

        normalized_choices = []
        
        for choice in choices:
            if not isinstance(choice, str) or not choice.strip(): #"" -> False
                raise ValueError("각 choice는 비어 있지 않은 문자열이어야 합니다.")
            normalized_choices.append(choice.strip())

        if not isinstance(answer, int) or answer not in (1, 2, 3, 4):
            raise ValueError("answer는 1~4 사이의 정수여야 합니다.")

        #@classmethod 안에서 class 이름 대신 cls 씀 = 이 메서드를 호출한 클래스 기준으로 객체 생성
        return cls(question=question, choices=normalized_choices, answer=answer)