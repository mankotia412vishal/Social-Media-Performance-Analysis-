# Social Media Performance Analysis

This project aims to analyze social media engagement using DataStax Astra DB, Langflow for workflow automation, and GPT for generating insights. It simulates the performance of different post types (e.g., carousel, reels, static images) and provides insights based on the engagement data.

## Pre-Hackathon Assignment: Social Media Performance Analysis
**Submission Deadline:** January 8th

### **Objective:**
To develop a basic analytics module that can analyze engagement data from mock social media accounts, leveraging Langflow and DataStax to provide insights.

### **Required Tools:**
- **DataStax Astra DB** for database operations.
- **Langflow** for workflow creation and GPT integration.
  
### **Task Details:**

1. **Fetch Engagement Data:**
   - Created a mock dataset simulating social media engagement (likes, shares, comments, and post types).
   - Stored this data in DataStax Astra DB for further analysis.

2. **Analyze Post Performance:**
   - Using Langflow, I constructed a flow that:
     - Accepts post types (e.g., carousel, reels, static images) as input.
     - Queries the dataset in Astra DB to calculate average engagement metrics for each post type.
     
3. **Provide Insights:**
   - Integrated GPT with Langflow to generate simple insights based on the data.
   - Example outputs:
     - "Carousel posts have 20% higher engagement than static posts."
     - "Reels drive 2x more comments compared to other formats."

### **Features:**
- **Data Simulation**: Simulated a variety of social media posts and engagement data.
- **Post Type Analysis**: Provides insights into which post types have higher engagement.
- **Insights Generation**: GPT-based insights that help determine what content performs best.
  
### **Tech Stack:**
- **DataStax Astra DB**: Cloud database to store and retrieve engagement data.
- **Langflow**: Workflow automation tool to connect and query data, and integrate GPT.
- **GPT**: To generate insights based on social media performance data.

### **Demo Video:**
A video is recorded showcasing:
- **Langflow workflow**: Explanation of the steps involved in creating the workflow.
- **DataStax Usage**: How DataStax Astra DB is used to store and query the engagement data.
- **GPT Integration**: How GPT is leveraged to generate insights from the data.

[Link to Demo Video (YouTube)](your-video-link)

### **Installation and Setup:**

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/mankotia412vishal/Social-Media-Performance-Analysis.git
   ```
2. Navigate to the project directory:

bash
Copy code
cd Social-Media-Performance-Analysis
Install required dependencies:

bash
```
pip install -r requirements.txt
```
Set up DataStax Astra DB:

Sign up for DataStax Astra DB here.
Follow the instructions to create a database and get your database connection details.
Configure your .env file with your DataStax credentials.

Run the application:

bash
```
python app.py
```
