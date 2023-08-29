import pandas as pd
import streamlit as st

from utils import AWSSession

st.header("AWS Sagemaker Endpoints")
# st.subheader("Skin Cancer Detection")

aws_session = AWSSession()
aws_session.set_sessions()

response = aws_session.get_sagemaker_endpoints()
endpoints = response.get("Endpoints")

if endpoints:
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
    st.table(df_table)

else:
    st.info("There are currently no endpoints deployed", icon="ℹ️")


# if test_image:
#     image = Image.open(test_image)
#     image_file = io.BytesIO(test_image.getvalue())
#     files = {"file": image_file}

#     col1, col2 = st.columns(2)

#     with col1:
#         # Display the uploaded image in the first column
#         st.image(test_image, caption="", use_column_width="always")

#     with col2:
#         if st.button("Start Prediction"):
#             with st.spinner("Prediction in Progress. Please Wait..."):
#                 # Send a POST request to FastAPI for prediction
#                 output = requests.post(FASTAPI_ENDPOINT, files=files, timeout=8000)
#             st.success("Success! Click the Download button below to retrieve prediction results (JSON format)")
#             # Display the prediction results in JSON format
#             st.json(output.json())
#             # Add a download button to download the prediction results as a JSON file
#             st.download_button(
#                 label="Download",
#                 data=json.dumps(output.json()),
#                 file_name="cnn_skin_cancer_prediction_results.json",
#             )
