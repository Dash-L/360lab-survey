import csv
from ast import literal_eval
import matplotlib


def compute_headers(raw_headers: list[str], readable_headers: list[str],
                    header_map: list[str]) -> list[tuple[str, str]]:
    headers: list[tuple[str, str]] = []
    print(raw_headers, end='\n\n')
    for header_inst in header_map:
        is_string = True
        raw: str = literal_eval(header_inst)['ImportId']
        if raw.lower() in map(lambda s: s.lower(), raw_headers):
            idx = list(map(lambda s: s.lower(),
                           raw_headers)).index(raw.lower())
        elif (raw_without_id := raw.replace('ID', '')) in raw_headers:
            idx = raw_headers.index(raw_without_id)
            is_string = False
        elif (raw_without_id_text :=
              raw_without_id.replace('_TEXT', '')) in raw_headers:
            idx = raw_headers.index(raw_without_id_text)
        else:
            idx = -1

        headers.append((raw_headers[idx], readable_headers[idx],
                        is_string) if idx != -1 else (raw, None, is_string))

    return headers


with open('data.csv', 'r', newline='') as file:
    reader = csv.reader(file)
    raw_data = list(reader)
    raw_headers = raw_data[0]
    readable_headers = raw_data[1]
    header_map = raw_data[2]

    headers = compute_headers(raw_headers, readable_headers, header_map)

    full_responses = list(
        map(
            lambda row: {
                headers[i][0]: (str(headers[i][1])
                                if headers[i][1] is not None else None,
                                str(response), headers[i][2])
                for i, response in enumerate(row)
            }, raw_data[3:]))

    responses = map(
        lambda resp: {
            key: value
            for key, value in resp.items() if 'Q' in key
        }, full_responses)

    for response in responses:
        print("\n-------------------------\n")
        for question_id, (question, answer, is_string) in response.items():
            if is_string:
                print(f"{question}:\t{answer}")
