import pandas as pd
import streamlit as st

from utils import AWSSession, timeit

# stores cache for 3600 seconds / 1h
@st.cache_data(ttl=3600)
def get_endpoint_response()->list:
    aws_session = AWSSession()
    aws_session.set_sessions()
    response = aws_session.get_sagemaker_endpoints()
    return response.get("Endpoints")

@st.cache_data(ttl=3600)
@timeit
def transform_endpoints(endpoints:list) -> pd.DataFrame:
    df = pd.DataFrame.from_records(endpoints)
    df_table = df.drop(columns=["CreationTime", "LastModifiedTime"])
    df_table["Creation Time"] = pd.to_datetime(df.LastModifiedTime).dt.strftime(
        "%m/%d/%Y %H:%M:%S"
    )
    df_table = df_table.rename(
        columns={
            "EndpointName": "Endpoint Name",
            "EndpointArn": "Endpoint Arn",
            "EndpointStatus": "Endpoint Status",
        }
    )
    return df_table



st.header("AWS Sagemaker Endpoints")

if st.button("Reload endpoints"):
    # Clear values from *all* all in-memory and on-disk data caches:
    # i.e. clear values from both square and cube
    st.cache_data.clear()

endpoints = get_endpoint_response()

if endpoints:
    table = transform_endpoints(endpoints=endpoints)
    st.table(table)
else:
    st.info("There are currently no endpoints deployed", icon="ℹ️")
