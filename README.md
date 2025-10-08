# UKBIobank-Bifrost

Repository for supporting both the transforming of the DataConnector and Marjorie logs into usage metrics in Bifrost Grafana. Currently this is a monthly manual process to combine logs from Marjorie and DataConnector.

The UK Biobank NNEDH solution consists of applying the NNEDH storage as a solution for UK Biobank datasets:

- UKBB53639

- UKBB53639_users

Within the solution architecture, users can access the data in the following ways:

1. Via DataConnector in Marjorie
2. Via Datahub UI
3. Via NNEDH DMACLI command-line tools

## **1. Via DataConnector in Marjorie**

DataConnector logs that capture dataset operations for each UKBB dataset are provided by the DataConnector team on a monthly basis. There are no current automated processes to receive them and these logs are sent manually to the UKBB DevOps team through email from the DataConnector team.

The DataConnector logs contain user ids (```uid```)and not user initials for each S3 operation (Create, Read, Write) in each row in the log.

|Month|Filename of log|Dataset|
|--|--|--|
|Dec 2024|dhukbb53639xggxe5eucentral1_DEC2024.csv|UKBB53639|
|Jan 2025|january_2025_dhukbb53639xggxe5eucentral1.csv|UKBB53639|
|Jan 2025|january_2025_dhukbb53639userskbqll1eucentral1.csv|UKBB53639_users|
|Feb 2025|UKBB53639_feb_2025.logs|UKBB53639|
|Feb 2025|UKBB53639users__feb_2025.logs|UKBB53639_users|
|Mar 2025|dhukbb53639xggxe5eucentral1-march_2025.log|UKBB53639|
|Mar 2025|dhukbb53639userskbqll1eucentral1-march_2025.log|UKBB53639_users|
|Apr 2025|dhukbb53639xggxe5eucentral1_apr_2025.log|UKBB53639|
|Apr 2025|dhukbb53639userskbqll1eucentral1_apr_2025.log|UKBB53639_users|
|May 2025|dhukbb53639xggxe5eucentral1_may_2025.log|UKBB53639|
|May 2025|dhukbb53639userskbqll1eucentral1_may_2025.log|UKBB53639_users|

Currently to map the user ids to their corresponding user initials, a python script ```generate_username_uid_mapping.py``` is run on a daily basis as a cron job (see task below) to generate all Marjorie users initials (```user_name```) and their corresponding user ids (```uid```) into a .csv file.
These lists are written to a S3 bucket ```uid-username-mapping-hpc``` in the ```AWS-NN-UKBioBank-PRD``` AWS account (975050080250).
Note that there is a script named ```generate_username_uid_mapping_1.0.0_release.py``` that was released as part of the UK Biobank NNEDH v1.0.0 technical release. This script enables the generation of the .csv file locally.

In order to enable the writing of the ```usernames_uid_gids_yyyy_mm_dd.csv``` file to the S3 bucket, an **IAM Roles Anywhere** was set-up in the AWS account so as to have authenticated access to the AWS account's S3 bucket. For more information on how the preceding steps to set-up AWS IAM Roles Anywhere, refer to:

<https://novonordisk.sharepoint.com/sites/cloud/SitePages/Using.aspx>

A profile "developer" was created in the ```.aws/config``` file using the ```aws_signing_helper``` and the Roles Anywhere setup - see below.
This role was created:  

```

arn:aws:iam::975050080250:role/Role-anywhere-uid

[profile developer]
credential_process = ./aws_signing_helper credential-process --certificate /novo/users/wmt/iamroleanywhere/certificate.crt --private-key /novo/users/wmt/iamroleanywhere/new.key --trust-anchor-arn arn:aws:rolesanywhere:eu-central-1:975050080250:trust-anchor/b1a591d0-74fd-4647-a290-32035a6977fc --profile-arn arn:aws:rolesanywhere:eu-central-1:975050080250:profile/a4126515-8713-4c3c-810c-ffb301acbb74 --role-arn arn:aws:iam::975050080250:role/Role-anywhere-uid
```

### **cron job task**

```

wmt@marjorie:~$ crontab -l

* * * * * /path/to/script.sh# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
0 0 * * * python3 /novo/users/wmt/generate_username_uid_mapping.py

```

Note: When Marjorie has a scheduled maintenance, whereby jobs on the Marjorie HPC cluster are terminated, it is important to check and verify that the cron job is resumed. Use ``crontab -e``` to set up the cron job task if required to add the task above.

## 2. Via Datahub UI

S3 operations are captured via the S3 bucket's AWS CloudTrail data events in the CloudWatch Log group ```dh-weKCUB-audittrail-DatahubAuditTrailLogGroupA5314186-FOVOt9KAjaA9```

## 3. Via NNEDH DMACLI command-line tools

S3 operations are captured via the S3 bucket's AWS CloudTrail data events in the CloudWatch Log group ```dh-weKCUB-audittrail-DatahubAuditTrailLogGroupA5314186-FOVOt9KAjaA9```

## Repository contents

This repository is used to achieve the following goals:

1. Code repository for all python scripts:
   - ```generate_username_uid_mapping.py``` (currently running daily in Marjorie in a wmt-user tmux session to extract list of all users' initials and their user ids)
   - ```data_dictionary.py```(creates a data_dictio
   - ```ukbb53639_add_timestamp_uid_action_jan.py```(add new columns in the monthly DataConnector log for users' initials after mapping to their user ids and the name of the S3 operation)

2. Logs repository for the generated and combined monthly Bifrost grafana DataConnector logs:

   |Month|Filename of log|Dataset|Purpose|
   |--|--|--|--|
   |-|data_dictionary.csv|-|File containing 2 columns for username and userid values - extracted from the latest month's ```usernames_uid_gids_yyyy_mm_dd.csv``` file|
   |Dec 2024|output_ukbb53639_with_usernames_dec2024.csv|UKBB53639|Shows all users' activities via DataConnector in Dec 2024. No users have accessed the UKBB53639_users dataset, therefore no logs were received from DataConnector|
   |Jan 2025|output_ukbb53639_with_usernames_jan2025.csv|UKBB53639|Shows all users' activities via DataConnector in Jan 2025|
   |Jan 2025|output_ukbb53639_with_usernames_jan2025_users.csv|UKBB53639_users|Shows all users' activities via DataConnector in Jan 2025|
   |Feb 2025|output_ukbb53639_with_usernames_feb_object.csv|UKBB53639|Shows all users' activities via DataConnector in Feb 2025|
   |Feb 2025|output_ukbb53639_with_usernames_feb_users_object.csv|UKBB53639_users|Shows all users' activities via DataConnector in Feb 2025|
   |Mar 2025|output_ukbb53639_with_usernames_mar_object.csv|UKBB53639|Shows all users' activities via DataConnector in Mar 2025|
   |Mar 2025|output_ukbb53639_with_usernames_mar_users_object.csv|UKBB53639_users|Shows all users' activities via DataConnector in Mar 2025|
