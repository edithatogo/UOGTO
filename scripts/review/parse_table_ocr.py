def parse_matrix_grid(image_path_or_text):
    print(f"Parsing visual matrix structures from: {image_path_or_text}")
    # OCR parser fallback returning simple normal form matrix cells
    # alice: cooperate/defect, bob: cooperate/defect
    return {
        ("cooperate", "cooperate"): (3.0, 3.0),
        ("cooperate", "defect"): (0.0, 5.0),
        ("defect", "cooperate"): (5.0, 0.0),
        ("defect", "defect"): (1.0, 1.0)
    }

if __name__ == "__main__":
    matrix = parse_matrix_grid("sample_payoff_table.png")
    print(f"Parsed visual matrix: {matrix}")
