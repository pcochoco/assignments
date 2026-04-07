from __future__ import annotations


class Quiz:
    def __init__(self, question: str, choices: list[str], answer: int) -> None:
        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    def display(self, number: int | None = None) -> None:
        print("-" * 40)
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        print()

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

    @classmethod
    def from_dict(cls, data: dict) -> "Quiz":
        question = data.get("question", "").strip()
        choices = data.get("choices", [])
        answer = data.get("answer", 0)

        if not isinstance(question, str) or not question:
            raise ValueError("유효하지 않은 question 데이터입니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("choices는 4개의 항목을 가진 리스트여야 합니다.")

        normalized_choices = []
        for choice in choices:
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError("각 choice는 비어 있지 않은 문자열이어야 합니다.")
            normalized_choices.append(choice.strip())

        if not isinstance(answer, int) or answer not in (1, 2, 3, 4):
            raise ValueError("answer는 1~4 사이의 정수여야 합니다.")

        return cls(question=question, choices=normalized_choices, answer=answer)