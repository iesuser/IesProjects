# ეს სკრიპტი გააგზავნის Post Request-ებს /api/project-ზე და დაამატებს ინფორმაციას CSV ფაილიდან
# ამ სკრიპტის გამოსაყენებლად დაგჭირდებათ requests ბიბლიოთეკა
# დარწმუნდით რომ სწორად გაქვთ JWT_TOKEN ჩასმული 
# JWT ტოკენის აღება: გაიარეთ ავტორიზაცია ->
# გახსენით Developer Tools (F12) -> Application -> Local Storage -> access_token-ის Value დააკოპირეთ
# ჩაწერეთ JWT_TOKEN-ში


# File Path-ში მიუთითეთ CSV ფაილის მისამართი

# დარწმუნდით რომ CSV ფაილი სწორი ფორმატითაა
# პროექტის სახელი,ხელშეკრულების ნომერი,დაწყების დრო,დასრულების დრო,დამკვეთი,ადგილმდებარეობა,განედი,გრძედი,გეოლოგიური კვლევა,გეოფიზიკური კვლევა,სხვა ტიპის კვლევა,



import csv
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

JWT_TOKEN = ""
FILE_PATH = ""
url = "https://iesdata.iliauni.edu.ge:2022/api/projects"


def main():
    data = get_data(FILE_PATH)

    for d in data:
        status_code, response_text = send_request(JWT_TOKEN, d,url)
        print(f"Status Code: {status_code}, Response: {response_text}")


def get_data(file_path):
    data_list = []
    try:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                data = {
                    "projects_name": row["პროექტის სახელი"].strip(),
                    "contract_number": row["ხელშეკრულების ნომერი"].strip(),
                    "start_time": row["დაწყების დრო"].strip() or "1990-01-01",
                    "end_time": row["დასრულების დრო"].strip() or "1990-01-01",
                    "contractor": row["დამკვეთი"].strip(),
                    "proj_location": row["ადგილმდებარეობა"].strip() or "სეისმო",
                    "proj_latitude": row["განედი"].strip(),
                    "proj_longitude": row["გრძედი"].strip(),
                }
                data_list.append(data)

    except FileNotFoundError:
        print(f"File Not Found {file_path}")
    
    return data_list
def send_request(jwt_token,data,url = "https://iesdata.iliauni.edu.ge:2022/api/projects"):

    headers = {
    "Authorization": f"Bearer {jwt_token}",
    }

    response = requests.post(
            url,
            headers=headers,
            data=data,
            verify=False,
        )
    
    return response.status_code, json.dumps(response.json(), ensure_ascii=False)



if __name__ == "__main__":
    main()
        