import streamlit as st
import requests
import json
import time

# Load Lottie file
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load brain animation

# Updated API call function for AWS Lambda via API Gateway
def call_api(query):
    # Replace with your actual API Gateway endpoint that triggers the Lambda function
    api_url = "https://lnuv0i4a09.execute-api.us-east-1.amazonaws.com/dev/"
    
    try:
        # Prepare the payload with the user's query
        response = requests.post(api_url, json={"user_query": query})
        
        # Handle bad status codes
        response.raise_for_status()
        
        # Return the JSON response from the Lambda function
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while calling the API: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON response: {str(e)}")
        return None

# Streamlit app
def main():
    st.set_page_config(page_title="Ask John Calvin", page_icon="🕂", layout="wide")

    st.title("Ask John Calvin")

    # User input for the question
    user_question = st.text_input("Ask your question:")

    if st.button("Receive Answer"):
        if user_question:
            # Display spinning brain while processing
            with st.spinner("Thinking..."):
                brain_placeholder = st.empty()
                with brain_placeholder:
                    st_lottie(lottie_brain, height=200, key="brain")
                
                # Call API
                result = call_api(user_question)
                
                # Remove spinning brain
                brain_placeholder.empty()

            if result:
                # Display the response in a nice format
                st.subheader("Response:")
                st.write(result.get('Answer', 'No response available'))

                # Display additional information
                with st.expander("See details"):
                    st.json({
                        "Question": result.get('Question', 'N/A'),
                        "Status Code": result.get('statusCode', 'N/A'),
                        "Citation": result.get('Citation', 'N/A')
                    })
            else:
                st.error("Failed to get a valid response from the API.")
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
