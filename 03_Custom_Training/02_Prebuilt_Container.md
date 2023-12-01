# AutoML - Hands-On

## Custom Training with Pre-built Container

### 1. Setup a bucket using Cloud Storage

> We already create a bucket before. So let's just use it

- Create a file on the bucket named "prebuilt-container".
- Upload the iris dataset into the file. You can get the dataset from workshop folder /03_Custom_Training/Data

### 2. Create notebook in jupyterlab

- Create a folder name "prebuilt-container"
- Inside this container, upload file train.ipyb. You can get the folder from training folder /03_Custom_Training/02_Prebuilt_Container

### 3. Test training Code Using Notebook

- Change the CSV_FILE_PATH at cell 2"df
  - = pd.read_csv("[CSV_FILE_PATH]") "df = pd.read_csv("gs://prebuilt_container_training/IRIS.csv")
- Run all the cell
- Delete the "model_output" folder in the bucket as this only for code testing phase.

### 4. Prepare the code for training

1.  **Convert train.ipyb into train.py**
    - **Add** argparse to the code
      - Add new cell after the 1st cell, and copy the content of "/03_Custom_Training/02_Prebuilt_Container/argparser.py/" into the new cell
      - Change "df = pd.read_csv()" to "df = pd.read_csv(input_file)"
      - Change "model.save()" to "model.save(output_file)"
    - We use terminal to convert it - For google colab / Conda Jupyter notebook also have without need to use terminal
    - Open terminal
      - File -> New -> Terminal
      - Use command "jupyter nbconvert train.ipynb --to python"
      - Rename the output file into "train.py"
      - Clean the inside of the "train.py"
        - **Remove** "df" - line 43
        - **Remove** "dummy_y" - line 66
        - **Remove** "print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]\*100))" - line 88
        - **Remove** "test" - line 101
2.  **Create \_\_init\_\_.py (module)**

    - To create a module, we need to create a folder first. Named it as "trainer"
    - Move "train.py" into the the folder
    - Go the folder.
    - Create a text file, named it "\_\_init\_\_.py" and leave it empty

3.  **Create setup.py**
    - Upload the "setup.py" from the "/03_Custom_Training/02_Prebuilt_Container/"
      - In setup.py
        - REQUIRED_PACKAGES - What package do we want to use?
        - Because we will used tensorflow container later, we do not need to put tensorflow as one of the package
      - "name" is the code is the name of your folder containing your "\_\_init\_\_.py" and "train.py"
4.  **Create the package**
    - Make sure all are completes
      - setup.py
      - /trainer/\_\_init\_\_.py
      - /trainer/train.py
    - Copy content of build_package.txt and paste it into terminal.
    - If success, there will be 2 folder created.
      - "dist"
      - "trainer.egg-info"
5.  **Copy the package file into the Google Storage**
    - In terminal, change directory into "dist" folder
      - Run "cd /dist/"
      - Run "gsutil ls" to see all of our bucker
      - Copy the "trainer-0.1.tar.gz" by running "gsutil

### 5. Train the model using Prebuilt container

- Search for **Vertex AI** on the GCP search tab
- On the left-side navbar - choose "Training" and choose "Train New Model"
- A training configuration will be popup

  - **Training Method**
    - Because we prepare the dataset ourself, instead of using dataset features in we need to select "No Managed Dataset" on the dataset option
    - Model training method - Defaul will be custom training
  - **Model Details**

    - Choose "train new model" (Default)
      - "Train new version" used when you already have trained previous model and you want to train new version of it.
      - Name the model to **"iris_prebuilt"**
      - Go advance options
        - For **Service account**, choose "Compute Engine default service account"

  - **Training Container**

    - For **Container Type**, choose "Pre-built container"
    - For **Model Framework**, choose "Tensorflow"
    - For **Model Framework Version**, choose same as your kernel version where you test the training code before.
    - In **Pre-built container settings**
      - For **Package Location**, choose the package that we copy to cloud storage before.
      - For **Python Module**, insert "trainer.train"
        - "trainer" is the name of folder that we used to create the package.
        - "train" is the name of python file inside the python trainer.
      - For **Arguments**, copy content from arg_train.txt and paste into it.
        - --data_input="[DATA_PATH_IN_GS]", change [DATA_PATH_IN_GS] to your data path
          - Example: **--data_input="gs://03-custom-training/prebuilt-container/Iris.csv"**
        - --model_output="[OUTPUT_PATH_IN_GS]", change [OUTPUT_PATH_IN_GS] to your output path
          - Example: **--model_output="gs://03-custom-training/prebuilt-container/model_iris"**

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
    - Choose "Import model artifacts into a new pre-built container
      - This is because we don't have a custom container for our deployment. Only for training.
    - **Pre-built container settings**
      - For **Model Framework**, choose "Tensorflow"
      - For **Model Framework Verion**,choose same as your training before.
        - If not sure check the model information.
      - For **Model Artifact Locaton**, choose the folder where folder where the model_output located.
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
