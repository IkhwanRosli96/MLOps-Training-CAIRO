# Custom Training - Hands-On

## Custom Training with Custom Container

### 1. Create notebook instances in Jupyterlab

- Before we can create a notebook instance, we mut create a instances first.
  - Make sure you are in the "INSTANCES" tab.
  - Click "Create New"
    1.  **Details**
        - Change the instances name (optional)
        - Change the region to "us-central1"
        - Click continue
    2.  **Environment**
        - Ignore and click continue
    3.  **Machine Type**
        - This is where you want to configure your resource.
          - Choose **E2 Series** and for the "Machine Type", choose "e2-standard-2 (2 vCPU, 1 core, 8 GB memory)"
        - Click continue
    4.  **Machine Type**
        - On "data disk type", choose **Standard Persistent Disk**
        - Click continue
    5.  **Networking**
        - Ignore and click continue
    6.  **IAM and security**
        - Ignore and click continue
    7.  **System Health** - Click Create

> **It will take a few minutes to complete, do step 2 first and then proceed with this step**

- On the workbench, click "OPEN JUPYTERLAB"
- There are many kernel(env to run the notebooks) already prepared,
- For the training, we will use python3 kernel
- Upload file Training.ipyb. You can get the folder from training folder /03_Custom_Training/01_Custom Container
- Then select python3 as the kernel
- Go to step 3

> Even the workbench instances is not running, you still need to pay for it. Make sure to backup all your notebooks and delete the workbench if you are not gonna use it anymore.

### 2. Setup a bucket using Cloud Storage

- Create a bucket for our data using Google Storage
- Search the **cloud storage** on the GCP search tab
- Create a bucket
  - Change region to US-central1
- Upload the iris dataset to the bucket. You can get the dataset from workshop folder /03_Custom_Training/Data

### 3. Test training Code Using Notebook

- Run all the cell
- Delete the model.pickle as this only for code testing phase.

### 4. Create a docker image using the training code

- Before we can create the docker image files, we need to do 3 things
  - Convert train.ipyb into train.py
  - Create a DockerFile - Contains command for the docker when it build - setup env
  - Create requirements.txt - contains all of the python library needed
- Then will push it into artifact registry
- Prerequisite:
  1. **Convert train.ipyb into train.py**
     - We use terminal to convert it - For googla colab / Conda Jupyter notebook also have without need to use terminal
     - Open terminal
       - File -> New -> Terminal
       - Use command "jupyter nbconvert [IPYB_CODE] -- to python"
       - Rename the output file into "train.py"
       - Clean the inside of the "train.py"
         - Remove "type(data)"
         - Remove "data"
         - Remove "X_train.shape"
         - Remove "X_test.shape"
         - Remove "y_train.shape"
         - Remove "y_test.shape"
         - Remove "svn"
  2. **Create requirements.txt**
     - Right click on the same space of the train.py
     - Choose New File
     - Rename the txt file into requirements.txt
     - Copy content from /03_Custom_Training/01_Custom Container/requirements.txt into the requirements.txt and save
     - Content of requirements.txt
       - List of python libraries we want to use.
       - As default, in jupyter notebook, all of the python libraries that we used today already installed on the python3 kernel
       - However, for build a docker image which we not sure whether the base image has the library that we want, it is better to prepare the requirements.txt.
  3. **Create Dockerfile**
     - Right click on the same space of the train.py
     - Choose New File
     - Rename the txt file into Dockerfile
     - Copy content from /03_Custom_Training/01_Custom Container/Dockerfile into the Dockerfile and save
     - Content of Dockerfile
       - **"FROM python:3.7-buster"** - so will will take the base image is python base image with tag 3.7-buster
         - We use this base image because this base image already with linux based stuff and at the same time python.
       - **"WORKDIR /root"** - we will choose the /root directory as working directory.
       - **"COPY train.py /root/train.py"** -this command will copy the train.py file from our instances into the docker image
       - **"COPY requirements.txt /root/requirements.txt"** - this command will copy the requirements.txt file from our instances into the docker image
       - "RUN pip install -r /root/requirements.txt" - this command will install all the libraries in the requirements.txt to our docker env.
       - **"ENTRYPOINT ["python", "train.py"]"** - Entrypoint is a command to configure the executables that will always run after the container is initiated.
         - Everytime you started the docker container, this command will automatically running.
