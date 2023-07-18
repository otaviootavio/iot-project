## Config google cloud

Create pub sub
```gcloud pubsub topics create <topic-name>```

Create a bucket
```gsutil mb gs://<bucket-name>```

Create big query
```bq mk <bigquery-dataset-name>```

Create big query table
```bq mk <bigquery-dataset-name>.<table-name> name:STRING,country:STRING, <column-name>:<data-type>```

## Dataflow
Created by a template

## Publishing the data
You must send it on json