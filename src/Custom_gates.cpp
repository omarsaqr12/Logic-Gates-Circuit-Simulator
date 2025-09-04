#include <stack>
#include <unordered_map>
#include <stdexcept>
#include <string>

using namespace std;

class LogicalExpressionEvaluator {
private:
    bool isOperator(char c) {
        return (c == '&' || c == '|' || c == '~' || c == '(' || c == ')');
    }

    int precedence(char c) {
        switch (c) {
            case '|':
                return 1;
            case '&':
                return 2;
            case '~':
                return 3;
            case '(':
            case ')':
                return 0;
        }
        return -1;
    }

    bool evaluate(bool a, char op) {
        switch (op) {
            case '~':
                return !a;
        }
        throw runtime_error("Invalid unary operator.");
    }

    bool evaluate(bool a, bool b, char op) {
        switch (op) {
            case '&':
                return a && b;
            case '|':
                return a || b;
        }
        throw runtime_error("Invalid binary operator.");
    }

    string extractOperand(string& expression, int& pos) {
        string operand = "";
        while (pos < expression.length() && !isOperator(expression[pos])) {
            operand += expression[pos];
            pos++;
        }
        return operand;
    }

public:
    bool evaluateInfixExpression(string expression, unordered_map<string, bool>& variables) {
        stack<bool> operands;
        stack<char> operators;
        int i = 0;

        while (i < expression.length()) {
            char c = expression[i];
            if (!isOperator(c)) {
                string operand = extractOperand(expression, i);
                if (variables.find(operand) != variables.end()) {
                    operands.push(variables[operand]);
                } else {
                    throw runtime_error("Undefined variable: " + operand);
                }
                continue;
            }
            if (c == '(') {
                operators.push(c);
            } else if (c == ')') {
                while (operators.top() != '(') {
                    if (operators.top() == '~') {
                        bool a = operands.top();
                        operands.pop();
                        operands.push(evaluate(a, operators.top()));
                    } else {
                        bool b = operands.top();
                        operands.pop();
                        bool a = operands.top();
                        operands.pop();
                        operands.push(evaluate(a, b, operators.top()));
                    }
                    operators.pop();
                }
                operators.pop(); // Discard the '('
            } else if (isOperator(c)) {
                while (!operators.empty() && precedence(c) <= precedence(operators.top())) {
                    if (operators.top() == '~') {
                        bool a = operands.top();
                        operands.pop();
                        operands.push(evaluate(a, operators.top()));
                    } else {
                        bool b = operands.top();
                        operands.pop();
                        bool a = operands.top();
                        operands.pop();
                        operands.push(evaluate(a, b, operators.top()));
                    }
                    operators.pop();
                }
                operators.push(c);
            }
            i++;
        }

        while (!operators.empty()) {
            if (operators.top() == '~') {
                bool a = operands.top();
                operands.pop();
                operands.push(evaluate(a, operators.top()));
            } else {
                bool b = operands.top();
                operands.pop();
                bool a = operands.top();
                operands.pop();
                operands.push(evaluate(a, b, operators.top()));
            }
            operators.pop();
        }
        return operands.top();
    }
};
