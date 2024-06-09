import requests

API_BASE_URL = "http://localhost:3000"


def upload_file(file_path: str, description: str):
    with open(file_path, "rb") as file:
        response = requests.post(
            f"{API_BASE_URL}/uploadfile/",
            files={"file": file},
            params={"description": description}
        )
        if response.status_code == 200:
            print("File uploaded successfully.")
            print(response.json())
        else:
            print("Failed to upload file.")
            print(response.text)


def download_file(file_id: str, save_path: str):
    response = requests.get(f"{API_BASE_URL}/uploads/{file_id}")
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download file.")
        print(response.text)


# Пример использования
upload_file("test.txt", "This is a test file.")
download_file("test.txt", "test1.txt")
