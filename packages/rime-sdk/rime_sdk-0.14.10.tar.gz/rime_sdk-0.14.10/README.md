# RIME SDK

The RIME SDK provides an interface to RIME backend services for starting and viewing the progress of RIME stress test jobs.
There are four objects available in the `rime_sdk` package:
* RIMEClient
* RIMEStressTestJob
* RIMEProject
* CustomImage

To use these objects, import them from the package like so:
```Python
from rime_sdk import RIMEClient, RIMEStressTestJob, RIMEProject, RIMECTInstance
```

## RIMEClient

The `RIMEClient` provides an interface to RIME's backend services for creating projects, starting stress test jobs, and querying the backend for current stress test jobs.
To initialize the RIMEClient, provide the address of your RIME instance.
```Python
rime_client = RIMEClient("my_vpc.rime.com", "api-key")
```

### `start_stress_test()`

This allows you to start an AI Stress Test job on the RIME backend.

**Arguments:**

* `test_run_config: dict`

  Specifies paths to the model and dataset to be used in the stress test.
* `project_id: Optional[str] = None`

  Specify the project to file the stress test result under.
  If omitted, the stress test result will be stored in the default project.

* `rime_managed_image: Optional[str] = None`

  Specify the name of the RIME Managed Image to run the stress test on.
  Managed Images are the preferred method of running RIME on an image with custom Pip requirements.
  See the documentation for `create_managed_image()` and `list_managed_images()` for further information.

* `custom_image: Optional[CustomImage] = None`

  Specify a custom Docker image to run the stress test job on.
  This image could include custom libraries that your model depends on.
  If no custom image is provided, the backend will use the default image specified by the cluster configuration.

* `ram_request_megabytes: Optional[int] = None`

  Specify the megabytes of RAM to request for a stress test job. If none
  specified, will default to 4000MB. The limit will be set as 2x the request.

* `cpu_request_millicores:  Optional[int] = None`

  Specify the millicores of CPU to request for a stress test job. If none
  specified, will default to 1500mi. The limit will be set as 2x the request.

**Return Value:**

A `RIMEStressTestJob` object that provides an interface for monitoring the job in the backend.

**Example:**

```Python
# This example will likely not work for you because it requires permissions to a specific S3 bucket.
# This demonstrates how you might specify such a configuration.
config = {
  "run_name": "Titanic",
  "data_info": {
    "label_col": "Survived",
    "ref_path": "s3://rime-datasets/titanic/titanic_example.csv", "eval_path": "s3://rime-datasets/titanic/titanic_example.csv"
  },
  "model_info": {
    "path": "s3://rime-models/titanic_s3_test/titanic_example_model.py"
  }
}
# Run the job using the specified config and the default Docker image in the RIME backend.
# Store the results under project ID "foo"
# Use the RIME Managed Image "tensorflow115".
# This assumes you have already created the Managed Image and waited for it to be ready.
job = rime_client.start_stress_test_job(test_run_config=config, project_id="foo", rime_managed_image="tensorflow115")
```

### `create_managed_image()`

This method allow you to create new managed Docker images to run RIME on.
These managed Docker images are managed by the RIME backend and will automatically be upgraded when you update your version of RIME.
Images take a few minutes to be built.
This method returns an object that can be used to track the progress of the image building job.
The new custom image is only available for use in a stress test once it has status `READY`.

**Arguments**

* `name: str`

  The name of the new managed image.
  This acts as the unique identifier of the managed image.
  The call will fail if an image with the specified name already exists.

