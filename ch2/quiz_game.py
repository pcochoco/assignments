from __future__ import annotations

import json
from pathlib import Path

from quiz import Quiz


class QuizGame:
    def __init__(self) -> None:
        self.state_file = Path("state.json")
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.loaded_from_file: bool = False #

        self.load_state() #함수 호출 

    def get_default_quizzes(self) -> list[Quiz]: #Quiz type list
        return [ #Quiz의 기본생성자 활용
            Quiz(
                question="Python의 창시자는 누구인가요?",
                choices=["Guido van Rossum", "Linus Torvalds", "James Gosling", "Bjarne Stroustrup"],
                answer=1,
            ),
            Quiz(
                question="Python에서 리스트를 나타내는 기호는 무엇인가요?",
                choices=["{}", "()", "[]", "<>"],
                answer=3,
            ),
            Quiz(
                question="Python에서 조건문에 사용하는 키워드는 무엇인가요?",
                choices=["repeat", "if", "switch", "case"],
                answer=2,
            ),
            Quiz(
                question="Python에서 반복문으로 알맞은 것은 무엇인가요?",
                choices=["for", "loop", "repeat", "iterate"],
                answer=1,
            ),
            Quiz(
                question="Python에서 함수 정의에 사용하는 키워드는 무엇인가요?",
                choices=["func", "define", "def", "function"],
                answer=3,
            ),
        ]

    def run(self) -> None:
        try:
            while True:
                self.show_menu()
                #choice min 1 max 5
                choice = self.read_int("선택: ", 1, 5)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quiz_list()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    self.safe_exit()
                    break

        except KeyboardInterrupt:
            print("\nCtrl+C가 입력되었습니다.")
            self.safe_exit() 
        except EOFError: #ctrl z(입력 더 이상 x)
            print("\n입력 스트림이 종료되었습니다.")
            self.safe_exit()

    def show_menu(self) -> None:
        print("\n" + "=" * 40)
        print("         퀴즈 게임")
        print("=" * 40)

        if self.loaded_from_file:
            print(
                f" 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score if self.best_score is not None else '없음'})"
            )
            print("=" * 40)

        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def read_text(self, prompt: str) -> str:
        while True:
            try:
                value = input(prompt).strip()
            except KeyboardInterrupt:
                raise #exception 던짐
            except EOFError:
                raise

            if not value:
                print("빈 입력은 허용되지 않습니다. 다시 입력하세요.")
                continue

            return value

    def read_int(self, prompt: str, min_value: int, max_value: int) -> int:
        while True:
            try:
                raw = input(prompt).strip()
            except KeyboardInterrupt:
                raise
            except EOFError:
                raise

            if raw == "":
                print(f"빈 입력은 허용되지 않습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            try: #"123" into 123 (str -> int)
                value = int(raw)
            except ValueError: #예외에 대한 직접 처리 
                print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if value < min_value or value > max_value:
                print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return value

    def play_quiz(self) -> None:
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)\n")

        correct_count = 0

        #quizzes quiz 원소에 대해 idx 1부터 번호 붙여줌
        for idx, quiz in enumerate(self.quizzes, start=1):
            quiz.display(number=idx)
            user_answer = self.read_int("정답 입력 (1-4): ", 1, 4)

            if quiz.is_correct(user_answer):
                print("정답입니다!\n")
                correct_count += 1
            else:
                print(f" 오답입니다! 정답은 {quiz.answer}번입니다.\n")

        score = int((correct_count / len(self.quizzes)) * 100) #%

        print("=" * 40)
        print(f"결과: {len(self.quizzes)}문제 중 {correct_count}문제 정답! ({score}점)")

        if self.best_score is None or correct_count > self.best_score:
            self.best_score = correct_count
            print("새로운 최고 점수입니다!")
            self.save_state() #점수 저장용
        else:
            print("수고하셨습니다!")

        print("=" * 40)

    def add_quiz(self) -> None:
        print("\n새로운 퀴즈를 추가합니다.\n")

        question = self.read_text("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = self.read_text(f"선택지 {i}: ")
            choices.append(choice)

        answer = self.read_int("정답 번호 (1-4): ", 1, 4)

        new_quiz = Quiz(question=question, choices=choices, answer=answer)
        self.quizzes.append(new_quiz)
        self.save_state()

        print("\n퀴즈가 추가되었습니다!")

    def show_quiz_list(self) -> None:
        print()

        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print(f"등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)

        for idx, quiz in enumerate(self.quizzes, start=1):
            print(f"[{idx}] {quiz.question}")

        print("-" * 40)

    def show_best_score(self) -> None:
        print()

        if self.best_score is None:
            print("아직 퀴즈를 풀지 않았습니다.")
            return

        total_quiz_count = len(self.quizzes)
        score_percent = int((self.best_score / total_quiz_count) * 100) if total_quiz_count > 0 else 0

        print(f"최고 점수: {score_percent}점 ({total_quiz_count}문제 중 {self.best_score}문제 정답)")

    def load_state(self) -> None: #
        if not self.state_file.exists():
            print("state.json 파일이 없어 기본 퀴즈 데이터를 사용합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.loaded_from_file = False
            self.save_state()
            return

        try:
            with self.state_file.open("r", encoding="utf-8") as file:
                data = json.load(file) # json -> python

            #json data 값 없을 경우 default
            quizzes_data = data.get("quizzes", [])
            best_score = data.get("best_score", None) 

            if not isinstance(quizzes_data, list):
                raise ValueError("quizzes 데이터가 리스트가 아닙니다.")


            #json object : dictionary -> quizzes 의 quiz 대상
            #json array : list
            quizzes = [Quiz.from_dict(item) for item in quizzes_data]

            if best_score is not None:
                if not isinstance(best_score, int) or best_score < 0:
                    raise ValueError("best_score 데이터가 올바르지 않습니다.")

            self.quizzes = quizzes
            self.best_score = best_score
            self.loaded_from_file = True

        #json 형식 잘못된 경우 / 입력 값 error / os error
        except (json.JSONDecodeError, ValueError, OSError) as error:
            print(f" 데이터 파일을 읽는 중 문제가 발생했습니다: {error}")
            print("기본 퀴즈 데이터로 복구합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = None
            self.loaded_from_file = False
            self.save_state()

    def save_state(self) -> None:
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }

        try:
            with self.state_file.open("w", encoding="utf-8") as file: #ascii - 한글 표현 불가하므로 utf-8
                json.dump(data, file, ensure_ascii=False, indent=4) #indent : 들여쓰기 / json.dump : python -> json
        except OSError as error:
            print(f"파일 저장 중 오류가 발생했습니다: {error}")

    def safe_exit(self) -> None:
        self.save_state() #저장 후 종료 용도
        print("\n 데이터를 저장했습니다.")
        print(" 프로그램을 종료합니다.")