PROMPT_TEMPLATE = """
Answer the following question based on the provided Summary and Profile.
Question: {user_question}

In addition, get contact information including email, phone number, 
and city (most recent worked) from Profile.

Response should be professional and engaging, as if talking to a potential client or future employer. Make sure
to reference the Summary and Profile provided. The response be below 100 words.

Response format:
Response Text: <Your answer here>
Contact Email: <email here>
Contact Phone: <phone number here>
City: <city here>
"""
