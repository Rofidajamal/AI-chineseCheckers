from ChineseCheckers import ChineseCheckers

if __name__ == "__main__":
    while True:
        print("Please Choose the Game Mood:\n 1- Easy.\n 2- Medium.\n 3- Hard.\n")
        depth = int(input())
        if depth == 1 or depth == 2 or depth == 3:
            ChineseCheckers(depth)
            break
        else:
            print("\nInvalid Input, please Type 1, 2 or 3.\n")

