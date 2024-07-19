import streamlit as st
from sympy import sympify, SympifyError, solve, Eq
from sympy.parsing.sympy_parser import parse_expr
from langchain.chains import LLMChain

# Mock LLMChain for local use without requiring an API key
class MockLLMChain:
    def run(self, problem):
        try:
            # Parse the input string to a sympy expression
            expression = parse_expr(problem)
            
            # Check if it's an equation to solve
            if '=' in problem:
                lhs, rhs = problem.split('=')
                equation = Eq(parse_expr(lhs.strip()), parse_expr(rhs.strip()))
                solution = solve(equation)
            else:
                solution = expression.evalf()
            
            return str(solution)
        except (SympifyError, ValueError) as e:
            return f"Error: {e}"

# Function to solve the math problem using Mock LLMChain
def solve_math_problem(problem):
    if not problem:
        return "Please enter a math problem."
    
    # Create Mock LLMChain instance
    llm_chain = MockLLMChain()

    # Generate the solution
    solution = llm_chain.run(problem)
    return solution

# Streamlit application
st.title("Math Problem Solver")

problem = st.text_area("Enter a math problem:", height=150)

if st.button("Solve"):
    solution = solve_math_problem(problem)
    st.text_area("Result:", value=solution, height=150)
