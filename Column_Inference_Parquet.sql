CREATE OR REPLACE STAGE SYNTETIC_DATASET_STG;

CREATE FILE FORMAT PARQUET_FORMAT
  TYPE = parquet;

-- Don't compress the file for inference to work
PUT 'file://C:/Users/DanieleAbbatelli/OneDrive/Code/streamlit_editable_df/syntetic_dataset.parquet' @SYNTETIC_DATASET_STG AUTO_COMPRESS = FALSE;
--REMOVE @SYNTETIC_DATASET_STG;

LIST @SYNTETIC_DATASET_STG;

-- Check if we can infer the schema
SELECT *
  FROM TABLE(
    INFER_SCHEMA(
      LOCATION=>'@SYNTETIC_DATASET_STG/syntetic_dataset.parquet'
      , FILE_FORMAT=>'PARQUET_FORMAT'
      )
    );

-- Use the inferred schema to create a table
CREATE OR REPLACE TABLE SYNTETIC_DATASET
USING TEMPLATE (
    SELECT ARRAY_AGG(OBJECT_CONSTRUCT(*))
    FROM TABLE(
        INFER_SCHEMA(
        LOCATION=>'@SYNTETIC_DATASET_STG/syntetic_dataset.parquet'
        , FILE_FORMAT=>'PARQUET_FORMAT'
    )
));

-- Copy the data into the table
COPY INTO SYNTETIC_DATASET 
FROM @SYNTETIC_DATASET_STG/syntetic_dataset.parquet
FILE_FORMAT = (FORMAT_NAME='PARQUET_FORMAT')
MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
;

SELECT * FROM SYNTETIC_DATASET;