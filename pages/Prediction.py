"""Prediction page for Part 2 runtime inference."""

import pandas as pd
import streamlit as st

from config.config import MAX_UPLOAD_SIZE_MB, PREDICTION_FEATURES
from src.prediction import PredictionEngine, predict_incident
from src.upload_validation import validate_upload_size


def render():
    st.title("🔮 Severity Score Prediction")
    st.write(
        "Upload a CSV containing the required Part 2 prediction features. "
        "Prediction uses the fitted Part 2 runtime artifacts."
    )

    uploaded_file = st.file_uploader(
        "Upload incident CSV",
        type=["csv"],
        help=f"Maximum file size: {MAX_UPLOAD_SIZE_MB} MB.",
    )
    if uploaded_file is None:
        return

    try:
        validate_upload_size(uploaded_file, MAX_UPLOAD_SIZE_MB)
    except ValueError as error:
        st.error(str(error))
        return

    try:
        input_df = pd.read_csv(uploaded_file)
    except Exception as error:
        st.error(f"Unable to read the uploaded CSV: {error}")
        return

    st.subheader("Input Preview")
    st.dataframe(input_df.head(10), width="stretch")
    st.caption(f"Rows: {len(input_df):,} | Columns: {len(input_df.columns):,}")

    if st.button("Generate Predictions", type="primary"):
        try:
            missing = [column for column in PREDICTION_FEATURES if column not in input_df.columns]
            if missing:
                st.error(
                    "Prediction input is missing required features: "
                    + ", ".join(missing)
                )
                return

            validated_input = PredictionEngine.validate_input(input_df)
            result = predict_incident(validated_input)
        except ValueError as error:
            st.error(f"Prediction input validation failed: {error}")
            return
        except FileNotFoundError:
            st.error(
                "Prediction runtime artifacts are unavailable. "
                "Please sync the Part 2 model, preprocessor, and feature contract."
            )
            return
        except RuntimeError as error:
            st.error(f"Prediction runtime validation failed: {error}")
            return
        except Exception as error:
            st.error(f"Prediction failed unexpectedly: {error}")
            return

        st.success("Predictions generated successfully.")
        st.dataframe(result, width="stretch")
        st.download_button(
            "Download Predictions CSV",
            data=result.to_csv(index=False).encode("utf-8"),
            file_name="predictions.csv",
            mime="text/csv",
        )

        if "Confidence" in result.columns:
            st.subheader("Prediction Confidence")
            st.progress(float(result["Confidence"].mean()))
            st.caption(f"Average confidence: {result['Confidence'].mean():.2%}")


if __name__ == "__main__":
    render()
