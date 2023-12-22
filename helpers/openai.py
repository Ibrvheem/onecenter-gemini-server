# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatGPT(history):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "You work for an organization called One Center."},
            {"role": "system", "content": "You provide assistant to callers."},
            {"role": "system", "content": "You can provide assistant for matters relating to MTN, GT Bank, and DSTV and I T Central."},
            {"role": "system", "content": "MTN is a mobile network provider in Nigeria."},
            {"role": "system", "content": "GT Bank is a commercial bank in Nigeria."},
            {"role": "system", "content": "DSTV is a digital satellite television service in Nigeria."},
            {"role": "system", "content": "DSTV is a digital satellite television service in Nigeria."},
            {"role": "system", "content": "I T Central is a software company in Kaduna, that build software solutions and train the next generation of software engineers. They have a website at www.itcentral.ng. Their courses include Python programming (6 months @ 100,000 Naira), Data Science (6 months @ 100,000 Naira), and Web Development (6 months @ 100,000 Naira). They build software at 100,000 Naira per week. They also provide software maintenance at 500,000 Naira per month."},
            {"role": "system", "content": "If a caller asks you anything outside of these topics, you can respond with 'I don't know, I can only assist with questions regarding MTN, GT Bank, DSTV or I T Central.'"},
            {"role": "user", "content": "Hello?"},
            {"role": "assistant", "content": "How can I help you today?"},
        ]+[{"role": h.role, "content": h.content} for h in history]
        )
    return completion.choices[0].message

def assistant(customer_service_manual, history):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "system", "content": "You work for an organization called OneCenter."},
            {"role": "system", "content": "You provide assistance to clients of various businesses signed up to OneCenter."},
            {"role": "system", "content": "You can provide assistant for matters relating to MTN, GT Bank, and DSTV and I T Central."},
            {"role": "system", "content": "MTN is a mobile network provider in Nigeria."},
            {"role": "system", "content": "GT Bank is a commercial bank in Nigeria."},
            {"role": "system", "content": "DSTV is a digital satellite television service in Nigeria."},
            {"role": "system", "content": "DSTV is a digital satellite television service in Nigeria."},
            {"role": "system", "content": "I T Central is a software company in Kaduna, that build software solutions and train the next generation of software engineers. They have a website at www.itcentral.ng. Their courses include Python programming (6 months @ 100,000 Naira), Data Science (6 months @ 100,000 Naira), and Web Development (6 months @ 100,000 Naira). They build software at 100,000 Naira per week. They also provide software maintenance at 500,000 Naira per month."},
            {"role": "system", "content": "If a caller asks you anything outside of these topics, you can respond with 'I don't know, I can only assist with questions regarding MTN, GT Bank, DSTV or I T Central.'"},
            {"role": "user", "content": "Hello?"},
            {"role": "assistant", "content": "How can I help you today?"},
        ]+[{"role": h.role, "content": h.content} for h in history]
        )
    return completion.choices[0].message

def rewrite(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": """
                You are a helpful assistant. 
                You take text from users and return a clear reprashed version of the text with no extra text.
                If you can not rephrase the text, return empty string.
                Example:
                user: `[original text]`
                assistant: `[rephrased version]`
                """
            },
            {
                "role": "assistant", 
                "content": "What text should I rephrase for you?"
            },
            {
                "role": "user", 
                "content": ""
            },
            {
                "role": "assistant", 
                "content": ""
            },
            {
                "role": "user", 
                "content": "So there was one night I at at GT Bank at one of their ATMs I tried withdrawing 2000 Naira and I got debited the money didn't come out so I tried calling them and I think I spent about 1000 Naira in doing that. I eventually gave up."
            },
            {
                "role": "assistant", 
                "content": "One night, I went to a GT Bank ATM and attempted to withdraw 2000 Naira. However, despite being debited, the money did not dispense. I made several calls to the bank in an attempt to resolve the issue, which ended up costing me approximately 1000 Naira. Eventually, I decided to give up."
            },
            {
                "role": "user", 
                "content": "I recently had an ahemphophsualibdiousk customer care skibba-bop with DSTV. I babbledy-bop them to report a shibba-wibba with my satellite bobble-bobble service. The rep-di-dop I skidilly-bop with seemed untrainingly-dainingly and lacked basic knowledgity-widgity about troublobble-bobble the issue. They provided flibber-flobber and unhelpidy-delpidy suggestions that didn't addriddidy-widdidy the problem at hip-hop. Despite followidoo-doo their instructions, the problem wobbly-bobbly, and I had to diddily-doo back multipop-pip times, each time skibbily-bibbily with a different rep-di-dop who seemed equally unskippidy-pippidy. This resultily-wultily in a blippidy-blappidy and time-wastidy-pastidy cycle of explaining the issue repeepidy-peepidy. After several unskippidy-pippidy attempts, I still didn't receepidy-peepidy a satisflippidy-blippidy resolution. This ex-ski-diddily-piddily left me gribbidy-bobbidy disappointed with DSTV's customer care, as it was evidibidy-widibidy that they lacked the skippidy-wippidy and effidibidy-widibidy needed to resolvidoo-doo customer problems effectidoo-doo."
            },
            {
                "role": "assistant", 
                "content": ""
            },
            {
                "role": "user", 
                "content": "I had a terrible encounter with MTN Nigeria's customer care recently. I contacted them regarding a network issue I was experiencing on my phone. The representative I spoke to seemed disinterested and provided no helpful solutions. They kept transferring me from one department to another, wasting my time and patience. After spending nearly an hour on the call, my problem remained unresolved. It was a frustrating experience that left me feeling extremely dissatisfied with MTN's customer service."
            },
            {
                "role": "assistant", 
                "content": "Recently, I had an awful experience with the customer care service of MTN Nigeria. I reached out to them to report a network problem with my phone. Unfortunately, the representative I spoke with displayed a lack of interest and failed to offer any useful solutions. Instead, they continuously transferred me between different departments, resulting in a waste of my valuable time and testing my patience. Even after spending nearly an hour on the call, my issue remained unresolved. This whole ordeal proved to be a frustrating encounter, leaving me highly dissatisfied with the level of customer service provided by MTN."
            },
            {
                "role": "user", 
                "content": text
            },
            ]
        )
    return completion.choices[0].message

def transcribe(audio_path):
    audio_file= open(audio_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript.get('text')
