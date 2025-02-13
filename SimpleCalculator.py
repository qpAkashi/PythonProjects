numberOne = float(input("Enter the value of the first number: "))
numberTwo = float(input("Enter the value of the second number: "))
operator = input("Choose between +, -, /, * : ")

if operator == '+':
    result = numberOne + numberTwo
    print("The result is:", result)
elif operator == '-':
    result = numberOne - numberTwo
    print("The result is:", result)
elif operator == '/':
    if numberTwo == 0:
        print("Error: Division by zero is not allowed.")
    else:
        result = numberOne / numberTwo
        print("The result is:", result)
elif operator == '*':
    result = numberOne * numberTwo
    print("The result is:", result)
else:
    print("Invalid operator selected.")