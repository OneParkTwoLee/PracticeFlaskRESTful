# REST API server to classify image

### Required Settings

- python 3.6.10
- flask, flask-restful
- fast.ai

 ### Project Structure

```
server_tutorial
├ README.md
└ api
  ├ *api.py # code for server operation (download the image classifier, POST)
  ├ cat.py # data format that is a response to the POST requested by the client
  ├ status.py # to handle HTTP status code
  └ models
    ├ README.md 
    └ (model.pth) # does not exist in the directory, downloads when the server starts

*If you use a different model, you need to modify the url in api.py.
```

### What the implemented HTTP method does

- `POST http://YOUR_IP_ADDRESS:YOUR_PORT/api/cats`
  
- The images sent from the client are identified by the image classifier(`model.pth`).
  
- In response to the client's `POST` request, separates each classes of requested images by comma, and sends the string in the field called `predicted_label` in `JSON` format.
  
    ```json
    // example JSON response to POST request
    // when there are 2 images requested,
    {
    	"predicted_label": "tiger, lion"
    }
    ```
- An example on Android is:
  
  ```java
  // example POST request on Android(client)
  // when there are 3 images requested,
    OkHttpClient client = new OkHttpClient().newBuilder().build();
  
    MediaType mediaType = MediaType.parse("text/plain");
  
    RequestBody body = new MultipartBody.Builder().setType(MultipartBody.FORM)
    .addFormDataPart("cat","IMAGE_NAME1",
        RequestBody.create(MediaType.parse("application/octet-stream"),
      new File("IMAGE_PATH1")))
      .addFormDataPart("cat","IMAGE_NAME2",
        RequestBody.create(MediaType.parse("application/octet-stream"),
        new File("IMAGE_PATH2")))
      .addFormDataPart("cat","IMAGE_NAME3",
        RequestBody.create(MediaType.parse("application/octet-stream"),
        new File("IMAGE_PATH3")))
      .build();
    
    Request request = new Request.Builder()
      .url("http://YOUR_IP_ADDRESS:YOUR_PORT/api/cats")
      .method("POST", body)
      .build();
    
    Response response = client.newCall(request).execute();
  ```
  
    *The above code is generated through postman and may cause problems in application.