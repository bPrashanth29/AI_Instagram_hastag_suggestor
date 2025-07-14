import openai
import requests
import os

# Replace with your actual Azure keys and endpoints
VISION_KEY = "4vFq4I1LVbe7bagaidnkdMG2hFN38bNfYQ2KNDGL0TOnNJdxjvicJQQJ99BGACfhMk5XJ3w3AAAFACOGTiUk"
VISION_ENDPOINT = "https://face52945878.cognitiveservices.azure.com"  # ✅ no trailing slash

OPENAI_KEY = "BvddphHSutnGPt2T723Q7hcEq3VTxdnFQhouL7NT2HRPm51FP7YhJQQJ99BGACHYHv6XJ3w3AAAAACOGcyKL"
OPENAI_ENDPOINT = "https://project52944729-resource.openai.azure.com"
DEPLOYMENT_NAME = "gpt-4o"

image_path = "images/uploaded_image.jpg"

def get_image_tags(image_path):
    vision_url = f"{VISION_ENDPOINT}/vision/v3.2/analyze?visualFeatures=Tags"
    headers = {
        'Ocp-Apim-Subscription-Key': VISION_KEY,
        'Content-Type': 'application/octet-stream'
    }

    with open(image_path, 'rb') as image_data:
        response = requests.post(vision_url, headers=headers, data=image_data)
        response.raise_for_status()
        tags = response.json().get('tags', [])
        return [tag['name'] for tag in tags]

def generate_hashtags(tags):
    openai.api_type = "azure"
    openai.api_base = OPENAI_ENDPOINT
    openai.api_key = OPENAI_KEY
    openai.api_version = "2023-12-01-preview"

    prompt = f"Suggest creative and trending Instagram hashtags for the following image tags: {', '.join(tags)}"

    print("🤖 Calling OpenAI to generate hashtags...")

    response = openai.ChatCompletion.create(
        engine=DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are an expert social media content creator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=100
    )
    return response['choices'][0]['message']['content']

# Run the pipeline
try:
    tags = get_image_tags(image_path)
    print("✅ Tags detected:", tags)
    hashtags = generate_hashtags(tags)

    os.makedirs("output", exist_ok=True)
    with open("output/hashtags.txt", "w") as f:
        f.write(hashtags)

    print("✅ Hashtags generated successfully!")
    print("📁 Saved to: output/hashtags.txt")

except requests.exceptions.HTTPError as e:
    print("❌ HTTP Error:", e.response.status_code, e.response.text)
except Exception as ex:
    print("❌ Error:", str(ex))
