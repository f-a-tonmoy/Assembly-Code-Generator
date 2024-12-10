## 📝 Project Overview

This project converts arithmetic expressions into assembly code using Python. It generates instructions for four types of addressing modes: **three-address**, **two-address**, **one-address**, and **zero-address**. The program supports prefix and infix expressions as input and ensures that the generated instructions are efficient and easily interpretable.

---

## 📂 Project Structure

```plaintext
├── generator.py                   # Core program logic
├── expressions.txt                # Sample prefix expressions for testing
├── README.md                      # Project documentation
├── requirements.txt               # Python dependencies
```

---

## 🚀 Features

1. **Expression Parsing**:
   - Validates input expressions for correctness.
   - Supports both **prefix** and **infix** input.

2. **Address Instruction Generation**:
   - Generates assembly instructions for:
     - **Three-Address Mode**: Intermediate code with at most three operands.
     - **Two-Address Mode**: Uses temporary storage and one operand for results.
     - **One-Address Mode**: Operates on a single register and one operand.
     - **Zero-Address Mode**: Stack-based instruction generation.

3. **Interactive User Interface**:
   - Menu-driven terminal interface for:
     - Reading expressions from `expressions.txt`.
     - Manual input of prefix or infix expressions.

4. **Memory and Instruction Analysis**:
   - Provides the number of instructions and memory accesses for each addressing mode.
   - Highlights efficient instruction sets using colored output.

---

## 📂 Input and Output

### Input:
- Prefix expressions (e.g., `+AB`, `-*CDE`) or infix expressions (e.g., `(A+B)*C`).
- Example prefix expressions are provided in `expressions.txt`.

### Output:
- Assembly instructions in **three-address**, **two-address**, **one-address**, and **zero-address** formats.
- Example:
  For the prefix expression `*-ABC`:
  - **Three-Address Mode**:
    ```plaintext
    SUB  R, A, B
    MPY  R, R, C
    ```
  - **Zero-Address Mode**:
    ```plaintext
    PUSH A
    PUSH B
    SUB
    PUSH C
    MPY
    POP
    ```

---

## 🛠️ Dependencies

Install the required libraries using:
```bash
pip install -r requirements.txt
```

### `requirements.txt` Content:
```plaintext
termcolor
prettytable
```

---

## 🔍 How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/f-a-tonmoy/prefix-to-assembly-converter.git
   cd prefix-to-assembly-converter
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the program:
   ```bash
   python converter.py
   ```

4. Follow the menu options:
   - **Option 1**: Read prefix expressions from `expressions.txt`.
   - **Option 2**: Enter prefix or infix expressions manually.
   - **Option 0**: Exit the program.

---

## 🧪 Results

- **Three-Address Instructions**:
  - Most efficient in terms of readability and ease of conversion.
- **Two-Address Instructions**:
  - Reduces instruction length but requires temporary storage.
- **One-Address Instructions**:
  - Operates with a single register but increases instruction count.
- **Zero-Address Instructions**:
  - Completely stack-based, suitable for theoretical stack machines.

---

## 🔬 Analysis

### **Time Complexity**:
- Expression validation and conversion functions: **O(n)**.
- Instruction generation functions: **O(n)**.
- Overall time complexity: **O(n²)** due to nested loops in certain conversions.

### **Space Complexity**:
- Uses stacks and temporary storage for parsing: **O(n)**.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 💬 Contact

For inquiries or feedback:
- **Fahim Ahamed**: [f.a.tonmoy00@gmail.com](mailto:f.a.tonmoy00@gmail.com)
- GitHub: [f-a-tonmoy](https://github.com/f-a-tonmoy)
```
