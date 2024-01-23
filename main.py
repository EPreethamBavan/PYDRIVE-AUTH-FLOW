import requests,json

url = 'https://oauth2.googleapis.com/token'
print(0)
print(1/0)

data = {
    'client_id': '704741266613-pt65jkq2r8iuvuq60hgmos5nqe3qrvdm.apps.googleusercontent.com',
    'client_secret': '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',
    'grant_type':'refresh_token',
    'refresh_token':'1//0gU6d7xNsmDigCgYIARAAGBASNwF-L9IrnxNGaj-30s3yFHvc2WP5y6Og4YSMq0nQIjueNTotyN_9npagP5RjMb6uWLqUrfFB7GE'
}


response = requests.post(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})


if response.status_code == 200:

    print(response.text)
    access=response.json()['access_token']
    print(access)

else:

    print(f"Request failed with status code {response.status_code}")
    print(response.text)

a=input("1.Single Part\n2.Multi Part\n3.Resumable\n4.Exit\n")
#simple upload
while a!='4':
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
print('')            