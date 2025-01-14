
def get_lines_from_file(file_path: str, strip_lines=True) -> list[int]:
    lines = []
    with open(file_path, "r") as file:
        for line in file:
            if strip_lines:
                line = line.strip()
            
            if len(line) > 0:
                lines.append(line)
    
    return lines