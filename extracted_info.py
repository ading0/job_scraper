
class ExtractedInfo(object):
    
    def __init__(self, states: list[str] | None, languages: list[str], estimated_salary: float | None):
        self.states = states
        self.languages = languages
        self.estimated_salary = estimated_salary