
score = 0
print("Answer the following 3 questions.\n")


print("1. What is the capital of Nigeria?")
answer = input("Your answer: ")

if answer.strip() == "abuja":
    print("Correct!\n")
    score += 1
else:
    print("Wrong! The correct answer is Abuja.\n")

# Question 2
print("2. What is 12 x 5?")
answer = input("Your answer: ")

if answer.strip() == "60":
    print("Correct!\n")
    score += 1
else:
    print("Wrong! The correct answer is 60.\n")


print("3. Which planet is known as the Red Planet?")
answer = input("Your answer: ")

if answer.strip().lower() == "mars":
    print("Correct!\n")
    score += 1
else:
    print("Wrong! The correct answer is Mars.\n")


print("           QUIZ RESULTS")
print(f"You scored {score}/3.")

if score == 3:
    print("Excellent! You got all the answers right!")
elif score == 2:
    print("Well done! You did great!")
elif score == 1:
    print("Good try! Keep practising!")
else:
    print("Don't give up! Try again!")

