import random

def generate_random_number(start: int, end: int) -> int:
    """
    生成一个指定范围内的随机整数。

    Args:
        start (int): 范围起始值（包含）。
        end (int): 范围结束值（包含）。

    Returns:
        int: 生成的随机整数。
    """
    return random.randint(start, end)

def get_user_guess() -> int:
    """
    获取用户输入的猜测数字。

    Returns:
        int: 用户输入的整数。
    """
    while True:
        try:
            guess_str = input("请输入你猜的数字: ")
            return int(guess_str)
        except ValueError:
            print("输入无效，请输入一个整数。")

def play_game() -> None:
    """
    运行猜数字游戏的主循环。
    """
    target_number: int = generate_random_number(1, 100)
    print("我已经想好了一个 1 到 100 之间的数字。")

    attempts: int = 0
    while True:
        guess: int = get_user_guess()
        attempts += 1

        if guess < target_number:
            print("太小了！再试一次。")
        elif guess > target_number:
            print("太大了！再试一次。")
        else:
            print(f"恭喜你！你猜对了，答案就是 {target_number}。")
            print(f"你总共猜了 {attempts} 次。")
            break

if __name__ == "__main__":
    play_game()