* `requirements: List[ManagedImage.PipRequirement]`

  List of additional pip requirements to be installed on the managed image.
  A `ManagedImage.PipRequirement` can be created with the helper method `RIMEClient.pip_requirement(name: str, version_specifier: Optional[str] = None)`.
  The first argument is the name of the library (e.g. `"tensorflow"` or `"xgboost"`) and the second argument is a valid pip
  [version specifier](https://www.python.org/dev/peps/pep-0440/#version-specifiers) (e.g. `">=0.1.2"` or `"==1.0.2"`).

**Return Value**

A `RIMEImageBuilder` object that provides an interface for monitoring the job in the backend.

**Example**

```python
requirements = [
   # Fix the version of `xgboost` to `1.0.2`.
   rime_client.pip_requirement("xgboost", "==1.0.2"),
   # We do not care about the installed version of `tensorflow`.
   rime_client.pip_requirement("tensorflow")
 ]

# Start a new image building job 
builder_job = rime_client.create_managed_image("xgboost102_tensorflow", requirements)
# Wait until the job has finished and print out status information.
# Once this prints out the `READY` status, your image is available for use in stress tests.
builder_job.get_status(verbose=True, wait_until_finish=True)
```

### `list_managed_images()`

This method allows you to query the backend for managed Docker images.
This is where the true power of the managed images feature lies.
You can search for images with specific pip libraries installed so that you do not have to create a new managed image every time you need to run a stress test.

**Arguments**

* `pip_library_filters: Optional[List[ListImagesRequest.PipLibraryFilter]] = None`

  A list of filters used to query the managed images stored in the backend.
  Query results will match the intersection of the filters.
  You may construct `ListImagesRequest.PipLibraryFilter` objects using the `RIMEClient.pip_library_filter(name: str, fixed_version: Optional[str] = None)` helper method.


* `page_token: str = ""`

  Page token used for paginating the API results.
  To get access to the next page of results, use the second value in the tuple returned by the previous call.

* `page_size: int = 100`

  Number of results to output.
  Default is 100 managed images to be returned.

**Return Value**

A `Tuple[List[Dict], str]` object.
The first value in the tuple is a list of dictionary representations of Managed Images.
The second value in the tuple is the next page token.

**Example**

```python
# Filter for an image with catboost1.0.3 and tensorflow installed.
filters = [
  rime_client.pip_library_filter("catboost", "1.0.3"),
  rime_client.pip_library_filter("tensorflow"),
]

# Query for the images.
images, next_page_token = rime_client.list_managed_images(pip_library_filters=filters)

# List comprehension to get all the names of the images.
names = [x["name"] for x in images]
```

### `create_project()`

Projects allow you to organize stress test runs as you see fit.
A natural way to organize stress test runs is to create a project for each specific ML task, such as predicting whether a transaction is fradulent.

**Arguments:**

* `name: str`

  The name of the project.
  You can change this later in the UI.
* `description: str`

  A short blurb about the project.

**Return Value:**

A `RIMEProject` that describes the created project.
Its `project_id` attribute can be used in `start_stress_test()` and `list_stress_test_jobs()`.

**Example:**

```Python
project = rime_client.create_project(name='foo', description='bar')
```

### `list_stress_test_jobs()`

Query the backend for a list of jobs filtered by status and project ID.
This is a good way to recover `RIMEStressTestJob` objects.
Note that this only returns jobs from the last two days, because the time-to-live of job objects in the backend is set at two days.

**Arguments:**

* `status_filters: Optional[List[str]] = None`

  Select jobs by a union of statuses.
  If this is omitted, jobs will not be filtered by status.
  Acceptable values are in the following array:
  ```Python
  ['UNKNOWN_JOB_STATUS', 'PENDING', 'RUNNING', 'FAILING', 'SUCCEEDED']
  ```
* `project_id: Optional[str] = None`

  Select jobs by project.
  If this is omitted, jobs from across different projects will be returned.

**Return Value:**

A list of `RIMEStressTestJob` objects.
These are not guaranteed to be in any sorted order.

**Example:**
```Python
# Get all running and succeeded jobs for project 'foo'
jobs = rime_client.list_stress_test_jobs(status_filters=['RUNNING', 'SUCCEEDED'], project_id='foo')
```

### `get_ct_instance()`

Query the backend for a `RIMECTInstance` which can be used to perform Continuous
Testing operations. If the CT Instance you are trying to fetch does not exist,
this will error.

**Arguments:**

* `ct_instance_id: str`

  ID of the CT instance.

**Return Value:**

A `RIMECTInstance` object.

**Example:**
```Python
# Get CT instance foo if it exists.
ct_instance = rime_client.get_ct_instance("foo")
```

### `get_active_ct_instance_for_project()`

Query the backend for an active `RIMECTInstance` in a specified project  which
can be used to perform Continuous Testing operations. If there is no active
CT instance for the project, this call will error.

**Arguments:**

* `project_id: str`

  ID of the project which contains an activeCT instance.

**Return Value:**

A `RIMECTInstance` object.

**Example:**
```Python
# Get CT instance in foo-project if it exists.
ct_instance = rime_client.get_active_ct_instance_for_project("foo-project")
```

### `create_ct_instance()`

Create a CTInstance for a given project. This CTInstance will be inactive by default.

**Arguments:**

* `name: str`

  Name of the CT instance.

* `bin_size_seconds: int`

  Bin size in seconds. Only supports 3600(hourly) and 86400(daily)

* `ot_test_run_id: str`

  ID of the stress test to associate all continuous test runs with.

* `project_id: str`

  ID of the project this CTInstance belongs to.

**Return Value:**

A `RIMECTInstance` object.

**Example:**
```Python
# Create CT instance based on foo stress test in bar project.
ct_instance = rime_client.create_ct_instance("ct name", 86400, "foo", "bar")    
```

### `start_continuous_test_from_reference()`

This allows you to start an AI Continuous Test job on the RIME backend. This
will run a stress test, create a ct instance, and then run continuous tests
on your dataset.

**Arguments:**

* `test_run_config: dict`

  Specifies paths to the model and dataset to be used in the continuous test.
* `project_id: Optional[str] = None`

  Specify the project to file the continuous test result under.
  If omitted, the continuous test result will be stored in the default project.

* `rime_managed_image: Optional[str] = None`

  Specify the name of the RIME Managed Image to run the continuous test on.
  Managed Images are the preferred method of running RIME on an image with custom Pip requirements.
  See the documentation for `create_managed_image()` and `list_managed_images()` for further information.

* `custom_image: Optional[CustomImage] = None`

  Specify a custom Docker image to run the continuous test job on.
  This image could include custom libraries that your model depends on.
  If no custom image is provided, the backend will use the default image specified by the cluster configuration.

* `ram_request_megabytes: Optional[int] = None`

  Specify the megabytes of RAM to request for a continuous test job. If none
  specified, will default to 4000MB. The limit will be set as 2x the request.

* `cpu_request_millicores:  Optional[int] = None`

  Specify the millicores of CPU to request for a continuous test job. If none
  specified, will default to 1500mi. The limit will be set as 2x the request.

**Return Value:**

A `RIMEStressTestJob` object that provides an interface for monitoring the job in the backend.

**Example:**

```Python
# This example will likely not work for you because it requires permissions to a specific S3 bucket.
# This demonstrates how you might specify such a configuration.
config_from_reference = {
  "run_name": "Five Day Fraud Detection",
  "data_info": {
    "label_col": "is_fraud",
    "pred_col": "is_fraud_preds",
    "ref_path": "s3://rime-datasets/fraud_continuous_testing/ref.csv",
    "eval_path": "s3://rime-datasets/fraud_continuous_testing/eval_2021_04_01_to_2021_04_06.csv"
  },
  "continuous_info": {
    "timestamp_col": "timestamp",
    "bin_size": "day"
  },
}
# Run the job using the specified config and the default Docker image in the RIME backend.
# Store the results under project ID "foo"
# Use the RIME Managed Image "tensorflow115".
# This assumes you have already created the Managed Image and waited for it to be ready.
job = rime_client.start_continuous_test_from_reference(test_run_config=config_from_reference, 
                                                       project_id="foo",
                                                       rime_managed_image="tensorflow115",
                                                       ram_request_megabytes=8000,
                                                       cpu_request_millicores=2000)
```

## RIMEStressTestJob

This object provides an interface for monitoring the status of a stress test job in the RIME backend.

### `get_status()`

Query the RIME backend for the job's status.
This includes flags for blocking until the job is complete and printing information to `stdout`.
This method can help with monitoring the progress of stress test jobs, because it prints out helpful information such as running time and the progress of the test run.

**Arguments:**

* `verbose: bool = False`

  Whether to print additional status information to `stdout`.
  If this flag is enabled and the job status is `'SUCCEEDED'` or `'FAILING'`, the logs of the testing engine will be dumped to `stdout` to help with debuggability.
  Note that this logs have no strict form and will be subject to significant change in future versions.
* `wait_until_finish: bool = False`

  Whether to block until the job status is `'SUCCEEDED'` or `'FAILING'`.
  If `verbose` is enabled too, information about the job including running time and progress will be printed to `stdout` every `poll_rate_sec`.
* `poll_rate_sec: float = 5.0`

  How often to ping the RIME backend services for the status of the job.
  Units are in seconds.

**Return Value:**

A dictionary representing the status of the `RIMEStressTestJob`.
```Python
{
  "name": str
  "type": str
  "status": str
  "start_time_secs": int64
  "running_time_secs": double
}
```
`type` will be an element in the following array:
```Python
['MODEL_STRESS_TEST', 'UNKNOWN_JOB_TYPE']
```
`status` will be an element in the following array:
```Python
['UNKNOWN_JOB_STATUS', 'PENDING', 'RUNNING', 'FAILING', 'SUCCEEDED']
```

**Example:**

```Python
# Block until this job is finished and dump monitoring info to stdout.
job_status = job.get_status(verbose=True, wait_until_finish=True)
```

### `get_test_cases_result()`

Retrieve all the test cases for a completed stress test run in a dataframe.
This gives you the ability to perform granular queries on test cases.
For example, if you only care about subset performance tests and want to see the results on each
feature, you can fetch all the test cases in a dataframe, then query on that dataframe by test type.
This only works on stress test jobs that have succeeded.

*Note: this does not work on <0.14.0 RIME test runs.*

**Arguments:**

* `version: Optional[str] = None`

  Semantic version of the results to be returned.
  This allows users to pin the version of the results, which is helpful if you write any code on top of RIME data.
  If you upgrade the SDK and do not pin the version in your code, it may break because the output not guaranteed to be stable across versions.
  The latest output will be returned by default.

**Return Value:**

A `pandas.DataFrame` object containing the test case results.
Here is a selected list of columns in the output:
1. `test_run_id`: ID of the parent test run.
2. `features`: List of features that the test case ran on.
3. `test_batch_type`: Type of test that was run (e.g. Subset AUC, Must be Int, etc.).
4. `status`: Status of the test case (e.g. Pass, Fail, Skip, etc.).
5. `severity`: Metric that denotes the severity of the failure of the test.

**Example:**

 ```Python
 # Wait until the job has finished, since this method only works on SUCCEEDED jobs.
 job.get_status(verbose=True, wait_until_finish=True)
 # Dump the test cases in dataframe `df`.
 # Pin the version to RIME version 0.14.0.
 df = job.get_test_cases_result(version="0.14.0")
 # Print out the column names and types.
 print(df.columns)
 ```

### `get_test_run_result()`

Retrieve high level summary information for a complete stress test run in a single-row dataframe.
By concatenating these rows together, this allows you to build a table of test run results for sake of comparison.
This only works on stress test jobs that have succeeded.

*Note: this does not work on <0.14.0 RIME test runs.*

**Arguments:**

* `version: Optional[str] = None`

  Semantic version of the results to be returned.
  This allows users to pin the version of the results, which is helpful if you write any code on top of RIME data.
  If you upgrade the SDK and do not pin the version in your code, it may break because the output not guaranteed to be stable across versions.
  The latest output will be returned by default.

**Return Value:**

A `pandas.DataFrame` object containing the test run result.
There are a lot of columns, so it is worth viewing them with the `.columns` method to see what they are.
Generally, these columns have information about the model and datasets as well as
summary statistics like the number of failing test cases or number of high severity test cases.

**Example:**

 ```Python
 # Wait until the job has finished, since this method only works on SUCCEEDED jobs.
 job.get_status(verbose=True, wait_until_finish=True)
 # Dump the test cases in dataframe `df`.
 # Pin the version to RIME version 0.14.0.
 df = job.get_test_run_result(version="0.14.0")
 # Print out the column names and types.
 print(df.columns)
 ```
## RIMEProject

This object describes a project in the RIME backend.

**Attributes:**

* `project_id: str`

  How to refer to the project in the backend.
  Use this attribute to specify the project for the backend in `start_stress_test_job()` and `list_stress_test_jobs()`.
* `name: str`
* `description: str`

## RIMECTInstance

This object describes a RIMECTInstance in the Rime Backend

**Attributes:**

* `ct_instance_id: str`

  How to refer to the CTInstance in the backend.
  Use this attribute to specify the CTInstance for tasks in the backend.

### `activate_ct_instance()`

Mark a CTInstance as active. This will deactivate any existing CTInstance in the project and set this CTInstance as the one associated with a given project.

### `deactivate_ct_instance()`

Mark a CTInstance as inactive. This will deactivate the CTInstance, preventing it from being viewed in the frontend.

### `start_incremental_continuous_test()`

This allows you to start an Incremental Continuous Test job on the RIME backend. This
will run an incremental continuous test on new data for an existing CT Instance.

**Arguments:**

* `test_run_config: dict`

  Specifies paths to the dataset to be used in the continuous test.

* `rime_managed_image: Optional[str] = None`

  Specify the name of the RIME Managed Image to run the continuous test on.
  Managed Images are the preferred method of running RIME on an image with custom Pip requirements.
  See the documentation for `create_managed_image()` and `list_managed_images()` for further information.

* `custom_image: Optional[CustomImage] = None`

  Specify a custom Docker image to run the continuous test job on.
  This image could include custom libraries that your model depends on.
  If no custom image is provided, the backend will use the default image specified by the cluster configuration.

* `ram_request_megabytes: Optional[int] = None`

  Specify the megabytes of RAM to request for a continuous test job. If none
  specified, will default to 4000MB. The limit will be set as 2x the request.

* `cpu_request_millicores:  Optional[int] = None`

  Specify the millicores of CPU to request for a continuous test job. If none
  specified, will default to 1500mi. The limit will be set as 2x the request.

**Return Value:**

A `RIMEStressTestJob` object that provides an interface for monitoring the job in the backend.

**Example:**

```Python
# This example will likely not work for you because it requires permissions to a specific S3 bucket.
# This demonstrates how you might specify such a configuration.
incremental_config = {
  "eval_path": "s3://rime-datasets/fraud_continuous_testing/eval_2021_04_30_to_2021_05_01.csv",
  "timestamp_col": "timestamp"
}
# Run the job using the specified config and the default Docker image in the RIME backend.
# Use the RIME Managed Image "tensorflow115".
# This assumes you have already created the Managed Image and waited for it to be ready.
ct_instance = rime_client.get_ct_instance("foo")
job = ct_instance.start_incremental_continuous_test(test_run_config=incremental_config, 
                                                       rime_managed_image="tensorflow115",
                                                       ram_request_megabytes=8000,
                                                       cpu_request_millicores=2000)
```
