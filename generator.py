
import os
from time import sleep
from termcolor import colored as clr
from prettytable import PrettyTable as pt


# Dictionary to map operators to their respective op code
operators = {
    "+": "ADD",
    "-": "SUB",
    "*": "MPY",
    "/": "DIV",
    "+.": clr("ADD", "green"),
    "-.": clr("SUB", "green"),
    "*.": clr("MPY", "green"),
    "/.": clr("DIV", "green")
}


# This function checks if an expression is valid by ensuring it has matching operators, operands, and balanced parentheses.
def is_valid_exp(exp):
    if len(exp) < 3:
        return False
    
    operator_count = operand_count = bracket_count = 0
    for ch in exp:
        if ch in operators:
            operator_count += 1
        elif 65 <= ord(ch) <= 90:
            operand_count += 1
        elif ch in ["(", ")"]:
            bracket_count += 1 if ch == "(" else -1
    
    return operator_count == operand_count - 1 and bracket_count == 0


# This function checks if an expression is in infix notation by validating operator placement.
def is_infix(exp):
    def in_bound_n_operands(i):
        if not (0 < i < len(exp) - 1):
            return False
        
        return exp[i - 1] not in operators and exp[i + 1] not in operators
    
    return all(in_bound_n_operands(i) for i in range(len(exp)) if exp[i] in operators)


# This function converts a prefix expression to either an infix or postfix expression based on the `to_in` flag.
def pre_to_in_or_post(prefix, to_in=False):
    stk = []
    
    for ch in prefix[::-1]:
        if ch in operators:
            if len(stk) < 2:
                return None
            if to_in:
                res = f"({stk.pop()}{ch}{stk.pop()})"
            else:
                res = f"{stk.pop()}{stk.pop()}{ch}"
            stk.append(res)
        else:
            stk.append(ch)
    
    res = stk.pop() if len(stk) == 1 else None
    return res[1:-1] if res and to_in else res


# This function converts an infix expression to a postfix expression by following operator precedence and parentheses.
def in_to_post(infix):
    prio = {"+": 1, "-": 1, "*": 2, "/": 2}
    stk, postfix = [], []
    
    for ch in infix:
        if ch in ["(", ")"]:
            if ch == "(":
                stk.append(ch)
            else:
                while stk and stk[-1] != "(":
                    postfix.append(stk.pop())
                stk.pop()
        elif ch in prio:
            if not stk or stk[-1] == "(" or prio[ch] > prio[stk[-1]]:
                stk.append(ch)
            else:
                while stk and stk[-1] != "(" and prio[ch] <= prio[stk[-1]]:
                    postfix.append(stk.pop())
                stk.append(ch)
        else:
            postfix.append(ch)
    
    while stk:
        postfix.append(stk.pop())
    
    return "".join(postfix)


# This function converts a postfix expression to a prefix expression using a stack.
def postfix_to_prefix(postfix):
    stack = []
    operators = set(['+', '-', '*', '/'])
    
    for ch in postfix:
        if ch in operators:
            op2 = stack.pop()
            op1 = stack.pop()
            prefix = ch + op1 + op2
            stack.append(prefix)
        else:
            stack.append(ch)
    
    return stack[-1]


# This function prints generated instructions in a formatted table along with the count of memory accesses and operations.
def print_instructions(n, instructions, no_mem_access):
    print(clr(f"\n{n} address instructions:".upper(), "cyan"))
    table = pt(["Operation", "Operands", "Comment"])
    table.align["Operation"] = table.align["Operands"] = table.align["Comment"] = 'l'
    
    for op_code, operands, comment in instructions:
        table.add_row([op_code, operands, comment])
    print(table)
    ops = len(instructions)
    print("Number of instructions:", clr(str(ops), "green"))
    print("Memory accesses:", clr(
        f"{ops} op + {ops - no_mem_access} d", "green"))


# This function generates three-address instructions from a postfix expression.
def generate_3_address(postfix):
    stk = []
    loaded = set()
    instructions = []
    no_mem_access = 0

    for ch in postfix:
        both_loaded = False
        if ch in operators:
            op2, op1 = stk.pop(), stk.pop()
            if op1 in loaded or op2 in loaded:
                res = op1 if op1 in loaded else op2
            else:
                res = f"R{len(loaded)}" if loaded else "R"
                loaded.add(res)
            if op1 in loaded and op2 in loaded:
                no_mem_access += 1
                both_loaded = True
                loaded.remove(op2)
            stk.append(res)
            res = (operators.get(ch + ".") if both_loaded else operators.get(ch),
                   f"{res}, {op1}, {op2}", f"{res} = {op1} {ch} {op2}")
            instructions.append(res)
        else:
            stk.append(ch)
    
    print_instructions("Three", instructions, no_mem_access)


