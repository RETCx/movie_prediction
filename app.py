# !pip install gradio ipywidgets
import pandas as pd
import gradio as gr
import re
import joblib

def get_quarter(month):

    if (month <= 3):
        return 'Q1'
    
    elif (month <= 6) and (month > 3):
        return 'Q2'
              
    elif (month <= 9) and (month > 6):
        return 'Q3'

    elif (month <= 12) and (month > 9):
        return 'Q4'
# Load the pipeline and label_pipeline
pipeline = joblib.load("pipeline.joblib")
label_pipeline = joblib.load("label_pipeline.joblib")
available_genres = joblib.load("available_genres.joblib")
companies = joblib.load("companies.joblib")
production_countrieslist = joblib.load("production_countrieslist.joblib")
spoken_languages = joblib.load("spoken_languages.joblib")
languages =joblib.load("languages.joblib")


# Define the predict function
def predict(release_date,vote_average, vote_count, original_language, runtime, adult, budget, popularity, genres, production_companies, production_countries, spoken_languages):
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not date_pattern.match(release_date):
        print("Please enter the release date in the format YYYY-MM-DD.")
    else:
        print(release_date)
        Year, Month, Day = map(int, release_date.split('-'))  # Split the date into Year, Month, and Day
    print(genres)
    sample = dict()
    sample["vote_average"] = float(vote_average)
    sample["vote_count"] = int(vote_count)
    sample["original_language"] =  original_language
    sample["runtime"] = runtime
    sample["adult"] = True if adult == "True" else False
    sample["budget"] = budget
    sample["popularity"] = popularity
    sample["genres"] = ', '.join(genres)
    sample["production_companies"] = ', '.join(production_companies)
    sample["production_countries"] = ', '.join(production_countries)
    sample["spoken_languages"] = ', '.join(spoken_languages)
    sample["Year"] = Year
    sample["Month"] = Month
    sample["Day"] = Day
    sample["Quarter"] = get_quarter(Month)
    sample["YearQuarter"] = str(Year) + get_quarter(Month)

    print(sample["genres"])

    # Make prediction
    revenue = pipeline.predict(pd.DataFrame([sample]))
    revenue = label_pipeline.inverse_transform([revenue])

    return int(revenue[0][0])


# Define the interface
with gr.Blocks() as blocks:
    vote_average = gr.Textbox(label="Vote Average(approximate )")
    vote_count = gr.Number(label="Vote Count(approximate )")
    original_language = gr.Dropdown(label="Original Language", choices=list(languages.keys()))
    runtime = gr.Number(label="Runtime")
    adult = gr.Radio(["True", "False"], label="Adult")
    budget = gr.Number(label="Budget($)")
    popularity = gr.Number(label="Popularity(approximate )")
    genres = gr.Dropdown(available_genres, multiselect=True, label="genres")
    production_companies = gr.Dropdown(companies,multiselect=True,label="Production Companies")
    production_countries = gr.Dropdown(production_countrieslist,multiselect=True,label="Production Countries")
    spoken_languages = gr.Dropdown(spoken_languages,multiselect=True,label="Spoken Languages")
    release_date = gr.Textbox(label="Release Date",placeholder="YYYY-MM-DD") 
    revenue = gr.Number(label="Revenue")

    inputs = [release_date,vote_average, vote_count, original_language, runtime, adult, budget, popularity, genres, production_companies, production_countries, spoken_languages]
    outputs = [revenue]
    
    predict_btn = gr.Button("Predict")
    predict_btn.click(predict, inputs=inputs, outputs=outputs)


if __name__ == "__main__":
    blocks.launch() # Local machine only
    # blocks.launch(server_name="0.0.0.0") # LAN access to local machine
    # blocks.launch(share=True) # Public access to local machine
