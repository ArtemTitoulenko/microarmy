# Override any keys below by putting them in a local_settings.py. Some
# overrides are required, signaled by a #* on the same line.

import os

### Get these from: http://aws-portal.amazon.com/gp/aws/developer/account/index.html?action=access-key
aws_access_key = '' #*
aws_secret_key = '' #*

### aws security config
security_groups = ['sample-1'] #*

### key pair name
key_pair_name = 'sample' #*

### path to ssh private key
### Will resolve ~
ec2_ssh_key = '~/.ssh/sample.pem' #*
ec2_ssh_username = 'ubuntu' # ami specific
ec2_ssh_key_password = None # only required if your ssh key is encrypted

### five cannons is a healthy blast
num_cannons = 5

### Availbility zones: http://alestic.com/2009/07/ec2-availability-zones
placement = 'us-east-1b'

### ami key from: http://uec-images.ubuntu.com/releases/11.10/release/
ami_key = 'ami-a7f539ce'
instance_type = 't1.micro'

### enable cloud init, so that a second deploy step is not required
enable_cloud_init = True

### scripts for building environments
env_scripts_dir = os.path.abspath(os.path.dirname('./env_scripts/'))

### cannon build script
cannon_init_script = 'build_cannon.sh'

### script to be run on `fire`
cannon_projectile_script = 'projectile.sh'

try:
    from local_settings import *
except:
    pass
