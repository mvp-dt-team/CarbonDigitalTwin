# import requests
# import time

# start_time = time.time()
# response = requests.get(
#     url=f"http://localhost:3000/measurement?"
#     + "&".join(["measurement_source_ids=" + str(x) for x in [1, 2]])
# )
# end_time = time.time()
# elapsed_time = end_time - start_time
# print(f"ДАННЫЕ: {elapsed_time:.6f} секунд")

import requests
import time


def timed_request(session, url, **kwargs):
    for i in range(100):
        start_time = time.time()
        response = session.get(url, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Request to {url} took {elapsed_time:.4f} seconds")
    return response


# Пример использования с сессией
with requests.Session() as session:
    url = f"http://localhost:3000/measurement?" + "&".join(
        ["measurement_source_ids=" + str(x) for x in [1, 2]]
    )
    response = timed_request(session, url)
    print(response.status_code)


with requests.Session() as session:
    url = f"http://localhost:3000/measurement?" + "&".join(
        ["measurement_source_ids=" + str(x) for x in [1, 2]]
    )
    response = session.get(url)
    print(response.status_code)
