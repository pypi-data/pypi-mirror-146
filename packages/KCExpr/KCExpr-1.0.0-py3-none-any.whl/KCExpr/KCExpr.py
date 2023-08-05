# KCExpr — created by Kyle James Catterall

import math
import regex

RE_REAL_NUM = r"[+-]?([0-9]*[.])?[0-9]+"

RECOGNISED_FUNCTIONS = ("abs", "sqrt", "root", "ncr", "npr", "sigma", "pi", 
                        "ln", "log", "sin", "sina", "csc", "sinh", "sinha", 
                        "csch", "cos", "cosa", "sec", "cosh", "cosha", "sech", 
                        "tan", "tana", "cot", "tanh", "tanha", "coth")

CONSTANTS = {
    "PI": math.pi,
    "E": math.e,
    "EM": 0.577215664901533,
    "GOLDEN": 1.6180339887498948,
    "MM": 0.261497212847643,
    "BERNSTEIN": 0.280169499023869,
    "GKW": 0.303663002898733,
    "HSM": 0.3532363718549960,
    "OMEGA": 0.5671432904097839,
    "GD": 0.624329988543551,
    "CAHEN": 0.6434105462,
    "TP": 0.660161815846870,
    "LAPLACE": 0.662743419349182,
    "ET": 0.70258,
    "LR": 0.764223653589221,
    "BRUNPQ": 0.87058838,
    "BRUNPT": 1.902160583104,
    "CATALAN": 0.9159655941772190,
    "VISWANATH": 1.13198824,
    "APERY": 1.202056903159594,
    "CONWAY": 1.303577269034297,
    "MILLS": 1.306377883863081,
    "PLASTIC": 1.3247179572447460,
    "RS": 1.4513692348833811,
    "BACKHOUSE": 1.456074948582690,
    "PORTER": 1.467078079433975,
    "LIEB": 1.4670780794,
    "EB": 1.606695152415292,
    "NIVEN": 1.705211140105368,
    "UPC": 2.2955871493926381,
    "FEIGENBAUMA": 2.5029078750958929,
    "FEIGENBAUMD": 4.6692016091029907,
    "SIERPINSKI": 2.584981759579253,
    "KHINCHIN": 2.685452001065307,
    "FR": 2.807770242028519,
    "LEVY": 3.275822918721811,
    "RF": 3.359885666243178
}

ans = 0  # KCExpr.parse() will change this value; this value is used as [ans]


