from extracted_info import ExtractedInfo
from llm_utils import call_llm
from pathlib import Path
from personal_scoring import compute_score
from reader import try_get_text_from_url
import time
from url_scraper import OttaScraper
from utils import get_lines_from_file

all_states = set(map(lambda s: s.lower(), get_lines_from_file("known_data/us_states.txt", strip_lines=True)))
all_languages = set(map(lambda l: l.lower(), get_lines_from_file("known_data/languages.txt", strip_lines=True)))


def try_find_string_between(text: str, begin: str, end: str) -> str | None:
    first_split = text.split(begin)
    if len(first_split) < 2:
        return None
    
    second_split = first_split[1].split(end)
    if len(second_split) < 2:
        return None
    
    return second_split[0]


def extract_info(text: str) -> ExtractedInfo:
    system_prompt = """
    You are evaluating a job posting and extracting specific information.
    Respond in the following format:
    <t>give your detailed thought process here</t>
    <l>a list of US states where the job can be worked at, separated by commas</l>
    <s>a salary estimate in USD; return only a single number; respond None if you cannot find one, and don't include any currency sign.</s>
    <pr>a list of programming languages that the job posting mentions, separated by commas</pr> 
    """

    user_prompt = f"Here is the posting:\n{text}"

    response = call_llm(system_prompt, user_prompt)

    print(response)

    states_raw = try_find_string_between(response, "<l>", "</l>")
    salary_raw = try_find_string_between(response, "<s>", "</s>")
    languages_raw = try_find_string_between(response, "<pr>", "</pr>")

    states = []
    if states_raw is not None:
        for st in states_raw.split(","):
            st = st.strip().lower()
            if st in all_states:
                states.append(st)
    
    languages = []
    if languages_raw is not None:
        for lang in languages_raw.split(","):
            lang = lang.strip().lower()
            if lang in all_languages:
                languages.append(lang)
    
    salary = None
    if salary_raw is not None:
        try:
            parsed_salary = float(salary_raw)
            salary = parsed_salary
        except ValueError:
            pass
    
    return ExtractedInfo(states, languages, salary)


if __name__ == "__main__":
    Path("output").mkdir(parents=True, exist_ok=True)

    scraper = OttaScraper()
    scraper.initialize()
    
    urls_generator = scraper.get_urls()
    
    with open("output/postings.txt", "a+") as output_file:

        for i in range(1000):
            url = next(urls_generator)

            url_text = try_get_text_from_url(url)
            if url_text is None:
                continue
            
            extracted_info = extract_info(url_text)
            score = compute_score(extracted_info)

            states_str = f"[{", ".join(extracted_info.states)}]"
            langs_str = f"[{", ".join(extracted_info.languages)}]"
            salary_str = "???" if extracted_info.estimated_salary is None else str(extracted_info.estimated_salary)
            output_file.write(f"score: {score}, url: {url}, est. salary: {salary_str}, langs: {langs_str}, "
                              f"states: {states_str}\n")
            
            if i % 5 == 0:
                output_file.flush()
            
            print(f"parsed url: {url}")

            time.sleep(1.0)