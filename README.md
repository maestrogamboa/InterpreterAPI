# InterpreterAPI
This project is for the API portion of the Interpreter App Submition for the Google Hackathon project

# InterpreterAPI
The project uses Docker for development purposes. Here's how to get setup.
1. Clone the respository
2. Open Docker desktop app or make sure is running in the background
3. Create docker image
```bash
docker build -t <DockerImageName> .
```
4. Run docker container
```bash
docker run -p 8080:5000 <DockerImageName>
```

#API Reference
To make a request, reference your hostname (ie localhost) with port 8080:
```bash
http://localhost:8080
```