class KCExpr:
    
    """
    KCExpr - a small python parser to parse mathematical expressions
    Built entirely with regular expressions!
    """
    
    def __init__(self) -> None:
        self.expr = ""
        
    def set_expr(self, expr) -> None:
        
        def gpm(expression) -> str:
            
            """
            General Product Modifier
            Modifies expressions so that numerous multiplication notation
            is all converted to standard computer notation of a*b.
            
            Args:
                expression (str): a mathematical expression.

            Returns:
                str: a mathematical expression that uses a*b notation.
            """
            
            expression = expression.replace("#", "(#)")
            for match in regex.finditer(
r"[0-9](\(|\[)|(\)|\])[a-z]|(\)|\])(\(|\[)|[0-9][a-z]|!([0-9]|[a-z]|(\(|\[))", 
expression):
                expr = match.group(0)
                exprm = f"{expr[0]}*{expr[1]}"
                expression = expression.replace(expr, exprm)
            return expression
        
        def constm(expression) -> str:
            
            """
            Constant Modifier
            Replaces constants, such as [pi] or [ans], with their values.
            e.g. "12*[pi]" -> "12*3.14..."

            Args:
                expression (str): a mathematical expression that may contain 
                constants.

            Raises:
                SyntaxError: raised if a constant in expresion is not in 
                CONSTANTS.

            Returns:
                str: a mathematical constants with any constants replaced
                by their values.
            """
            
            if regex.search(r"\[.+\]", expression):
                for match in regex.finditer(r"\[(.+)\]", expression):
                    const_name = match.group(1)
                    if const_name.upper(
                        ) not in CONSTANTS and const_name != "ans":
                        raise SyntaxError(
                        f"{const_name} is not a valid constant")
                    else:
                        if const_name == "ans":
                            expression = expression.replace(
                                "[ans]", f"{ans}")
                        else:
                            expression = expression.replace(
                        f"[{const_name}]", f"{CONSTANTS[const_name.upper()]}")
            return expression
        
        def cfactorial(expression) -> None:
            
            """
            Check Factorial
            Checks whether any factorials are not following factorial syntax.
            
            Args:
                expression (str): a mathematical expression that may contain
                factorials.

            Raises:
                SyntaxError: raised if a factorial in expression is not
                following factorial syntax.
            """
            
            for match in regex.finditer(f".!", expression):
                factorial = match.group(0)
                if not regex.search(r"[0-9]|\)|\]", factorial):
                    raise SyntaxError("invalid factorial")
        
        def cfunction(expression) -> None:
            
            """
            Check Function
            Checks whether any mathematical functions are not following
            function syntax.

            Args:
                expression (str): a mathematical expression that may contain
                mathematical functions.

            Raises:
                SyntaxError: raised if a factorial in expression is not
                following function syntax.
            """
            
            for match in regex.finditer(f"[a-z]+", expression):
                func = match.group(0)
                if func not in RECOGNISED_FUNCTIONS:
                    raise SyntaxError(
                        f"{func} is not a valid function")
                if not (
expression[match.span()[1]] == "(" or expression[match.span()[1]] == "<"):
                    raise SyntaxError(f"missing ( after {func}")
                if expression.count("(") != expression.count(")"):
                    raise SyntaxError(f"unequal number of ( and )")
                if "sigma" in expression and not (
                    temp := regex.search(
                        r"sigma\([+-]?[0-9]+,[+-]?[0-9]+,.+\)", 
                        expression)):
                    raise SyntaxError("invalid sigma syntax")
                if "pi" in expression and not (
                    temp := regex.search(
                        r"pi\([+-]?[0-9]+,[+-]?[0-9]+,.+\)", 
                        expression)):
                    raise SyntaxError("invalid pi syntax")
        
        # Set self.expr to an expression with no whitespace, then run through
        # the nested functions above to clean the expression.
        
        self.expr = f"({expr})".strip().replace(
            " ", "").replace("\n", "").replace("\t", "")
        self.expr = gpm(self.expr)
        self.expr = constm(self.expr)
        self.expr = self.expr.replace("(#)", "#")
        cfactorial(self.expr)
        cfunction(self.expr)
    
    def parse(self) -> str:
        
        """
        Parse
        Parses a mathematical expression using different functions of KCExpr.

        Raises:
            SyntaxError: raised if an expression has not been set.
        """
        
        if self.expr == "":
            raise SyntaxError(
                "expression not set; please use KCExpr.set_expr(expr) where \
expr is type <str>.")
        else:
            self.expr = self.__eval_brackets(self.expr)
            self.expr = self.__calc(self.expr)
            return self.expr
    
    def __eval_brackets(self, expression) -> None:
        
        """
        Evaluate Brackets
        Evaluates brackets in an expression, starting from most-nested.
        All calculations done via KCExpr.__calc().
        """
        
        while "(" in expression and ")" in expression:
            match = regex.search(r"\(((?:[^()]+|R)+)\)", expression)
            inner_most = match.group(1)
            inner_most_pattern = regex.escape(inner_most)
            if "#" in inner_most:
                if not (temp := regex.search(
                    fr"(sigma|pi)\({inner_most_pattern}\)", expression)):
                    expression = expression[:match.span()[0]] + f"\
<{inner_most}>" + expression[match.span()[1]:]
                else:
                    old_func = temp.group(0)
                    new_func = old_func.replace("<", "(").replace(">", ")")
                    new_func_val = str(self.__calc(new_func))
                    expression = expression.replace(old_func, new_func_val)
            else:
                if inner_most.count(",") == 1:
                    values = inner_most.split(",")
                    a = str(eval(values[0]))
                    b = str(eval(values[1]))
                    old_func = regex.search(
                        fr"([a-z]+)\({inner_most_pattern}\)", expression)
                    new_func_name = old_func.group(1)
                    old_func = old_func.group(0)
                    new_func = f"{new_func_name}({a},{b})"
                    new_func_val = str(self.__calc(new_func))
                    expression = expression.replace(old_func, new_func_val)
                else:
                    if old_func := regex.search(
                        f"([a-z]+)\(({inner_most_pattern})\)", expression):
                        new_func_name = old_func.group(1)
                        new_func = f"{new_func_name}({eval(old_func.group(2))})"
                        old_func = old_func.group(0)
                        new_func_val = str(self.__calc(new_func))
                        expression = expression.replace(old_func, new_func_val)
                    else:
                        result = str(self.__calc(inner_most))
                        expression = expression.replace(f"({inner_most})", 
                        f"{result}")
        return expression
    
    def __calc(self, expression) -> float:
        
        """
        Calculate
        Calculates expressions using regular expressions and logic.

        Args:
            expression (str): a mathematical expression to be calculated.

        Returns:
           float: the calculated value of expression.
        """
        
        global ans
        
        # Factorial (additional operator)
        if match := regex.search(fr"({RE_REAL_NUM})!", expression):
            factorial = match.group(0)
            x = float(match.group(1))
            result = math.gamma(x + 1)
            expression = expression.replace(factorial, f"{result}")
        
        # Absolute
        if match := regex.search(fr"abs\(({RE_REAL_NUM})\)", expression):
            absv = match.group(0)
            x = float(match.group(1))
            result = abs(x)
            expression = expression.replace(absv, f"{result}")
        
        # Sqrt
        if match := regex.search(fr"sqrt\(({RE_REAL_NUM})\)", expression):
            sqrt = match.group(0)
            x = float(match.group(1))
            result = x ** 0.5
            expression = expression.replace(sqrt, f"{result}")
        
        # nth-Root
        if match := regex.search(
            fr"root\(({RE_REAL_NUM}),({RE_REAL_NUM})\)", expression):
            nroot = match.group(0)
            x = float(match.group(1))
            n = float(match.group(3))
            result = x ** (1 / n)
            expression = expression.replace(nroot, f"{result}")
        
        # n C r
        if match := regex.search(r"ncr\(([0-9]+),([0-9]+)\)", expression):
            ncr = match.group(0)
            n = int(match.group(1))
            r = int(match.group(2))
            result, k = 1, 1
            if r != 0:
                while r:
                    result *= n
                    k *= r
                    m = math.gcd(result, k)
                    result //= m    
                    k //= m
                    n -= 1
                    r -= 1
            else:
                result = 1
            expression = expression.replace(ncr, f"{result}")
        
        # n P r
        if match := regex.search(r"npr\(([0-9]+),([0-9]+)\)", expression):
            npr = match.group(0)
            n = int(match.group(1))
            r = int(match.group(2))
            result = math.floor(self.__calc(f"{n}!") / self.__calc(
                f"{n - r}!"))
            expression = expression.replace(npr, f"{result}")
        
        # Sigma
        if match := regex.search(
            r"sigma\(([+-]?[0-9]+),([+-]?[0-9]+),(.+)\)", expression):
            sigma = match.group(0)
            start = match.group(1)
            end = match.group(2)
            expr = match.group(3)
            if int(start) > int(end):
                start, end = end, start
            result = 0
            for x in range(int(start), int(end) + 1):
                cexpr = expr.replace("#", str(x))
                cexpr = self.__eval_brackets(cexpr)
                result += self.__calc(cexpr)
            expression = expression.replace(sigma, f"{result}")
        
        # Pi
        if match := regex.search(
            r"pi\(([+-]?[0-9]+),([+-]?[0-9]+),(.+)\)", expression):
            pi = match.group(0)
            start = match.group(1)
            end = match.group(2)
            expr = match.group(3)
            if int(start) > int(end):
                start, end = end, start
            result = 1
            for x in range(int(start), int(end) + 1):
                cexpr = expr.replace("#", str(x))
                cexpr = self.__eval_brackets(cexpr)
                result *= self.__calc(cexpr)
            expression = expression.replace(pi, f"{result}")
        
        # Natural Logarithm of x
        if match := regex.search(fr"ln\(({RE_REAL_NUM})\)", expression):
            ln = match.group(0)
            x = float(match.group(1))
            result = math.log(x)
            expression = expression.replace(ln, f"{result}")
        
        # Logarithm of x to the base b
        if match := regex.search(
            fr"log\(({RE_REAL_NUM}),({RE_REAL_NUM})\)", expression):
            log = match.group(0)
            x = float(match.group(1))
            b = float(match.group(3))
            result = math.log(x, b)
            expression = expression.replace(log, f"{result}")
        
        # Sine of x
        if match := regex.search(fr"sin\(({RE_REAL_NUM})\)", expression):
            sin = match.group(0)
            x = float(match.group(1))
            result = math.sin(x)
            expression = expression.replace(sin, f"{result}")
        
        # Arcsine of x
        if match := regex.search(fr"sina\(({RE_REAL_NUM})\)", expression):
            sina = match.group(0)
            x = float(match.group(1))
            result = math.asin(x)
            expression = expression.replace(sina, f"{result}")
        
        # Cosecant of x
        if match := regex.search(fr"csc\(({RE_REAL_NUM})\)", expression):
            csc = match.group(0)
            x = float(match.group(1))
            result = 1 / math.sin(x)
            expression = expression.replace(csc, f"{result}")
        
        # Hyperbolic sine of x
        if match := regex.search(fr"sinh\(({RE_REAL_NUM})\)", expression):
            sinh = match.group(0)
            x = float(match.group(1))
            result = math.sinh(x)
            expression = expression.replace(sinh, f"{result}")
        
        # Arc-hyperbolic-sine of x
        if match := regex.search(fr"sinha\(({RE_REAL_NUM})\)", expression):
            sinha = match.group(0)
            x = float(match.group(1))
            result = math.asinh(x)
            expression = expression.replace(sinha, f"{result}")
        
        # Hyperbolic cosecant of x
        if match := regex.search(fr"csch\(({RE_REAL_NUM})\)", expression):
            csch = match.group(0)
            x = float(match.group(1))
            result = 1 / math.sinh(x)
            expression = expression.replace(csch, f"{result}")

        # Cosine of x
        if match := regex.search(fr"cos\(({RE_REAL_NUM})\)", expression):
            cos = match.group(0)
            x = float(match.group(1))
            result = math.cos(x)
            expression = expression.replace(cos, f"{result}")
        
        # Arccosine of x
        if match := regex.search(fr"cosa\(({RE_REAL_NUM})\)", expression):
            cosa = match.group(0)
            x = float(match.group(1))
            result = math.acos(x)
            expression = expression.replace(cosa, f"{result}")
        
        # Secant of x
        if match := regex.search(fr"sec\(({RE_REAL_NUM})\)", expression):
            sec = match.group(0)
            x = float(match.group(1))
            result = 1 / math.cos(x)
            expression = expression.replace(sec, f"{result}")
        
        # Hyperbolic cosine of x
        if match := regex.search(fr"cosh\(({RE_REAL_NUM})\)", expression):
            cosh = match.group(0)
            x = float(match.group(1))
            result = math.cosh(x)
            expression = expression.replace(cosh, f"{result}")
        
        # Arc-hyperbolic-cosine of x
        if match := regex.search(fr"cosha\(({RE_REAL_NUM})\)", expression):
            cosha = match.group(0)
            x = float(match.group(1))
            result = math.acosh(x)
            expression = expression.replace(cosha, f"{result}")
        
        # Hyperbolic secant of x
        if match := regex.search(fr"sech\(({RE_REAL_NUM})\)", expression):
            sech = match.group(0)
            x = float(match.group(1))
            result = 1 / math.cosh(x)
            expression = expression.replace(sech, f"{result}")
        
        # Tangent of x
        if match := regex.search(fr"tan\(({RE_REAL_NUM})\)", expression):
            tan = match.group(0)
            x = float(match.group(1))
            result = math.tan(x)
            expression = expression.replace(tan, f"{result}")
        
        # Arctan of x
        if match := regex.search(fr"tana\(({RE_REAL_NUM})\)", expression):
            tana = match.group(0)
            x = float(match.group(1))
            result = math.atan(x)
            expression = expression.replace(tana, f"{result}")
        
        # Cotangent of x
        if match := regex.search(fr"cot\(({RE_REAL_NUM})\)", expression):
            cot = match.group(0)
            x = float(match.group(1))
            result = 1 / math.tan(x)
            expression = expression.replace(cot, f"{result}")
        
        # Hyperbolic tangent of x
        if match := regex.search(fr"tanh\(({RE_REAL_NUM})\)", expression):
            tanh = match.group(0)
            x = float(match.group(1))
            result = math.tanh(x)
            expression = expression.replace(tanh, f"{result}")
        
        # Arc-hyperbolic-tangent of x
        if match := regex.search(fr"tanha\(({RE_REAL_NUM})\)", expression):
            tanha = match.group(0)
            x = float(match.group(1))
            result = math.atanh(x)
            expression = expression.replace(tanha, f"{result}")
        
        # Hyperbolic cotangent of x
        if match := regex.search(fr"coth\(({RE_REAL_NUM})\)", expression):
            coth = match.group(0)
            x = float(match.group(1))
            result = 1 / math.tanh(x)
            expression = expression.replace(coth, f"{result}")
        
        ans = float(eval(expression))  # global ans; used for [ans] "constant"
        return ans                     # (not CONSTANT but follows [..] syntax)
    
    # Overload operators
    
    def __add__(self, expression):
        if isinstance(expression, str):
            p = KCExpr()
            p.set_expr(f"{self.expr}+{expression}")
            return p
        if isinstance(expression, KCExpr):
            p = KCExpr()
            p.set_expr(f"{self.expr}+{expression.expr}")
            return p
        raise TypeError(f"{expression} is not of class str or KCExpr")

    def __sub__(self, expression):
        if isinstance(expression, str):
            p = KCExpr()
            p.set_expr(f"{self.expr}-{expression}")
            return p
        if isinstance(expression, KCExpr):
            p = KCExpr()
            p.set_expr(f"{self.expr}-{expression.expr}")
            return p
        raise TypeError(f"{expression} is not of class str or KCExpr")

    def __mul__(self, expression):
        if isinstance(expression, str):
            p = KCExpr()
            p.set_expr(f"{self.expr}*{expression}")
            return p
        if isinstance(expression, KCExpr):
            p = KCExpr()
            p.set_expr(f"{self.expr}*{expression.expr}")
            return p
        raise TypeError(f"{expression} is not of class str or KCExpr")

    def __pow__(self, expression):
        if isinstance(expression, str):
            p = KCExpr()
            p.set_expr(f"{self.expr}**{expression}")
            return p
        if isinstance(expression, KCExpr):
            p = KCExpr()
            p.set_expr(f"{self.expr}**{expression.expr}")
            return p
        raise TypeError(f"{expression} is not of class str or KCExpr")

    def __truediv__(self, expression):
        if isinstance(expression, str):
            p = KCExpr()
            p.set_expr(f"{self.expr}/{expression}")
            return p
        if isinstance(expression, KCExpr):
            p = KCExpr()
            p.set_expr(f"{self.expr}/{expression.expr}")
            return p
        raise TypeError(f"{expression} is not of class str or KCExpr")

    def __floordiv__(self, expression):
        if isinstance(expression, str):
            p = KCExpr()
            p.set_expr(f"{self.expr}//{expression}")
            return p
        if isinstance(expression, KCExpr):
            p = KCExpr()
            p.set_expr(f"{self.expr}//{expression.expr}")
            return p
        raise TypeError(f"{expression} is not of class str or KCExpr")

    def __mod__(self, expression):
        if isinstance(expression, str):
            p = KCExpr()
            p.set_expr(f"{self.expr}%{expression}")
            return p
        if isinstance(expression, KCExpr):
            p = KCExpr()
            p.set_expr(f"{self.expr}%{expression.expr}")
            return p
        raise TypeError(f"{expression} is not of class str or KCExpr")


