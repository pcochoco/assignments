from __future__ import annotations


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