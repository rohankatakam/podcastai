import json
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
from fireworks.client import Fireworks
import requests
import json

def is_overlap(interval1, interval2, interval3):
    # Check if three intervals overlap
    start = max(interval1['start_word'], interval2['start_word'], interval3['start_word'])
    end = min(interval1['end_word'], interval2['end_word'], interval3['end_word'])
    return start <= end

def find_common_overlapping_intervals(list1, list2, list3):
    # Sort each list by start_word
    list1.sort(key=lambda x: x['start_word'])
    list2.sort(key=lambda x: x['start_word'])
    list3.sort(key=lambda x: x['start_word'])
    
    # List to hold the result of overlapping intervals common among all three lists
    common_overlaps = []
    
    # Check for common overlaps by iterating over each combination of intervals from the three lists
    for interval1 in list1:
        for interval2 in list2:
            for interval3 in list3:
                if is_overlap(interval1, interval2, interval3):
                    common_overlaps.append((interval1, interval2, interval3))

    return common_overlaps

def getInsights(podcastTitle, url):
    AUDIO_URL = {
        "url": url
    }
    
    API_KEY = "d4cf2539a5bfccf3f2819db95b44655ac961b64f"
    
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(API_KEY)
    
        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            sentiment=True,
            intents=True,
            summarize="v2",
            topics=True,
        )
    
        # STEP 3: Call the transcribe_url method with the audio payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)
        
        # STEP 4: Print the response
        # print(response.to_json(indent=4))
    
        
        data = json.loads(response.to_json(indent=4))
        
        results = data["results"]
        summary = results["summary"]
        topics = results["topics"]["segments"]
        intents = results["intents"]["segments"]
        sentiments = results["sentiments"]["segments"]
    
        #print(summary)
    
        common_overlaps = find_common_overlapping_intervals(topics, sentiments, intents)
    
        ideas = []
        
        for overlap in common_overlaps:
            topic = overlap[0]['topics'][0]['topic']
            topic_desc = overlap[0]['text']
            intent = overlap[2]['intents'][0]['intent']
            intent_desc = overlap[2]['text']
            sentiment = overlap[1]['sentiment']
            ideas.append({
                "topic" : topic,
                "topic_desc" : topic_desc,
                "intent" : intent,
                "intent_desc" : intent_desc,
                "sentiment" : sentiment
            })
    
        promptStr = ""
        summary = results["summary"]
        title = podcastTitle
        
        titleStr = "Podcast Title = " +  title + "\n"
        summaryStr = "Podcast Summary = " + summary['short'] + "\n"
        prompStr = titleStr + summaryStr
    
        idea_idx = 1
        for idea in ideas:
            idea_number = "Idea #" + str(idea_idx) + "\n"
            topic = "Topic = " + idea["topic"] + "\n"
            topic_description = "Topic Description = " + idea["topic_desc"] + "\n"
            intent = "Intent = " + idea["intent"] + "\n"
            intent_description = "Intent Description = " + idea["intent_desc"] + "\n"
            sentiment = "Sentiment = " + idea["sentiment"] + "\n"
            idea = idea_number + topic + topic_description + intent + intent_description + sentiment
            promptStr += idea
            idea_idx += 1
    
        promptQuestion = "Given a list of ideas (its topic, sentiment, and intent) expressed in a podcast in chronological order, the title of the podcast, and an overall description of the podcast, generate a more accurate, detailed, and more lengthy description of what is discussed in the podcast and outline the main ideas discussed in the article in a list. Make sure that the response is well-formatted and well-spaced when loaded into a JavaScript string: \n"
    
    
        url = "https://api.fireworks.ai/inference/v1/chat/completions"
        payload = {
          "model": "accounts/fireworks/models/mixtral-8x7b-instruct",
          "max_tokens": 4096,
          "top_p": 1,
          "top_k": 40,
          "presence_penalty": 0,
          "frequency_penalty": 0,
          "temperature": 0.6,
          "messages": [{
              "role": "user",
              "content": promptQuestion + "\n" + promptStr
            }]
        }
        headers = {
          "Accept": "application/json",
          "Content-Type": "application/json",
          "Authorization": "Bearer tcvXtlrzEnYjQaAel8jqCdovjmFqHkGNPanATyTa46gE8RGh"
        }
        
        test = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        return test.json()
    except Exception as e:
        return f"Exception: {e}"