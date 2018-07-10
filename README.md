# Kiali REST test cases

## Preparing the Environment

- `./setup.sh` will provide a quickstart environment for RHEL or Fedora with virtualenv called kiali-qe-rest and all the pip modules intalled.

- You can manually activate the environment by `source .kiali-qe-rest/bin/activate`

- If you don't want to create a virtualenv, a simple `pip install -r requirements.txt` will be install the requirements needed on your python environment

## Environment Variables

- You must change `kiali_hostname`, `kiali_username` and `kiali_password` according to your configuration.


## Running the Tests

- You can run the testing by `py.test` on root folder of this project (`kiali-qe-rest`)

or

- You can configure Pycharm to run the test for you. 
