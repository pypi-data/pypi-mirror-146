=================
KCExpr for Python
=================

KCExpr allows for the parsing of mathematical expressions as strings. KCExpr currently supports 27 mathematical functions, such as summation, products, and trigonometric functions, as well as supporting 37 mathematical constants, such as pi, e, and the golden ratio.

In all cases of KCExpr, the implementation structure is relatively similar. Firstly, declare an object of the KCExpr() class. Next, set the expression of that object. Finally, parse the object. The code blocks below highlight this process, both for single and multiple objects.

**Basic implementation**

.. code-block:: python

 import KCExpr.KCExpr as kce
 
 p = kce.KCExpr()
 p.set_expr("1 + 2")
 result = p.parse()
 print(result)  # prints "3" to the console

**Further implementation**

.. code-block:: python
 
 import KCExpr.KCExpr as kce
 
 p1, p2 = kce.KCExpr(), kce.KCExpr()
 p1.set_expr("1")
 p2.set_expr("2")
 p3 = p1 + p2
 result = p3.parse()
 print(result)  # prints "3" to the console 

**Mathematical functions parsable by KCExpr**

The syntax for functions can be found in the docs folder (see GitHub). The following is a list of functions included in the KCExpr class.

- abs, sqrt, root, ncr, npr, sigma, pi, ln, log, sin, sina, csc, sinh, csch, sinha, cos, acos, sec, cosh, sech, cosha, tan, atan, cot, tanh, coth, tanha.

**Using mathematical constants in KCExpr**

The syntax for mathematical constants can be found in the docs folder (see GitHub). The following is a list of constants included in the KCExpr class.

.. list-table:: 
   :widths: 4 1
   :header-rows: 1

   * - Constant
     - Code

   * - Pi
     - pi
   * - Euler's Number
     - e
   * - Euler–Mascheroni constant
     - em
   * - The golden ratio
     - golden
   * - Meissel-Mertens constant
     - mm
   * - Bernstein's constant
     - bernstein
   * - Gauss-Kuzmin-Wirsing constant
     - gkw
   * - Hafner-Sarnak-McCurley constant
     - hsm
   * - Omega constant
     - omega
   * - Golomb-Dickman constant
     - gd
   * - Cahen's constant
     - cahen
   * - The twin prime constant
     - tp
   * - The laplace limit
     - laplace
   * - Embree-Trefethen constant
     - et
   * - Landau-Ramanujan constant
     - lr
   * - Brun's constant for prime quadruplets
     - brunpq
   * - Brun's constant for prime twins
     - brunpt
   * - Catalan's constant
     - catalan
   * - Viswanath's constant
     - viswanath
   * - Apéry's constant
     - apery
   * - Conway's constant
     - conway
   * - Mills' constant
     - mills
   * - The plastic number
     - plastic
   * - Ramanujan-Soldner constant
     - rs
   * - Backhouse's constant
     - backhouse
   * - Porter's constant
     - porter
   * - Lieb's square ice constant
     - lieb
   * - Erdős–Borwein constant
     - eb
   * - Niven's constant
     - niven
   * - The universal parabolic constant
     - upc
   * - Feigenbaum's α constant
     - feigenbauma
   * - Feigenbaum's δ constant
     - feigenbaumd
   * - Sierpinski's constant
     - sierpinski
   * - Khinchin's constant
     - khinchin
   * - Fransén–Robinson constant
     - fr
   * - Lévy's constant
     - levy
   * - The reciprocal Fibonacci constant
     - rf