- We need to build docker image and the push it into the artifact registry
  - Search for **Artifact Registry** on the GCP search tab
  - Click "Create Repository"
    - Insert name perhaps "custom-training-artifact"
    - There are many format of artifac that we can create but for this purpose of training, we want to use docker.
  - Region is us-central1
  - Ignore other options and create
  - When created, open the docker there. There will be nothing there.
  - Click **Setup Instructions**, copy the command under **Configure Docker** and paste it on the terminal before go back to the artifact registry page
    - Input "y" and enter
  - Then, copy the docker image path and copy it on somehing - txt/ docs
  - **Example of path** : "us-central1-docker.pkg.dev/mlops-traning/custom-training-artifact"
    - **"us-central1-docker.pkg.dev"** is the registry path
    - **"mlops-traning"** is the name of our project
    - **"custom-training-artifact"** is the name of our artifact repository
  - However, there are something missing here. To build our docker, we need to specify the docker image name
  - Add "/[IMAGE_NAME]:[IMAGE_TAG]" to the path on the txt file so it will become us-central1-docker.pkg.dev/mlops-traning/custom-training-artifact/[IMAGE_NAME]:[IMAGE_TAG]
  - Change image name and image tag and add "export IMAGE_URI=" in front of the command
    - export IMAGE_URI=us-central1-docker.pkg.dev/mlops-traning/custom-training-artifact/iris_custom:v1
    - This command is to set the environment variable.
  - Copy the command and paste it into terminal
  - "echo $IMAGE_URI" - to validate if the varible assign correcty
  - Run "docker build -f Dockerfile -t ${IMAGE_URI} ./"
    - "-f" represent file which we use Dockerfile
    - "-t" represent tag is is our IMAGE_URI
    - "./" represent current directory
  - Run "docker image ls" to check if the docker image ls
  - Run "docker push ${IMAGE_URI}"

### 5. Train the model using custom container

- Search for **Vertex AI** on the GCP search tab
- On the left-side navbar - choose "Training" and choose "Train New Model"
- A training configuration will be popup

  - **Training Method**
    - Because we prepare the dataset ourself, instead of using dataset features in we need to select "No Managed Dataset" on the dataset option
    - Model training method - Defaul will be custom training
  - **Model Details**
    - Choose "train new model" (Default)
      - "Train new version" used when you already have trained previous model and you want to train new version of it.
      - Name the model to **"iris_custom"**
  - **Training Container**
    - Choose "Custom Container"
    - For "Custom Container Settings"
      - On "Container Image", click browse and choose the docker that we have made on the artifact registry.
      - For "Model Output Directory", browse and choose any path in our bucket to save our output model.
  - **Hyperparameter**
    - You can make hyperparameter tuning in this section.
    - We will ignore this
  - **Compute and Pricing**
    - Choose "us-central1" as the **Region**.
    - For **Machine Type**, choose "n1-standard-4"
    - Ignore **Accelerator Type** - This is GPU
    - **Disk Type** change to "Standard"
    - **Disk Size** will be the same as 100 is the lowest it can be
  - **Compute and Pricing**
    - Choose "No Prediction Container"

- Check bucket after the training done to ensure the model are there.

  > This training only will take a few minutes. Stay tuned!

### 5. Deploy the model to a endpoint

- We already trained the model and export it into our google storage.
- However, the model are not automatically appear in the model registry as our automl model.
- So we need to import it.
- - Search for **Vertex AI** on the GCP search tab
- On the left-side navbar - choose "Model Registry" and choose "IMPORT"
  - **Name and region**
    - Choose "Import as new model"
    - Give name to the model.
    - Choose "us-central1" as the **Region**
  - **Model Settings**
    - Choose "Import model artifacts into a new pre-built container "
      - This is because we don't have a custom container for our deployment. Only for training.
    - **Pre-built container settings**
      - For **Model Framework**, choose scikit-learn
      - For **Model Framework Verion**, we will use "0.24" because we use the same version for training.
      - For **Model Artifact Locaton**, choose the folder where the model location in the bucket.
      - **Ignore** other parameter
    - **Explainability**
      - For **Explainability Options** choose "No explainability"
    - Click **IMPORT** to continue
- To test the model, you need to create an endpoint first
  - Click on "Deploy & Test", and then click Deploy to endpoint"
  - **Define Your Endpoint**
    - "Create a new endpoint" if you don't have or you want to create a new endpoint
    - "Use existing endpoint" if you want use existing endpoint
    - For **Region**, choose "us-central1"
    - For **Access**, choose "Standard"
  - **Model Settings**
    - For **Traffic Split**, stay the same 100%
    - For **Minimum Number of Compute Nodes**, use 1
    - For **Maximum Number of Compute Nodes**, use 1
    - For **Machine Type**, choose "n1-standard-2"
    - For **Service Account**, choose "Compute Engine Default Service Account"
    - For **Logging**, disable "Enable access logging for this endpoint"
    - **Ignore** other
    - Click "Done" and then "Continue"
  - **Model monitoring**
    - **Ignore** this part as we learning.
    - In production, you might want to enable this so if anything happened to your endpint there will alert you.

### 5. Testing the endpoint

- **Web**
  - Go to "Deploy & Test" tab
  - Copy the content of the "/03_Custom_Training/01_Custom Container/Test/Sample/INPUT-JSON" and paste it
  - Click Predict
  - **API**
    - For the python api, there are some bug on the official github.
    - However, we already fix the bug.
    - Upload the "/Hands-on/03_Custom_Training/01_Custom Container/Test/Code/api_request.py" to cloud shell
    - Changed this parameter based on your endpoint
      - project
      - endpoint_id
      - location
