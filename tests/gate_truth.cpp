// Independent truth-table checks for the legacy expression evaluator.
// This tests the evaluator, not circuit scheduling or propagation delay.
#include "../src/Custom_gates.cpp"

#include <array>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>

static void check(const std::string &expression, int width, int mask, bool expected) {
    std::unordered_map<std::string, bool> variables;
    for (int i = 0; i < width; ++i) {
        variables["i" + std::to_string(i + 1)] = (mask & (1 << i)) != 0;
    }
    LogicalExpressionEvaluator evaluator;
    bool actual = evaluator.evaluateInfixExpression(expression, variables);
    if (actual != expected) {
        throw std::runtime_error("Truth-table mismatch: " + expression +
                                 " input mask=" + std::to_string(mask));
    }
}

int main() {
    try {
        for (int mask = 0; mask < 4; ++mask) {
            const bool a = (mask & 1) != 0;
            const bool b = (mask & 2) != 0;
            check("i1&i2", 2, mask, a && b);
            check("i1|i2", 2, mask, a || b);
            check("~(i1&i2)", 2, mask, !(a && b));
            check("(i1&~i2)|(~i1&i2)", 2, mask, a != b);
        }
        check("~i1", 1, 0, true);
        check("~i1", 1, 1, false);
        for (int mask = 0; mask < 8; ++mask) {
            const bool a = (mask & 1) != 0;
            const bool b = (mask & 2) != 0;
            const bool c = (mask & 4) != 0;
            check("(i1&i2)|((i1&i3)|(i2&i3))", 3, mask,
                  (a && b) || (a && c) || (b && c));
        }
        std::unordered_map<std::string, bool> variables{{"i1", true}};
        LogicalExpressionEvaluator evaluator;
        bool threw = false;
        try {
            (void)evaluator.evaluateInfixExpression("i2", variables);
        } catch (const std::runtime_error &) {
            threw = true;
        }
        if (!threw) {
            throw std::runtime_error("Undefined gate operand was silently accepted");
        }
    } catch (const std::exception &error) {
        std::cerr << "FAIL: " << error.what() << '\n';
        return 1;
    }
    std::cout << "PASS: 26 gate truth-table cases plus undefined-variable rejection\n";
    return 0;
}
