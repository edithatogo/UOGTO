import re

def extract_equations(text):
    if not text:
        return []
    
    # 1. LaTeX matching ($...$ or $$...$$)
    latex_inline = re.findall(r"\$(.+?)\$", text)
    latex_block = re.findall(r"\$\$(.+?)\$\$", text)
    
    # 2. MathML simple representation tag matching
    mathml = re.findall(r"<math[^>]*>(.*?)</math>", text, re.DOTALL)
    
    # 3. Typst style formula matching (#math.equation or $...$)
    typst = re.findall(r"#math\((.*?)\)", text)
    
    # 4. Quarto inline formulas (re-uses latex matching style)
    
    all_eqs = latex_inline + latex_block + mathml + typst
    return [eq.strip() for eq in all_eqs if eq.strip()]

if __name__ == "__main__":
    test_text = "The payoff is given by $u_i(s) = \\sum p_j v_j$ and block equation $$x^2 + y^2 = z^2$$ or mathml <math><mrow><mi>x</mi></mrow></math>"
    eqs = extract_equations(test_text)
    print(f"Extracted equations: {eqs}")
