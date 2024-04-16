from flask import Flask, request, jsonify
from flask_cors import CORS
import googleapiclient.discovery

app = Flask(__name__)
CORS(app)

@app.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    # Create a YouTube API client
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyDnTNR9nICegR7f10pl-9dhX-erWqsr6c0")

    # Call the search.list method to retrieve search results with order by view count
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=10,  # You can adjust the number of results as needed
        order="viewCount"  # Sort by view count
    ).execute()

    # Extract video titles and IDs from the search results
    results = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            video_id = search_result["id"]["videoId"]
            results.append({"title": title, "videoId": video_id})

    # If no results are found, retry search without order by view count
    if not results:
        # Retry search without order by view count
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=10,  # You can adjust the number of results as needed
        ).execute()

        # Extract video titles and IDs from the search results
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                title = search_result["snippet"]["title"]
                video_id = search_result["id"]["videoId"]
                results.append({"title": title, "videoId": video_id})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
