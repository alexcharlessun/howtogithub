import random

def guess_number_game():
    print("🎉 欢迎来到猜数字游戏！🎉")
    print("我已经想好了一个 1 到 100 之间的数字。")
    print("你能几次猜中它呢？")
    
    number_to_guess = random.randint(1, 100)
    attempts = 0
    low = 1
    high = 100
    
    while True:
        try:
            user_input = input(f"\n请输入你的猜测 ({low}-{high}): ")
            guess = int(user_input)
            attempts += 1
            
            if guess < 1 or guess > 100:
                print("请认真点，范围是 1 到 100 哦！")
                continue
                
            if guess < number_to_guess:
                print("太小了！试试大一点的。")
                if guess >= low:
                    low = guess + 1
            elif guess > number_to_guess:
                print("太大了！试试小一点的。")
                if guess <= high:
                    high = guess - 1
            else:
                print(f"\n✨ 恭喜你！猜对了！答案就是 {number_to_guess}。")
                print(f"你总共猜了 {attempts} 次。")
                break
                
        except ValueError:
            print("❌ 只能输入整数数字哦！")

if __name__ == "__main__":
    guess_number_game()
