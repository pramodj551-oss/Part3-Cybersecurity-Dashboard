"""
==========================================================
AI-Powered Cybersecurity Dashboard
Prediction Page
Version: 3.0
==========================================================
"""

import pandas as pd
import streamlit as st

from src.prediction import predict_incident


def render():

    st.title("🤖 Cybersecurity Incident Prediction")

    st.markdown(
        """
Upload a CSV file containing cybersecurity incidents to
predict the incident severity using the trained machine
learning model.
        """
    )

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"],
        key="prediction_upload"
    )

    if uploaded_file is None:

        st.info("Please upload a CSV dataset.")

        return

    try:

        input_df = pd.read_csv(uploaded_file)

    except Exception as error:

        st.error(f"Unable to read CSV file.\n\n{error}")

        return

    st.success("Dataset loaded successfully.")

    st.subheader("Input Preview")

    st.dataframe(
        input_df.head(),
        use_container_width=True
    )

    st.write(f"Records Available: **{len(input_df)}**")

    st.divider()

    if st.button(
        "Generate Predictions",
        type="primary"
    ):

        with st.spinner("Running prediction..."):

            try:

                prediction_df = predict_incident(
                    input_df
                )

                st.success(
                    "Prediction completed successfully."
                )

                st.subheader("Prediction Results")

                st.dataframe(
                    prediction_df,
                    use_container_width=True
                )

                st.download_button(

                    label="Download Predictions",

                    data=prediction_df.to_csv(
                        index=False
                    ),

                    file_name="prediction_results.csv",

                    mime="text/csv"

                )

                if (
                    "Confidence"
                    in prediction_df.columns
                ):

                    st.subheader(
                        "Prediction Confidence"
                    )

                    st.progress(
                        float(
                            prediction_df[
                                "Confidence"
                            ].mean()
                        )
                    )

                    st.metric(
                        "Average Confidence",
                        f"{prediction_df['Confidence'].mean()*100:.2f}%"
                    )

            except Exception as error:

                st.error(
                    f"Prediction failed.\n\n{error}"
                )


if __name__ == "__main__":

    render()
