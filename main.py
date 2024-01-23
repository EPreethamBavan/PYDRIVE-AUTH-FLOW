import requests,json

url = 'https://oauth2.googleapis.com/token'

data = {
    'client_id': '',
    'client_secret': '',
    'grant_type':'refresh_token',
    'refresh_token':''
}


response = requests.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})


if response.status_code == 200:

    print(response.text)
    access=response.json()['access_token']
    print(access)
    a=input("1.Single Part\n2.Multi Part\n3.Resumable\n4.Exit\n")
    while a!='4':
        #simple upload
        if a=="1":
            url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=media"


            headers = {
                "Authorization": f"Bearer {access}", 
                "Content-Type": "image/png"
            }


            with open('sample.png', 'rb') as file:

                response = requests.post(url, headers=headers, data=file)


            if response.status_code == 200:

                print("File uploaded successfully.")
            else:

                print("Error uploading file. Status code:", response.status_code)
                print("Response content:", response.text)
        #multipart
        elif a=="2":

            url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"




            headers = {
                "Authorization": f"Bearer {access}",
            }


            form_data = {
                "metadata": ("new.json.txt", open("new.json.txt", "rb")),
                "file": ("sample.png", open("sample.png", "rb"))
            }


            response = requests.post(url, headers=headers, files=form_data)


            if response.status_code == 200:

                print("File uploaded successfully.")
            else:
                
                print("Error uploading file. Status code:", response.status_code)
                print("Response content:", response.text)
        #resumable upload
        elif a=='3':
            

            url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable"

            headers = {
                "Authorization": f"Bearer {access}",
                "Content-Type": "application/json",
            }

            json_data = {
        "name" : "resumable.txt",
        "description" : "This is a resuamble example text file"
        }
            json_data_str = json.dumps(json_data)

            response = requests.post(url, headers=headers,data=json_data_str)

            if response.status_code in [200, 201]:

                location = response.headers.get('Location')


                with open("example.txt", "rb") as binary_file:
                    binary_data = binary_file.read()


                put_response = requests.put(location, data=binary_data)


                if put_response.status_code == 200:
                    print("Upload successful.")
                else:
                    print(f"PUT request failed with status code {put_response.status_code}: {put_response.text}")

            else:
                print(f"Initial POST request failed with status code {response.status_code}: {response.text}")
        a=input("1.Single Part\n2.Multi Part\n3.Resumable\n4.Exit\n")        

else:

    print(f"Request failed with status code {response.status_code}")
    print(response.text)

