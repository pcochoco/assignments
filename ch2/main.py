from quiz_game import QuizGame


def main() -> None:
    game = QuizGame() #main으로 quiz_game 생성
    game.run() #실행


if __name__ == "__main__": #파이썬이 파일마다 넣어주는 변수: 직접 실행 시만 main() 실행 ex) python main.py
    #타 파일에서 import 시는 __name__이 __main__이 아님 (해당 호출 주체 파일이 __name__)
    main() 