from pyngrok import ngrok
# Set up ngrok
ngrok.set_auth_token("2iGg2l1JGx7tznan8GQg940lB1h_Mnw7vfcyBc43SgDoSncv")

# Run Streamlit app in the background
get_ipython().system_raw('streamlit run main.py --server.port 8501 &')

# Expose the Streamlit app via ngrok
public_url = ngrok.connect(8501)
print(f'Public URL: {public_url}')
