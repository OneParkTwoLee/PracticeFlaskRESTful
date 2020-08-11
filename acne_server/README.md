# REST API server to classify acne image

### Required Settings

- python 3.6.10
- flask, flask-restful
- fast.ai

 ### Project Structure

```
acne_server
├ README.md
└ api
  ├ api.py # code for server operation (download the acne image classifier, POST)
  ├ acne.py # data format that is a response to the POST requested by the client
  ├ status.py # to handle HTTP status code
  └ models
    ├ README.md 
    └ (model.pth) # does not exist in the directory, downloads when the server starts
```

### What the implemented HTTP method does

- `POST http://YOUR_IP_ADDRESS:YOUR_PORT/api/acnes`
  - The images sent from the client are identified by the acne image classifier(`model.pth`).

  - In response to the client's `POST` request, separates each acne types of requested acne images by comma, and sends the string in the field called `predicted_label` in `JSON` format.

    ```json
    // example JSON response to POST request
    // when there are 3 acne images requested,
    {
    	"predicted_label": "1,2,5"
    }
  ```
    
  - The types of acne for each number are:

    - `"1"`: whitehead
    - `"2"`: blackhead
    - `"3"`: papule
    - `"4"`: pustule
    - `"5"`: warning (nodular, cystic)

  - An example on Android is:

    ```java
    // example POST request on Android(client)
    // when there are 3 acne images requested,
    OkHttpClient client = new OkHttpClient().newBuilder().build();
    
    MediaType mediaType = MediaType.parse("text/plain");
    
    RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
      .addFormDataPart("acne","IMAGE_NAME1",
        RequestBody.create(MediaType.parse("application/octet-stream"),
        new File("IMAGE_PATH1")))
      .addFormDataPart("acne","IMAGE_NAME2",
        RequestBody.create(MediaType.parse("application/octet-stream"),
        new File("IMAGE_PATH2")))
      .addFormDataPart("acne","IMAGE_NAME3",
        RequestBody.create(MediaType.parse("application/octet-stream"),
        new File("IMAGE_PATH3")))
      .build();
    
    Request request = new Request.Builder()
      .url("http://YOUR_IP_ADDRESS:YOUR_PORT/api/acnes")
      .method("POST", body)
      .build();
    
    Response response = client.newCall(request).execute();
    ```

    *The above code is generated through postman and may cause problems in application.