# This function generates two-address instructions from a postfix expression.
def generate_2_address(postfix):
    stk = []
    loaded = set()
    instructions = []
    no_mem_access = 0

    for ch in postfix:
        if ch in operators:
            op2, op1 = stk.pop(), stk.pop()
            if op1 in loaded and op2 in loaded:
                no_mem_access += 1
                loaded.remove(op2)
                res = (operators.get(ch + "."),
                       f"{op1}, {op2}", f"{op1} = {op1} {ch} {op2}")
                stk.append(op1)
            elif op1 not in loaded and op2 not in loaded:
                res = f"R{len(loaded) + 1}"
                loaded.add(res)
                stk.append(res)
                instructions.append(
                    ("MOVE", f"{res}, {op1}", f"{res} = {op1}"))
                res = (operators.get(ch),
                       f"{res}, {op2}", f"{res} = {res} {ch} {op2}")
            elif op1 not in loaded and op2 in loaded:
                res = (operators.get(ch),
                       f"{op2}, {op1}", f"{op2} = {op1} {ch} {op2}")
                stk.append(op2)
            else:
                res = (operators.get(ch),
                       f"{op1}, {op2}", f"{op1} = {op1} {ch} {op2}")
                stk.append(op1)
                instructions.append(res)
        else:
            stk.append(ch)
    
    instructions.append(("MOVE", f"R, {stk[-1]}", f"R = {stk[-1]}"))
    print_instructions("Two", instructions, no_mem_access)


# This function generates one-address instructions from a postfix expression.
def generate_1_address(postfix):
    stk = []
    loaded = set()
    instructions = []

    for ch in postfix:
        if ch in operators:
            op2, op1 = stk.pop(), stk.pop()
            if op1 in loaded and op2 in loaded:
                loaded.remove(op1)
                res = (operators.get(ch), op1, f"AC = {op1} {ch} AC")
                stk.append(op2)
            elif op1 not in loaded and op2 not in loaded:
                temp = ""
                if len(loaded):
                    temp = f"T{len(loaded)}"
                    loaded.add(temp)
                    instructions.append(("STORE", temp, f"{temp} = AC"))
                res = "AC"
                loaded.add(res)
                if "AC" in stk:
                    stk[stk.index("AC")] = temp
                stk.append(res)
                instructions.append(("LOAD", f"{op1}", f"{res} = {op1}"))
                res = (operators.get(ch), f"{op2}",
                       f"{res} = {res} {ch} {op2}")
            elif op1 not in loaded and op2 in loaded:
                res = (operators.get(ch), f"{op1}",
                       f"{op2} = {op1} {ch} {op2}")
                stk.append(op2)
            else:
                res = (operators.get(ch), f"{op2}",
                       f"{op1} = {op1} {ch} {op2}")
                stk.append(op1)
            instructions.append(res)
        else:
            stk.append(ch)
    
    instructions.append(("STORE", f"R", "R = AC"))
    print_instructions("One", instructions, 0)


# This function generates zero-address instructions from a postfix expression.
def generate_0_address(postfix):
    stk = []
    instructions = []
    no_mem_access = 0
    for ch in postfix:
        if ch in operators:
            no_mem_access += 1
            op2, op1 = stk.pop(), stk.pop()
            res = (operators.get(ch + "."), "-", f"TOS = {op1}{ch}{op2}")
            stk.append(f"({op1}{ch}{op2})")
            instructions.append(res)
        else:
            stk.append(ch)
            instructions.append((f"PUSH", ch, f"TOS = {ch}"))
    instructions.append((f"POP", "R", f"R = {stk[-1][1:-1]}"))
    print_instructions("Zero", instructions, no_mem_access)


# This function generates all types of assembly instructions (three, two, one, and zero address) for a given postfix expression.
def generate_instructions(postfix):
    sleep(0.5)
    generate_3_address(postfix)
    sleep(0.5)
    generate_2_address(postfix)
    sleep(0.5)
    generate_1_address(postfix)
    sleep(0.5)
    generate_0_address(postfix)


# This function displays the header text for the program.
def header():
    print("=" * 60)
    print("PREFIX CODE TO ASSEMBLY CODE GENERATOR".center(60))
    print("=" * 60)


# This function displays the menu options for the program.
def options():
    print("\nAvailable options:")
    print("1. Read from file")
    print("2. Input manually (Prefix/Infix)")
    print("0. Exit")


# Main function
if __name__ == '__main__':
    header()
    file_read = False
    file_line_no = -1

    while True:
        options()
        prefix = infix = postfix = ""
        op = input("\nEnter option: ")
        
        if op == "0":
            print(clr("PROGRAM TERMINATED", "cyan"))
            break
        elif op == "1":
            if not file_read:
                file_path = "expressions.txt"
                if not os.path.exists(file_path):
                    print(clr(f"Error: {file_path} not found.", "red"))
                    continue
                with open(file_path, "r") as file:
                    lines = file.readlines()
            
            file_line_no += 1
            if file_line_no == len(lines):
                print(clr("END OF FILE", "yellow"))
                continue

            prefix = lines[file_line_no].strip()
            prefix = prefix.split(" ")[-1].upper()
        elif op == "2":
            print("Enter expression: ", end="")
            exp = input().strip().upper()
            
            if not is_valid_exp(exp):
                print(clr("INVALID EXPRESSION", "red"))
                continue
            if is_infix(exp):
                infix = exp
            else:
                prefix = exp
        else:
            print(clr("INVALID OPTION", "red"))
            continue
        
        infix = pre_to_in_or_post(prefix, to_in=True) if not infix else infix
        postfix = pre_to_in_or_post(prefix) if prefix else in_to_post(infix)

        if infix and postfix:
            table = pt(["Type", "Expression"])
            table.align["Type"] = table.align["Expression"] = 'l'
            prefix = postfix_to_prefix(postfix)
        if prefix and infix and postfix:
            table.add_row(["Prefix", prefix])
            table.add_row(["Infix", infix])
            table.add_row(["Postfix", postfix])
            print(table)
            generate_instructions(postfix)
        else:
            print(clr("EXPRESSION IS NEITHER PREFIX NOR INFIX", "red"))
